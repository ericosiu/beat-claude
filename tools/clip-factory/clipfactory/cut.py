"""Render 9:16 clips: pick the active speaker's camera, crop vertical,
lay the mic mix over it, burn word-timed captions and the hook overlay.

Audio always comes from the mic WAVs (broadcast quality), never the camera
scratch track. Video comes from the majority speaker's camera; the wide cam
is the fallback when coverage is missing or the exchange is 50/50.
"""
import argparse
import os
import re
import subprocess

from .common import fmt_ts, load_json, log, run

W, H = 1080, 1920
FONT = os.environ.get("CLIP_FACTORY_FONT", "DejaVu Sans")

ASS_HEADER = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Caption,{FONT},88,&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,6,2,2,60,60,420,1
Style: Hook,{FONT},84,&H0000FFFF,&H00FFFFFF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,7,3,8,60,60,180,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""


def caption_events(words, clip_start, clip_end, group_words=3, max_span=1.6):
    """Group word timings into short punchy caption cards."""
    events, group = [], []
    for w in words:
        if w["t1"] <= clip_start or w["t0"] >= clip_end:
            continue
        group.append(w)
        span = group[-1]["t1"] - group[0]["t0"]
        if len(group) >= group_words or span >= max_span \
                or re.search(r"[.!?,]$", w["text"]):
            events.append(group)
            group = []
    if group:
        events.append(group)

    lines = []
    for g in events:
        t0 = max(g[0]["t0"] - clip_start, 0)
        t1 = min(g[-1]["t1"] - clip_start + 0.08, clip_end - clip_start)
        text = " ".join(w["text"] for w in g).upper()
        text = re.sub(r"[{}\\]", "", text)
        lines.append(f"Dialogue: 0,{fmt_ts(t0)},{fmt_ts(t1)},Caption,,0,0,0,,{text}")
    return lines


def write_ass(path, clip, words, hook_seconds=2.8):
    lines = [ASS_HEADER]
    overlay = re.sub(r"[{}\\]", "", clip["overlay"])
    dur = clip["end"] - clip["start"]
    lines.append(
        f"Dialogue: 1,{fmt_ts(0)},{fmt_ts(min(hook_seconds, dur))},Hook,,0,0,0,,{overlay}")
    lines += caption_events(words, clip["start"], clip["end"])
    with open(path, "w") as f:
        f.write("\n".join(lines) + "\n")


def pick_source(clip, words, offsets, manifest):
    """Majority-speaker cam covering the window; wide cam as fallback."""
    talk = {}
    for w in words:
        if clip["start"] <= w["t0"] < clip["end"]:
            talk[w["speaker"]] = talk.get(w["speaker"], 0) + (w["t1"] - w["t0"])
    total = sum(talk.values()) or 1.0
    lead_speaker, lead_time = max(talk.items(), key=lambda kv: kv[1],
                                  default=(clip["speaker"], 0))
    prefer_wide = lead_time / total < 0.65  # real back-and-forth: show both

    def covers(name):
        o = offsets.get(name)
        return o and o["offset"] <= clip["start"] \
            and clip["end"] <= o["offset"] + o["duration"]

    ranked = []
    for f in manifest["files"]:
        if f["role"] == "cam" and f["speaker"] == lead_speaker:
            ranked.append((1 if prefer_wide else 0, f["name"]))
        elif f["role"] == "wide":
            ranked.append((0 if prefer_wide else 1, f["name"]))
    for _, name in sorted(ranked):
        if covers(name):
            return name
    raise RuntimeError(
        f"no synced camera covers {clip['id']} "
        f"({clip['start']:.0f}-{clip['end']:.0f}s) — check offsets.json")


def build_mix(manifest, media_dir, work_dir):
    """Mix the mic WAVs once; every clip trims from this."""
    mix = os.path.join(work_dir, "master_mix.wav")
    if os.path.exists(mix):
        return mix
    mics = [os.path.join(media_dir, f["name"])
            for f in manifest["files"] if f["role"] == "mic"]
    cmd = ["ffmpeg", "-v", "error", "-y"]
    for m in mics:
        cmd += ["-i", m]
    cmd += ["-filter_complex", f"amix=inputs={len(mics)}:normalize=0",
            "-c:a", "pcm_s16le", mix]
    run(cmd)
    return mix


def render(clip, source, offsets, mix, media_dir, out_dir, ass_path, crf=20):
    local_start = clip["start"] - offsets[source]["offset"]
    dur = clip["end"] - clip["start"]
    out = os.path.join(out_dir, f"{clip['id']}.mp4")
    ass_escaped = ass_path.replace("\\", "/").replace(":", r"\:").replace("'", r"\'")
    vf = (f"crop=ih*9/16:ih,scale={W}:{H},"
          f"subtitles=filename='{ass_escaped}'")
    run(["ffmpeg", "-v", "error", "-y",
         "-ss", f"{local_start:.3f}", "-i", os.path.join(media_dir, source),
         "-ss", f"{clip['start']:.3f}", "-i", mix,
         "-t", f"{dur:.3f}",
         "-map", "0:v:0", "-map", "1:a:0",
         "-vf", vf,
         "-af", "loudnorm=I=-14:TP=-1.5:LRA=11",
         "-c:v", "libx264", "-preset", "veryfast", "-crf", str(crf),
         "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
         "-movflags", "+faststart", out])
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--media", default="media")
    ap.add_argument("--work", default="work")
    ap.add_argument("--clips", default="work/clips.json")
    ap.add_argument("--transcript", default="work/transcript.json")
    ap.add_argument("--offsets", default="work/offsets.json")
    ap.add_argument("--out", default="clips")
    ap.add_argument("--only", nargs="*", help="only these clip ids")
    args = ap.parse_args(argv)

    manifest = load_json(args.manifest)
    clips = load_json(args.clips)
    words = load_json(args.transcript)["words"]
    offsets = load_json(args.offsets)
    os.makedirs(args.out, exist_ok=True)

    mix = build_mix(manifest, args.media, args.work)
    manifest_out = []
    for clip in clips:
        if args.only and clip["id"] not in args.only:
            continue
        source = pick_source(clip, words, offsets, manifest)
        ass_path = os.path.join(args.work, f"{clip['id']}.ass")
        write_ass(ass_path, clip, words)
        log(f"rendering {clip['id']} from {source} ...")
        out = render(clip, source, offsets, mix, args.media, args.out, ass_path)
        manifest_out.append({**{k: clip[k] for k in
                                ("id", "start", "end", "overlay", "caption")},
                             "source": source, "file": out})
        log(f"done: {out}")

    from .common import save_json
    save_json(os.path.join(args.out, "clips_manifest.json"), manifest_out)


if __name__ == "__main__":
    main()
