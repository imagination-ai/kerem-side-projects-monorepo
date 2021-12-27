from style.utils.utils import sanitize_author_name


def test_sanitize_author_name():
    cases = [
        "Jefferson, Thomas, 1743-1826",
        "George Fyler, 1814-1900 [Translator]",
        "Townsend, George Fyler, 1814-1900 [Translator]",
    ]

    expects = ["thomas_jefferson", "george_fyler", "george_fyler_townsend"]

    for case, expect in zip(cases, expects):
        assert sanitize_author_name(case) == expect
