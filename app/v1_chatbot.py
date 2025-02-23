import asyncio
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Input, Static
from textual.containers import VerticalScroll
from mistralai import Mistral
from mistralai.models import UserMessage

class ChatApp(App):
    CSS_PATH = "chat.css"
    BINDINGS = [("q", "quit", "Beenden")]

    def __init__(self, api_key, model, agent_id):
        super().__init__()
        self.api_key = api_key
        self.agent_id = agent_id
        self.model = model
        self.client = Mistral(api_key=api_key)

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield VerticalScroll(id="chat")
        yield Input(placeholder="DU: ", id="input")

    def on_mount(self) -> None:
        self.query_one(Input).focus()
        self.query_one("#chat").mount(Static("Los gehts! Mit :q hörts auf"))

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        user_input = event.value
        if user_input.lower() == ':q':
            self.exit()
        else:
            self.query_one(Input).value = ""
            self.query_one("#chat").mount(Static(f"DU: {user_input}"))
            try:
                response = await self.get_response(user_input)
                self.query_one("#chat").mount(Static(f"CHAT: {response}"))
            except Exception as e:
                self.query_one("#chat").mount(Static(f"Fehler: {str(e)}"))
            self.scroll_to_bottom()

    async def get_response(self, user_input):
        response = await self.client.agents.stream_async(
            agent_id=self.agent_id,
            messages=[
                UserMessage(content=user_input)
            ],
        )
        full_response = ""
        async for chunk in response:
            if chunk.data.choices[0].delta.content is not None:
                full_response += chunk.data.choices[0].delta.content
        return full_response

    def scroll_to_bottom(self):
        chat = self.query_one("#chat")
        chat.scroll_end()

def main():
    api_key = "jdPpFGIGPxddyd7S1OuWj4wLdVsY8SQI"
    agent_id = "ag:5012507f:20250219:gql1:4172857b"
    model = "ministral-8b-latest"
    app = ChatApp(api_key, model, agent_id)
    app.run()

if __name__ == "__main__":
    main()