import warnings
import pytest

from dreamteam.crew import Dreamteam


def test_no_pydantic_mixing_warning():
    # Catch warnings during Dreamteam initialization
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        _ = Dreamteam()
    # Assert that no mixing warning is present
    messages = [str(warning.message) for warning in w]
    assert not any("Mixing V1 models and V2 models" in msg for msg in messages), \
        "Le warning Pydantic mixing V1/V2 n'est pas supprimé correctement."
