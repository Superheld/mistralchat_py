from ui import ChatApp

def main():
    api_key = "jdPpFGIGPxddyd7S1OuWj4wLdVsY8SQI"
    model = "ministral-8b-latest"
    app = ChatApp(api_key, model)
    app.run()

if __name__ == "__main__":
    main()
