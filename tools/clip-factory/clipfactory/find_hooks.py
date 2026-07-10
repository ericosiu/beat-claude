"""Pick clip candidates and score their opening line as a hook.

A shortform clip lives or dies on its first ~2 seconds, so candidates are
anchored on utterance openings that already work as a cold open — claims,
numbers, contrarian takes, curiosity gaps — then extended to a natural
endpoint (pause or speaker turn) inside the 18-75s window.

Scoring is heuristic-first so the pipeline runs fully offline. If
ANTHROPIC_API_KEY is set (or --anthropic passed), candidates are re-ranked
by Claude, which also writes the on-screen hook overlay text and a post
caption per clip.
"""
import argparse
import json
import os
import re

from .common import load_json, log, save_json

MIN_LEN, MAX_LEN, TARGET = 18.0, 75.0, 45.0

# Signals that make a first line stop the scroll.
HOOK_PATTERNS = [
    (r"\$[\d,.]+|[\d,.]+ ?(percent|%|x\b|million|billion|k\b)", 3.0, "number"),
    (r"\b(nobody|no one|most people|everyone) (talks about|tells you|is doing|gets|knows|understands|thinks)", 4.0, "contrarian"),
    (r"\b(stop|never|don't|quit) (doing|using|buying|posting|running|hiring)", 3.5, "imperative"),
    (r"\b(the biggest mistake|the (one|single) (thing|reason)|the truth (is|about)|here's (what|why|how|the thing))", 3.5, "curiosity"),
    (r"\b(i (lost|made|spent|wasted|paid)|we (grew|went from|scaled|lost))", 3.0, "story"),
    (r"\b(is dead|is over|doesn't work( anymore)?|is a (lie|scam|waste))", 3.5, "spiky"),
    (r"^(what|why|how|would you|did you know|have you ever)\b", 2.0, "question"),
    (r"\b(secret|counterintuitive|unpopular opinion|hot take|controversial)\b", 2.5, "tease"),
    (r"\b(ai|chatgpt|claude|agents?|automation)\b", 1.5, "topical"),
    (r"\bif (you|your)\b.{0,40}\b(then|you should|you need)\b", 2.0, "conditional"),
]

FILLER_OPEN = re.compile(
    r"^(um+|uh+|so+|yeah|like|you know|i mean|okay|ok|and|but|well)[,\s]", re.I)


def sentence_starts(utt):
    """Word indices that begin a sentence within an utterance."""
    starts = [0]
    for i, w in enumerate(utt["words"][:-1]):
        if re.search(r"[.!?]$", w["text"]):
            starts.append(i + 1)
    return starts


def hook_score(text):
    score, tags = 0.0, []
    head = text[:160].lower()
    for pat, pts, tag in HOOK_PATTERNS:
        if re.search(pat, head):
            score += pts
            tags.append(tag)
    if FILLER_OPEN.match(text):
        score -= 2.0
    first_words = len(text.split()[:12])
    if first_words < 4:
        score -= 1.0
    return score, tags


def build_candidates(utterances):
    cands = []
    for ui, utt in enumerate(utterances):
        for si in sentence_starts(utt):
            w0 = utt["words"][si]
            text_from = " ".join(w["text"] for w in utt["words"][si:])
            score, tags = hook_score(text_from)
            if score <= 0:
                continue
            # Extend across following utterances to a natural end.
            end, end_texts = None, [text_from]
            last_t1 = utt["t1"]
            for nxt in utterances[ui + 1:]:
                if last_t1 - w0["t0"] >= MIN_LEN and (
                        nxt["t0"] - last_t1 > 1.0 or last_t1 - w0["t0"] >= TARGET):
                    break
                if nxt["t0"] - w0["t0"] > MAX_LEN:
                    break
                end_texts.append(f"[{nxt['speaker']}] {nxt['text']}")
                last_t1 = min(nxt["t1"], w0["t0"] + MAX_LEN)
            end = last_t1
            dur = end - w0["t0"]
            if dur < MIN_LEN:
                continue
            # Prefer clips near TARGET length.
            length_bonus = 1.0 - abs(dur - TARGET) / TARGET
            cands.append({
                "start": round(w0["t0"], 2),
                "end": round(end, 2),
                "speaker": utt["speaker"],
                "hook_line": " ".join(text_from.split()[:30]),
                "text": " ".join(end_texts)[:2000],
                "score": round(score + length_bonus, 2),
                "signals": tags,
            })
    return cands


