from TableauConMan import yaml_connector
import unittest


class TestServerConnector(unittest.TestCase):
    pass


class TestYamlConnector(unittest.TestCase):
    def setUp(self):
        test_yaml = """
            groups:
              - group_name: Test Group
            """
        test_file = "test_spec.yaml"
        self.connector_1 = yaml_connector.YamlConnector(yaml=test_yaml)
        self.connector_2 = yaml_connector.YamlConnector(test_file)

    def test_get(self):
        valid_connector_1 = [{"group_name": "Test Group"}]
        valid_connector_2 = [{"group_name": "All Users"}, {"group_name": "Test Group"}]

        self.assertEqual(self.connector_1.get_yaml("groups"), valid_connector_1)
        self.assertNotEqual(self.connector_1.get_yaml("projects"), valid_connector_1)

        self.assertEqual(self.connector_2.get_yaml("groups"), valid_connector_2)
        self.assertNotEqual(self.connector_2.get_yaml("projects"), valid_connector_2)


if __name__ == "__main__":
    unittest.main()
