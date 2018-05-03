#!/usr/bin/env python

#   Author: Perry Blalock (perryblalock@gmail.com)
#
#   This code is free software: you can redistribute it and/or modify
#   The author provides no warranties regarding the software, which is
#   provided "AS-IS" and your use of this software is entirely at your
#   own risk.  IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR DAMAGES OF ANY
#   KIND RELATING TO USE OF THE SOFTWARE, INCLUDING WITHOUT LIMITATION
#   ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
#   DAMAGES; ANY PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
#   DATA, OR PROFITS; OR BUSINESS INTERRUPTION, HOWEVER CAUSED AND ON ANY
#   THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#   (INCLUDING NEGLIGENCE), EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

## Import some useful Python modules

import os
import os.path
from os.path import isfile, join
from os import listdir
#from os import walk
import jinja2
from jinja2 import Environment, FileSystemLoader
#from netmiko import ConnectHandler
import csv
import sys
import re


## Add some text formatting
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



files1 = os.listdir('./data_csv')
print "   "
print "####     The below listed CSV files were found on your system,"
print "#### Please be sure to select the correct file for your configs generation"
print "   "
for index,file in enumerate(files1):
    print('{num} - {dir}'.format(num=index+1,dir=file))
print "   "
x = input('Choose a CSV file: ')
print "   "
print "##### The following file will be used for your DATA input: ", color.BOLD + (files1[x-1]) + color.END
print "   "
print "   "
files = os.listdir('./templates')
print "   "
print "####     The below listed template files were found on your system,"
print "#### Please be sure to select the correct file for your configs generation"
print "   "
for index,file in enumerate(files):
    print('{num} - {dir}'.format(num=index+1,dir=file))
print "   "

y = input('Choose a template file: ')
print "   "
print "##### The following file will be used for your config TEMPLATE: ", color.BOLD + (files[y-1]) + color.END
print "   "
print "   "

#print(files[x-1])

CSVDATA_FILENAME = (files1[x-1]) 
TEMPLATE_FILENAME = (files[y-1])

## ---------------------------------------------------------------------------
## create a jinja2 environment and load the template file
## ---------------------------------------------------------------------------

env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.getcwd()),
    trim_blocks=True, lstrip_blocks=True)

template = env.get_template('./templates/' + TEMPLATE_FILENAME)


## ---------------------------------------------------------------------------
## now read the CSV file, processing each row, and creating a
## rendered file for each 'hostname'
## ---------------------------------------------------------------------------


os.chdir('configs/') # chnge to dir we want to write to
#for row in csv.DictReader(open('../' + CSVDATA_FILENAME)): # open and read from one dir up
for row in csv.DictReader(open('../data_csv/' + CSVDATA_FILENAME)): # open and read from one dir up
    with open(row['host_name'], 'w+') as f: # iterate thru rows, write and prepend host_name key to file
##    with open(row['host_name'] + '.txt', 'w+') as f: # iterate thru rows, write and prepend host_name key to file .txt
#file_name = './post_results/'+ ip + '.txt'
       f.write(template.render(row))





print "Your config files have been written to the configs/ directory"
print " "
print " "

##
## all done!
##

