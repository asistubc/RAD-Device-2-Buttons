# Created By: ASIS&T@UBC
# Title: RAD Device 2 Button
# Description: Prints random book recommendations from CSVs with two buttons.
#   In our diagram, GPIO 23 maps to booklist1. GPIO 17 maps to booklist2. If
#   only one booklist CSV exists, both buttons will use the sole booklist.
#   The purpose was to offer child friendly content AND more mature content.
#   See the original RAD Device documentation for additional setup info.
# Created: 2014
# Updated: 2015-04-21


from random import randrange

import csv
import textwrap
import printer
import os.path

def createhashmap (filename):
    hashmap = []
    if(os.path.isfile(filename)):
        with open(filename,'rb') as csvfile:
            spamreader = csv.reader(csvfile, delimiter='|')
            for row in spamreader:
                hashmap.append(row)
    return hashmap

def printstuff (wrapped_title, wrapped_author, wrapped_desc):
    p=printer.ThermalPrinter(serialport="/dev/ttyAMA0")
    p.print_text("\nHey book lovers! How's it going?\n")
    p.justify("C")
    p.print_text("Check out")
    p.linefeed()
    p.justify("C")
    p.underline_on()
    p.print_text(wrapped_title)
    p.underline_off()
    p.linefeed()
    p.justify("C")
    p.print_text("by ")
    p.underline_on()
    p.print_text(wrapped_author)
    p.underline_off()
    p.linefeed()
    p.justify()
    p.print_text(wrapped_desc)
    p.linefeed()
    p.linefeed()
    p.linefeed()
    p.linefeed()
    p.linefeed()
    return



#create hashmap with csv file contents
hashmap1 = []
hashmap2 = []

#FILE PATH SHOULD REFLECT ACTUAL FILE DIRECTORY
docpath1 = '/git/RAD-device/booklist1.csv'
docpath2 = '/git/RAD-device/booklist2.csv'

if(os.path.isfile(docpath1) and os.path.isfile(docpath2)):
    hashmap1 = createhashmap(docpath1)
    hashmap2 = createhashmap(docpath2)
elif(os.path.isfile(docpath1) and not(os.path.isfile(docpath2))):
    hashmap1 = createhashmap(docpath1)
    hashmap2 = createhashmap(docpath1)
elif(os.path.isfile(docpath2) and not(os.path.isfile(docpath1))):
    hashmap1 = createhashmap(docpath2)
    hashmap2 = createhashmap(docpath2)


#code for button connection
from time import sleep
import RPi.GPIO as GPIO
GPIO.setmode (GPIO.BCM)
GPIO.setup(23, GPIO.IN)
GPIO.setup(17, GPIO.IN)

while True:
    if(GPIO.input(23) == False):
        #generate random number
        random_num = randrange(0,len(hashmap1))

	#print random line from csv
        book = hashmap1[random_num]

        #formatting for printing the line
        wrapped_title = textwrap.fill(book[0],32)
        wrapped_author = textwrap.fill(book[1],32)

        if(len(book) > 2):
            wrapped_desc = textwrap.fill(book[2],32)
        else:
            wrapped_desc = ""

        printstuff(wrapped_title, wrapped_author, wrapped_desc)
	sleep(2)
        sleep(0.25)

    elif(GPIO.input(17) == False):
        #generate random number
        random_num = randrange(0,len(hashmap2))

	#print random line from csv
        book = hashmap2[random_num]

        #formatting for printing the line
        wrapped_title = textwrap.fill(book[0],32)
        wrapped_author = textwrap.fill(book[1],32)

        if(len(book) > 2):
            wrapped_desc = textwrap.fill(book[2],32)
        else:
            wrapped_desc = ""

        printstuff(wrapped_title, wrapped_author, wrapped_desc)
	sleep(2)
    sleep(0.25)
        

