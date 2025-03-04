from ui import ChatApp

def main():
    api_key = "alt ;-)"
    model = "ministral-8b-latest"
    app = ChatApp(api_key, model)
    app.run()

if __name__ == "__main__":
    main()
