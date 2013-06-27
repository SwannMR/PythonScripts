#! /usr/bin/python
import os
import paramiko
import MySQLdb
import optparse
import re
import subprocess

class sshclient():
	def __init__(self):
        	self.connections = []
        	self.fail = True
        
	def connect(self, runway, host, user, passwd, prt):
        	client = paramiko.SSHClient()
        	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        	try:
            		client.connect("%s" % (host), username="%s" % (user), password="%s" % (passwd), port=prt, timeout=120)
            		self.connections.append(client)
        	except:
            		print ("can't connect to %s %s" % (host, runway))
            		return 0         

	def command(self, cmd):
        	for conn in self.connections:
            		stdin,stdout,stderr = conn.exec_command("""%s""" % (cmd),timeout=900)
            		err = stderr.readlines()
            		data = stdout.readlines()
            		return data
	
	def scp(self,src,dst):
		for conn in self.connections:
			scp = conn.open_sftp()
 			print ("copying %s" % src)
			try:
				scp.put(src,dst)
				scp.close()
			except:
				print("The file could not be copied. Check your source and destination locations are correct")	
				scp.close()
				return 0

	def close(self):
        	for conn in self.connections:
           		conn.close()
	    		self.connections.pop()

def getBranches():
	"""
	Process the vibe.conf file on EHL heandend. Extract
	the vibe tunnel name and inet address and return
	a dictionary of branch (key) and inet ip address
	"""
	vibe_conf = open("/home/michael/ellerines/ellerines-vibe.conf", "r")
	branches = {}
	for line in vibe_conf:
        	if re.search("name",line):
                	branch = re.search('(".*.")',line, re.IGNORECASE)
                	branch = branch.group(1)
                	branch = re.sub('"','',branch)
                	brnum = re.search('(BR[:\d]\d{3,4})',branch,re.IGNORECASE)
                	if brnum:
                        	brnum = brnum.group(1)
				brnum = re.sub(r'BR:''(?i)','',brnum, re.IGNORECASE)
				brnum = re.sub(r'BR','',brnum)
	# Get Inet Address
        	if re.search("network.10.60.*32 ", line):
                	# define a default variable before entering a check
                	inet = re.search('(network )(\d*.\d*.\d*.\d*)', line)
                	inet =  inet.group(2)
			branches[brnum] = inet
	vibe_conf.close()
	return branches

def checkHost(ip):
	""" 
	check if the host is pingable. If alive
	return True else return False
	"""
        alive = subprocess.call("ping -c 3 %s" % ip,
			shell=True,
			stdout=open('/dev/null', 'w'),
			stderr=subprocess.STDOUT)
	if alive == 0:
                return True
        else:
                return False

def process_cmd(result):
        result = "".join(result)
        result = re.sub("\n","",result)
        return result

def main():
    	parser = optparse.OptionParser()
    	parser.add_option("--branch", "-b", dest="branch", help="Connect to EHL branch")
    	parser.add_option("--all", "-A", dest="all", help="Run report for all branches")
    	options, arguments = parser.parse_args()
    	if options.branch:
        	host = m.getHost("%s" % (options.branch))
        	getData(host)
    	if options.all:
        	hosts = m.getAllHosts()
        	getData(hosts)

#if __name__ == "__main__":
#    	main()
