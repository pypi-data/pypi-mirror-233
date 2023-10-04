import unittest

from arikedb_tools.tables import format_table


class TableTests(unittest.TestCase):

    def test_format_table(self):

        tab = format_table("title", ["h1", "h2"], [(1, 2), ("a", "b")])
        expected_tab = "╭───────────╮\n" \
                       "│   title   │\n" \
                       "├─────┬─────┤\n" \
                       "│  h1 │  h2 │\n" \
                       "├─────┼─────┤\n" \
                       "│ 1   │ 2   │\n" \
                       "├─────┼─────┤\n" \
                       "│ a   │ b   │\n" \
                       "╰─────┴─────╯"
        self.assertEqual(tab, expected_tab)

    def test_format_table_len(self):

        tab = format_table("title", ["h1", "h2"], [(1, 2), ("a", "b")], 5)
        expected_tab = "╭─────────────╮\n" \
                       "│    title    │\n" \
                       "├──────┬──────┤\n" \
                       "│  h1  │  h2  │\n" \
                       "├──────┼──────┤\n" \
                       "│ 1    │ 2    │\n" \
                       "├──────┼──────┤\n" \
                       "│ a    │ b    │\n" \
                       "╰──────┴──────╯"
        self.assertEqual(tab, expected_tab)

    def test_format_table_len_iter(self):

        tab = format_table("title", ["h1", "h2"], [(1, 2), ("a", "b")], [5, 6])
        expected_tab = "╭──────────────╮\n" \
                       "│    title     │\n" \
                       "├──────┬───────┤\n" \
                       "│  h1  │   h2  │\n" \
                       "├──────┼───────┤\n" \
                       "│ 1    │ 2     │\n" \
                       "├──────┼───────┤\n" \
                       "│ a    │ b     │\n" \
                       "╰──────┴───────╯"
        self.assertEqual(tab, expected_tab)


if __name__ == '__main__':
    unittest.main()
