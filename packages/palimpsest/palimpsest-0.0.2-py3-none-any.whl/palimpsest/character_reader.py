import yaml

REQUIRED_FIELDS = ["name", "age", "occupation"]


def validate_character_sketch(character_data):
    missing_fields = [field for field in REQUIRED_FIELDS if field not in character_data]
    if missing_fields:
        msg = f'Missing required fields: {", ".join(missing_fields)}'
        raise ValueError(msg)


def read_character_sketch(file_path):
    with open(file_path) as file:
        character_data = yaml.safe_load(file)

    validate_character_sketch(character_data)

    return character_data
