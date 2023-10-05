import unittest
from threading import Thread
from unittest.mock import patch, Mock

from arikedb.arikedb import ArikedbClient
from arikedb_tools.exceptions import ArikedbClientError
from arikedb_tools.events import TagEvent
from arikedb_tools.command import Command


class ArikedbClientTests(unittest.TestCase):

    @patch.object(ArikedbClient, "send_command")
    def test_list_databases(self, mock_send_command):
        mock_send_command.return_value = {
            "status": 0,
            "databases": ["db1", "db2"]
        }

        client = ArikedbClient()
        databases = client.list_databases()
        expected_databases = ["db1", "db2"]
        self.assertListEqual(databases, expected_databases)

        mock_send_command.return_value = {
            "status": 1,
            "msg": "Mock Error"
        }
        err = "Error listing databases. Err code 1. Mock Error"

        client = ArikedbClient()
        self.assertRaisesRegex(ArikedbClientError, err, client.list_databases)

    @patch.object(ArikedbClient, "send_command")
    def test_list_roles(self, mock_send_command):
        mock_send_command.return_value = {
            "status": 0,
            "roles": [{"role": 1}, {"role": 2}]
        }

        client = ArikedbClient()
        roles = client.list_roles()
        expected_roles = [{"role": 1}, {"role": 2}]
        self.assertListEqual(roles, expected_roles)

        mock_send_command.return_value = {
            "status": 1,
            "msg": "Mock Error"
        }
        err = "Error listing roles. Err code 1. Mock Error"

        client = ArikedbClient()
        self.assertRaisesRegex(ArikedbClientError, err, client.list_roles)

    @patch.object(ArikedbClient, "send_command")
    def test_list_users(self, mock_send_command):
        mock_send_command.return_value = {
            "status": 0,
            "users": ["user1", "user2"]
        }

        client = ArikedbClient()
        users = client.list_users()
        expected_users = ["user1", "user2"]
        self.assertListEqual(users, expected_users)

        mock_send_command.return_value = {
            "status": 1,
            "msg": "Mock Error"
        }
        err = "Error listing users. Err code 1. Mock Error"

        client = ArikedbClient()
        self.assertRaisesRegex(ArikedbClientError, err, client.list_users)

    @patch.object(ArikedbClient, "send_command")
    def test_list_variables(self, mock_send_command):
        mock_send_command.return_value = {
            "status": 0,
            "variables": ["FLOAT: var1", "INT: var2"]
        }

        client = ArikedbClient()
        variables = client.list_variables([])
        expected_variables = [{"var_name": "var1", "var_type": "FLOAT"},
                              {"var_name": "var2", "var_type": "INT"}]
        self.assertListEqual(variables, expected_variables)

        mock_send_command.return_value = {
            "status": 1,
            "msg": "Mock Error"
        }
        err = "Error listing variables. Err code 1. Mock Error"

        client = ArikedbClient()
        self.assertRaisesRegex(ArikedbClientError, err, client.list_variables,
                               [])

    @patch.object(ArikedbClient, "send_command")
    def test_set_config(self, mock_send_command):
        mock_send_command.return_value = {
            "status": 0
        }

        client = ArikedbClient()
        rc = client.set_config(x=1, y=2)
        self.assertEqual(rc, 0)

        mock_send_command.return_value = {
            "status": 1,
            "msg": "Mock Error"
        }
        err = "Error setting database configurations. Err code 1. Mock Error"

        client = ArikedbClient()
        self.assertRaisesRegex(ArikedbClientError, err, client.set_config)

    @patch.object(ArikedbClient, "send_command")
    def test_reset_config(self, mock_send_command):
        mock_send_command.return_value = {
            "status": 0
        }

        client = ArikedbClient()
        rc = client.reset_config()
        self.assertEqual(rc, 0)

        mock_send_command.return_value = {
            "status": 1,
            "msg": "Mock Error"
        }
        err = "Error resetting database configurations. Err code 1. Mock Error"

        client = ArikedbClient()
        self.assertRaisesRegex(ArikedbClientError, err, client.reset_config)

    @patch.object(ArikedbClient, "send_command")
    def test_get_config(self, mock_send_command):
        mock_send_command.return_value = {
            "status": 0,
            "msg": '{"mock": "config"}'
        }

        client = ArikedbClient()
        conf = client.get_config()
        self.assertDictEqual(conf, {"mock": "config"})

        mock_send_command.return_value = {
            "status": 1,
            "msg": "Mock Error"
        }
        err = "Error getting database configurations. Err code 1. Mock Error"

        client = ArikedbClient()
        self.assertRaisesRegex(ArikedbClientError, err, client.get_config)

    @patch.object(ArikedbClient, "send_command")
    def test_use(self, mock_send_command):
        mock_send_command.return_value = {
            "status": 0
        }

        client = ArikedbClient()
        rc = client.use("db1")
        self.assertEqual(rc, 0)

        mock_send_command.return_value = {
            "status": 1,
            "msg": "Mock Error"
        }
        err = "Error using database. Err code 1. Mock Error"

        client = ArikedbClient()
        self.assertRaisesRegex(ArikedbClientError, err, client.use, "db1")

    @patch.object(ArikedbClient, "send_command")
    def test_set(self, mock_send_command):
        mock_send_command.return_value = {
            "status": 0
        }

        client = ArikedbClient()
        rc = client.set({"t1": 1}, {"meta1": 2}, 12345.12)
        self.assertEqual(rc, 0)

        mock_send_command.return_value = {
            "status": 1,
            "msg": "Mock Error"
        }
        err = "Error setting variables. Err code 1. Mock Error"

        client = ArikedbClient()
        self.assertRaisesRegex(ArikedbClientError, err, client.set, {})

    @patch.object(ArikedbClient, "send_command")
    def test_rm(self, mock_send_command):
        mock_send_command.return_value = {
            "status": 0
        }

        client = ArikedbClient()
        rc = client.rm(["var*"])
        self.assertEqual(rc, 0)

        mock_send_command.return_value = {
            "status": 1,
            "msg": "Mock Error"
        }
        err = "Error removing variables. Err code 1. Mock Error"

        client = ArikedbClient()
        self.assertRaisesRegex(ArikedbClientError, err, client.rm, [])

    @patch.object(ArikedbClient, "send_command")
    def test_set_event(self, mock_send_command):
        mock_send_command.return_value = {
            "status": 0
        }

        client = ArikedbClient()
        rc = client.set_event(["*"], TagEvent.ON_SET, 1, 2, 3, 4)
        self.assertEqual(rc, 0)

        mock_send_command.return_value = {
            "status": 1,
            "msg": "Mock Error"
        }
        err = "Error setting variables event. Err code 1. Mock Error"

        client = ArikedbClient()
        self.assertRaisesRegex(ArikedbClientError, err, client.set_event, [],
                               TagEvent.ON_RISING_EDGE)

    @patch.object(ArikedbClient, "send_command")
    def test_get(self, mock_send_command):
        mock_send_command.return_value = {
            "status": 0,
            "values": ["v1", "v2"]
        }

        client = ArikedbClient()
        values = client.get(["tag1", "tag2"], "s", 1, 2)
        self.assertListEqual(values, ["v1", "v2"])

        mock_send_command.return_value = {
            "status": 1,
            "msg": "Mock Error"
        }
        err = "Error getting variable values. Err code 1. Mock Error"

        client = ArikedbClient()
        self.assertRaisesRegex(ArikedbClientError, err, client.get, [])

    @patch.object(ArikedbClient, "send_command")
    def test_pget(self, mock_send_command):
        mock_send_command.return_value = {
            "status": 0,
            "values": ["v1", "v2"]
        }

        client = ArikedbClient()
        values = client.pget(["tag1*", "tag[23]"], "s", 1, 2)
        self.assertListEqual(values, ["v1", "v2"])

        mock_send_command.return_value = {
            "status": 1,
            "msg": "Mock Error"
        }
        err = "Error getting variable values. Err code 1. Mock Error"

        client = ArikedbClient()
        self.assertRaisesRegex(ArikedbClientError, err, client.pget, [])

    @patch.object(Thread, "start")
    @patch.object(ArikedbClient, "send_command")
    def test_subscribe(self, mock_send_command, mock_start):
        mock_send_command.return_value = {
            "status": 0,
            "sub_id": "1234"
        }
        callback = Mock()

        client = ArikedbClient()
        t = client.subscribe(["t1"], callback, "s", TagEvent.ON_SET, 1, 2, 3, 4)
        self.assertIsInstance(t, Thread)
        mock_start.assert_called_once()
        client._subscribed = "1234"

        mock_send_command.return_value = {
            "status": 1,
            "msg": "Mock Error"
        }
        err = "Error subscribing to variables. Err code 1. Mock Error"

        client = ArikedbClient()
        self.assertRaisesRegex(ArikedbClientError, err, client.subscribe, [],
                               "callback")

    @patch.object(Thread, "start")
    @patch.object(ArikedbClient, "send_command")
    def test_psubscribe(self, mock_send_command, mock_start):
        mock_send_command.return_value = {
            "status": 0,
            "sub_id": "1234"
        }
        callback = Mock()

        client = ArikedbClient()
        t = client.psubscribe(["t1"], callback, "s", TagEvent.ON_SET,
                              1, 2, 3, 4)
        self.assertIsInstance(t, Thread)
        mock_start.assert_called_once()
        client._subscribed = "1234"

        mock_send_command.return_value = {
            "status": 1,
            "msg": "Mock Error"
        }
        err = "Error psubscribing to variables. Err code 1. Mock Error"

        client = ArikedbClient()
        self.assertRaisesRegex(ArikedbClientError, err, client.psubscribe, [],
                               "callback")

    @patch.object(ArikedbClient, "_send_unack_command")
    def test_unsubscribe(self, mock__send_unack_command):
        mock__send_unack_command.return_value = None

        client = ArikedbClient()
        client._subscribed = True
        rc = client.unsubscribe()
        self.assertEqual(rc, 0)
        self.assertFalse(client._subscribed)

    @patch.object(ArikedbClient, "send_command")
    def test_add_database(self, mock_send_command):
        mock_send_command.return_value = {
            "status": 0
        }

        client = ArikedbClient()
        rc = client.add_database("db1")
        self.assertEqual(rc, 0)

        mock_send_command.return_value = {
            "status": 1,
            "msg": "Mock Error"
        }
        err = "Error creating database. Err code 1. Mock Error"

        client = ArikedbClient()
        self.assertRaisesRegex(ArikedbClientError, err, client.add_database, "")

    @patch.object(ArikedbClient, "send_command")
    def test_del_database(self, mock_send_command):
        mock_send_command.return_value = {
            "status": 0
        }

        client = ArikedbClient()
        rc = client.del_database("db1")
        self.assertEqual(rc, 0)

        mock_send_command.return_value = {
            "status": 1,
            "msg": "Mock Error"
        }
        err = "Error deleting database. Err code 1. Mock Error"

        client = ArikedbClient()
        self.assertRaisesRegex(ArikedbClientError, err, client.del_database, "")

    @patch.object(ArikedbClient, "send_command")
    def test_auth(self, mock_send_command):
        mock_send_command.return_value = {
            "status": 0
        }

        client = ArikedbClient()
        rc = client.auth("john", "123")
        self.assertEqual(rc, 0)

        mock_send_command.return_value = {
            "status": 1,
            "msg": "Mock Error"
        }
        err = "Error authenticating. Err code 1. Mock Error"

        client = ArikedbClient()
        self.assertRaisesRegex(ArikedbClientError, err, client.auth, "a", "1")

    @patch.object(ArikedbClient, "send_command")
    def test_add_role(self, mock_send_command):
        mock_send_command.return_value = {
            "status": 0
        }

        client = ArikedbClient()
        rc = client.add_role("new_role", [Command.PGET, Command.GET])
        self.assertEqual(rc, 0)

        mock_send_command.return_value = {
            "status": 1,
            "msg": "Mock Error"
        }
        err = "Error creating role. Err code 1. Mock Error"

        client = ArikedbClient()
        self.assertRaisesRegex(ArikedbClientError, err, client.add_role, "", [])

    @patch.object(ArikedbClient, "send_command")
    def test_del_role(self, mock_send_command):
        mock_send_command.return_value = {
            "status": 0
        }

        client = ArikedbClient()
        rc = client.del_role("new_role")
        self.assertEqual(rc, 0)

        mock_send_command.return_value = {
            "status": 1,
            "msg": "Mock Error"
        }
        err = "Error deleting role. Err code 1. Mock Error"

        client = ArikedbClient()
        self.assertRaisesRegex(ArikedbClientError, err, client.del_role, "")

    @patch.object(ArikedbClient, "send_command")
    def test_add_user(self, mock_send_command):
        mock_send_command.return_value = {
            "status": 0
        }

        client = ArikedbClient()
        rc = client.add_user("admin", "john", "123")
        self.assertEqual(rc, 0)

        mock_send_command.return_value = {
            "status": 1,
            "msg": "Mock Error"
        }
        err = "Error creating user. Err code 1. Mock Error"

        client = ArikedbClient()
        self.assertRaisesRegex(ArikedbClientError, err, client.add_user,
                               "", "", "")

    @patch.object(ArikedbClient, "send_command")
    def test_del_user(self, mock_send_command):
        mock_send_command.return_value = {
            "status": 0
        }

        client = ArikedbClient()
        rc = client.del_user("john")
        self.assertEqual(rc, 0)

        mock_send_command.return_value = {
            "status": 1,
            "msg": "Mock Error"
        }
        err = "Error deleting user. Err code 1. Mock Error"

        client = ArikedbClient()
        self.assertRaisesRegex(ArikedbClientError, err, client.del_user, "")


if __name__ == '__main__':
    unittest.main()
