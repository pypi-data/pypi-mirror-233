import pythoness

def count_chars(s: str, c: str) -> int:
    """
    Given a string s and a character c, return the number of times c appears in s.
    """
    return s.count(c)
print('Running tests.')
assert count_chars('hello, this is a test.', 't') == 3
assert count_chars('hello, this is a test.', 'e') == 2
assert count_chars('hello, this is a test.', 's') == 3
assert count_chars('hello, this is a test.', 'i') == 2
assert count_chars('hello, this is a test.', 'q') == 0
print('Tests complete.')