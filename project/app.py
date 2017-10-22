from flask import Flask, render_template
import json
from bs4 import BeautifulSoup as bs
import src.fb_chat as fb_chat
from datetime import datetime
app = Flask(__name__)

@app.route('/api/message')
def message(text_file, user):
    import httplib, urllib, base64

    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': API_KEY,
    }

    params = urllib.urlencode({
    })

    try:
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
        print body
        conn.request("POST", "/text/analytics/v2.0/sentiment?%s" % params, json.dumps(body), headers)
        response = conn.getresponse()
        data = response.read()
        print(data)
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
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
                    str(msg.next_sibling.string.encode('utf-8'))
                )
            )
    thread = fb_chat.Thread(user, thread_list)
    return py_to_json(thread)


if __name__ == '__main__':
    app.run(debug=True)
