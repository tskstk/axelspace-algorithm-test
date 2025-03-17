from typing import Dict


def make_km_table(pattern: str) -> Dict[str, int]:
    """Creates the bad character table for a given pattern.

    This table records the distance from the end of the pattern for each character
    in the pattern (excluding the last character), which is used to determine the shift
    when a mismatch occurs during the search.

    Args:
        pattern (str): The pattern string for which the table is created.

    Returns:
        Dict[str, int]: A dictionary mapping each character in the pattern to its shift distance.
    """
    table = dict()
    pattern_length = len(pattern)

    for i in range(pattern_length - 1):
        table[pattern[i]] = pattern_length - 1 - i

    return table


class Bm(object):
    """A class that implements the Boyer-Moore string search algorithm using the bad character rule.

    Attributes:
        text (str): The text in which to search for the pattern.
        pattern (str): The pattern to search for.
        bad_char_table (Dict[str, int]): The bad character table for the pattern.
    """

    def __init__(self, text: str, pattern: str):
        """Initializes the Bm instance with text and pattern, and creates the bad character table.

        Args:
            text (str): The text string to be searched.
            pattern (str): The pattern string to search for.
        """
        self.text = text
        self.pattern = pattern
        self.table = make_km_table(pattern)

    def decide_slide_width(self, c: str) -> int:
        """Determines the shift width based on the current heuristic(s).

        Currently, this function uses the bad character rule. It may be extended
        in the future to incorporate additional heuristics such as the good suffix rule.

        Args:
            c (str): The character in the text that caused the mismatch.

        Returns:
            int: The number of positions to shift the pattern. If the character is not found in the pattern,
                 the pattern length is returned.
        """
        assert len(c) == 1
        return self.table.get(c, len(self.pattern))

    def search(self) -> int:
        """Searches for the pattern in the text using the Boyer-Moore algorithm.

        The search compares the pattern and text from right to left and shifts the pattern based on
        the result of 'decide_slide_width' when a mismatch occurs.

        Returns:
            int: The starting index of the pattern in the text if found; otherwise, -1.
        """
        pattern_length = len(self.pattern)
        text_length = len(self.text)

        if pattern_length == 0 or pattern_length > text_length:
            return -1

        if self.pattern == self.text:
            return 0

        text_index = pattern_length - 1

        while text_index < text_length:
            pattern_index = pattern_length - 1
            current_text_index = text_index

            while pattern_index >= 0 and self.pattern[pattern_index] == self.text[current_text_index]:
                pattern_index -= 1
                current_text_index -= 1

            if pattern_index < 0:
                return current_text_index + 1

            text_index += self.decide_slide_width(self.text[text_index])

        return -1
