def check_request(request_data: dict, check_list: list):
    try:
        for prop in check_list:
            key = request_data[prop]

            if type(key) == str and not len(key):
                return False

            if type(key) == int and key < 0:
                return False

            if type(key) == bool:
                pass

    except Exception as error:
        print(error)
        return False

    return True
