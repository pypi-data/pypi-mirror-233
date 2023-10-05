def merge_upgrade(first_req: dict, second_req: dict) -> dict:
    new_req = {}

    for key, value in first_req.items():
        if key not in new_req:
            new_req[key] = value

        elif translate_to_int(new_req[key]) < translate_to_int(value):
            new_req[key] = value

    for key, value in second_req.items():
        if key not in new_req:
            new_req[key] = value

        elif translate_to_int(new_req[key]) < translate_to_int(value):
            new_req[key] = value

    return new_req


def merge_downgrade(first_req: dict, second_req: dict) -> dict:
    new_req = {}

    for key, value in first_req.items():
        if key not in new_req:
            new_req[key] = value

        elif translate_to_int(new_req[key]) < translate_to_int(value):
            new_req[key] = value

    for key, value in second_req.items():
        if key not in new_req:
            new_req[key] = value

        elif translate_to_int(new_req[key]) > translate_to_int(value):
            new_req[key] = value

    return new_req


def translate_to_int(version: str) -> int:
    return int("".join(version.split(".")))


def translate_dict_to_file(data: dict) -> str:
    content = ""

    for key, value in data.items():
        content += key + "==" + value + "\n"

    return content
