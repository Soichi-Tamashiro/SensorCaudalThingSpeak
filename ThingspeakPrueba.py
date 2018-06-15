# Import all the libraries we need to run

import sys
import RPi.GPIO as GPIO
import os
from time import sleep
import urllib2
DEBUG = 1

# Setup the pins we are connect to

GPIO.setmode(GPIO.BOARD)  #GPIO pin numbering board
inpt = 13                   #Set input pin
GPIO.setup(inpt,GPIO.IN)  #Set input as inpt pin
rate_cnt = 0                #Rate of counts (L/min)
tot_cnt = 0               #Total counts (total liters)
minutes = 0               #Total minutes
constant = 0.10           #Convert pulses to liters
time_new = 0.0             #Keep next time

#_______________________________________________________
#Setup our API and delay
#_______________________________________________________
myAPI = "TD7SAKOGM3UUO0DF"

myDelay = 0 #how many seconds between posting data

# main() function

def main(data1,data2):
        print("starting...")
        baseURL = 'https://api.thingspeak.com/update?api_key=%s' % myAPI
        print(baseURL)
        try:
#_______________________________________________________
# Aqui pones la data
#_______________________________________________________

                f = urllib2.urlopen(baseURL +"&field1=%s&field2=%s" % (data1,data2))
                print f.read()
                #print(data1+""+data2)
                f.close()
                sleep(int(myDelay))

        except:
                print("exiting.")

#_______________________________________________________
# FUNCION PRINCIPAL DEL CODIGO
#_______________________________________________________
while True:                    #Loop Forever
        time_new = time.time() +  0.05    #+60 = 1minute (0.05 PARA TESTING)
        rate_cnt = 0                 #Reset flow rate counter
        while time.time() <= time_new:
                if GPIO.input(inpt)!= 0:   #Look for pulses
                        rate_cnt += 1           #Pulses per time ( CAUDAL DE LITROS)
                        tot_cnt += 1            #Total pulses( TOTAL DE LITROS )
              
        minutes += 1                        # Increment total minutes
        caudal=round(rate_cnt * constant,4)
        print('\nLiters / min ', caudal)
        acumulado=round(tot_cnt * constant,4)
        print('Total Liters ', acumulado)
        main(caudal,acumulado) # Envia datos a thingspeak
        time.sleep(2)

GPIO.cleanup()                #Reset ports

