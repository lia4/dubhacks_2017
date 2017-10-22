from flask import Flask, render_template, request, redirect, url_for
import json
from bs4 import BeautifulSoup as bs
import src.fb_chat as fb_chat
import os
import httplib, urllib, base64
from datetime import datetime as dt
from datetime import timedelta
from twitter import getTweets
import logging

logger = logging.getLogger(__name__)

app = Flask(__name__);
@app.route('/api/trump', methods=['GET'])
def tweets():
    test = json.dumps(getTweets(20));
    return test;
    
@app.route('/')
def index():
    return render_template('index.html')

def dump(obj):
  for attr in dir(obj):
    print("obj.%s = %s" % (attr, getattr(obj, attr)))

@app.route('/api/text', methods=['POST', 'GET'])
def text():
    print("Request to api/text")
    # I'm guessing we want to parse text here
    parsed_dict = parse_text(json.loads(request.data), ['Foris Kuang', 'Andrew Li']);
    print(parsed_dict)

    cog_results = {}
    for k, v in parsed_dict.iteritems():
        cog_results[k] = cog_api_call(v)
        print cog_results[k]
        
    return 'cjuss'

'''
@app.route('/api/message/<parsed_dict>', methods=['GET'])
def message(parsed_dict):
    logger.info(parsed_dict)
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
'''

def parse_text(text_file, users):
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
    base_datetime = thread_list[0].date_time
    thread = fb_chat.Thread(users, thread_list)
    by_users = [fb_chat.Thread(u, thread.by(u)) for u in thread.people]
    msgs_between = {}
    for i in range(21):
        time_start = base_datetime - timedelta(days=i)
        time_end = base_datetime - timedelta(days=i - 1)
        for user_thread in by_users:
            list_of_messages = user_thread.sent_between(time_start, time_end)
            list_of_messages.sort(key=lambda x: x.date_time)
            concat_messages = ""
            for m in list_of_messages :
                remove_p = str(m.text).replace("<p>", "")
                remove_end_p = remove_p.replace("</p>", "")
                concat_messages += remove_end_p + " "
            if len(concat_messages) != 0 :
                msgs_between[(user_thread.people, str(time_start))] = concat_messages
    return msgs_between

def cog_api_call(text):
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

if __name__ == '__main__':
    app.run(debug=True)
