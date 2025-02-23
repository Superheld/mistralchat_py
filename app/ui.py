# ui.py
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Input, Static
from textual.containers import VerticalScroll, Horizontal
from agents import ChatLogic

class ChatApp(App):
    CSS_PATH = "chat.css"  # Pfad zur CSS-Datei für das Styling der Anwendung
    BINDINGS = [("q", "quit", "Beenden")]  # Tastenkombinationen für die Anwendung

    def __init__(self, api_key, model):
        super().__init__()
        self.api_key = api_key  # API-Schlüssel für die Chat-Logik
        self.model = model  # Modell, das verwendet wird
        self.chat_logic = None  # Chat-Logik wird später initialisiert
        self.input_values = {}
        self.current_response = ""  # Zum Speichern der aktuellen Antworttext
        self.response_widget = None  # Zum Speichern des Antwort-Widgets

    def compose(self) -> ComposeResult:
        # Layout der Anwendung definieren
        yield Header()  # Kopfzeile
        yield Footer()  # Fußzeile
        with Horizontal(id="main_container"):  # Horizontales Container-Widget
            with VerticalScroll(id="input_agents"):  # Vertikales Scroll-Widget für Eingabefelder
                yield Static("Max Tokens:")  # Statisches Text-Widget
                yield Input(id="max_tokens", placeholder="Max Tokens", value="0")  # Eingabefeld für Max Tokens
                yield Static("Stream:")
                yield Input(id="stream", placeholder="Stream", value="false")
                yield Static("Stop:")
                yield Input(id="stop", placeholder="Stop", value="string")
                yield Static("Random Seed:")
                yield Input(id="random_seed", placeholder="Random Seed", value="0")
                yield Static("Response Format:")
                yield Input(id="response_format", placeholder="Response Format", value='{"type": "text"}')
                yield Static("Tools:")
                yield Input(id="tools", placeholder="Tools", value='[{"type": "function", "function": {"name": "string", "description": "", "strict": false, "parameters": {}}}]')
                yield Static("Tool Choice:")
                yield Input(id="tool_choice", placeholder="Tool Choice", value="auto")
                yield Static("Presence Penalty:")
                yield Input(id="presence_penalty", placeholder="Presence Penalty", value="0")
                yield Static("Frequency Penalty:")
                yield Input(id="frequency_penalty", placeholder="Frequency Penalty", value="0")
                yield Static("N:")
                yield Input(id="n", placeholder="N", value="1")
                yield Static("Prediction:")
                yield Input(id="prediction", placeholder="Prediction", value='{"type": "content", "content": ""}')
                yield Static("Agent ID:")
                yield Input(id="agent_id", placeholder="Agent ID", value="ag:5012507f:20250222:testagent:825aaefe")
            yield VerticalScroll(id="chat_agents")  # Vertikales Scroll-Widget für Chat-Nachrichten
        yield Input(placeholder="DU: ", id="content")  # Eingabefeld für Benutzereingaben

    def on_mount(self) -> None:
        # Wird aufgerufen, wenn die Anwendung gestartet wird
        self.query_one(Input).focus()  # Fokus auf das erste Eingabefeld setzen
        self.query_one("#chat_agents").mount(Static("Los gehts! Mit :q hörts auf"))  # Begrüßungsnachricht anzeigen
        # Chat-Logik mit dem bereitgestellten API-Schlüssel und Agent-ID initialisieren
        self.chat_logic = ChatLogic(self.api_key)

    async def get_response(self, input_values):
        # Antwort vom Chat-Logik-Modul abrufen
        response = self.chat_logic.get_response(input_values)
        async for chunk in response:
            self.current_response += chunk  # Antwort in der aktuellen Antwort speichern
            self.update_chat()  # Chat aktualisieren

    def update_chat(self):
        # Chat-Widget aktualisieren
        if self.response_widget is None:
            self.response_widget = Static(f"AI: {self.current_response}")  # Neues Antwort-Widget erstellen
            self.query_one("#chat_agents").mount(self.response_widget)  # Antwort-Widget zum Chat hinzufügen
        else:
            self.response_widget.update(f"AI: {self.current_response}")  # Bestehendes Antwort-Widget aktualisieren
        self.scroll_to_bottom()  # Zum Ende des Chats scrollen

    def on_input_submitted(self, event: Input.Submitted) -> None:
        # Wird aufgerufen, wenn eine Eingabe übermittelt wird
        user_input = event.value  # Benutzereingabe abrufen
        self.query_one("#chat_agents").mount(Static(f"DU: {user_input}"))  # Benutzereingabe zum Chat hinzufügen
        self.scroll_to_bottom()  # Zum Ende des Chats scrollen
        self.current_response = ""  # Aktuelle Antwort zurücksetzen

        # Alle Eingabewerte sammeln
        input_values = {
            "max_tokens": self.query_one("#max_tokens").value,
            "stream": self.query_one("#stream").value,
            "stop": self.query_one("#stop").value,
            "random_seed": self.query_one("#random_seed").value,
            "response_format": self.query_one("#response_format").value,
            "tools": self.query_one("#tools").value,
            "tool_choice": self.query_one("#tool_choice").value,
            "presence_penalty": self.query_one("#presence_penalty").value,
            "frequency_penalty": self.query_one("#frequency_penalty").value,
            "n": self.query_one("#n").value,
            # "prediction": self.query_one("#prediction").value,
            "agent_id": self.query_one("#agent_id").value,
            "content": user_input  # Benutzereingabe hinzufügen
        }

        self.response_widget = None  # Antwort-Widget zurücksetzen
        self.run_worker(self.get_response(input_values))  # Antwort abrufen und anzeigen
        # Eingabefeld nach der Übermittlung leeren
        event.input.value = ""

    def scroll_to_bottom(self):
        # Zum Ende des Chats scrollen
        chat = self.query_one("#chat_agents")
        chat.scroll_end()

if __name__ == "__main__":
    app = ChatApp(api_key="your_api_key", model="your_model")  # Anwendung mit API-Schlüssel und Modell starten
    app.run()  # Anwendung ausführen