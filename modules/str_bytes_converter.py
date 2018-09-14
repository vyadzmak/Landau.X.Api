def to_bytes(bytes_or_str):
    try:
        if isinstance(bytes_or_str, str):
            value = bytes_or_str.encode()  # uses 'utf-8' for encoding
        else:
            value = bytes_or_str
        return value  # Instance of bytes
    except Exception as e:
        raise e


def to_str(bytes_or_str):
    try:
        if isinstance(bytes_or_str, bytes):
            value = bytes_or_str.decode()  # uses 'utf-8' for encoding
        else:
            value = bytes_or_str
        return value  # Instance of str
    except Exception as e:
        raise e