import warnings
import pytest

from squadmanager.crew import squadmanager


def test_no_pydantic_mixing_warning():
    # Catch warnings during squadmanager initialization
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        _ = squadmanager()
    # Assert that no mixing warning is present
    messages = [str(warning.message) for warning in w]
    assert not any("Mixing V1 models and V2 models" in msg for msg in messages), \
        "Le warning Pydantic mixing V1/V2 n'est pas supprimé correctement."
