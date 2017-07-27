import sys
import os
import json
import requests
import time

path = 'C:/Users/Administrator/Dropbox/IFTTT/SMS/tvrequest.txt'

timestr = time.strftime("%Y%m%d-%H%M%S")

url ='http://localhost:8989/api'
key = 'd04eda1b9881426cada5f14cbf46e3db'

temp = ''

log = open('C:/pylog.txt', 'a+')
log.write('starting program at '+timestr+'\n')


log.write('opening: ' + str(path) + '\n')
try:
    reader = open(path,'r')

    for line in reader:
        temp += line
    reader.close()
    os.remove(path)
except FileNotFoundError:
    log.write('no file '+timestr+'\n')

temp_nospaces = temp.replace(' ','%20')

lookup_url = url + '/series/lookup?term='+temp_nospaces+'&apikey='+key

response = requests.get(lookup_url)
data_get = json.loads(response.text)

max_pair = [0,0]
best = -1
for show,index in zip(data_get,range(len(data_get))):
    if str(show['title']).lower() == temp.lower():
        best = index
    if show['year']>max_pair[0]:
        max_pair[0]=show['year']
        max_pair[1]=index
if best > -1:
    max_pair[1]=best

add_url = url + '/series'
data_get_choice = data_get[max_pair[1]]
data={'tvdbId':data_get_choice['tvdbId'],
                                              'title':data_get_choice['title'], 
                                              'qualityProfileId': 1,
                                              'titleSlug':data_get_choice['titleSlug'],
                                              'images':data_get_choice['images'],
                                              'seasons':data_get_choice['seasons'],
                                              'rootFolderPath':'F:\\Video\\TV',
                                              'seasonFolder': 'true',
                                              'monitored': 'true'}
params={'apikey':key}
post_response = requests.post(add_url, params=params, json=data)
data_post = json.loads(post_response.text)

log.write('GET: ' + lookup_url + '\n'+str(data_get_choice)+'\n')
log.write('POST: ' + add_url + '\n'+str(data_post)+'\n')
log.close()


quit()
