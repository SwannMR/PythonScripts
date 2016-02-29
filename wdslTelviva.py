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

    # Call Enswitch Methods

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

    def delete_queue_destinations(self, queue_id):
        client = http.client.HTTPConnection(self.host)
        body = self.request.replace('<<method>>','delete_queue_destination')
        enswitch_headers = '<enswitch:queue>%s</enswitch:queue>' % (queue_id)
        body = body.replace('<<enswitch_headers>>', enswitch_headers)
        client.request('POST', self.url, body, headers=self.headers)
        response = client.getresponse()
        data = xmlToDictionary(response)
        return data

    def get_coses(self, customer):
        """
        Get list of class of services
        customer - ID of customer to get classes of service for. 0 for own customer.
        """
        client = http.client.HTTPConnection(self.host)
        body = self.request.replace('<<method>>','get_coses')
        enswitch_headers = '<enswitch:customer>%s</enswitch:customer>' % (customer)
        body = body.replace('<<enswitch_headers>>', enswitch_headers)
        client.request('POST', self.url, body, headers=self.headers)
        response = client.getresponse()
        data = xmlToDictionary(response)
        return data

    def get_cos_outroutes(self, cos):
        """
        Get a list of exceptions
        """
        client = http.client.HTTPConnection(self.host)
        body = self.request.replace('<<method>>','get_cos_outroutes')
        enswitch_headers = '<enswitch:cos>%s</enswitch:cos>' % (cos)
        body = body.replace('<<enswitch_headers>>', enswitch_headers)
        client.request('POST', self.url, body, headers=self.headers)
        response = client.getresponse()
        data = xmlToDictionary(response)
        return data

    def get_conferences(self):
        """
        Get a list of get_conferences
        """
        client = http.client.HTTPConnection(self.host)
        body = self.request.replace('<<method>>','get_conferences')
        enswitch_headers = ''
        body = body.replace('<<enswitch_headers>>', enswitch_headers)
        client.request('POST', self.url, body, headers=self.headers)
        response = client.getresponse()
        data = xmlToDictionary(response)
        return data

    def get_conference(self, confid):
        """
        Get conference based on the id
        """
        client = http.client.HTTPConnection(self.host)
        body = self.request.replace('<<method>>','get_conference')
        enswitch_headers = '<enswitch:confid>%s</enswitch:confid>' % (confid)
        body = body.replace('<<enswitch_headers>>', enswitch_headers)
        client.request('POST', self.url, body, headers=self.headers)
        response = client.getresponse()
        data = xmlToDictionary(response)


    def get_customers(self,
            parent,
            bill_type,
            name_type,
            name,
            deleted,
            directory):
            """
            parent = ID of parent customer
            bill_type = Filter by customers of a certain billing type
            name_type = 'filter type contains|equals'
            name = name of customer
            deleted = -1 for all customers, 0 for non-deleted customers, 1 for deleted customers
            directory = -1 for all customers, 1 for customers in directory, 0 for those not in directory
            """
            pass

    def get_people(self, customer=0):
        """
        Get a list people from a customer
        """
        client = http.client.HTTPConnection(self.host)
        body = self.request.replace('<<method>>','get_people')
        enswitch_headers = '<enswitch:customer>%s</enswitch:customer>' % (customer)
        body = body.replace('<<enswitch_headers>>', enswitch_headers)
        client.request('POST', self.url, body, headers=self.headers)
        response = client.getresponse()
        data = xmlToDictionary(response)
        return data

    def get_cdrs(self,
            customer,
            cost_customer,
            start,
            end,
            status,
            direction,
            peer,
            stype,
            smatch,
            snumber,
            ctype,
            cmatch,
            cnumber,
            dtype,
            dmatch,
            dnumber,
            phone,
            invoice,
            minimum_talktime,
            maximum_talktime,
            sort,
            descending

            ):

