import time
import os
from datetime import datetime
import asyncio
import subprocess
from sys import argv


# В key_arr 7 значений.  0 позиция отведена под программу, которая находится в avto.py , остальные 1..6  это релюшки .

#key_dict = {'зрительный':1, 'торжественный':2, 'гостиная':3, 'администрация':4, 'студия':5, 'приточка':6 }

#key_arr = [False]*9

# эта строчка нужна что бы можно было запускать с включенным расписанием timestack() .
#if len(argv) != 1:
#    key_arr[0] = True

arr_vent=[]
horogstoptime = ''


def startvent (i):
    #key_arr[i] =  True
    s = 'HW554_' + str(i) + '=1'
    subprocess.call(["usbrelay", s], stdout=open(os.devnull, "w"), stderr=subprocess.STDOUT)
    #print(s)
   
   
def stopvent (i):
    #key_arr[i] =  False
    s = 'HW554_' + str(i) + '=0'
    subprocess.call(["usbrelay", s], stdout=open(os.devnull, "w"), stderr=subprocess.STDOUT)
    #print(s)
    
        
def timeview():
    datetimenow = datetime.now()
    time = datetimenow.strftime('%H:%M')
    res = str(time)
    res = res.strip()
    return res
     
def timeday():
    datetimenow = datetime.now()
    time = datetimenow.strftime('%d %B %y')
    return str(time)



def read_file():
    global horogstoptime
    f_h = open('/var/vent/horeog.txt', 'r')
    i = f_h.read().split('\n')
    i = list(filter(lambda x: x != '', i))
    #print(i)
    i = i[-1]
    i = i.split()
    if len(i) == 1:
        horogstoptime = (i[0]).strip()
    f_h.close()


    global arr_vent
    f_a = open('/var/vent/auto.txt', 'r')
    i = f_a.read().split('\n')
    i = list(filter(lambda x: x != '', i))
    arr_vent = i
    f_a.close()





#print('arr_vent =', arr_vent)
read_file()

print('arr_vent=', arr_vent)

def read_file_time():
    global horogstoptime
    global arr_vent
    if timeview() in ['09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00','22:00','23:00']:
        read_file()
        


def main():
    global horogstoptime

    read_file_time()

    if horogstoptime == timeview():
        startvent(6)
        horogstoptime = ''
        f_h = open('/var/vent/horeog.txt', 'a')
        f_h.write(' start vent 6 in day: ' + timeday() + ' \n')
        f_h.close()


    if arr_vent[0] == 'True':
        for i in arr_vent[1:]:
            a = i.split()
            if ( len(a) == 3 ) and ( a[0] == timeview() ):
                if a[1] == 'start':
                   startvent(a[2])
                   print('start_', a[2])
                if a[1] == 'stop':
                   stopvent(a[2])
                   print('stop_', a[2])


while ( __name__ == "__main__" ):
    main()
    time.sleep(55)
