import pickle

import pytest

import crystalai

EXCEPTION_TEST_CASES = [
    crystalai.InvalidRequestError(
        "message",
        "param",
        code=400,
        http_body={"test": "test1"},
        http_status="fail",
        json_body={"text": "iono some text"},
        headers={"request-id": "asasd"},
    ),
    crystalai.error.AuthenticationError(),
    crystalai.error.PermissionError(),
    crystalai.error.RateLimitError(),
    crystalai.error.ServiceUnavailableError(),
    crystalai.error.SignatureVerificationError("message", "sig_header?"),
    crystalai.error.APIConnectionError("message!", should_retry=True),
    crystalai.error.TryAgain(),
    crystalai.error.Timeout(),
    crystalai.error.APIError(
        message="message",
        code=400,
        http_body={"test": "test1"},
        http_status="fail",
        json_body={"text": "iono some text"},
        headers={"request-id": "asasd"},
    ),
    crystalai.error.OpenAIError(),
]


class TestExceptions:
    @pytest.mark.parametrize("error", EXCEPTION_TEST_CASES)
    def test_exceptions_are_pickleable(self, error) -> None:
        assert error.__repr__() == pickle.loads(pickle.dumps(error)).__repr__()
