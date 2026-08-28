import hashlib

BITS_PER_CHAR = 8


def text_to_binary(text):
    """Convert an ASCII string to its eight-bit binary representation."""
    return "".join(format(ord(character), "08b") for character in text)


def binary_to_text(binary_text):
    return chr(int(binary_text[:BITS_PER_CHAR], 2))


def encode(binary_message, key):
    """Encode a binary message by applying a one-time-pad XOR key."""
    xor_result = int(binary_message, 2) ^ int(key, 2)
    return format(xor_result, "0" + str(len(key)) + "b")


def decode(encoded_message, key):
    """Decode a binary one-time-pad message back into text."""
    xor_result = int(encoded_message, 2) ^ int(key, 2)
    xor_result_string = format(xor_result, "0" + str(len(key)) + "b")
    bytes_array = [
        xor_result_string[index : index + BITS_PER_CHAR]
        for index in range(0, len(xor_result_string), BITS_PER_CHAR)
    ]
    return "".join(binary_to_text(character) for character in bytes_array)


def get_string_hash(message, hash_length=0):
    """Return the notebook's original MD5 integrity digest contract."""
    hash_object = hashlib.md5(message.encode())
    if hash_length == 0:
        return hash_object.hexdigest()
    return hash_object.hexdigest()[:hash_length]


def split_message_hash(full_message, hash_length):
    message = full_message[: len(full_message) - hash_length]
    hash_string = full_message[len(full_message) - hash_length :]
    return message, hash_string


def validate_hash(message, hash_string, hash_length):
    hash_object = hashlib.md5(message.encode())
    return hash_string == hash_object.hexdigest()[:hash_length]
