import os
from flask import Flask, request
import requests
from flask_cors import CORS
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

CORS(app, resources={r'/*': {'origins': '*'}})

@app.route('/', methods=['POST'])
def proxy_post():  # put application's code here
    data = request.get_json() # returns a Python dictionary
    headers = request.headers

    api_key_req = headers.get("X-Api-Key", None)
    api_key = os.getenv("API_KEY")

    if not api_key_req or api_key_req != api_key:
        return "Incorrect Api Key", 401

    del headers["X-Api-Key"]

    print(f"Post request for url {data['url']} with headers:")
    for header in headers:
        print(header)

    response = requests.get(data["url"], headers=headers)
    print("Status: ", response.status_code)

    return response.text


if __name__ == '__main__':
    ENV = os.getenv('FLASK_ENV', default='development')
    if ENV == 'development':
        host = '127.0.0.1'  # localhost for development
    else:
        host = '0.0.0.0'  # public IP for production
    app.run(host=host)