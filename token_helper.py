import json


def get_token() -> int:
    """ Gets token for discord bot in json file

    :return:
    :rtype:
    """
    try:
        with open("token.json") as json_file:
            token = json.load(json_file).get("token")
            if not token:
                quit("Invalid token.json syntax -> {\"token\": token}")
            json_file.close()
    except FileNotFoundError:
        quit("Add json file with following syntax: token.json -> {\"token\": token}")

    return token
