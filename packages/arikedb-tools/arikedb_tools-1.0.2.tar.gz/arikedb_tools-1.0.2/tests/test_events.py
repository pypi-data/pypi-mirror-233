import unittest

from arikedb_tools.events import TagEvent


class CommandTests(unittest.TestCase):

    def test_command(self):

        self.assertEqual(len(TagEvent.__dict__["_member_names_"]), 10)
        self.assertEqual(TagEvent.ON_SET.value, "on_set")
        self.assertEqual(TagEvent.ON_CHANGE.value, "on_change")
        self.assertEqual(TagEvent.ON_RISING_EDGE.value, "on_rising_edge")
        self.assertEqual(TagEvent.ON_FALLING_EDGE.value, "on_falling_edge")
        self.assertEqual(TagEvent.ON_CROSS_LOW_THRESHOLD.value,
                         "on_cross_low_threshold")
        self.assertEqual(TagEvent.ON_CROSS_HIGH_THRESHOLD.value,
                         "on_cross_high_threshold")
        self.assertEqual(TagEvent.ON_RANGE_OUT.value, "on_range_out")
        self.assertEqual(TagEvent.ON_RANGE_IN.value, "on_range_in")
        self.assertEqual(TagEvent.ON_HIGH_POS_RATE.value, "on_high_pos_rate")
        self.assertEqual(TagEvent.ON_HIGH_NEG_RATE.value, "on_high_neg_rate")


if __name__ == '__main__':
    unittest.main()
