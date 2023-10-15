from deadcode.cli import main
from deadcode.tests.base import BaseTestCase


class TestNoqaComments(BaseTestCase):
    def test_unused_class_is_unchanged_if_noqa_comment_is_provided(self):
        self.files = {
            "foo.py": """
                class MyTest:  # noqa: DC003
                    pass
                """
        }

        unused_names = main(["foo.py", "--no-color", "--fix"])

        self.assertFiles(
            {
                "foo.py": """
                class MyTest:  # noqa: DC003
                    pass
                """
            }
        )

        self.assertEqual(unused_names, None)


    # | DC001  | unused-variable    | Variable `{name}` is never used
    # | DC002  | unused-function    | Function `{name}` is never used
    # | DC003  | unused-class       | Class `{name}` is never used
    # | DC004  | unused-method      | Method `{name}` is never used
    # | DC005  | unused-attribute   | Attribute `{name}` is never used
    # | DC006  | unused-name        | Name `{name}` is never used
    # | DC007  | unused-import      | Import `{name}` is never used
    # | DC008  | unused-property    | Property `{name}` is never used
    # | DC009  | unreachable-code   | Unreachable `else` block
    # | DC011  | empty-file         | Empty file
    # | DC012* | commented-out-code | Commented out code
    # | DC013* | ignore-expression  | *This error code can ony be used in `# noqa: DC013` comments (no errors will be reported for expression which begins in current line)*

