"""End-to-end pipeline test on synthetic media (no Whisper, no network).

Builds a fake 90s session: two mic WAVs with alternating speech-band noise
bursts, three 'camera' MP4s whose audio is the room mix shifted by known
offsets. Verifies sync recovers the offsets, hook scoring surfaces the
strong openers from a stub transcript, and cut renders real 1080x1920
files with burned captions.

Run:  python -m tests.test_pipeline   (from tools/clip-factory/)
"""
import json
import os
import subprocess
import sys
import wave

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from clipfactory import cut, find_hooks, sync  # noqa: E402

SR = 48000
DUR = 90.0
# camera_name -> true offset (master_time = offset + cam_time), start, length
CAMS = {
    "CAM-ERIC.MP4": (-4.0, 94.0),   # cam started 4s before the recorder
    "CAM-NEIL.MP4": (2.5, 87.0),    # cam started 2.5s after
    "CAM-WIDE.MP4": (0.7, 89.0),
}
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixture")


def speech_like(rng, n):
    """Noise bursts with syllable-ish 4 Hz amplitude modulation."""
    t = np.arange(n) / SR
    return rng.standard_normal(n) * (0.4 + 0.6 * np.abs(np.sin(2 * np.pi * 4 * t)))


def build_mics():
    rng = np.random.default_rng(7)
    n = int(SR * DUR)
    eric, neil = np.zeros(n), np.zeros(n)
    # alternating 6s turns with 0.5s gaps
    turn, who, t = 6.0, 0, 0.0
    while t < DUR - 1:
        i0, i1 = int(t * SR), min(int((t + turn - 0.5) * SR), n)
        (eric if who == 0 else neil)[i0:i1] = speech_like(rng, i1 - i0) * 0.5
        who ^= 1
        t += turn
    for name, sig in (("MIC-ERIC.WAV", eric), ("MIC-NEIL.WAV", neil)):
        with wave.open(os.path.join(ROOT, name), "wb") as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(SR)
            w.writeframes((sig * 32767 * 0.6).astype(np.int16).tobytes())
    return eric + neil


def build_cams(mix):
    for name, (offset, length) in CAMS.items():
        # cam audio = master mix from time `offset` for `length` seconds
        i0 = int(offset * SR)
        n = int(length * SR)
        pad_pre = max(-i0, 0)
        seg = mix[max(i0, 0): max(i0, 0) + n - pad_pre]
        audio = np.concatenate([np.zeros(pad_pre), seg,
                                np.zeros(n - pad_pre - len(seg))])
        raw = os.path.join(ROOT, name + ".wav")
        with wave.open(raw, "wb") as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(SR)
            w.writeframes((audio * 32767 * 0.5).astype(np.int16).tobytes())
        subprocess.run(
            ["ffmpeg", "-v", "error", "-y",
             "-f", "lavfi", "-i", f"testsrc2=size=1920x1080:rate=30:duration={length}",
             "-i", raw, "-shortest", "-c:v", "libx264", "-preset", "ultrafast",
             "-c:a", "aac", os.path.join(ROOT, name)], check=True)
        os.unlink(raw)


def stub_transcript():
    """Word-timed transcript; one utterance is a deliberately strong hook."""
    lines = [
        ("eric", 6.5, "So yeah I think we can talk about that later today."),
        ("neil", 12.5, "Most people are doing AI content completely wrong and it costs them real traffic."),
        ("eric", 19.0, "We went from zero to 1 million visits in 9 months without writing a single post ourselves."),
        ("neil", 26.0, "And the crazy part is the tooling is basically free if you know what to chain together."),
        ("eric", 33.0, "Right, and that compounds every single week."),
        ("neil", 40.0, "Um, well, another thing on the schedule next quarter."),
        ("eric", 47.0, "Stop hiring writers before you fix distribution, that's the biggest mistake I see."),
        ("neil", 54.0, "Totally agree, distribution first, content second."),
        ("eric", 61.0, "SEO is dead as a standalone channel, it only works stacked with brand now."),
        ("neil", 68.0, "Yeah and that's why we changed the whole playbook."),
    ]
    words, utterances = [], []
    for speaker, t0, text in lines:
        ws = []
        t = t0
        for tok in text.split():
            w = {"t0": round(t, 3), "t1": round(t + 0.28, 3),
                 "text": tok, "speaker": speaker}
            words.append(w)
            ws.append(w)
            t += 0.32
        utterances.append({"speaker": speaker, "t0": t0,
                           "t1": ws[-1]["t1"], "text": text, "words": ws})
    return {"words": words, "utterances": utterances}


def main():
    os.makedirs(ROOT, exist_ok=True)
    os.chdir(ROOT)
    manifest = {"files": [
        {"name": "MIC-ERIC.WAV", "role": "mic", "speaker": "eric"},
        {"name": "MIC-NEIL.WAV", "role": "mic", "speaker": "neil"},
        {"name": "CAM-ERIC.MP4", "role": "cam", "speaker": "eric"},
        {"name": "CAM-NEIL.MP4", "role": "cam", "speaker": "neil"},
        {"name": "CAM-WIDE.MP4", "role": "wide"},
    ]}
    with open("manifest.json", "w") as f:
        json.dump(manifest, f)

    print("== building synthetic media ==")
    mix = build_mics()
    build_cams(mix)

    print("== sync ==")
    sync.main(["--manifest", "manifest.json", "--media", ".",
               "--out", "work/offsets.json"])
    offsets = json.load(open("work/offsets.json"))
    for name, (true_off, _l) in CAMS.items():
        got = offsets[name]["offset"]
        assert abs(got - true_off) <= 0.05, \
            f"{name}: recovered {got}, expected {true_off}"
        print(f"OK {name}: {got:+.3f}s (true {true_off:+.1f}s, "
              f"conf {offsets[name]['confidence']})")

    print("== hooks ==")
    tr = stub_transcript()
    with open("work/transcript.json", "w") as f:
        json.dump(tr, f)
    os.environ.pop("ANTHROPIC_API_KEY", None)
    find_hooks.main(["--transcript", "work/transcript.json",
                     "--out", "work/clips.json", "--top", "3"])
    clips = json.load(open("work/clips.json"))
    assert len(clips) >= 2, "expected at least 2 clips"
    hook_starts = {round(c["start"]) for c in clips}
    assert hook_starts & {12, 19, 47, 61}, \
        f"strong openers not surfaced, got starts {hook_starts}"
    assert all(round(c["start"]) != 6 for c in clips), \
        "filler opener should not be picked"

    print("== cut ==")
    # keep only clips the short fixture cams can cover
    clips = [c for c in clips if c["end"] <= 80][:2]
    with open("work/clips.json", "w") as f:
        json.dump(clips, f)
    cut.main(["--manifest", "manifest.json", "--media", ".", "--work", "work",
              "--clips", "work/clips.json",
              "--transcript", "work/transcript.json",
              "--offsets", "work/offsets.json", "--out", "out"])
    rendered = json.load(open("out/clips_manifest.json"))
    assert rendered, "no clips rendered"
    for r in rendered:
        probe = subprocess.run(
            ["ffprobe", "-v", "error", "-select_streams", "v:0",
             "-show_entries", "stream=width,height",
             "-of", "csv=p=0", r["file"]],
            check=True, capture_output=True, text=True).stdout.strip()
        assert probe == "1080,1920", f"{r['file']} is {probe}, want 1080,1920"
        print(f"OK {r['file']}: 1080x1920, source {r['source']}, "
              f"overlay {r['overlay']!r}")

    print("\nALL TESTS PASSED")


if __name__ == "__main__":
    main()
