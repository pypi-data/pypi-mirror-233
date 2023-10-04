import specification
import yaml_connector as connectors
import yaml

if __name__ == "__main__":
    raw_spec = connectors.YamlConnector("../tests/test_spec.yaml")

    file_text = open("../tests/test_spec.yaml", "r")
    with file_text:
        try:
            file_text_list = yaml.safe_load(file_text)
        except yaml.YAMLError as exc:
            print(exc)

    test_spec = specification.Specification()

    test_spec.load_spec(file_text_list)
