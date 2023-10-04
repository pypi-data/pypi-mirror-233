import requests
import json


class GetActionBuilder:
    def __init__(self):
        self._instance = GetAction()

    def set_base_url(self, base_url):
        self._instance.base_url = base_url
        return self

    def set_endpoint(self, endpoint):
        self._instance.endpoint = endpoint
        return self

    def set_headers(self, headers):
        self._instance.headers = json.loads(headers)
        return self

    def set_params(self, params):
        self._instance.params = json.loads(params)
        return self

    def build(self):
        return self._instance


class GetAction:
    def __init__(self):
        self.base_url = None
        self.endpoint = None
        self.headers = {}
        self.params = {}

    def execute(self):
        url = f"{self.base_url}/{self.endpoint}"
        response = requests.get(url, headers=self.headers, params=self.params)
        return response.json()

    @staticmethod
    def prepare(data):
        builder = GetActionBuilder()
        return (
            builder.set_base_url(data["base_url"])
            .set_endpoint(data["endpoint"])
            .set_headers(data["headers"])
            .set_params(data["params"])
            .build()
        )


class PatchActionBuilder:
    def __init__(self):
        self._instance = PatchAction()

    def set_base_url(self, base_url):
        self._instance.base_url = base_url
        return self

    def set_endpoint(self, endpoint):
        self._instance.endpoint = endpoint
        return self

    def set_headers(self, headers):
        self._instance.headers = json.loads(headers)
        return self

    def build(self):
        return self._instance


class PatchAction:
    def __init__(self):
        self.base_url = None
        self.endpoint = None
        self.headers = {}

    def execute(self, payload):
        url = f"{self.base_url}/{self.endpoint}"
        response = requests.patch(url, headers=self.headers, json=payload)
        return response.json()

    @staticmethod
    def prepare(data):
        builder = PatchActionBuilder()
        return (
            builder.set_base_url(data["base_url"])
            .set_endpoint(data["endpoint"])
            .set_headers(data["headers"])
            .build()
        )


class PostActionBuilder:
    def __init__(self):
        self._instance = PostAction()

    def set_base_url(self, base_url):
        self._instance.base_url = base_url
        return self

    def set_endpoint(self, endpoint):
        self._instance.endpoint = endpoint
        return self

    def set_headers(self, headers):
        self._instance.headers = json.loads(headers)
        return self

    def build(self):
        return self._instance


class PostAction:
    def __init__(self):
        self.base_url = None
        self.endpoint = None
        self.headers = {}

    def execute(self, payload):
        url = f"{self.base_url}/{self.endpoint}"
        response = requests.post(url, headers=self.headers, json=payload)
        return response.json()

    @staticmethod
    def prepare(data):
        builder = PostActionBuilder()
        return (
            builder.set_base_url(data["base_url"])
            .set_endpoint(data["endpoint"])
            .set_headers(data["headers"])
            .build()
        )


class PutActionBuilder:
    def __init__(self):
        self._instance = PutAction()

    def set_base_url(self, base_url):
        self._instance.base_url = base_url
        return self

    def set_endpoint(self, endpoint):
        self._instance.endpoint = endpoint
        return self

    def set_headers(self, headers):
        self._instance.headers = json.loads(headers)
        return self

    def build(self):
        return self._instance


class PutAction:
    def __init__(self):
        self.base_url = None
        self.endpoint = None
        self.headers = {}

    def execute(self, payload):
        url = f"{self.base_url}/{self.endpoint}"
        response = requests.put(url, headers=self.headers, json=payload)
        return response.json()

    @staticmethod
    def prepare(data):
        builder = PutActionBuilder()
        return (
            builder.set_base_url(data["base_url"])
            .set_endpoint(data["endpoint"])
            .set_headers(data["headers"])
            .build()
        )


class DeleteActionBuilder:
    def __init__(self):
        self._instance = DeleteAction()

    def set_base_url(self, base_url):
        self._instance.base_url = base_url
        return self

    def set_endpoint(self, endpoint):
        self._instance.endpoint = endpoint
        return self

    def set_headers(self, headers):
        self._instance.headers = json.loads(headers)
        return self

    def build(self):
        return self._instance


class DeleteAction:
    def __init__(self):
        self.base_url = None
        self.endpoint = None
        self.headers = {}

    def execute(self):
        url = f"{self.base_url}/{self.endpoint}"
        response = requests.delete(url, headers=self.headers)
        return response.status_code

    @staticmethod
    def prepare(data):
        builder = DeleteActionBuilder()
        return (
            builder.set_base_url(data["base_url"])
            .set_endpoint(data["endpoint"])
            .set_headers(data["headers"])
            .build()
        )