def dedupe(cands, min_gap=20.0):
    """Keep the best candidate per neighborhood so clips don't overlap."""
    out = []
    for c in sorted(cands, key=lambda c: -c["score"]):
        if all(abs(c["start"] - o["start"]) > min_gap for o in out):
            out.append(c)
    return out


def overlay_from_hook(hook_line):
    clause = re.split(r"[,.;:!?]", hook_line)[0]
    if len(clause.split()) < 3:  # too short a clause, fall back to word cap
        clause = hook_line
    text = " ".join(clause.split()[:8]).rstrip(",.;:")
    return text.upper()


def anthropic_rerank(cands, top_n):
    import urllib.request
    key = os.environ["ANTHROPIC_API_KEY"]
    prompt = (
        "You are a shortform video editor for a marketing podcast (Eric Siu & "
        "Neil Patel style). Below are candidate clips with transcripts. Pick "
        f"the {top_n} that will perform best on TikTok/Reels/Shorts, favoring "
        "spiky claims, numbers, and curiosity gaps in the first line. For each "
        "pick, write: overlay (on-screen hook text, max 8 punchy words, may "
        "rephrase), and caption (1-sentence post caption + 3 hashtags). "
        "Return JSON: [{index, overlay, caption, why}].\n\n" +
        json.dumps([{ "index": i, "hook_line": c["hook_line"],
                      "text": c["text"][:600]} for i, c in enumerate(cands)]))
    body = json.dumps({
        "model": os.environ.get("CLIP_FACTORY_MODEL", "claude-sonnet-5"),
        "max_tokens": 4000,
        "messages": [{"role": "user", "content": prompt}],
    }).encode()
    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages", data=body,
        headers={"x-api-key": key, "anthropic-version": "2023-06-01",
                 "content-type": "application/json"})
    with urllib.request.urlopen(req) as resp:
        text = json.load(resp)["content"][0]["text"]
    picks = json.loads(re.search(r"\[.*\]", text, re.S).group(0))
    out = []
    for p in picks:
        c = dict(cands[p["index"]])
        c["overlay"] = p["overlay"]
        c["caption"] = p["caption"]
        c["why"] = p.get("why", "")
        out.append(c)
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--transcript", default="work/transcript.json")
    ap.add_argument("--out", default="work/clips.json")
    ap.add_argument("--top", type=int, default=10)
    ap.add_argument("--anthropic", action="store_true",
                    help="re-rank with Claude (needs ANTHROPIC_API_KEY)")
    args = ap.parse_args(argv)

    tr = load_json(args.transcript)
    cands = dedupe(build_candidates(tr["utterances"]))
    log(f"{len(cands)} deduped candidates")

    if args.anthropic or os.environ.get("ANTHROPIC_API_KEY"):
        try:
            clips = anthropic_rerank(cands[: args.top * 3], args.top)
        except Exception as e:  # offline etc. — heuristics still ship clips
            log(f"anthropic re-rank failed ({e}); using heuristic ranking")
            clips = cands[: args.top]
    else:
        clips = cands[: args.top]

    for i, c in enumerate(clips):
        c.setdefault("overlay", overlay_from_hook(c["hook_line"]))
        c.setdefault("caption", c["hook_line"][:120])
        c["id"] = f"clip{i+1:02d}"
    save_json(args.out, clips)
    for c in clips:
        log(f"{c['id']} [{c['start']:.0f}s-{c['end']:.0f}s] "
            f"({c['speaker']}, {c['score']}) {c['overlay']}")


if __name__ == "__main__":
    main()
