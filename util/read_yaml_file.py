import yaml


def read_yaml_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        return yaml.load(file, Loader=yaml.FullLoader)
