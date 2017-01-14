#!/usr/bin/env python

import urllib.request
import json
import os
import requests
from bs4 import BeautifulSoup
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
        for word in query_string:
            if word[0]=='@':
                handle = word[1:]
                break
       # print(platform)
       # print(query_string)
        #print(handle)
        res = makeWebhookResult2(platform,handle)

    elif req.get("result").get("action") == "generate.randomproblem":
        keyword = req.get("result").get("parameters").get("coding-problem-tags")
        query_string = req.get("result").get("resolvedQuery").strip().split()
        for word in query_string:
            if word[0]=='@':
                handle = word[1:]
                break
        count = req.get("result").get("parameters").get("count")
        print(count)
        #print(keyword)
        res = makeWebhookResult3(keyword,handle,count)

    elif req.get("result").get("action") == "editorial":
        query_string = req.get("result").get("resolvedQuery").strip().split()
        for word in query_string:
            if word[0]=='@':
                problemcode = word[1:]
                break
        problemcode = problemcode.upper()
        print(problemcode)
        res = makeWebhookResult_editorial(problemcode)
    return res

def makeWebhookResult_editorial(problem_code):
    url = 'http://www.codechef.com/problems/' + problem_code
    res=requests.get(url)
    res.raise_for_status()
    soup = BeautifulSoup(res.text,'html.parser')

    container = soup.find('table', attrs = {'align':'left'})
    if "Editorial" in container.text:
        y = container.findAll('tr')
        i=0
        while i < len(y):
            e = y[i]
            if "Editorial" in e.text:
                s=e.find('a')
                speech = s.text
                break
            i=i+1
        
    else:
        speech = "I am afraid, this problem has no Editorial"
    print(speech)
    return {
        "speech": speech,
        "displayText": speech,
        #"data": data,
        # "contextOut": [],
        "source": "editorialsource"
    }



def makeWebhookResult3(keyword,handle,count):
    #print(count)
    url = 'http://code-drills.com/profile?handles=' + handle
    #print(url)
    data = requests.get(url).text
    soup = BeautifulSoup(data, 'html.parser')
    container = soup.find('div', attrs = {'id': keyword})
    links = container.findAll('a')
    speech = 'Here you go:'
    speech += '\n'
    speech += '\n'
    cnt = int(count)
    for i in range(cnt):
        speech += links[i].get('href')
        speech += '\n'
        speech += '\n'
        #print(speech)
    

    return {
        "speech": speech,
        "displayText": speech,
        "data": data,
        # "contextOut": [],
        "source": "randomproblemgenerator"
    }






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
    
    #print(platform)
    if(platform == "codeforces"):
        url = 'http://codeforces.com/api/user.info?handles=' + handle
        print(url)
        response = urllib.request.urlopen(url)
        data = json.loads(response.read().decode('utf-8'))

        speech = 'Current Rating : ' + str(data['result'][0]['rating']) + '\n'
       # print(speech)
        speech += 'Current Rank   : ' + data['result'][0]['rank'] + '\n'
        speech += 'Max Rating     : ' + str(data['result'][0]['maxRating']) +'\n'
        speech += 'Max Rank       : ' + data['result'][0]['maxRank']
        
    elif(platform == "codechef"):
        #print('working here')
        url = 'https://www.codechef.com/users/' + handle
        #print(url)
        res = requests.get(url)
        res.raise_for_status()
        soupobj = BeautifulSoup(res.text,'html.parser')
        ranks = soupobj.select('hx')
        if ranks[0].getText()=='NA':
                speech = 'Long Challenge: ' +'NA' + '\n'
        else:
                speech = 'Long Challenge: '+ranks[0].getText()+' / '+ranks[1].getText() + '\n'
        if len(ranks)<3 or ranks[2].getText()=='NA':
                speech += 'Short Challenge: '+'NA' + '\n'
        else:
                speech += 'Short Challenge: '+ranks[2].getText()+' / '+ranks[3].getText() + '\n'
        if len(ranks)<4 or ranks[4].getText()=='NA':
                speech += 'LunchTime: '+ 'NA' + '\n'
        else:	
                speech += 'LunchTime: '+ranks[4].getText()+' / '+ranks[5].getText() + '\n'
        speech += 'Global Rank / Country Rank'
        #speech = "working"
    #data = result

    elif(platform == "hackerearth"):
        url = 'https://www.hackerearth.com/@' + handle
        #print(url)
        data = requests.get(url).text
        soup = BeautifulSoup(data, 'html.parser')

        container = soup.findAll('span', attrs = {'class': 'track-following-num'})
        anchor = container[1].find('a')
        hackerearth_rating = anchor.text
        speech = "Here it is : " + hackerearth_rating
        #print(hackerearth_rating)

    elif(platform == "spoj" or platform == "SPOJ")
        url='http://www.spoj.com/users/' + handle
        data = requests.get(url).text
        soup = BeautifulSoup(data, 'html.parser')
        container = soup.find('div', attrs = {'id':'user-profile-left'})
        links = container.findAll('p')
        print(links[2].text)
        speech = "Here it is : " + links[2].text
        

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
