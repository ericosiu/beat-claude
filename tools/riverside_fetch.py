#!/usr/bin/env python3
"""Fetch a Riverside recording's assets, word-level transcript, and media via a share token.

Usage:
    python3 riverside_fetch.py --session <SESSION_ID> --clip <CLIP_ID> --token <TOKEN> \
                               [--track <ARCHIVE_ID>] [--out work/] [--no-media]

Outputs in --out:
    assets.json            clip-assets API response (tracks, durations, screen-share offsets)
    transcript-words.json  word-level [word, start_ms, duration_ms] per speaker
    captions.srt           caption blocks on the source timeline
    source.mp4             muxed video+audio from the share HLS (~720p), unless --no-media

Requires: curl, ffmpeg on PATH. riverside.com and vod.riverside.com must be
reachable through the session's network policy.
"""

import argparse
import concurrent.futures as cf
import json
import os
import subprocess
import sys

BASE = "https://riverside.com"
UA = "Mozilla/5.0 (X11; Linux x86_64) Chrome/126.0.0.0 Safari/537.36"


def curl(url, out=None):
    cmd = ["curl", "-sS", "-H", f"User-Agent: {UA}", "-w", "%{http_code}"]
    cmd += ["-o", out] if out else ["-o", "/dev/null"]
    if out is None:
        cmd = ["curl", "-sS", "-H", f"User-Agent: {UA}", url]
        r = subprocess.run(cmd, capture_output=True, text=True)
        return r.stdout
    r = subprocess.run(cmd + [url], capture_output=True, text=True)
    return r.stdout.strip()


def srt_ts(ms):
    return f"{ms//3600000:02d}:{ms%3600000//60000:02d}:{ms%60000//1000:02d},{ms%1000:03d}"


def write_srt(words, path):
    blocks, cur = [], []
    for w in words:
        if cur and (len(cur) >= 7 or w[1] - cur[0][1] > 2800 or w[1] - (cur[-1][1] + cur[-1][2]) > 700):
            blocks.append(cur)
            cur = []
        cur.append(w)
    if cur:
        blocks.append(cur)
    with open(path, "w") as f:
        for i, b in enumerate(blocks, 1):
            f.write(f"{i}\n{srt_ts(b[0][1])} --> {srt_ts(b[-1][1] + b[-1][2])}\n"
                    + " ".join(x[0] for x in b) + "\n\n")


def fetch_media(session, track, token, out_dir):
    for kind, playlist in (("video", "part_0_.m3u8"), ("audio", "hls_from_concat_part_1_.m3u8")):
        url = f"{BASE}/api/v4/vod/{session}/{track}/share?playlist={playlist}&t={token}"
        pl = os.path.join(out_dir, f"{kind}.m3u8")
        code = curl(url, pl)
        if code != "200":
            sys.exit(f"playlist fetch failed ({code}) for {kind}; is vod access set up?")
        urls = [l.strip() for l in open(pl) if l.startswith("https")]
        seg_dir = os.path.join(out_dir, kind)
        os.makedirs(seg_dir, exist_ok=True)

        def dl(iu):
            i, u = iu
            p = os.path.join(seg_dir, f"{i:04d}.ts")
            for _ in range(3):
                if curl(u, p) == "200" and os.path.getsize(p) > 0:
                    return None
            return i

        with cf.ThreadPoolExecutor(12) as ex:
            bad = [b for b in ex.map(dl, enumerate(urls)) if b is not None]
        if bad:
            sys.exit(f"{kind}: segments failed: {bad} (signatures expire - refetch the playlist)")
        with open(os.path.join(out_dir, f"{kind}_all.ts"), "wb") as w:
            for i in range(len(urls)):
                w.write(open(os.path.join(seg_dir, f"{i:04d}.ts"), "rb").read())
        print(f"{kind}: {len(urls)} segments")
    src = os.path.join(out_dir, "source.mp4")
    r = subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
                        "-i", os.path.join(out_dir, "video_all.ts"),
                        "-i", os.path.join(out_dir, "audio_all.ts"),
                        "-map", "0:v:0", "-map", "1:a:0", "-c", "copy",
                        "-movflags", "+faststart", src], capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"mux failed: {r.stderr[-500:]}")
    print(f"muxed -> {src}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--session", required=True)
    ap.add_argument("--clip", required=True)
    ap.add_argument("--token", required=True)
    ap.add_argument("--track", help="archiveId of the track to download (default: first camera track)")
    ap.add_argument("--out", default="work")
    ap.add_argument("--no-media", action="store_true")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)

    assets_path = os.path.join(a.out, "assets.json")
    code = curl(f"{BASE}/api/v4/take/{a.session}/clip/{a.clip}/clip-assets/share?t={a.token}", assets_path)
    if code != "200":
        sys.exit(f"clip-assets fetch failed ({code}) - check session/clip ids and share token")
    assets = json.load(open(assets_path))
    tracks = [t for t in assets["clip"]["timeline"]["assets"] if t.get("type") == "track"]
    cam = next((t for t in tracks if t["metadata"].get("kind") == "participant"), tracks[0])
    track = a.track or cam["metadata"]["archiveId"]
    print(f"tracks: {[(t['metadata'].get('archiveId'), t['metadata'].get('resolution')) for t in tracks]}")
    print(f"using track: {track}  duration: {cam['duration']/1000:.1f}s")

    tr_path = os.path.join(a.out, "transcript-raw.json")
    code = curl(f"{BASE}/api/v4/transcriptions/editable/{a.session}?t={a.token}", tr_path)
    if code == "200":
        data = json.load(open(tr_path))["data"]
        words = sorted((w for sp in data["speakers"] for s in sp["sentences"] for w in s["words"]),
                       key=lambda x: x[1])
        json.dump(words, open(os.path.join(a.out, "transcript-words.json"), "w"))
        write_srt(words, os.path.join(a.out, "captions.srt"))
        print(f"transcript: {len(words)} words, ends {words[-1][1]/1000:.1f}s")
    else:
        print(f"WARNING: transcript fetch failed ({code}) - continuing without timestamps")

    if not a.no_media:
        fetch_media(a.session, track, a.token, a.out)


if __name__ == "__main__":
    main()
