import requests
#import bs4
from bs4 import BeautifuSoup
url = 'http://www.codechef.com/problems/' + 'TRANDED'
res=requests.get(url)
print(url)
res.raise_for_status()
soup = bs4.BeautifulSoup(res.text,'html.parser')

container = soup.find('table', attrs = {'align':'left'})
print('SSSSSS')
if "Editorial" in container.text:
    print('$$$$$$$$$$$$$$$$$')
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

