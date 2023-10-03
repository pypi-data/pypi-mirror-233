import unittest

from pythonUtilitiesProject.utilities.utilities import Utilities

class TestUtilities(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestUtilities, self).__init__(*args, **kwargs)

    def test_clean_special_characters(self) -> None:
        """
        The function `test_clean_special_characters` tests the
        `clean_special_characters` function in the `Utilities` class by comparing
        the expected output with the actual output.
        """
        test_value = "\tdef\nin\ant"
        expected = "defin\ant"
        result = Utilities.clean_special_characters(test_value)
        self.assertEqual(result, expected, "The input {} should return {} with the special characters \t and \n removed".format(test_value, expected))

    def test_modify_special_characters(self) -> float:
        """
        The function `test_modify_special_characters` tests the
        `modify_special_characters` function in the `Utilities` class by checking if it
        correctly replaces the special character `\xa0` with a space.
        """
        test_value = "mal\xa0mike"
        expected = "mal mike"
        result = Utilities.modify_special_characters(test_value)
        self.assertEqual(result, expected, "The input {} should return {} with the special characters \\xa0 replaced with a space".format(test_value, expected))
