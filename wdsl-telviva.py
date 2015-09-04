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
    #for child in root:
    #    print (child)
    
    #Enswitch name space
    #for child in root[0]:
    #    print (child)

    #Enswitch gensyms
    for child in root[0][0]:
        r = {}
        for element in child:
            option = element.tag.split('}')[1]
            value = element.text
            r[option] = value
        resp.append(r)
    return resp

def soapRequest(method):

    username = "API-MIKE"
    secret = "apimike123"
    host = "197.155.250.189"

    request = ""
    request += """<?xml version="1.0" encoding="UTF-8"?>"""
    request += """<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:soapenc="http://schemas.xmlsoap.org/soap/encoding/" xmlns:xsd="http://www.w3.org/2001/XMLSchema" soap:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:enswitch="Integrics/Enswitch/API">"""
    request += """<soap:Body>"""
    request += """<enswitch:%s>""" % (method)
    request += """<enswitch:username>%s</enswitch:username>""" % (username)
    request += """<enswitch:password>%s</enswitch:password>""" % (secret)
    request += """<enswitch:id>137</enswitch:id>"""
    request += """</enswitch:%s>""" % (method)
    request += """</soap:Body>"""
    request += """</soap:Envelope>"""

    return request


request = str.encode(soapRequest("get_queues"))

conn = http.client.HTTPConnection("197.155.250.189",80)
conn.putrequest("POST", "/api/soap/")
conn.putheader("User-Agent", "python-poser")
conn.putheader("Accept: text/xml")
conn.putheader("Content-length", "%d" % (len(request)))
conn.endheaders()
conn.send(request)

response = conn.getresponse()
data = response.read()
print (response.status)
data = data.decode("utf-8")
conn.close()

print (convertResponse(data))

queues = convertResponse(data)
for q in queues:
    print (q['id'],q['name'])


class Telviva(object):
    """Python SOAP API wrapper for Telviva"""

    def __init__(self, url, username=None, password=None, headers=None):

        """
        Instantiates an instance to Telviva. Takes basic parameters
        for authentication
        """
    
        self.data = None

        # Set Attributes for SOAP constuction
        self.url = url
        self.username = username
        self.password = password

        # Set Headers
        if self.headers is None:
            self.headers = {
                'User-Agent' : 'Telviva Python Library',
                'Accetp' : 'text/xml',
                'Content-length' : ''
            }
