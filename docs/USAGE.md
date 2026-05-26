# Usage

## Setup

```bash
python -m uv sync --group dev
```

## Quick Example

```python
from captchard.nsut import load_model, predict_captcha

model = load_model("model/final_captcha_model.h5")
result = predict_captcha("examples/example_1.jpg", model=model)
print(result)
```

## API Surface

- `load_model(model_path: str | Path | None = None)`
- `segment_captcha(image)`
- `predict_captcha(image, model=None, model_path=None)`

Supported `image` input types:
- `str` file path
- `pathlib.Path`
- raw `bytes`
- file-like stream (`.read()`)

## Configuration

Core settings are in `captchard/nsut/config/settings.py`.

## Tests

```bash
python -m uv run pytest tests/
```
