import pytest
from _pytest.capture import CaptureFixture
from typer.testing import CliRunner

from api_compose.cli.main import app


@pytest.fixture()
def test_runner() -> CliRunner:
    return CliRunner()


@pytest.fixture()
def clean_up(
        capsys: CaptureFixture,
        test_runner,
):
    yield
    with capsys.disabled() as disabled:
        # Clean
        result = test_runner.invoke(app, [
            "clean",
        ])


def test_can_compile(
        capsys: CaptureFixture,
        test_runner,
        clean_up,
):
    """Assert that manifests can be compiled"""
    with capsys.disabled() as disabled:
        result = test_runner.invoke(
            app,
            [
                "compile",
            ],
            # Let Result Capture return_value
            standalone_mode=False
        )
        assert result.exit_code == 0, "Result is non-zero"
