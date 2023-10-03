import os
import re

class Utilities(object):
    @classmethod
    def clean_special_characters(cls, string) -> str:
        """
        The function `clean_special_characters` removes special characters such as
        tabs and newlines from a given string and returns the cleaned string.

        :param cls: The parameter "cls" is typically used as a reference to the
        class itself. It is commonly used in class methods to access class-level
        variables or methods. However, in the given code snippet, the "cls"
        parameter is not being used, so it can be safely removed
        :param string: The `string` parameter is a string that may contain special
        characters such as tabs (`\t`) and newlines (`\n`)
        :return: a string.
        """
        return re.sub('\\t|\\n', '', string).strip()

    @classmethod
    def modify_special_characters(cls, string) -> str:
        """
        The function `modify_special_characters` replaces the special character `\xa0`
        with a space and removes any leading or trailing whitespace from the input
        string.

        :param cls: The parameter `cls` is a reference to the class itself. It is
        commonly used in class methods to access class-level variables or methods.
        However, in the given code snippet, `cls` is not used, so it can be safely
        removed from the method signature
        :param string: The `string` parameter is a string that may contain special
        characters
        :return: a modified version of the input string with special characters replaced
        by spaces and any leading or trailing whitespace removed.
        """
        return re.sub('\\xa0', ' ', string).strip()
