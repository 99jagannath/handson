import yaml

with open("test.yaml", "r") as stream:
    try:
        data = list(yaml.safe_load_all(stream))
        print(data)
    except yaml.YAMLError as exc:
        print(exc)