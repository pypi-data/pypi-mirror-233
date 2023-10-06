import yaml


def load_yaml(path: str):
    with open(path, "r") as stream:
        try:
            config = yaml.load(stream, Loader=yaml.FullLoader)
            return config
        except yaml.YAMLError as exc:
            print(exc)


def save_yaml(path: str, my_dict) -> None:
    with open(path, "w") as file:
        yaml.dump(my_dict, file)
