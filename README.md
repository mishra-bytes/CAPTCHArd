# CAPTCHArd

CAPTCHArd is a production-oriented Python service library for preprocessing, segmenting, and predicting NSUT-style 5-digit CAPTCHA images.

## Note for Recruiters

This repository demonstrates end-to-end engineering ownership across:

- Computer vision and ML inference (`OpenCV`, `TensorFlow`, `NumPy`)
- API design and package architecture (modular service layers)
- Secure artifact operations (release-based model delivery with SHA256 verification)
- Reproducible developer experience (`uv`-managed environments + lockfile)
- Automated quality gates (`pytest` + GitHub Actions CI)
- Open-source maintainability (clear structure, documentation, and release workflow)

## What This Service Does

CAPTCHArd provides a clean public API for:

- Loading a pretrained CAPTCHA model
- Segmenting captcha images into digit tiles
- Predicting full 5-digit CAPTCHA strings from multiple input types
- Supporting both sync and async endpoint-style prediction flows

Supported input formats:

- File path (`str`)
- `pathlib.Path`
- Raw bytes
- File-like streams (`.read()`)

## Why This Project Uses `uv` (Not Plain `pip`)

`uv` is used as the primary workflow tool because it gives:

- Faster dependency resolution and install times
- Reproducible environments through `uv.lock`
- One-command environment sync (`uv sync --group dev`)
- Reliable command execution inside the managed environment (`uv run ...`)

This reduces dependency drift and local/CI mismatch.

## Installation

Prerequisites:

- Python 3.10+
- `uv` (either globally installed or via `python -m uv`)

```bash
git clone https://github.com/mishra-bytes/CAPTCHArd.git
cd CAPTCHArd
python -m uv sync --group dev
python -m uv run python scripts/download_model.py --tag v1.0
```

The download script pulls `nsut.h5` from GitHub Release assets and verifies it against `checksums/nsut.h5.sha256` before saving to `model/nsut.h5`.

## Quick Start

```python
import captchard.nsut as nsut

model = nsut.load_model("model/nsut.h5")
prediction = nsut.predict_captcha("examples/example_1.jpg", model=model)
print(prediction)
```

## Public API

- `load_model(model_path: str | Path | None = None)`
- `segment_captcha(image)`
- `predict_captcha(image, model=None, model_path=None)`
- `predict_captcha_endpoint(image, model=None, model_path=None)` (async)
- `segment_captcha_endpoint(image)` (async)

## Model Versioning and Release Strategy

Model weights are intentionally versioned as release artifacts, not tracked in Git history.

Release workflow:

1. Create a Git tag (for example `v1.0`).
2. Create the matching GitHub Release.
3. Upload the model weight file (for example `nsut.h5`) under release binaries.
4. Store and commit the trusted SHA256 value in `checksums/nsut.h5.sha256`.
5. Consume the exact version using:

```bash
python -m uv run python scripts/download_model.py --tag v1.0
```

This enables reproducible rollbacks, cleaner source control, and safer artifact distribution.

## Development and Testing

Run tests:

```bash
python -m uv run -- python -m pytest tests/
```

Target a specific test module:

```bash
python -m uv run -- python -m pytest tests/test_public_api.py -v
```

## CI

GitHub Actions CI currently validates:

- Python 3.12
- Dependency sync via `uv`
- Test suite execution with `pytest`

## Repository Layout

```text
CAPTCHArd/
|- captchard/                # Installable package namespace
|  \- nsut/                  # NSUT-specific modules
|     |- adapters/           # External integrations (model loader, clients)
|     |- api/                # Public API entrypoints
|     |- core/               # Vision preprocessing and segmentation logic
|     |- services/           # Prediction and orchestration services
|     \- config/             # Centralized settings
|- checksums/                # Trusted SHA256 hashes for release assets
|- examples/                 # Sample captcha images
|- scripts/                  # Operational utilities (download/verify model)
|- tests/                    # Automated tests
|- pyproject.toml            # Project metadata and dependencies
\- uv.lock                   # Locked dependency graph
```

## Contributing

Contributions are welcome. Please keep changes focused, tested, and documented:

- Add or update tests for behavioral changes
- Preserve API clarity and backward compatibility where possible
- Keep release and checksum integrity in sync when model artifacts change

## License

MIT. See [LICENSE](LICENSE).
