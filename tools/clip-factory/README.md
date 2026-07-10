# clip-factory

Turns a multicam podcast session into captioned 9:16 shortform clips that
open on a strong hook. Built for the `0709` Eric x Neil studio session
(`manifest.json` already points at the Drive file IDs) but works for any
session with per-speaker mic WAVs + speaker cams + an optional wide cam.

## What it does

1. **download** — pulls session media from Google Drive (gdown).
   `--skip-video` grabs only the two mic WAVs (~1.3 GB), which is enough to
   transcribe and pick clips before committing to the ~150 GB of video.
2. **transcribe** — faster-whisper with word timestamps on each mic track.
   Dual mic tracks = perfect speaker attribution, no diarization model.
3. **hooks** — scores every sentence opening as a cold-open hook (numbers,
   contrarian claims, "stop doing X", curiosity gaps, story leads; filler
   openers penalized), extends each to a natural endpoint in the 18–75 s
   window, dedupes overlaps, ranks. With `ANTHROPIC_API_KEY` set, Claude
   re-ranks the shortlist and writes the on-screen overlay text + post
   caption per clip; without it, heuristics produce both.
4. **sync** — cross-correlates each camera's scratch audio against the mic
   mix to recover per-file start offsets (±20 ms), so transcript timestamps
   map onto any camera file. Warns on low-confidence alignment.
5. **cut** — per clip: picks the majority speaker's camera (wide cam when
   it's a real back-and-forth), crops to 1080x1920, lays the mic mix over
   it (never camera scratch audio), normalizes to -14 LUFS (social spec),
   burns 3-word caption cards from word timings plus a 2.8 s hook overlay,
   and writes `clips/clipNN.mp4` + `clips/clips_manifest.json` with the
   caption copy for posting.

## Run it

```bash
cd tools/clip-factory
pip install -r requirements.txt   # plus: ffmpeg on PATH

# Cheap first pass: audio only -> review the clip list
python run.py download --manifest manifest.json --skip-video
python run.py transcribe --manifest manifest.json            # GPU: --device cuda
python run.py hooks --top 10                                  # + ANTHROPIC_API_KEY for Claude re-rank

# Review work/clips.json (edit/trim/reorder freely), then fetch only the
# video files the picked clips actually need and render:
python run.py download --manifest manifest.json
python run.py sync --manifest manifest.json
python run.py cut --manifest manifest.json
```

`python run.py all --manifest manifest.json` runs the whole chain.

### Hardware notes

- Transcription: `large-v3` needs a GPU to be pleasant; on CPU use
  `--model medium.en` (~2x realtime on 8 cores for two ~1 h tracks).
- Rendering: each 45 s clip re-encodes in roughly real time on CPU.
- Disk: full session is ~150 GB. The `--skip-video`-first flow plus
  `download --only <files>` keeps peak usage to the cams you actually cut.

### Private Drive files

gdown handles files shared as "anyone with the link". For a private
folder, either run on a machine with the folder synced locally (drop the
files into `media/` and skip download) or `rclone copy` with an authorized
Drive remote.

## Verify

`python tests/test_pipeline.py` builds a synthetic session (two mic
tracks, three cameras with known start offsets), then asserts sync
recovers offsets within 50 ms, hook scoring surfaces spiky openers and
rejects filler ones, and rendered files are 1080x1920 with captions
burned. No network or Whisper model needed.
