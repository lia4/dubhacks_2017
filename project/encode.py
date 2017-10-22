#!/usr/bin/env python3

import json
from datetime import datetime as dt
import src.fb_chat as fb_chat

dtFormat = '%A, %B %d, %Y at %I:%M%p %Z'

def json_encode(py_obj):
    """This is the method to be passed into the 'default' argument
    of json.dump."""

    if isinstance(py_obj, fb_chat.Chat):
        return {'threads': py_obj.threads}
    elif isinstance(py_obj, fb_chat.Thread):
        return {'messages': py_obj.messages,
                'people': py_obj.people}
    elif isinstance(py_obj, fb_chat.Message):
        return {'text': py_obj.text[3:-4],
                'date_time': py_obj.date_time,
                'sender': py_obj.sender}
    elif isinstance(py_obj, dt):
        return py_obj.strftime(dtFormat)
    elif isinstance(py_obj, set):
        return list(py_obj)
    raise TypeError('{} is not JSON serializable'.format(repr(py_obj)))


def py_to_json(py_obj, name='messages.json'):
    with open(name, 'w') as f:
        json.dump(py_obj, f, default=json_encode, indent=2)
