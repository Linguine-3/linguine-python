def round_json_floats(data, precision: int = 8):
    if isinstance(data, float):
        return '{:.{precision}f}'.format(data, precision=precision)
    elif isinstance(data, dict):
        return {key: round_json_floats(value, precision) for key, value in data.items()}
    elif isinstance(data, list):
        return [round_json_floats(value, precision) for value in data]
    else:
        return data
