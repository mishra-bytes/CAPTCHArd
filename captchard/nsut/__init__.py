from .api.predict import (
    predict_captcha,
    load_model,
    segment_captcha,
    predict_captcha_endpoint,
    segment_captcha_endpoint,
)

# Also expose predict_captcha simply as 'predict' for convenience
predict = predict_captcha

__all__ = [
    "predict",
    "predict_captcha",
    "load_model",
    "segment_captcha",
    "predict_captcha_endpoint",
    "segment_captcha_endpoint",
]
