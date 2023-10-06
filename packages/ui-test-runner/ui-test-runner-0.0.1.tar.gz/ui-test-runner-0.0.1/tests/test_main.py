"""Test the UI Test Runner."""
import pytest

from ui_test_runner import run_ui_test


def test_run_test(httpx_mock):
    """Test that a UI test can successfully run."""
    # initial submission
    httpx_mock.add_response(json={"status": "success", "data": "123"})
    # getting the status
    httpx_mock.add_response(json={"status": "success"})
    # getting the response
    httpx_mock.add_response(
        json={
            "data": {
                "results": [
                    {
                        "subject": "PUBCHEM.COMPOUND:000001",
                        "object": "MONDO:0005737",
                        "predicate": "treats",
                    },
                ],
            },
        }
    )
    output = run_ui_test(
        "ci",
        "treats(creative)",
        "Acceptable",
        "MONDO:0005737",
        "PUBCHEM.COMPOUND:000001",
    )

    assert output == "Passed!"
