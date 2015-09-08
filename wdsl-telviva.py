#! /usr/bin/python

import http.client
import xml.etree.ElementTree as etree

def xmlToDictionary(response):
    """
    Convert XML to a dictionary encapsulated in a list
    and Return
    """
    result = []
    print (response.status, response.reason)
    xml = response.read().decode("utf-8")
    root = etree.fromstring(xml)
    #Enswitch gensyms
    for child in root[0][0]:
        r = {}
        for element in child:
            option = element.tag.split('}')[1]
            value = element.text
            r[option] = value
        result.append(r)
    return result

class Telviva(object):
    """Python SOAP API wrapper for Telviva"""

    def __init__(self, host, url, username=None, password=None, headers=None, client_args={}):

        """
        Instantiates an instance to Telviva. Takes basic parameters
        for authentication
        """
    
        self.data = None

        # Set Attributes for SOAP constuction
        self.host = host
        self.url = url
        self.username = username
        self.password = password

        # Set Headers
        self.headers = headers
        if self.headers is None:
            self.headers = {
                'User-Agent' : 'Telviva Python Library',
                'Accept' : 'text/xml',
            }
        
        
        self.request = ""
        self.request += """<?xml version="1.0" encoding="UTF-8"?>"""
        self.request += """<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:soapenc="http://schemas.xmlsoap.org/soap/encoding/" xmlns:xsd="http://www.w3.org/2001/XMLSchema" soap:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:enswitch="Integrics/Enswitch/API">"""
        self.request += """<soap:Body>"""
        self.request += """<enswitch:<<method>>>"""
        self.request += """<enswitch:username>%s</enswitch:username>""" % (username)
        self.request += """<enswitch:password>%s</enswitch:password>""" % (password)
        self.request += """<<enswitch_headers>>"""
        self.request += """</enswitch:<<method>>>"""
        self.request += """</soap:Body>"""
        self.request += """</soap:Envelope>"""

    #Call Enswitch Methods

    def get_phones(self):
        client = http.client.HTTPConnection(self.host)
        body = self.request.replace('<<method>>','get_phones')
        enswitch_headers = ''
        body = body.replace('<<enswitch_headers>>',enswitch_headers)
        client.request('POST', self.url, body, headers=self.headers)
        response = client.getresponse()
        data = xmlToDictionary(response)
        return data

    def get_phone(self, phone):
        client = http.client.HTTPConnection(self.host)
        body = self.request.replace('<<method>>','get_phone')
        enswitch_headers = '<enswitch:phone>%s</enswitch:phone>' % (phone)
        body = body.replace('<<enswitch_headers>>',enswitch_headers)
        client.request('POST', self.url, body, headers=self.headers)
        response = client.getresponse()
        data = xmlToDictionary(response)
        return data

    def get_numbers(self):
        """
        Return a list of numbers and feature codes
        """
        client = http.client.HTTPConnection(self.host)
        body = self.request.replace('<<method>>','get_numbers')
        enswitch_headers = ''
        body = body.replace('<<enswitch_headers>>',enswitch_headers)
        client.request('POST', self.url, body, headers=self.headers)
        response = client.getresponse()
        data = xmlToDictionary(response)
        return data

    def get_number(self, stype, snumber):
        """
        Return a spefic feature code of number
            stype = 'code' or 'number'
            snumber = number to search for
        """
        client = http.client.HTTPConnection(self.host)
        body = self.request.replace('<<method>>','get_number')
        enswitch_headers = '<enswitch:stype>%s</enswitch:stype>' % (stype)
        enswitch_headers += '<enswitch:snumber>%s</enswitch:snumber>' % (snumber)
        body = body.replace('<<enswitch_headers>>',enswitch_headers)
        client.request('POST', self.url, body, headers=self.headers)
        response = client.getresponse()
        data = xmlToDictionary(response)
        return data

