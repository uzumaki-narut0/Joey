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
    if req.get("result").get("action") != "codingevents.response":
        return {}
    baseurl = 'https://tranquil-caverns-50595.herokuapp.com/'
#    yql_query = makeYqlQuery(req)
#    if yql_query is None:
#        return {}
#    yql_url = baseurl + urllib.urlencode({'q': yql_query}) + "&format=json"
    result = urllib.request.urlopen(baseurl).read()
    data = json.loads(result)
    res = makeWebhookResult(data,req)
    return res


#def makeYqlQuery(req):
#    result = req.get("result")
#    parameters = result.get("parameters")
#    city = parameters.get("geo-city")
#    if city is None:
#        return None

#    return "select * from weather.forecast where woeid in (select woeid from geo.places(1) where text='" + city + "')"


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

    speech = "here are your contest results: " #+ #result[0]["name"]
    data = result

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        "data": data,
        # "contextOut": [],
        "source": "apiai-weather-webhook-sample"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

#    print "Starting app on port %d" % port

    app.run(debug=False, port=port, host='0.0.0.0')
