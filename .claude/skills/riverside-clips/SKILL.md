---
name: riverside-clips
description: Turn a Riverside share link into social clips — shortform (60–90s 9:16), midform (2–5min 16:9), and a 10-min YT longform edit script with montage/cliffhanger cold open. Use when given a riverside.com share/preview URL and asked to "clip this up".
---

# Riverside → Social Clips

Input: a Riverside share URL like
`https://riverside.com/editor/preview/<SESSION_ID>/<CLIP_ID>?share-token=<TOKEN>&content-shared=recording-preview`
(also works from `/dashboard/studios/.../recordings/<SESSION_ID>?share-token=<TOKEN>` — the SESSION_ID + token are what matter).

Network prerequisites: `riverside.com` AND `vod.riverside.com` must be allowed by the session's network policy. If `vod.riverside.com` CONNECTs fail (000/403 tunnel errors), everything except segment download still works — do the plan + timecodes, and tell the user to allowlist `vod.riverside.com`.

## Step 1 — Fetch assets, transcript, and media

Run `tools/riverside_fetch.py` (in this repo):

```bash
python3 tools/riverside_fetch.py --session <SESSION_ID> --clip <CLIP_ID> --token <TOKEN> --out work/
```

It hits Riverside's share API (no login needed, just the share token):
- `api/v4/take/{session}/clip/{clip}/clip-assets/share?t={token}` → track list, durations, screen-share segment offsets
- `api/v4/transcriptions/editable/{session}?t={token}` → **word-level timestamps** (the key asset — every cut gets exact timecodes)
- `api/v4/vod/{session}/{trackId}/share?playlist=part_0_.m3u8&t={token}` (+ `hls_from_concat_part_1_.m3u8` for audio) → HLS segments on vod.riverside.com, downloaded in parallel and muxed to `source.mp4`

Outputs: `source.mp4`, `transcript-words.json`, `captions.srt`, `assets.json`.
Note: share-link HLS is ~720p — good for review cuts and social midforms; for publish-quality masters ask for the 4K/1080 export from Riverside and re-render against it (same timecodes).

## Step 2 — Pick clips from the transcript

Read the whole transcript before cutting. Select by hook strength, not chronology:

- **Shortform (8-ish, 60–90s, 1080×1920):** each must open ON the hook line — a contrarian command ("fire all of them"), a number ("$25,000", "60 hours"), or a quotable thesis. No lead-in. Rank them; mark a lead clip.
- **Midform (5-ish, 2–5min, 1920×1080):** self-contained segments (one demo/story each) with a cold-open peak quote and per-clip post copy for X/LinkedIn.
- **Longform (10 min, YT):** edit script with a 0:00–0:45 cold-open montage of 5–7 pulls — include at least two cliffhangers (cut a story before it resolves) — then sections that pay each cliffhanger off; titles, thumbnail direction, chapters.
- **CTA rotation** per the current brand push (check #comms-central for what's live — e.g. Skill Dojo / the Game / Loops Creator / singlegrain.com/apply).

Anchor every clip by exact quote, then align to word timestamps (match normalized token runs against `transcript-words.json`) to produce start/end timecodes. Pad −0.3s in, +0.9s out.

## Step 3 — Render

Write `clips.csv` (`id,label,start,end,format,mode,in_cue`) and run:

```bash
python3 tools/cut_clips.py --source work/source.mp4 --csv clips.csv --out renders/
```

Framing modes (see `content/2026-07-09-ai-loops-webinar/tools/cut_clips.py` for the canonical filters):
- `vertical/crop` — hybrid 9:16: half-width crop anchored on the speaker's seat position + blurred fill. **Never use a raw 9:16 center crop on Eric's close-up framing — it clips his face.** Verify the anchor (`iw*0.27` worked for the July 2026 setup) by extracting 3–4 frames across the runtime and LOOKING at them before batch rendering.
- `vertical/blurpad` — full 16:9 frame on blurred 9:16 background; use whenever the screen-share content matters.
- `landscape/scale` — 1920×1080 for midforms.

Always extract and visually inspect at least one frame per framing mode before delivering.

## Step 4 — Deliver

- Commit the clip plans + cut list + edit script to the working branch (markdown, not MP4s).
- Send rendered MP4s via chat (≤30 MiB per file — compress delivery copies with CRF 25 / 720p if needed) or drop them in the Drive episodes folder.
- Deliverable docs to include: shortform plan (hook text, why-it-works, caption/CTA per clip), midform plan (post copy per clip), longform edit script (montage table with timecodes, section payoffs, titles, thumbnail).
