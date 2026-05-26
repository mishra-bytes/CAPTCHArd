"""Download the NSUT model weights from GitHub Releases with SHA256 verification."""

from __future__ import annotations

import argparse
import hashlib
import shutil
import sys
import tempfile
from pathlib import Path
from urllib.request import urlopen


DEFAULT_REPO = "mishra-bytes/CAPTCHArd"
DEFAULT_TAG = "v1.0"
DEFAULT_ASSET = "nsut.h5"
DEFAULT_CHECKSUM_FILE = Path("checksums") / "nsut.h5.sha256"


def _download(url: str, destination: Path) -> None:
    with urlopen(url) as response, destination.open("wb") as out:
        shutil.copyfileobj(response, out)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _read_expected_checksum(path: Path) -> str:
    first_token = path.read_text(encoding="utf-8").strip().split()[0]
    return first_token.lower()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Download nsut.h5 from GitHub Releases and verify its SHA256 checksum."
    )
    parser.add_argument("--repo", default=DEFAULT_REPO, help="GitHub repo in owner/name form.")
    parser.add_argument("--tag", default=DEFAULT_TAG, help="Release tag (default: v1.0).")
    parser.add_argument("--asset", default=DEFAULT_ASSET, help="Release asset filename.")
    parser.add_argument(
        "--checksum-file",
        default=str(DEFAULT_CHECKSUM_FILE),
        help="Local checksum file to validate against.",
    )
    parser.add_argument(
        "--sha256",
        default=None,
        help="Explicit expected SHA256 hash (overrides --checksum-file).",
    )
    parser.add_argument(
        "--output",
        default=str(Path("model") / DEFAULT_ASSET),
        help="Output path for downloaded model.",
    )
    args = parser.parse_args()

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    expected_hash = args.sha256.lower() if args.sha256 else None
    if expected_hash is None:
        checksum_path = Path(args.checksum_file)
        if not checksum_path.exists():
            print(
                f"Checksum file not found: {checksum_path}. "
                "Provide --sha256 or add checksums/nsut.h5.sha256.",
                file=sys.stderr,
            )
            return 2
        expected_hash = _read_expected_checksum(checksum_path)

    base = f"https://github.com/{args.repo}/releases/download/{args.tag}"
    asset_url = f"{base}/{args.asset}"

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir) / args.asset
        print(f"Downloading {asset_url}")
        _download(asset_url, tmp_path)

        actual_hash = _sha256(tmp_path)
        if actual_hash != expected_hash:
            print(
                "SHA256 mismatch.\n"
                f"Expected: {expected_hash}\n"
                f"Actual:   {actual_hash}",
                file=sys.stderr,
            )
            return 3

        shutil.move(str(tmp_path), output_path)
        print(f"Saved verified model to {output_path}")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
