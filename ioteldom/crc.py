import zlib

import json

def crc32(payload: dict):
    """
    Eldom's CRC32 checksum algorithm.
    """

    payload_string = json.dumps(
        payload, separators=(",", ":")
    )
    json_data = payload_string[1:-1]  # Remove the outer curly braces
    crc_input_bytes = json_data.encode('utf-8')
    checksum_int = zlib.crc32(crc_input_bytes) & 0xFFFFFFFF
    crc = f'{checksum_int:08X}'

    return crc
