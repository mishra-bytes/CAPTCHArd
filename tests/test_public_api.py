import sys
from pathlib import Path
import unittest
from unittest.mock import patch

# Ensure package root is on sys.path when running this file directly
sys.path.append(str(Path(__file__).resolve().parents[1]))

import captchard.nsut


class PublicApiTests(unittest.TestCase):
    def test_public_exports_are_callable(self):
        self.assertTrue(callable(captchard.nsut.load_model))
        self.assertTrue(callable(captchard.nsut.segment_captcha))
        self.assertTrue(callable(captchard.nsut.predict_captcha))

    @patch(
        "captchard.nsut.api.predict.predict_from_image",
        return_value={"prediction": "12345", "latency_ms": 2.5},
    )
    def test_predict_captcha_with_explicit_model(self, predict_from_image_mock):
        model = object()
        result = captchard.nsut.predict_captcha("dummy.png", model=model)

        self.assertEqual(result, "12345")
        predict_from_image_mock.assert_called_once_with("dummy.png", model)

    @patch("captchard.nsut.api.predict.load_model", return_value=None)
    def test_predict_captcha_without_available_model(self, load_model_mock):
        result = captchard.nsut.predict_captcha("dummy.png")
        self.assertEqual(result, "Error: Model not loaded")
        load_model_mock.assert_called_once_with(model_path=None)

    @patch(
        "captchard.nsut.api.predict._extract_digits",
        return_value=["d1", "d2", "d3", "d4", "d5"],
    )
    def test_segment_captcha_uses_segmentation_pipeline(self, extract_digits_mock):
        result = captchard.nsut.segment_captcha(b"raw-bytes")
        self.assertEqual(result, ["d1", "d2", "d3", "d4", "d5"])
        extract_digits_mock.assert_called_once_with(b"raw-bytes")


class AsyncApiTests(unittest.IsolatedAsyncioTestCase):
    @patch(
        "captchard.nsut.api.predict.predict_from_image",
        return_value={"prediction": "67890", "latency_ms": 4.1},
    )
    async def test_predict_captcha_endpoint_returns_latency_dict(
        self, predict_from_image_mock
    ):
        from captchard.nsut.api.predict import predict_captcha_endpoint

        model = object()
        result = await predict_captcha_endpoint("dummy.png", model=model)

        self.assertEqual(
            result, {"prediction": "67890", "latency_ms": 4.1}
        )
        predict_from_image_mock.assert_called_once_with("dummy.png", model)

    @patch(
        "captchard.nsut.api.predict._extract_digits",
        return_value=["d1", "d2", "d3", "d4", "d5"],
    )
    async def test_segment_captcha_endpoint(self, extract_digits_mock):
        from captchard.nsut.api.predict import segment_captcha_endpoint

        result = await segment_captcha_endpoint("dummy.png")
        self.assertEqual(result, ["d1", "d2", "d3", "d4", "d5"])
        extract_digits_mock.assert_called_once_with("dummy.png")

