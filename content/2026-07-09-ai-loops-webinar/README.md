# Clip Package — "How I Grow Revenue With AI Loops: The Three I Run Every Week"

**Source:** Riverside recording `268dd33f-c27e-4ec2-86ef-37fb50d4b156` (studio `leveling-up-shorts`), webinar recorded 2026-07-09, 9:30 AM PDT.
Preview link (share token required):
`https://riverside.com/editor/preview/268dd33f-c27e-4ec2-86ef-37fb50d4b156/6a4fd7fdf2609eef92c42d88?share-token=f8f28d4ffd82ddc7c1bd&content-shared=recording-preview`

## What's in this folder

| File | What it is |
|---|---|
| `clip-plan-shortform.md` | 8 shortform clips (60–90s, 1080×1920 vertical) with hooks, verbatim in/out cues, captions, CTAs |
| `clip-plan-midform.md` | 5 midform clips (2–5 min, 1920×1080 landscape) for X / LinkedIn |
| `longform-edit-script.md` | 10-minute YouTube longform edit script with cold-open highlight montage + cliffhanger intro, titles, thumbnail direction |
| `transcript-webinar-public-portion.txt` | Reference transcript (public webinar portion only) |
| `tools/clips.csv` | Machine-readable cut list — exact timecodes for all shorts (S*), midforms (M*), and longform montage pulls (X*) |
| `tools/captions-source-timeline.srt` | Word-accurate captions on the source timeline (from Riverside's transcript) |
| `tools/cut_clips.py` | ffmpeg batch renderer — cuts every clip in `clips.csv` from the source export in the right dimensions |

## How timecodes work (read this first)

All timecodes are **exact on the source recording timeline**, aligned to Riverside's own word-level transcript for the recording (fetched via the share link). Source runtime is **43:33**; the recording starts right at go-live ("Alright guys, it's time" at 00:00:03) and ends on "goodbye" — there is no pre/post-roll to trim. Each clip also carries its verbatim in-cue quote as a cross-check.

`tools/captions-source-timeline.srt` is generated from the same word-level timing — burn it directly, or re-cut caption blocks from it; timestamps are on the source timeline, and ffmpeg's subtitles filter offsets them automatically when cutting with `-ss`.

## Rendering the actual files

Once you have the source export (MP4) locally:

```bash
python3 tools/cut_clips.py --source /path/to/webinar-export.mp4 --csv tools/clips.csv --out renders/
# add --srt tools/captions-source-timeline.srt to burn captions
# add --only S1,S2 to render a subset
```

Vertical clips render as center-crop 9:16 or blur-padded 9:16 (full frame on a blurred background) per the `mode` column in `clips.csv` — blur-pad is preset on the clips where Eric's screen content matters (S4 recruiting demo, S6 CRO demo).

## Why the MP4s aren't in this branch

`riverside.com` is reachable from this session (that's how the assets, HLS playlists, and word-level transcript above were pulled), but the actual video segments are served from **`vod.riverside.com`**, which the session's network policy still blocks. One more allowlist entry (`vod.riverside.com`, or `*.riverside.com`) and the render pipeline below runs end-to-end. Note the share-link HLS tops out at 640×360 — fine for review cuts; for publish-quality renders, export the 4K/1080 source from Riverside (or drop it in the Drive episodes folder) and point `cut_clips.py` at it.
