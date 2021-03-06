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
import numpy as np

logger = logging.getLogger(__name__)

app = Flask(__name__);
json_return = None
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

@app.route('/api/text/', methods=['POST','GET'])
def text():
    import operator
    global json_return
    if(request.method == 'POST'):
        print("Request to api/text")
        analyze_user = request.args.get('username')
        # I'm guessing we want to parse text here
        parsed_dict = parse_text(json.loads(request.data), [request.args.get('username'), request.args.get('recipient')], analyze_user);
        cog_results = {}
        key_phrase_count = {}
        for k, v in parsed_dict.iteritems():
            api_call = cog_api_call(v)
            cog_results[k] = api_call[0]
            print(api_call[1]['documents'])
            for kp in api_call[1]['documents']:
                for val in kp['keyPhrases']:
                    if val not in key_phrase_count:
                        key_phrase_count[val] = 1
                    else:
                        key_phrase_count[val] += 1
        key_phrase_result = sorted(key_phrase_count.iteritems(), key=lambda (k,v): (v,k), reverse=True)
        key_phrase_result = key_phrase_result[0:5]
        print key_phrase_result
        # change cog_results[k] to a json object to send to front end
        # front end then grabs dict values to display graph. Also, analyze
        # polyfit and include in json

        x = []
        y = []

        # TODO: Fix this so it actually gets a value we want (not hard code)

        for k, v in cog_results.iteritems() :
            if k[0] is analyze_user :
                x.append(k[2])
                y.append(v['documents'][0]['score'])
        serializable_cog_results = [{'key':k, 'value': v} for k, v in sorted(cog_results.iteritems())]
        average = reduce(lambda x, l: x + l, y) / len(y)
        best_fit = np.polyfit(x, y, 4).tolist()
        json_result = {"results": serializable_cog_results, "best_fit": best_fit, "keyPhrases": key_phrase_result, "average": average}
        json_return = json.dumps(json_result)
        print "SUCCESS"
        return render_template('index.html', status=200)
    else:
        print(json_return)
        return json_return 

@app.route('/api/message', methods=['GET'])
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
    conn.close()
    return json.dumps(data)

def parse_text(text_file, users, analyze_user):
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
            if(user_thread.people is analyze_user):
                list_of_messages = user_thread.sent_between(time_start, time_end)
                list_of_messages.sort(key=lambda x: x.date_time)
                concat_messages = ""
                for m in list_of_messages :
                    remove_p = str(m.text).replace("<p>", "")
                    remove_end_p = remove_p.replace("</p>", "")
                    concat_messages += remove_end_p + " "
                if len(concat_messages) != 0 :
                    msgs_between[(user_thread.people, str(time_start), 20 - i)] = concat_messages
    return msgs_between

def cog_api_call(text):
    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': 'dd9c4b679b0446f38042c90953b92c2f',
    }

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
    conn.request("POST", "/text/analytics/v2.0/sentiment", json.dumps(body), headers)
    response = conn.getresponse()
    data = response.read()
    conn.close()
    conn.request("POST", "/text/analytics/v2.0/keyPhrases", json.dumps(body), headers)
    response2 = conn.getresponse()
    data2 = response2.read()
    return [json.loads(data), json.loads(data2)]

if __name__ == '__main__':
    app.run(debug=True)
