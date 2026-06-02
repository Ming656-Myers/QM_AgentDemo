import json
from urllib.request import urlopen


#该函数访问URL并解析JSON
def get_json(url):
    with urlopen(url, timeout=10) as response:
        return json.loads(response.read().decode("utf-8"))