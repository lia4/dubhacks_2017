from flask import Flask, render_template, request
import json
from bs4 import BeautifulSoup as bs
import src.fb_chat as fb_chat
import os
import httplib, urllib, base64
from datetime import datetime as dt

app = Flask(__name__);

@app.route('/')
def index():
    return render_template('index.html')

def dump(obj):
  for attr in dir(obj):
    print("obj.%s = %s" % (attr, getattr(obj, attr)))

@app.route('/api/text', methods=['POST'])
def text():
    print 'Request to api/text was made!'
    # I'm guessing we want to parse text here
    parse_text(json.loads(request.data), "Foris Kuang");
    return 'cjuss'

@app.route('/api/message/', methods=['GET'])
def message():
    print request.args.get('message')
    text = request.args.get('message')

    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': 'dd9c4b679b0446f38042c90953b92c2f',
    }

    params = urllib.urlencode({
    })

    conn = httplib.HTTPSConnection('westus.api.cognitive.microsoft.com')
    body = {
        "documents": [
            {
                "language": "en",
                "id": "string",
                "text": text
            }
        ]
    }
    conn.request("POST", "/text/analytics/v2.0/sentiment?%s" % params, json.dumps(body), headers)
    response = conn.getresponse()
    data = response.read()
    print(data)
    conn.close()
    return json.dumps(data)

def parse_text(text_file, user):
    from encode import py_to_json
    soup = bs(text_file, "html.parser")
    dtFormat = '%A, %B %d, %Y at %I:%M%p %Z'
    thread_list = []
    for msg in soup.find_all(class_='message'):
        thread_list.append(
            fb_chat.Message(
                    str(msg.find(class_='user').string),
                    dt.strptime(str(msg.find(class_='meta').string), '%A, %B %d, %Y at %I:%M%p %Z'),
                    str(msg.next_sibling.encode('utf-8'))
                )
            )
    thread = fb_chat.Thread(user, thread_list)
    py_to_json(thread)

if __name__ == '__main__':
    app.run(debug=True)
