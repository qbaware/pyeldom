import json
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


_key = bytes(
    [
        57,
        16,
        127,
        45,
        31,
        100,
        201,
        53,
        0,
        217,
        254,
        8,
        193,
        76,
        91,
        123,
        213,
        1,
        175,
        72,
        28,
        44,
        30,
        12,
        84,
        3,
        8,
        14,
        105,
        228,
        19,
        47,
    ]
)
_init_vector = bytes([0] * 16)


def encrypt(payload_dict):
    try:
        json_str = json.dumps(payload_dict)
        cipher = AES.new(_key, AES.MODE_CBC, _init_vector)
        padded_data = pad(json_str.encode("utf-8"), AES.block_size)
        encrypted_bytes = cipher.encrypt(padded_data)

        return base64.b64encode(encrypted_bytes).decode("utf-8")
    except Exception as e:
        return f"Encryption Error: {e}"


def decrypt(base64_ciphertext):
    try:
        encrypted_bytes = base64.b64decode(base64_ciphertext)
        cipher = AES.new(_key, AES.MODE_CBC, _init_vector)
        decrypted_padded = cipher.decrypt(encrypted_bytes)
        decrypted_bytes = unpad(decrypted_padded, AES.block_size)
        decrypted_string = decrypted_bytes.decode("utf-8")

        return json.loads(decrypted_string)
    except Exception as e:
        return f"Decryption Error: {e}"
