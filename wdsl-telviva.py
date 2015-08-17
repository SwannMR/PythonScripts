#! /usr/bin/python

"""
script to create enswitch soap requests
"""

import http.client
import xml.etree.ElementTree as etree

def convertResponse(xml):
    resp = []
    
    root = etree.fromstring(xml)

    #root
    for child in root:
        print (child)
    
    #Enswitch name space
    for child in root[0]:
        print (child)

    #Enswitch gensyms
    for child in root[0][0]:
        r = {}
        for element in child:
            option = element.tag.split('}')[1]
            value = element.text
            print (option, value)
            r[option] = value
        resp.append(r)
    return resp


username = "API-MIKE"
secret = "apimike123"

f = """<?xml version="1.0" encoding="UTF-8"?><soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:soapenc="http://schemas.xmlsoap.org/soap/encoding/" xmlns:xsd="http://www.w3.org/2001/XMLSchema" soap:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:enswitch="Integrics/Enswitch/API"><soap:Body><enswitch:get_queues><enswitch:username>%s</enswitch:username><enswitch:password>%s</enswitch:password></enswitch:get_queues></soap:Body></soap:Envelope>""" % (username, secret)

request = str.encode(f)

conn = http.client.HTTPConnection("197.155.250.189",80)
conn.putrequest("POST", "/api/soap/")
conn.putheader("User-Agent", "python-poser")
conn.putheader("Accept: text/xml")
conn.putheader("Content-length", "%d" % (len(f)))
conn.endheaders()
conn.send(request)

response = conn.getresponse()
data = response.read()
print (response.status)
data = data.decode("utf-8")
conn.close()

queues = convertResponse(data)
for queue in queues:
    print (queue)

"""
{Integrics/Enswitch/API}play_position 0
{Integrics/Enswitch/API}ringtime 15
{Integrics/Enswitch/API}id 138
{Integrics/Enswitch/API}search_interval 60
{Integrics/Enswitch/API}music 0
{Integrics/Enswitch/API}allow_forwards 0
"""
