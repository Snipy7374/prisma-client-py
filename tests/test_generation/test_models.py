from pathlib import Path

import pytest
from pydantic import ValidationError
from prisma.generator.models import Module, Config


def test_module_serialization() -> None:
    path = Path(__file__).parent.parent.joinpath('scripts/partial_type_generator.py')
    module = Module(spec=str(path))
    assert Module.parse_raw(module.json()).spec.name == module.spec.name


def test_recursive_type_depth() -> None:
    for value in [-2, -3, 0, 1]:
        with pytest.raises(ValidationError) as exc:
            Config(recursive_type_depth=value)

        assert exc.match('Value must equal -1 or be greater than 1.')

    with pytest.raises(ValidationError) as exc:
        Config(recursive_type_depth='a')

    assert exc.match('value is not a valid integer')

    for value in [-1, 2, 3, 10, 99]:
        config = Config(recursive_type_depth=value)
        assert config.recursive_type_depth == value