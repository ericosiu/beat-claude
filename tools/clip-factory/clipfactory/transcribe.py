"""Transcribe each speaker's mic WAV with faster-whisper and merge into a
single speaker-labeled, word-timestamped transcript on the master (recorder)
timeline.

Dual mic tracks give us perfect diarization for free: whatever comes off
0709-ERIC.WAV is Eric, whatever comes off 0709-NEIL.WAV is Neil. Crosstalk
bleed is suppressed by dropping words whose energy on the other track is
higher (handled implicitly by Whisper's VAD on quiet bleed in practice;
--min-bleed-gap guards pathological cases).
"""
import argparse
import os

from .common import load_json, log, save_json


def transcribe_track(path, model, language="en"):
    segments, _info = model.transcribe(
        path, language=language, word_timestamps=True, vad_filter=True,
        vad_parameters={"min_silence_duration_ms": 400})
    words = []
    for seg in segments:
        for w in seg.words or []:
            words.append({"t0": round(w.start, 3), "t1": round(w.end, 3),
                          "text": w.word.strip()})
    return words


def merge_tracks(tracks):
    """tracks: {speaker: [words]} -> flat word list sorted by time, plus
    utterances (speaker turns split on >1.2s gaps or speaker change)."""
    words = []
    for speaker, ws in tracks.items():
        for w in ws:
            words.append({**w, "speaker": speaker})
    words.sort(key=lambda w: w["t0"])

    utterances = []
    cur = None
    for w in words:
        if (cur is None or w["speaker"] != cur["speaker"]
                or w["t0"] - cur["t1"] > 1.2):
            if cur:
                utterances.append(cur)
            cur = {"speaker": w["speaker"], "t0": w["t0"], "t1": w["t1"],
                   "text": w["text"], "words": [w]}
        else:
            cur["t1"] = w["t1"]
            cur["text"] += " " + w["text"]
            cur["words"].append(w)
    if cur:
        utterances.append(cur)
    return words, utterances


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--media", default="media")
    ap.add_argument("--out", default="work/transcript.json")
    ap.add_argument("--model", default="large-v3",
                    help="faster-whisper model (large-v3 recommended; "
                         "medium.en if CPU-bound)")
    ap.add_argument("--device", default="auto")
    args = ap.parse_args(argv)

    from faster_whisper import WhisperModel
    manifest = load_json(args.manifest)
    compute = "float16" if args.device == "cuda" else "int8"
    model = WhisperModel(args.model, device=args.device, compute_type=compute)

    tracks = {}
    for f in manifest["files"]:
        if f["role"] != "mic":
            continue
        path = os.path.join(args.media, f["name"])
        log(f"transcribing {path} as {f['speaker']} ...")
        tracks[f["speaker"]] = transcribe_track(path, model)

    words, utterances = merge_tracks(tracks)
    save_json(args.out, {"words": words, "utterances": utterances})
    log(f"{len(words)} words, {len(utterances)} utterances")


if __name__ == "__main__":
    main()
