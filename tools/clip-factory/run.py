#!/usr/bin/env python3
"""clip-factory: turn a multicam podcast recording into captioned 9:16
shortform clips with strong cold-open hooks.

Stages (each also runnable alone via `python run.py <stage> --help`):

  download    pull session media from Google Drive (gdown)
  transcribe  faster-whisper on each mic WAV -> speaker-labeled words
  hooks       pick + rank clip candidates by hook strength
  sync        cross-correlate cams against mic audio -> per-file offsets
  cut         render 1080x1920 clips w/ captions, hook overlay, -14 LUFS

  all         download -> transcribe -> hooks -> sync -> cut
"""
import sys

from clipfactory import cut, download, find_hooks, sync, transcribe

STAGES = {
    "download": download.main,
    "transcribe": transcribe.main,
    "hooks": find_hooks.main,
    "sync": sync.main,
    "cut": cut.main,
}


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print(__doc__)
        return 0
    stage, argv = sys.argv[1], sys.argv[2:]
    if stage == "all":
        common = [a for a in argv]
        download.main(common)
        transcribe.main(common)
        find_hooks.main([])
        sync.main(common)
        cut.main(common)
        return 0
    if stage not in STAGES:
        print(f"unknown stage: {stage}\n{__doc__}")
        return 1
    STAGES[stage](argv)
    return 0


if __name__ == "__main__":
    sys.exit(main())
