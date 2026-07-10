"""Download session media from Google Drive.

Uses gdown, which handles Drive's large-file confirmation flow for files
shared as "anyone with the link". For private files, either run this on a
machine where the Drive folder is synced (then just --link the local dir)
or use rclone with an authorized remote:

    rclone copy gdrive:<folder> media/ --drive-shared-with-me
"""
import argparse
import os

from .common import load_json, log


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--out", default="media")
    ap.add_argument("--only", nargs="*", help="only these file names")
    ap.add_argument("--skip-video", action="store_true",
                    help="download mic WAVs only (enough to transcribe + pick clips)")
    args = ap.parse_args(argv)

    import gdown  # deferred so the rest of the pipeline works without it

    manifest = load_json(args.manifest)
    os.makedirs(args.out, exist_ok=True)
    for f in manifest["files"]:
        if args.only and f["name"] not in args.only:
            continue
        if args.skip_video and f["role"] != "mic":
            continue
        dest = os.path.join(args.out, f["name"])
        if os.path.exists(dest):
            log(f"already have {dest}")
            continue
        log(f"downloading {f['name']} ...")
        gdown.download(id=f["drive_id"], output=dest, resume=True)
    log("download step done")


if __name__ == "__main__":
    main()
