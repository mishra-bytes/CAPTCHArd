"""Service layer."""

from captchard.nsut.services.predict_service import (
    predict_from_digits,
    predict_from_image,
)

__all__ = ["predict_from_digits", "predict_from_image"]