#            created_start,
#            created_end

        """
        Wow, there are a number of parameters to pass!!
        customer - ID of customer. '0' for user's own customer, 'all' for all customers, 'external' for all externally billed customers, 
                   'prepaid' for all prepaid customers, 'postpaid' for all postpaid customers, 'recursive' for all customers recursively,
                   'system' for all customers on system
        cost_customer - Customer to get cost for. 0 for us, ID of customer, 'scustomer' for CDR's scustomer, 
                        or 'card' for calling card making call
        start - unix timestamp of starting time
        end - unix timestamp of ending time
        status - 'answer', 'cancel', or empty string for all
        direction - 'in', 'out', 'internal', or empty string for all
        peer - ID of peer. 0 for all (should be 0)
        stype - Source type, empty for all
        smatch - Normally 'contains' (exact|start|end|contains)
        snumber - Only return source numbers containing given string. Empty string for all
        ctype - Called type. Empty string for all
        cmatch - Normally 'contains' (exact|start|end|contains)
        cnumber - Only return called numbers containing given string. Empty string for all
        dtype - Destination type. Empty string for all
        dmatch - normally 'contains' (exact|start|end|contains)
        dnumber - Only return destination numbers containing given string. Empty string for all
        phone - Only return calls to or from this telephone line
        invoice - ID of invoice call belongs to. 0 for calls not belonging to an invoice. -1 for any.
                  Set to -1 in almost all cases
        minimum_talktime - Minimum duration of call in seconds. 0 for all
        maximum_talktime - Maximum duration of call in seconds. -1 for all
        sort - Field to sort by. Normally 'start'
        descending - 1 to sort descending, 0 not to
        created_start - Start MySQL date/timestamp of time cdr entered into database (>=)
        created_end - End MySQL date/timestamp of time cdr entered into database (<)
        """

        """
        print ("customer: %s" % (customer))
        print ("cost_customer: %s" % (cost_customer))
        print ("start: %s" % (start))
        print ("end: %s" % (end))
        print ("status: %s" % (status))
        print ("direction: %s" % (direction))
        print ("peer: %s" % (peer))
        print ("stype: %s" % (stype))
        print ("smatch: %s" % (smatch))
        print ("snumber: %s" % (snumber))
        print ("ctype: %s" % (ctype))
        print ("smatch: %s" % (cmatch))
        print ("cnumber: %s" % (cnumber))
        print ("dtype: %s" % (dtype))
        print ("dmatch: %s" % (dmatch))
        print ("dnumber: %s" % (dnumber))
        print ("phone: %s" % (phone))
        print ("invoice: %s" % (invoice))
        print ("minimum_talktime: %s" % (minimum_talktime))
        print ("maximum_talktime: %s" % (maximum_talktime))
        print ("sort: %s" % (sort))
        print ("descending: %s" % (descending))
        """

        client = http.client.HTTPConnection(self.host)
        body = self.request.replace('<<method>>','get_cdrs')
        enswitch_headers = '<enswitch:customer>%s</enswitch:customer>' % (customer)
        enswitch_headers += '<enswitch:cost_customer>%s</enswitch:cost_customer>' % (cost_customer)
        enswitch_headers += '<enswitch:start>%s</enswitch:start>' % (start)
        enswitch_headers += '<enswitch:end>%s</enswitch:end>' % (end)
        enswitch_headers += '<enswitch:status>%s</enswitch:status>' % (status)
        enswitch_headers += '<enswitch:direction>%s</enswitch:direction>' % (direction)
        enswitch_headers += '<enswitch:peer>%s</enswitch:peer>' % (peer)
        enswitch_headers += '<enswitch:stype>%s</enswitch:stype>' % (stype)
        enswitch_headers += '<enswitch:smatch>%s</enswitch:smatch>' % (smatch)
        enswitch_headers += '<enswitch:snumber>%s</enswitch:snumber>' % (snumber)
        enswitch_headers += '<enswitch:ctype>%s</enswitch:ctype>' % (ctype)
        enswitch_headers += '<enswitch:cmatch>%s</enswitch:cmatch>' % (cmatch)
        enswitch_headers += '<enswitch:cnumber>%s</enswitch:cnumber>' % (cnumber)
        enswitch_headers += '<enswitch:dtype>%s</enswitch:dtype>' % (dtype)
        enswitch_headers += '<enswitch:dmatch>%s</enswitch:dmatch>' % (dmatch)
        enswitch_headers += '<enswitch:dnumber>%s</enswitch:dnumber>' % (dnumber)
        enswitch_headers += '<enswitch:phone>%s</enswitch:phone>' % (phone)
        enswitch_headers += '<enswitch:invoice>%s</enswitch:invoice>' % (invoice)
        enswitch_headers += '<enswitch:minimum_talktime>%s</enswitch:minimum_talktime>' % (minimum_talktime)
        enswitch_headers += '<enswitch:maximum_talktime>%s</enswitch:maximum_talktime>' % (maximum_talktime)
        enswitch_headers += '<enswitch:sort>%s</enswitch:sort>' % (sort)
        enswitch_headers += '<enswitch:descending>%s</enswitch:descending>' % (descending)
 #       enswitch_headers += '<enswitch:created_start>%s</enswitch:created_start>' % (created_start)
 #       enswitch_headers += '<enswitch:created_end>%s</enswitch:created_end>' % (dtype)
        body = body.replace('<<enswitch_headers>>',enswitch_headers)
        client.request('POST', self.url, body, headers=self.headers)
        response = client.getresponse()
        data = xmlToDictionary(response)
        return data

    def make_call(self, stype, snumber, callerid1, ctype, cnumber, callerid2, card, wait, warn1, warn2,screen1,screen2,answer1, answer2, recordgroup):
        """
        Initiate a call from Telviva
        """
        client = http.client.HTTPConnection(self.host)
        body = self.request.replace('<<method>>','make_call')
        enswitch_headers = '<enswitch:stype>%s</enswitch:stype>' % (stype)
        enswitch_headers += '<enswitch:snumber>%s</enswitch:snumber>' % (snumber)
        enswitch_headers += '<enswitch:callerid1>%s</enswitch:callerid1>' % (callerid1)
        enswitch_headers += '<enswitch:ctype>%s</enswitch:ctype>' % (ctype)
        enswitch_headers += '<enswitch:cnumber>%s</enswitch:cnumber>' % (cnumber)
        enswitch_headers += '<enswitch:callerid2>%s</enswitch:callerid2>' % (callerid2)
        enswitch_headers += '<enswitch:card>%s</enswitch:card>' % (card)
        enswitch_headers += '<enswitch:wait>%s</enswitch:wait>' % (wait)
        enswitch_headers += '<enswitch:warn1>%s</enswitch:warn1>' % (warn1)
        enswitch_headers += '<enswitch:warn2>%s</enswitch:warn2>' % (warn2)
        enswitch_headers += '<enswitch:screen1>%s</enswitch:screen1>' % (screen1)
        enswitch_headers += '<enswitch:screen2>%s</enswitch:screen2>' % (screen2)
        enswitch_headers += '<enswitch:answer1>%s</enswitch:answer1>' % (answer1)
        enswitch_headers += '<enswitch:answer2>%s</enswitch:answer2>' % (answer2)
        enswitch_headers += '<enswitch:recordgroup>%s</enswitch:recordgroup>' % (recordgroup)
        body = body.replace('<<enswitch_headers>>', enswitch_headers)
        client.request('POST', self.url, body, headers=self.headers)
        response = client.getresponse()
        data = xmlToDictionary(response)
        return data

    def redirect_call(self, server, uniqueid, ctype, cnumber):
        """
        Transfer a call. Need to keep track of which server the call is on
        """
        client = http.client.HTTPConnection(self.host)
        body = self.request.replace('<<method>>','redirect_call')
        enswitch_headers = '<enswitch:server>%s</enswitch:server>' % (server)
        enswitch_headers += '<enswitch:uniqueid>%s</enswitch:uniqueid>' % (uniqueid)
        enswitch_headers += '<enswitch:ctype>%s</enswitch:ctype>' % (ctype)
        enswitch_headers += '<enswitch:cnumber>%s</enswitch:cnumber>' % (cnumber)
        body = body.replace('<<enswitch_headers>>', enswitch_headers)
        client.request('POST', self.url, body, headers=self.headers)
        response = client.getresponse()
        data = xmlToDictionary(response)
        return data

    def hangup_call(self, server, uniqueid):
        """
        Hangup a call based on uniqueid
        """
        client = http.client.HTTPConnection(self.host)
        body = self.request.replace('<<method>>','hangup_call')
        enswitch_headers = '<enswitch:server>%s</enswitch:server>' % (server)
        enswitch_headers += '<enswitch:uniqueid>%s</enswitch:uniqueid>' % (uniqueid)
        body = body.replace('<<enswitch_headers>>', enswitch_headers)
        client.request('POST', self.url, body, headers=self.headers)
        response = client.getresponse()
        data = xmlToDictionary(response)
        return data

    def get_active_calls(self, customer, direction, sort, descending, set_info, stype, snumber, dtype, dnumber, callid):
        """
        List of active calls

        customer - ID of customer.
                '0' for user's own customer,
                'all' for all customers,
                'recursive' for my customer recursive,
                'system' for all customers on system.
        direction - 'in', 'out', 'internal', or empty string for all
        sort - Field to sort by. Normally 'start'
        descending - 1 to sort descending, 0 not to
        set_info - 1 to set full call information (slower), 0 not to (faster)
        stype - Source type to match, or empty string for all
        snumber - Source number to match, or empty string for all
        dtype - Destination type to match, or empty string for all
        dnumber - Destination number to match, or empty string for all
        callid - Callid to match, or empty string for all
        """

        client = http.client.HTTPConnection(self.host)
        body = self.request.replace('<<method>>','get_active_calls')
        enswitch_headers = '<enswitch:customer>%s</enswitch:customer>' % (customer)
        enswitch_headers += '<enswitch:direction>%s</enswitch:direction>' % (direction)
        enswitch_headers += '<enswitch:sort>%s</enswitch:sort>' % (sort)
        enswitch_headers += '<enswitch:descending>%s</enswitch:descending>' % (descending)
        enswitch_headers += '<enswitch:set_info>%s</enswitch:set_info>' % (set_info)
        enswitch_headers += '<enswitch:stype>%s</enswitch:stype>' % (stype)
        enswitch_headers += '<enswitch:snumber>%s</enswitch:snumber>' % (snumber)
        enswitch_headers += '<enswitch:dtype>%s</enswitch:dtype>' % (dtype)
        enswitch_headers += '<enswitch:dnumber>%s</enswitch:dnumber>' % (dnumber)
        enswitch_headers += '<enswitch:callid>%s</enswitch:callid>' % (callid)
        body = body.replace('<<enswitch_headers>>', enswitch_headers)
        client.request('POST', self.url, body, headers=self.headers)
        response = client.getresponse()
        data = xmlToDictionary(response)
        return data

    def get_remote_accesses(self):
        """
        Get a list of remote access accounts
        """
        client = http.client.HTTPConnection(self.host)
        body = self.request.replace('<<method>>','get_accesses')
        enswitch_headers = ''
        body = body.replace('<<enswitch_headers>>',enswitch_headers)
        client.request('POST', self.url, body, headers=self.headers)
        response = client.getresponse()
        data = xmlToDictionary(response)
        return data

    def get_remote_access(self, access_id):
        """
        Get a list of remote access accounts
        """
        client = http.client.HTTPConnection(self.host)
        body = self.request.replace('<<method>>','get_access')
        enswitch_headers = '<enswitch:id>%s</enswitch:id>' % (access_id)
        body = body.replace('<<enswitch_headers>>',enswitch_headers)
        client.request('POST', self.url, body, headers=self.headers)
        response = client.getresponse()
        data = xmlToDictionary(response)
        return data

    def save_remote_access(self,
    					   access_id,
    					   name,
    					   description,
    					   type,
    					   account,
    					   owner,
    					   cos,
    					   recordgroup,
    					   source,
    					   prefix,
    					   strip,
    					   callerid,
    					   callerid_internal,
    					   callerid_external,
    					   presentation_external,
    					   locked,
    					   play_balance,
    					   password,
    					   dtype,
    					   dnumber,
    					   dialplan,
    					   dtmf_connect_caller):
        """
        Create or update a remote access account

        id - ID of account to update. 0 for new
        name - Name of account
        description - Description
        type - menu, callback, direct
        account - Account number for authentication. Empty string for none
        owner - ID of person owning account. 0 for none
        cos - ID of COS for outbound calls. 1 for default
        recordgroup - ID of record group. 0 for none
        source - IP address for authentication. Empty string for any.
        prefix - Called number prefix for authentication. Empty string for none
        strip - Number of digits to strip from called number
        callerid - Callerid for authentication. Empty string for none
        callerid_internal - Callerid presented for internal calls. Empty for withheld, 'original' to leave unchanged.
        callerid_external - Callerid presented for external calls. Empty for withheld, 'original' to leave unchanged
        presentation_external - Either 1 or 32
        locked - 1 if account is locked, 0 if not
        play_balance - 1 to play balance to caller, 0 not to
        password - PIN for authentication. Empty string for none
        dtype - Force calls to a particular destination type. Normally empty string
        dnumber - Force calls to a particular destination number. Normally empty string
        dialplan - Dial plan for outbound calls. Empty string for default dial plan
        dtmf_connect_caller - DTMF to play to caller when the outbound call connects
        """

        print ("id: %s" % (access_id))
        print ("name: %s" % (name))
        print ("description: %s" % (description))
        print ("type: %s" % (type))
        print ("account: %s" % (account))
        print ("owner: %s" % (owner))
        print ("cos: %s" % (cos))
        print ("recordgroup: %s" % (recordgroup))
        print ("source: %s" % (source))
        print ("prefix: %s" % (prefix))
        print ("strip: %s" % (strip))
        print ("callerid: %s" %(callerid))
        print ("callerid_internal: %s" % (callerid_internal))
        print ("callerid_external: %s" % (callerid_external))
        print ("presentation_external: %s" % (presentation_external))
        print ("locked: %s" % (locked))
        print ("play_balance: %s" % (play_balance))
        print ("password: %s" % (password))
        print ("dtype: %s" % (dtype))
        print ("dnumber: %s" % (dnumber))
        print ("dialplan: %s" % (dialplan))
        print ("dtmf_connect_caller: %s" % (dtmf_connect_caller))


        client = http.client.HTTPConnection(self.host)
        body = self.request.replace('<<method>>','save_access')
        enswitch_headers = '<enswitch:id>%s</enswitch:id>' % (access_id)
        enswitch_headers += '<enswitch:name>%s</enswitch:name>' % (name)
        enswitch_headers += '<enswitch:description>%s</enswitch:description>' % (description)
        enswitch_headers += '<enswitch:type>%s</enswitch:type>' % (type)
        enswitch_headers += '<enswitch:account>%s</enswitch:account>' % (account)
        enswitch_headers += '<enswitch:owner>%s</enswitch:owner>' % (owner)
        enswitch_headers += '<enswitch:cos>%s</enswitch:cos>' % (cos)
        enswitch_headers += '<enswitch:recordgroup>%s</enswitch:recordgroup>' % (recordgroup)
        enswitch_headers += '<enswitch:source>%s</enswitch:source>' % (source)
        enswitch_headers += '<enswitch:prefix>%s</enswitch:prefix>' % (prefix)
        enswitch_headers += '<enswitch:strip>%s</enswitch:strip>' % (strip)
        enswitch_headers += '<enswitch:callerid>%s</enswitch:callerid>' % (callerid)      
        enswitch_headers += '<enswitch:callerid_internal>%s</enswitch:callerid_internal>' % (callerid_internal)
        enswitch_headers += '<enswitch:callerid_external>%s</enswitch:callerid_external>' % (callerid_external)
        enswitch_headers += '<enswitch:presentation_external>%s</enswitch:presentation_external>' % (presentation_external)
        enswitch_headers += '<enswitch:locked>%s</enswitch:locked>' % (locked)
        enswitch_headers += '<enswitch:play_balance>%s</enswitch:play_balance>' % (play_balance)
        enswitch_headers += '<enswitch:password>%s</enswitch:password>' % (password)
        enswitch_headers += '<enswitch:dtype>%s</enswitch:dtype>' % (dtype)
        enswitch_headers += '<enswitch:dnumber>%s</enswitch:dnumber>' % (dnumber)
        enswitch_headers += '<enswitch:dialplan>%s</enswitch:dialplan>' % (dialplan)
  #      enswitch_headers += '<enswitch:dtmf_connect_caller>%s</enswitch:dtmf_connect_caller>' % (dtmf_connect_caller)
        body = body.replace('<<enswitch_headers>>',enswitch_headers)
        client.request('POST', self.url, body, headers=self.headers)
        response = client.getresponse()
        data = xmlToDictionary(response)
        return data
