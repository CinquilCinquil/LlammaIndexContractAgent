import yaml

google_api_key = None

with open("resources/api_key.yaml") as stream:
    try:
        load = yaml.safe_load(stream)
        google_api_key = load['GOOGLE_API_KEY']
    except yaml.YAMLError as exc:
        print(exc)