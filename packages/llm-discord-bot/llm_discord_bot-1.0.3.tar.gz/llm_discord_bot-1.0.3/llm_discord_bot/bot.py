from typing import List
from typing import Optional

import arrow
import re
from abc import ABC
from abc import abstractmethod
from discord import ChannelType
from discord import Message
from discord.ext import commands
from langchain.chat_models.openai import ChatOpenAI
from langchain.schema import ChatMessage
from langchain.schema import HumanMessage
from langchain.schema import SystemMessage

from llm_discord_bot import chatroom
from llm_task_handler.dispatch import TaskDispatcher


def get_max_tokens(model_name: str):
    if model_name == 'gpt-4':
        max_tokens = 8192
    elif model_name == 'gpt-4-32k':
        max_tokens = 32768
    elif model_name == 'gpt-3.5-turbo':
        max_tokens = 4096
    elif model_name == 'gpt-3.5-turbo-16k':
        max_tokens = 16384

    return max_tokens


class LLMDiscordBot(commands.Bot, ABC):
    @abstractmethod
    def bot_token(self) -> str:
        """Discord bot token"""

    @abstractmethod
    def task_dispatcher(self, user_id: str) -> TaskDispatcher:
        """TaskDispatcher instance"""

    def monitored_channels(self) -> list[int]:
        return []

    def fully_readable_channels(self) -> list[int]:
        return self.monitored_channels()

    def conversation_llm_model(self, llm_convo_context: list[ChatMessage]) -> ChatOpenAI:
        used_tokens = sum([ChatOpenAI().get_num_tokens(m.content) for m in llm_convo_context])
        completion_tokens = 400

        required_tokens = used_tokens + completion_tokens
        if required_tokens < 2000:
            model_name = 'gpt-4'
        elif required_tokens < get_max_tokens('gpt-3.5-turbo'):
            model_name = 'gpt-3.5-turbo'
        else:
            model_name = 'gpt-3.5-turbo-16k'

        return ChatOpenAI(  # type: ignore
            model_name=model_name,
            temperature=0,
            max_tokens=completion_tokens,
        )

    def conversation_completion_tokens(self) -> int:
        return 400

    def conversation_system_prompt(self) -> str:
        return '''
You are ChatGPT, a large language model trained by OpenAI.
You are in a Discord chatroom.
Carefully heed the user's instructions.
        '''

    def is_authorized_to_read_message(self, message: Message) -> bool:
        if message.channel.id in self.fully_readable_channels():
            return True
        else:
            return self.user in message.mentions

    def should_reply_to_message(self, message: Message) -> bool:
        if message.author == self.user:
            # Never reply to self, to avoid infinite loops
            return False

        if self.user in message.mentions:
            return True

        if all([
            message.channel.id in self.monitored_channels(),
            not message.mentions,
            not message.author.bot,
        ]):
            return True

        return False

    async def on_message(self, message: Message) -> None:
        if not self.is_authorized_to_read_message(message):
            return

        if not self.should_reply_to_message(message):
            return

        async with message.channel.typing():
            reply = await self.reply_to_message(message) or await self.reply_to_conversation(message)
            if reply:
                await message.channel.send(reply)

    async def reply_to_message(self, message: Message) -> Optional[str]:
        return await self.task_dispatcher(message.author.id).reply(
            self.remove_ai_mention(message.content),
        )

    async def reply_to_conversation(self, message: Message) -> Optional[str]:
        llm_convo_context = await self.get_llm_convo_context(latest_message=message)

        continue_convo_prompter = chatroom.ContinueConversationPrompter(
            llm_convo_context, str(self.user.id)  # type: ignore
        )

        chat_model = self.conversation_llm_model(llm_convo_context)

        continue_convo_prompt = continue_convo_prompter.prompt(
            max_tokens=get_max_tokens(chat_model.model_name) - self.conversation_completion_tokens()
        )

        reply = chat_model([
            SystemMessage(content=self.conversation_system_prompt()),
            HumanMessage(content=continue_convo_prompt),
        ]).content

        reply = continue_convo_prompter.decode_reply(reply)

        return reply

    async def get_llm_convo_context(
        self,
        latest_message: Message,
    ) -> list[ChatMessage]:
        # Messages are ordered newest to oldest
        discord_messages = await self.preceding_messages(latest_message)

        chat_messages: List[ChatMessage] = []
        for msg in discord_messages:
            reply_reference = msg.reference.resolved if msg.reference and type(msg.reference.resolved) == Message else None
            chat_msg = ChatMessage(role=str(msg.author.id), content=msg.content)

            if reply_reference:
                chat_messages += [ChatMessage(role=str(reply_reference.author.id), content=reply_reference.content)]

            chat_messages += [chat_msg]

        return chat_messages

    async def preceding_messages(self, latest_message: Message) -> List[Message]:
        messages = [
            msg async for msg in latest_message.channel.history(
                after=arrow.now().shift(hours=-24).datetime,
                oldest_first=False,
                limit=40,
            )
            if self.is_authorized_to_read_message(msg)
        ]

        if latest_message.channel.type == ChannelType.public_thread:
            thread_start_msg = await latest_message.channel.parent.fetch_message(latest_message.channel.id)  # type: ignore
            messages += [thread_start_msg]

        return messages

    def remove_ai_mention(self, msg_content: str) -> str:
        return re.sub(rf'<@{self.user.id}> *', '', msg_content)  # type: ignore
