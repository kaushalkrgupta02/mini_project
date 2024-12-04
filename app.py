from flask import Flask
app = Flask(__name__)

@app.router("/")
def abc():
  return "BOT is Running"

if __name__ == "__main__"
  app.run()
