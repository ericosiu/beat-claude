#!/usr/bin/env python3
"""Batch-render social clips from the webinar source export with ffmpeg.

Usage:
    python3 cut_clips.py --source webinar.mp4 [--csv clips.csv] [--out renders/]
                         [--only S1,S2] [--srt captions.srt] [--dry-run]

Reads clips.csv (id,label,start,end,format,mode,in_cue) and renders each row:
  format=vertical  -> 1080x1920: mode=crop (center crop) or mode=blurpad
                      (full frame scaled onto a blurred 9:16 background)
  format=landscape -> 1920x1080 scale/pad

Timecodes in clips.csv are exact on the source recording timeline (aligned to
Riverside's word-level transcript). If your export is trimmed differently,
re-anchor with each clip's in_cue quote before rendering.
"""

import argparse
import csv
import shlex
import subprocess
import sys
from pathlib import Path

VF = {
    # Hybrid vertical: half-width crop anchored on the speaker's seat position
    # (x=27% of frame width for this recording's framing), blur-filled to 9:16.
    # A raw 9:16 center crop clips the face - the source is already a close-up.
    ("vertical", "crop"): (
        "split[a][b];"
        "[a]scale=1080:1920:force_original_aspect_ratio=increase,"
        "crop=1080:1920,gblur=sigma=30,eq=brightness=-0.15[bg];"
        "[b]crop=iw*0.5:ih:iw*0.27:0,scale=1080:-2[fg];"
        "[bg][fg]overlay=(W-w)/2:(H-h)/2,setsar=1"
    ),
    ("vertical", "blurpad"): (
        "split[a][b];"
        "[a]scale=1080:1920:force_original_aspect_ratio=increase,"
        "crop=1080:1920,gblur=sigma=30,eq=brightness=-0.15[bg];"
        "[b]scale=1080:-2[fg];"
        "[bg][fg]overlay=(W-w)/2:(H-h)/2,setsar=1"
    ),
    ("landscape", "scale"): (
        "scale=1920:1080:force_original_aspect_ratio=decrease,"
        "pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1"
    ),
}


def build_cmd(src, row, out_dir, srt=None):
    key = (row["format"], row["mode"])
    if key not in VF:
        raise ValueError(f"{row['id']}: unknown format/mode {key}")
    vf = VF[key]
    if srt:
        style = "FontSize=16,Bold=1,Outline=2,MarginV=60"
        vf += f",subtitles={shlex.quote(str(srt))}:force_style='{style}'"
    out = out_dir / f"{row['id']}-{row['label']}.mp4"
    # Input-side seek is fast but resets timestamps to 0, which would desync a
    # source-timeline SRT burn - use output-side seek (slower, exact) with --srt.
    seek = ["-ss", row["start"], "-to", row["end"]]
    cmd = (
        ["ffmpeg", "-hide_banner", "-y"]
        + ([] if srt else seek) + ["-i", str(src)] + (seek if srt else [])
        + [
        "-filter_complex" if "[a]" in vf else "-vf", vf,
        "-c:v", "libx264", "-preset", "medium", "-crf", "19",
        "-c:a", "aac", "-b:a", "192k",
        "-movflags", "+faststart",
        str(out),
    ])
    return cmd, out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", required=True, type=Path)
    ap.add_argument("--csv", type=Path, default=Path(__file__).parent / "clips.csv")
    ap.add_argument("--out", type=Path, default=Path("renders"))
    ap.add_argument("--only", help="comma-separated clip ids")
    ap.add_argument("--srt", type=Path, help="burn these captions into every clip")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    if not args.source.exists():
        sys.exit(f"source not found: {args.source}")
    args.out.mkdir(parents=True, exist_ok=True)
    only = set(args.only.split(",")) if args.only else None

    rows = [r for r in csv.DictReader(open(args.csv)) if not only or r["id"] in only]
    if not rows:
        sys.exit("no matching clips in csv")

    print("Timecodes are word-level exact on the source recording timeline; "
          "the in_cue quote is a cross-check if your export is trimmed differently.\n")
    failed = []
    for row in rows:
        cmd, out = build_cmd(args.source, row, args.out, args.srt)
        print(f"[{row['id']}] {row['start']}-{row['end']} -> {out.name}")
        print(f"    cue: \"{row['in_cue'][:70]}...\"")
        if args.dry_run:
            print("    " + " ".join(shlex.quote(c) for c in cmd))
            continue
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            failed.append(row["id"])
            print(f"    FAILED:\n{res.stderr[-800:]}")
    if failed:
        sys.exit(f"failed clips: {', '.join(failed)}")
    print(f"\ndone -> {args.out}/")


if __name__ == "__main__":
    main()
