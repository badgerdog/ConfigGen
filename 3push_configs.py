#!/usr/bin/env python

####################################
##
## Author:Brett M Spunt :: 4-22-2018
##
####################################

import os
import paramiko
import time
import re
import sys
import threading
import datetime
import csv
import getpass

#import click
import progressbar
from progressbar import ProgressBar
#from tqdm import tqdm, trange
from time import sleep


# future use
import os.path
import subprocess
import base64

## First add some text formatting
class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'
# EXAMPLE for formatting text:
#
# print color.BOLD + 'Hello World !' + color.END


# Start to write standard errors to log file
class Logger(object):
    def __init__(self):
        self.terminal = sys.stdout
        self.log = open('./logs/ssh_configuration.log', "w")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)  

    def flush(self):
        #this flush method is needed for python 3 compatibility.
        #this handles the flush command by doing nothing.
        #you might want to specify some extra behavior here.
        pass    

sys.stdout = Logger()
#sys.stdout = open('/usr/DCDP/logs/dcdp.log', 'w')
sys.stderr = open('./logs/ssh_configuration-err.log', 'w')

print "______________________________________________" 
print "   "
username = raw_input( "Enter username: " )
print "   "
print "______________________________________________" 
print "   "
print "______________________________________________" 
print "   "
print "####    ////////// Password will be hidden ///////////"
print "#### Please copy and paste your password from a text file"
print "   "
password = getpass.getpass()
print "   "
print "______________________________________________" 


################################
# BE SURE TO create CSV w/ no spaces, e.g. like below:(Using IP, Config which is the key,value)
# 10.52.0.1,us-dal-sw1.txt

# Or dictionary will not be created properly

#################################


with open('new_data_csv/no_header_host_data.csv', mode='r') as infile:
    reader = csv.reader(infile)
    with open('new_data_csv/ip-config_tmp.csv', mode='w') as outfile:
        writer = csv.writer(outfile)
        global ip_configs
        ip_configs = {rows[0]:rows[1] for rows in reader}
#################################

#ip_configs = {'10.52.1.253': 'us-dal-rt1.txt', '10.52.1.254': 'us-dal-rt2.txt'}

current_time=time.strftime("%Y-%m-%d %H:%M")

#setup max number of threads for Semaphore method to use. create sema variable for open ssh function to use
maxthreads = 25
sema = threading.BoundedSemaphore(value=maxthreads)


#Open SSHv2 connection to devices
def open_ssh_conn(ip, config):
    #Change exception message
    try:        
        #Logging into device
        session = paramiko.SSHClient()

	#For testing purposes, this allows auto-accepting unknown host keys
	#Do not use in production! The default would be RejectPolicy
        session.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        sema.acquire()
        time.sleep(10)
        sema.release()
        
	#Passing the necessary parameters
        session.connect(ip, username = username, password = password)
    
    
	#Start an interactive shell session on the router
        connection = session.invoke_shell()	
        
        selected_filename = open('./configs/' + config, 'r')
        #Starting from the beginning of the file

        selected_filename.seek(0)

        #Writing each line in the file to the device
        for each_line in selected_filename.readlines():
            connection.send(each_line + '\n')
            time.sleep(2)
        
            #Closing the command file
            selected_filename.close()
            #os.chdir('../')
#############################################################
        # Get around the 64K bytes (65536). paramiko limitation
        interval = 0.1
        maxseconds = 15
        maxcount = maxseconds / interval
        bufsize = 65535

        input_idx = 0
        timeout_flag = False
        start = datetime.datetime.now()
        start_secs = time.mktime(start.timetuple())
#############################################################
        router_output = ''

        while True:
            if connection.recv_ready():
                data = connection.recv(bufsize).decode('ascii')
                router_output += data

            if connection.exit_status_ready():
                break

            now = datetime.datetime.now()
            now_secs = time.mktime(now.timetuple())

            et_secs = now_secs - start_secs
            if et_secs > maxseconds:
                timeout_flag = True
                break

            rbuffer = router_output.rstrip(' ')
            if len(rbuffer) > 0 and (rbuffer[-1] == '#' or rbuffer[-1] == '>'): ## got a Cisco command prompt
                break
            time.sleep(0.200)
        if connection.recv_ready():
            data = connection.recv(bufsize)
            router_output += data.decode('ascii')
#############################################################

        if re.search(r"% Invalid input detected at", router_output):
            print "* There was at least one IOS syntax error on device %s" % ip
        elif re.search(r"% Authorization failed", router_output):
            print "   "
            print "** Authorization failed for %s Looks Like a TACACS issue." % ip
            print "** Try and run the program again."
        elif re.search(r"% Invalid command at", router_output):
            print "** There was at least one NX-OS syntax error (Could be other device, but most likely NX-OS) on %s" % ip

        else:
            print "\nCompleted device %s" % color.BOLD + config + '_' + ip + color.END + " Your post config outputs in written to /post_results directory"
        return router_output
        session.close()
     
    except paramiko.AuthenticationException:
        pass
        print "   "
        print "* Authentication Error for %s" % ip
        print "   "
        #print "* Closing program...\n"
    except paramiko.SSHException:
        pass
        print "   "
        print "* Incompatible SSH version. Paramiko requires SSHv2 on device %s" % ip

def write_files(ip, config):
#    file_name = '/usr/net-automation-cron-jobs/configs/sh-run/' + ip + '_' + current_time + '_sh-run.txt'
    file_name = './post_results/'+ config + '_' + ip + '.txt'
    fo = open(file_name, "w")
    #Calling the SSH function
    router_output = open_ssh_conn(ip, config)
    fo.write(router_output)
    fo.close()

def unique_ssh_configuration():
        threads = []
        for ip, config in ip_configs.iteritems():
            th = threading.Thread(target = write_files, args = (ip, config))   #args is a tuple      
            th.start()
            threads.append(th)
        
        for th in threads:
            th.join()

#def job(): # define function "job"
#    bar = progressbar.ProgressBar()
#    for i in bar(range(100)):
#        #time.sleep(0.02)
#        print "Progress"
#job() # invoke function "job"
#Calling threads creation function which then calls the open ssh function
unique_ssh_configuration()

