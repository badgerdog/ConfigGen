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

#  This script performs three main functions:
#    1. read original csv file, extract specific data cells and write output to new directory and file - keep original csv
#    2. extract specific data cells from csv and write to new file in diffeerent directory
#    3. remove headers from the new file and write to a result to temporary file in 


import os
import csv

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





## START Snippet1-------------------------------------------------------------
## This will section will operate on any "".csv" file in the "pathName" directory
## and extract specific cell(s) based on header column number, column[2:0] of the
## CSV file.  It iterates through until the end and writes the a new csv file to
## "new_data_csv/outputdata.csv" NOTE: "(column[0])" represents the csv header key
##  to print cell results from 
## ---------------------------------------------------------------------------


files = os.listdir('./data_csv')
print "   "
print "####     The below listed CSV DATA files were found on your system,"
print "   "
print "####     Please be sure to select the correct file for your project"
print "   "
for index,file in enumerate(files):
    print('{num} - {dir}'.format(num=index+1,dir=file))
print "   "

x = input('Choose a CSV file to work with: ')
print "   "
print "##### The following csv file Will be used as your Original DATA file: ", color.BOLD + (files[x-1]) + color.END
print "   "
print "   "

CSVDATA = (files[x-1]) 

#pathName = "./data_csv"
numFiles = (files[x-1]) 
#fileNames = os.listdir(pathName)
#for fileNames in fileNames:
#    if fileNames.endswith(".csv"):
#        numFiles.append(fileNames)

for i in numFiles:
    file = open('./data_csv/' + CSVDATA, "rU")
    reader = csv.reader(file, delimiter=',')
with open('./new_data_csv/outputdata.csv', 'w') as outfile:
    mywriter = csv.writer(outfile)
    for column in reader:
      mywriter.writerow(column[0:2])



#pathName = "./data_csv"
#numFiles = []
#fileNames = os.listdir(pathName)
#for fileNames in fileNames:
#    if fileNames.endswith(".csv"):
#        numFiles.append(fileNames)

#for i in numFiles:
#    file = open(os.path.join(pathName, i), "rU")
#    reader = csv.reader(file, delimiter=',')
#with open('./new_data_csv/outputdata.csv', 'w') as outfile:
#    mywriter = csv.writer(outfile)
#    for column in reader:
#      mywriter.writerow(column[0:2]) 
## END Snippet1---------------------------------------------------------------

## START Snippet2-------------------------------------------------------------
## This section removes the headers from just written "outputdata.csv" file,
## writes a new csv file to "no_header_host_data.csv," and removes file with
## the headers 
## ---------------------------------------------------------------------------


with open("./new_data_csv/outputdata.csv",'r') as f:
    with open("./new_data_csv/no_header_host_data.csv",'w') as f1:
        f.next() # skip header line
        for line in f:
            f1.write(line)
## Now remove original cav file "/new_data_csv/outputdata.csv" that contains
## headers

filename1 = "./new_data_csv/outputdata.csv"
## check if a file exists on disk ##
## if exists, delete it else show message on screen ##
if os.path.exists(filename1):
        try:
                os.remove(filename1)
        except OSError, e:
                print ("Error: %s - %s." % (e.filename1,e.strerror))
else:
        print("Sorry, I can not find %s file." % filename1)
## END Snippet2---------------------------------------------------------------




exit()

##
## all done!
##
