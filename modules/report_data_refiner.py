from modules.json_serializator import encode, decode
import uuid
import zlib
import base64


def to_bytes(bytes_or_str):
    if isinstance(bytes_or_str, str):
        value = bytes_or_str.encode()  # uses 'utf-8' for encoding
    else:
        value = bytes_or_str
    return value  # Instance of bytes


def to_str(bytes_or_str):
    if isinstance(bytes_or_str, bytes):
        value = bytes_or_str.decode()  # uses 'utf-8' for encoding
    else:
        value = bytes_or_str
    return value  # Instance of str


def add_uids(data):
    try:
        result = decode(data)
        for cell in result['cells']:
            if 'uid' not in cell['json']:
                cell['json']['uid'] = str(uuid.uuid4())[:8]
    except Exception as e:
        print(e)
    finally:
        return result


def delete_unused_props(data):
    try:
        for cell in data['cells']:
            cell['json'].pop('timestamp', None)
            cell['json'].pop('lastVal', None)
    except Exception as e:
        print(e)
    finally:
        return encode(data)


def compress_data(j_model):
    try:
        b_model = to_bytes(j_model)
        compstr = zlib.compress(b_model)
        b64encoded_data = base64.b64encode(compstr)
        result = str(b64encoded_data)
        return result
    except Exception as e:
        print(e)
        return ""


def decompress_data(data):
    try:
        s_cmpstr = data.replace("b'", "", 1)
        s_cmpstr = s_cmpstr.replace("'", "")
        b_cmpstr = to_bytes(s_cmpstr)
        compstr = base64.b64decode(b_cmpstr)
        b_model = zlib.decompress(compstr)
        str = to_str(b_model)
        return str
    except Exception as e:
        print(e)
        return ""
