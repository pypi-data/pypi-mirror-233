import pytest

from palimpsest import read_character_sketch, validate_character_sketch


def test_read_character_sketch():
    char_data = read_character_sketch("tests/data/example_character.yaml")
    assert isinstance(char_data, dict)


def test_read_character_sketch_content():
    char_data = read_character_sketch("tests/data/example_character.yaml")
    assert char_data["name"] == "Jane Doert"
    assert char_data["age"] == 39
    assert "Intelligent" in char_data["traits"]


def test_validate_character_sketch_valid():
    char_data = {
        "name": "Jane Doert",
        "age": 39,
        "occupation": "Engineer",
        "traits": ["Intelligent", "Introverted"],
        "relationships": [{"name": "Mary Sue", "relation": "Wife"}],
    }
    try:
        validate_character_sketch(char_data)
    except ValueError:
        pytest.fail("Valid sketch was rejected.")


def test_validate_character_sketch_invalid():
    char_data = {
        "name": "Jane Doert",
        "age": 39,
        # missing 'occupation'
        "traits": ["Intelligent", "Introverted"],
        "relationships": [{"name": "Mary Sue", "relation": "Wife"}],
    }
    with pytest.raises(ValueError):
        validate_character_sketch(char_data)
