import unittest

from arikedb_tools.command import Command


class CommandTests(unittest.TestCase):

    def test_command(self):

        self.assertEqual(len(Command.__dict__["_member_names_"]), 17)
        self.assertEqual(Command.SET.value, "SET")
        self.assertEqual(Command.RM.value, "RM")
        self.assertEqual(Command.SET_EVENT.value, "SET_EVENT")
        self.assertEqual(Command.GET.value, "GET")
        self.assertEqual(Command.PGET.value, "PGET")
        self.assertEqual(Command.SUBSCRIBE.value, "SUBSCRIBE")
        self.assertEqual(Command.PSUBSCRIBE.value, "PSUBSCRIBE")
        self.assertEqual(Command.ADD_DATABASE.value, "ADD_DATABASE")
        self.assertEqual(Command.DEL_DATABASE.value, "DEL_DATABASE")
        self.assertEqual(Command.ADD_ROLE.value, "ADD_ROLE")
        self.assertEqual(Command.DEL_ROLE.value, "DEL_ROLE")
        self.assertEqual(Command.ADD_USER.value, "ADD_USER")
        self.assertEqual(Command.DEL_USER.value, "DEL_USER")
        self.assertEqual(Command.SHOW.value, "SHOW")
        self.assertEqual(Command.VARIABLES.value, "VARIABLES")
        self.assertEqual(Command.LOAD_LICENSE.value, "LOAD_LICENSE")
        self.assertEqual(Command.CONFIG.value, "CONFIG")


if __name__ == '__main__':
    unittest.main()
