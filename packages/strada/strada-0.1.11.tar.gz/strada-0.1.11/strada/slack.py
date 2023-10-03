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


# # Example usage:
# if __name__ == "__main__":
#     # Initialize PostMessage action
#     post_message_builder = (
#         PostMessageActionBuilder().set_token("YOUR_SLACK_TOKEN").set_channel("#general")
#     )
#     post_message_action = post_message_builder.build()

#     # Post message
#     post_message_response = post_message_action.execute("Hello, world!")
#     print("Post Message Response:", post_message_response)

#     # Initialize CreateConversation action
#     create_conversation_builder = (
#         CreateConversationActionBuilder()
#         .set_token("YOUR_SLACK_TOKEN")
#         .set_is_private(False)
#     )
#     create_conversation_action = create_conversation_builder.build()

#     # Create a new conversation
#     create_conversation_response = create_conversation_action.execute("new_channel")
#     print("Create Conversation Response:", create_conversation_response)
