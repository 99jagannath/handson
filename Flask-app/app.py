from flask import Flask

app = Flask(__name__)

print(__name__)

@app.route('/')
def hello_world():
  return "Hello world!!"

if __name__ in ['main', '__main__']:
  app.run(debug=True, port=8080)