import io
import unittest
from contextlib import redirect_stdout

from otpUtils import (
    decode,
    encode,
    get_string_hash,
    split_message_hash,
    text_to_binary,
    validate_hash,
)
from utils import console_print, filter_none, int_array_to_str, state_to_bloch_vector


class UtilsTests(unittest.TestCase):
    def test_filter_none_keeps_other_falsy_values(self):
        self.assertEqual(filter_none([None, 0, False, "", "X", None]), [0, False, "", "X"])

    def test_int_array_to_str_concatenates_bits(self):
        self.assertEqual(int_array_to_str([0, 1, 0, 1]), "0101")

    def test_console_print_uses_original_separator(self):
        output = io.StringIO()
        with redirect_stdout(output):
            console_print("Alice", "sends", 3, "bits")

        self.assertEqual(
            output.getvalue(),
            "\n ----------------------------------------------------------------- \n$  Alice sends 3 bits\n",
        )

    def test_state_to_bloch_vector_for_zero_state(self):
        try:
            import qiskit  # noqa: F401
        except ImportError:
            self.skipTest("Qiskit is only required for the notebook simulation")

        x, y, z = state_to_bloch_vector([1, 0], trials=2000)

        self.assertAlmostEqual(x, 0, delta=0.1)
        self.assertAlmostEqual(y, 0, delta=0.1)
        self.assertAlmostEqual(z, 1, delta=0.01)


class OtpUtilsTests(unittest.TestCase):
    def test_text_to_binary_uses_eight_bits_per_ascii_character(self):
        self.assertEqual(text_to_binary("Az"), "0100000101111010")

    def test_encode_and_decode_round_trip(self):
        message = "BB84"
        binary_message = text_to_binary(message)
        key = "10100101" * len(message)

        encoded = encode(binary_message, key)

        self.assertEqual(len(encoded), len(key))
        self.assertEqual(decode(encoded, key), message)

    def test_hash_helpers_preserve_and_validate_original_md5_contract(self):
        message = "Hello World"
        digest = get_string_hash(message, 7)

        split_message, split_digest = split_message_hash(message + digest, len(digest))

        self.assertEqual(digest, "b10a8db")
        self.assertEqual((split_message, split_digest), (message, digest))
        self.assertTrue(validate_hash(split_message, split_digest, len(digest)))
        self.assertFalse(validate_hash(message + "!", digest, len(digest)))


if __name__ == "__main__":
    unittest.main()
