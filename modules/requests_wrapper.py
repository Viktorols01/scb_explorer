import requests
import json
import modules.disk_wrapper as disk_wrapper

cache_path = ".request_cache"


class RequestsWrapper:
    def __init__(self, rate_limiter):
        self.rate_limiter = rate_limiter

    def get(self, url):
        file_path = cache_path + "/" + url.replace("/", "")
        try:
            content = disk_wrapper.read_file(file_path, "rb")
        except:
            if self.rate_limiter:
                self.rate_limiter.acquire(1)
            response = requests.get(url)
            content = response.content
            disk_wrapper.write_file(file_path, content, "wb")
        return content

    def get_json(self, url):
        return json.loads(self.get(url))