# TODO: Add the whole list of options according to Telviva
    def save_number(self, 
            description = '',
            stype = '',
            snumber = '',
            sname = '',
            dtype = '',
            dnumber = '',
            owner = '',
            callerid = '',
            ):
        """
        Update feature code or number details
        """
        client = http.client.HTTPConnection(self.host)
        body = self.request.replace('<<method>>','save_number')
        enswitch_headers = '<enswitch:description>%s</enswitch:description>' % (description)
        enswitch_headers += '<enswitch:stype>%s</enswitch:stype>' % (stype)
        enswitch_headers += '<enswitch:snumber>%s</enswitch:snumber>' % (snumber)
        enswitch_headers += '<enswitch:sname>%s</enswitch:sname>' % (sname)
        enswitch_headers += '<enswitch:dtype>%s</enswitch:dtype>' % (dtype)
        enswitch_headers += '<enswitch:dnumber>%s</enswitch:dnumber>' % (dnumber)
        enswitch_headers += '<enswitch:owner>%s</enswitch:owner>' % (owner)
        enswitch_headers += '<enswitch:callerid>%s</enswitch:callerid>' % (callerid)
        body = body.replace('<<enswitch_headers>>',enswitch_headers)
        client.request('POST', self.url, body, headers=self.headers)
        response = client.getresponse()
        data = xmlToDictionary(response)
        return data   

    def delete_number(self, snumber):
        """
        Delete a feature code or number
        """
        client = http.client.HTTPConnection(self.host)
        body = self.request.replace('<<method>>','delete_number')
        enswitch_headers += '<enswitch:snumber>%s</enswitch:snumber>' % (snumber)
        body = body.replace('<<enswitch_headers>>',enswitch_headers)
        client.request('POST', self.url, body, headers=self.headers)
        response = client.getresponse()
        data = xmlToDictionary(response)
        return data

    def get_queues(self):
        """
        Return a list of queues
        """
        client = http.client.HTTPConnection(self.host)
        enswitch_headers = ''
        body = self.request.replace('<<method>>','get_queues')
        body = body.replace('<<enswitch_headers>>',enswitch_headers)
        client.request('POST', self.url, body, headers=self.headers)
        response = client.getresponse()
        data = xmlToDictionary(response)
        return data

    def get_queue(self, queue_id):
        """
        Return a spefic queue
        """
        client = http.client.HTTPConnection(self.host)
        body = self.request.replace('<<method>>','get_queue')
        enswitch_headers = '<enswitch:id>%s</enswitch:id>' % (queue_id)
        body = body.replace('<<enswitch_headers>>', enswitch_headers)
        client.request('POST', self.url, body, headers=self.headers)
        response = client.getresponse()
        data = xmlToDictionary(response)
        return data

    def delete_queue(self, queue_id):
        """
        Delete a queue
        """
        client = http.client.HTTPConnection(self.host)
        body = self.request.replace('<<method>>','delete_queue')
        enswitch_headers = '<enswitch:id>%s</enswitch:id>' % (queue_id)
        body = body.replace('<<enswitch_headers>>', enswitch_headers)
        client.request('POST', self.url, body, headers=self.headers)
        response = client.getresponse()
        data = xmlToDictionary(response)
        return data               

    def get_queue_destinations(self, queue_id):
        client = http.client.HTTPConnection(self.host)
        body = self.request.replace('<<method>>','get_queue_destinations')
        enswitch_headers = '<enswitch:id>%s</enswitch:id>' % (queue_id)
        body = body.replace('<<enswitch_headers>>', enswitch_headers)
        client.request('POST', self.url, body, headers=self.headers)
        response = client.getresponse()
        data = xmlToDictionary(response)
        return data

    def get_queue_destination(self, queueu_destination_id):
        client = http.client.HTTPConnection(self.host)
        body = self.request.replace('<<method>>','get_queue_destination')
        enswitch_headers = '<enswitch:id>%s</enswitch:id>' % (queue_destination_id)
        body = body.replace('<<enswitch_headers>>', enswitch_headers)
        client.request('POST', self.url, body, headers=self.headers)
        response = client.getresponse()
        data = xmlToDictionary(response)
        return data

    def delete_queue_destination(self, queue_destination_id):
        client = http.client.HTTPConnection(self.host)
        body = self.request.replace('<<method>>','delete_queue_destination')
        enswitch_headers = '<enswitch:id>%s</enswitch:id>' % (queue_destination_id)
        body = body.replace('<<enswitch_headers>>', enswitch_headers)
        client.request('POST', self.url, body, headers=self.headers)
        response = client.getresponse()
        data = xmlToDictionary(response)
        return data

    def get_customers(self, 
            parent, 
            bill_type, 
            name_type='contains', 
            name, 
            deleted=0, 
            directory=-1):
            """
            parent = ID of parent customer
            bill_type = Filter by customers of a certain billing type
            name_type = 'filter type contains|equals'
            name = name of customer
            deleted = -1 for all customers, 0 for non-deleted customers, 1 for deleted customers
            directory = -1 for all customers, 1 for customers in directory, 0 for those not in directory
            """
            pass

    def get_cdrs(self, 
            customer=0, 
            cost_customer=0, 
            start, 
            end, 
            status='',
            direction='',
            peer='',
            stype='',
            smatch='contains',
            snumber='',
            ctype='',
            cmatch='',
            cnumber='',
            dtype='',
            dmatch='',
            dnumber='',
            phone='',
            invoice='',
            minimum_talktime=0,
            maximum_talktime=-1,
            sort='start',
            descending=1,
            ):
        pass
