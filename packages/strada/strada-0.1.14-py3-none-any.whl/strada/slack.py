import json
import requests


class PostMessageActionBuilder:
    def __init__(self):
        self._instance = None

    def set_token(self, token):
        self._get_instance().token = token
        return self

    def set_channel(self, channel):
        self._get_instance().channel = channel
        return self

    def build(self):
        return self._get_instance()

    def _get_instance(self):
        if self._instance is None:
            self._instance = PostMessageAction()
        return self._instance


class PostMessageAction:
    def __init__(self):
        self.token = None
        self.channel = None

    def execute(self, text):
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-type": "application/json",
        }
        payload = json.dumps({"channel": self.channel, "text": text})
        response = requests.post(
            "https://slack.com/api/chat.postMessage", headers=headers, data=payload
        )
        return response.json()

    @staticmethod
    def prepare(data):
        builder = PostMessageActionBuilder()
        return (
            builder.set_token(data["access_token"]).set_channel(data["channel"]).build()
        )


class CreateConversationActionBuilder:
    def __init__(self):
        self._instance = None

    def set_token(self, token):
        self._get_instance().token = token
        return self

    def set_is_private(self, is_private):
        self._get_instance().is_private = is_private
        return self

    def build(self):
        return self._get_instance()

    def _get_instance(self):
        if self._instance is None:
            self._instance = CreateConversationAction()
        return self._instance


class CreateConversationAction:
    def __init__(self):
        self.token = None
        self.is_private = None

    def execute(self, name):
        headers = {"Authorization": f"Bearer {self.token}"}
        payload = {"name": name, "is_private": self.is_private}
        response = requests.post(
            "https://slack.com/api/conversations.create",
            headers=headers,
            data=payload,
        )
        return response.json()

    @staticmethod
    def prepare(data):
        builder = CreateConversationActionBuilder()
        return (
            builder.set_token(data["access_token"])
            .set_is_private(data["is_private"])
            .build()
        )


class SlackCustomHttpGetActionBuilder:
    def __init__(self):
        self._instance = None

    def set_url(self, url):
        self._get_instance().url = url
        return self

    def set_token(self, access_token):
        self._get_instance().token = access_token
        return self

    def set_headers(self, headers):
        self._instance.headers = json.loads(headers)
        return self

    def set_params(self, params):
        self._instance.params = json.loads(params)
        return self

    def build(self):
        return self._get_instance()

    def _get_instance(self):
        if self._instance is None:
            self._instance = SlackCustomHttpGetAction()
        return self._instance


class SlackCustomHttpGetAction:
    def __init__(self):
        self.url = None
        self.token = None
        self.headers = {}
        self.params = {}

    def execute(self):
        self.headers["Authorization"] = f"Bearer {self.token}"

        response = requests.get(
            self.url,
            headers=self.headers,
            data=self.params,
        )
        return response.json()

    @staticmethod
    def prepare(data):
        builder = SlackCustomHttpGetActionBuilder()
        return (
            builder.set_url(data["url"])
            .set_headers(data.get("headers", {}))
            .set_params(data.get("params", {}))
            .set_token(data["access_token"])
            .build()
        )


class SlackCustomHttpPostActionBuilder:
    def __init__(self):
        self._instance = None

    def set_url(self, url):
        self._get_instance().url = url
        return self

    def set_token(self, access_token):
        self._get_instance().token = access_token
        return self

    def set_headers(self, headers):
        self._instance.headers = json.loads(headers)
        return self

    def build(self):
        return self._get_instance()

    def _get_instance(self):
        if self._instance is None:
            self._instance = SlackCustomHttpPostAction()
        return self._instance


# SlackCustomHttpPostAction
class SlackCustomHttpPostAction:
    def __init__(self):
        self.url = None
        self.token = None
        self.headers = {}

    def execute(self, body):
        self.headers["Authorization"] = f"Bearer {self.token}"
        response = requests.post(self.url, headers=self.headers, json=body)
        return response.json()

    @staticmethod
    def prepare(data):
        builder = SlackCustomHttpPostActionBuilder()
        return (
            builder.set_url(data["url"])
            .set_headers(data.get("headers", {}))
            .set_token(data["access_token"])
            .build()
        )
