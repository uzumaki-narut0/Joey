#!/usr/bin/env python

import urllib.request
import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
    if req.get("result").get("action") == "codingevents.response":
        baseurl = 'https://tranquil-caverns-50595.herokuapp.com/'
        result = urllib.request.urlopen(baseurl).read()
        data = json.loads(result)
        res = makeWebhookResult(data,req)
    elif req.get("result").get("action") == "codinguser.status":
       # return {}
        platform = req.get("result").get("parameters").get("website").strip()
        query_string = req.get("result").get("resolvedQuery").strip().split()
        print(platform)
        print(query_string)
        handle = query_string[-1]
        print(handle)
        res = makeWebhookResult2(platform,handle)
        
        
    return res

def makeWebhookResult(data,req):

    query = data.get('result')
    if query is None:
        return {}
    contest_type = req.get("result").get("contest-type")
    if(contest_type == "present"):
        result = query.get('present_contests')
    else:
        result = query.get('upcoming_contests')
    if result is None:
        return {}
    # print(json.dumps(item, indent=4))

    speech = "Here are your results: "  #+ #result[0]["name"]
    speech += '\n'
    speech = speech + '\n'
    for i in range(3):
        speech = speech + result[i]["name"] + " on "
        speech = speech + result[i]["contest_url"]
        speech = speech + '\n'
        speech = speech + '\n'
    data = result

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        "data": data,
        # "contextOut": [],
        "source": "contesttracker"
    }


def makeWebhookResult2(platform,handle):
    
    print(platform)
    if(platform == "codeforces"):
        url = 'http://codeforces.com/api/user.info?handles=' + handle
        print(url)
        response = urllib.request.urlopen(url)
        data = json.loads(response.read().decode('utf-8'))

        speech = 'Current Rating : ' + str(data['result'][0]['rating'])
        print(speech)
       # speech += 'Current Rank   : ' + data['result'][0]['rank']
       # speech += 'Max Rating     : ' + str(data['result'][0]['maxRating'])
       # speech += 'Max Rank       : ' + data['result'][0]['maxRank']
    elif(platform == "codechef"):
            pass
    #data = result

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        #"data": data,
        # "contextOut": [],
        "source": "cf-stats"
    }







if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

#    print "Starting app on port %d" % port

    app.run(debug=False, port=port, host='0.0.0.0')
