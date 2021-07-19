from flask import jsonify, make_response

def respond(data=None, code: int=200): 
    """Send response with built object"""
    if data is None:
        return make_response('', code)
    else:
        return make_response(jsonify(data), code)

def check_query_param_contains_quotes(city_string: str, ascii_values: list) -> bool:

    for character in city_string:
        ascii_values.append(ord(character))

    try:
        if ascii_values[0] == 34 and ascii_values[-1] == 34 and len(ascii_values) > 2:
            return True
        else:
            return False
    except IndexError:
        return False

def convert_ascii_with_quotes_to_string_with_no_quotes(ascii_list: list) -> str :
    ascii_list.pop()
    ascii_list.pop(0)
    string_value_with_no_quotes: str = ''.join(chr(ascii_value) for ascii_value in ascii_list)
    return string_value_with_no_quotes