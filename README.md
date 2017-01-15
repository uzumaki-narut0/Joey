# Webhook implementation in Python 

This is a really simple webhook implementation that gets Api.ai classification JSON (i.e. a JSON output of Api.ai /query endpoint) and returns a fulfillment response. 

# Deploy to:
[![Deploy to Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

# What does the service do?
It's a coding related information fulfillment service that uses the concepts of website scraping using BeautifulSoup and  [CodersCalendar API](https://tranquil-caverns-50595.herokuapp.com/). This service is implemented using Flask (A Python Microframework).

The services takes various action and other parameters from the Api.ai classification JSON and packs the result in the Api.ai webhook-compatible response JSON and returns it to Api.ai 


