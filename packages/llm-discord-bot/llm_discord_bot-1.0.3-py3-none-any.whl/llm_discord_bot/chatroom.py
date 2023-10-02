import re
from typing import Dict
from typing import List
from typing import Tuple
from langchain.chat_models.openai import ChatOpenAI
from langchain.schema import ChatMessage


RoleCodec = Dict[str, str]


class ContinueConversationPrompter:
    def __init__(self, messages: List[ChatMessage], ai_role: str) -> None:
        self.messages = messages  # Ordered newest first
        self.ai_role = ai_role
        self.role_encoder, self.role_decoder = self.get_role_codec(self.messages, self.ai_role)

    def prompt(self, max_tokens: int) -> str:
        convo_lines = []
        tokens_used = 0
        for msg in self.messages:
            content = self.encode_discord_mentions(msg.content)
            content_tokens = ChatOpenAI().get_num_tokens(msg.content)
            if tokens_used + content_tokens > max_tokens:
                break
            convo_lines += [
                f'@{self.role_encoder[msg.role]} said: {content}\n'
            ]
            tokens_used += content_tokens

        # Change message order from newest first to oldest first
        convo_lines.reverse()

        convo_content = '\n'.join(convo_lines)

        return f'''
Complete the next message in this conversation:

{convo_content}
@{self.role_encoder[self.ai_role]} said: 
        ''' # noqa

    def decode_reply(self, content: str) -> str:
        return self.decode_discord_mentions(content)

    def encode_discord_mentions(self, content: str) -> str:
        discord_mentions_regex = re.compile(r'<@(\d+)>')

        def encode_mention(match):
            return f'@{self.role_encoder[match.group(1)]}'

        return discord_mentions_regex.sub(encode_mention, content)

    def decode_discord_mentions(self, content: str) -> str:
        encoded_mentions_regex = re.compile(r'@([0-9]+)[^0-9]?\b')

        def decode_mention(match):
            return f'<@{self.role_decoder[match.group(1)]}>'

        return encoded_mentions_regex.sub(decode_mention, content)

    def get_role_codec(self, messages: List[ChatMessage], ai_role: str) -> Tuple[RoleCodec, RoleCodec]:
        roles = {ai_role} | set([m.role for m in messages])

        encoder = {
            role: str(i)
            for i, role in enumerate(roles)
        }

        decoder = {v: k for k, v in encoder.items()}

        return encoder, decoder
