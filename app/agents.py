# agents.py
from mistralai import Mistral
from mistralai.models import UserMessage

class ChatLogic:
    def __init__(self, api_key):
        self.client = Mistral(api_key=api_key)

    async def get_response(self, user_input):

        response = await self.client.agents.stream_async(
            max_tokens = user_input.get('max_tokens'),
            stream = user_input.get('stream'),
            stop = user_input.get('stop'),
            random_seed = user_input.get('random_seed'),
            response_format = user_input.get('response_format'),
            tools = [ user_input.get('tools') ],
            tool_choice = user_input.get('tool_choice'),
            presence_penalty = user_input.get('presence_penalty'),
            frequency_penalty = user_input.get('frequency_penalty'),
            n = user_input.get('n'),
            prediction = user_input.get('prediction'),
            agent_id = user_input.get('agent_id'),  
            messages = [
                UserMessage(content = user_input.get('content')),
            ],
        )

        async for chunk in response:
            if chunk.data.choices[0].delta.content is not None:
                yield chunk.data.choices[0].delta.content
