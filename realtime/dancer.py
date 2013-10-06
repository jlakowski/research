import threading
import math
import OSC
from MidiInFile import MidiInFile
from MidiToList import MidiToList # the event handler
import fileinput

def pythag(x, y):
    x2 = math.pow(x,2)
    y2 = math.pow(y,2)
    return math.pow(x2+y2, .5)
# a function that calculates the hyptoenuse of a three points
def pythag3(x, y, z):
    x2 = math.pow(x,2)
    y2 = math.pow(y,2)
    z2 = math.pow(z,2)
    return math.pow(x2+y2+z2, .5)
#makes an OSC packet
def makeMsg(address, content):
    msg = OSC.OSCMessage();
    msg.setAddress(address)
    msg.append(content)
    return msg

def midiToFrequency(noteNum):
    #formula for changing a midinumber into a frequency
    n = noteNum - 69
    freq = 440* float(math.pow(2, n/12))
    return freq
def formMidiList():
    # read Midi file and form python list.
    test_file = '/home/jim/research/python/LaComparsa.mid'
    
    midiList = MidiToList()    # do parsing
    midiIn = MidiInFile(midiList, test_file)
    midiIn.read()
    return midiList

def is_number(s):
    # A utility function to make certain that an argument is a float
    try:
        float(s)
        return True
    except ValueError:
        return False
def secondMoment(xcom, ycom, zcom, points):
    #calculates the moment of the points about the z-axis

    for i in range (0,len(points),3):
        dx = points[i] - xcom
        dy = points[i+1] - ycom
        dz = points[i+2]- zcom
        moment = moment + dx*dx + dy*dy
    return moment
        

#thread that gets information from mo-cap server
def mocap():
    import socket
    global vol, getMocap, com
    global vel
   
    for i in range(0,3):
        vol[i] = 90.
    
    TCP_IP = 'zx81.isl.uiuc.edu'
    #TCP_IP = '192.168.10.1'
    TCP_PORT = 4710
   # TCP_IP = '130.126.127.232'  # 'car8.isl.uiuc.edu'
   # TCP_PORT = 4712

    # Create a socket
    s = socket.socket() # Does not work with this! (socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    
    t0 = time()
    xc = 0.0
    yc = 0.0
    zc = 0.0
    f = open('solo.trc')
    line = f.readline()
    
    while line:
        
    #while(getMocap):
        data = f.readline()
        print data
#data = s.recv(8192)
    
        # If we can't keep up, there may be multiple records.  Just take the first one.
        records = data.split("\n")
       
        for record in records:
            if re.search('start-of-record',record): # =='start-of-record':
                ss = record.split(",")
                break

        ss.pop(0)                  # Remove the first, "start-of-record" string
        fs = []
        newRecord = True
        for pt in ss:
            f2b = pt.replace('[','').replace(']','')
            if is_number( f2b):
                fs.append( float( f2b ) )    # pt.replace('[','').replace(']','') ) )
            else:
                print 'bad float', f2b
                newRecord = False
              

        # Find center "of mass"
        if newRecord:
            nc = len(fs)/3
            for i in range(0,nc):
                xc = xc + fs[i*3]
                yc = yc + fs[1+(i*3)]
                zc = zc + fs[2+(i*3)]

            if nc>1:
                t1 = time()
                dt = t1 - t0
                t0 = t1
              
                xclast = xc
                yclast = yc
                zclast = zc
                xc = xc / float(nc)
                yc = yc / float(nc)
                zc = zc / float(nc)
                moment = secondMoment(xc,yc,zc,fs)
                print moment
                print xc, yc, zc
            else:
                vol[0] = 60.0

        # car8 vol[0] = (-(xc)+2000.0) / 20.0
        # zx81
        vol[2] = ((-xc)+2000.0) / 25.0  # 2000
        vol[1] = (yc+1200.0) / 25.0  # 2000
        vol[0] = (zc+200.0) / 25.0 # 500


        #velocity array 
        vel[2] = vel[2]*.99 - .01 * (xc-xclast) #velocity smoothing
        vel[1] = yc-yclast 
        vel[0] = zc-zclast 
       # print [vel[0], vel[1]] 
         
        for i in range(0,3):
            if vol[i] < 5.0:
                vol[i] = 5.0
            if vol[i] > 120.0:
                vol[i] = 120.0

    s.close()
    f.close()

import re
# import midi
import OSC
from time import time

# The following are global variables, used by threads
vol = [0.0, 0.0, 0.0]
vel = [0.0, 0.0, 0.0]
com = [0.0, 0.0, 0.0]

getMocap = 1

t1 = threading.Thread(target=mocap)
t1.start()

timeScale = 1.5

# get data

midiList = formMidiList()

zerotime = time()
mytime = 0.0

client = OSC.OSCClient()                      # connect to OSCmidi.py
client.connect( ('127.0.0.1', 9002) )         # argument is a tupple and not two arguments

midiEvents = midiList.events

while mytime < timeScale*76.0:

    try:
        bundle = OSC.OSCBundle()              # Bundle all events that have occurred 

        mylist = midiEvents

        for iEvent,l in enumerate(mylist):

            if (timeScale*(float(l[4])/1000.0)) < mytime:

                velocity =  0 #vel[2]

                                               
                deltav = 0
                
                deltaf = 0.1 * deltav #change in frequency for normalization
                fade  = 0.5 #left/right pan paramter 0 is left, 1 is right
                             
                if(l[5] == 1):              
                    freq = midiToFrequency(l[2]) + deltaf
                    p1msg = makeMsg("/note/1", l[2])
                    bundle.append(p1msg)
                    p1freq =  makeMsg("/dfreq/1", deltaf)
                    bundle.append(p1freq)
                    p1vol = makeMsg("/vol/1", vol[1])
                    bundle.append(p1vol)
                if(l[5] == 2):              
                    freq = midiToFrequency(l[2]) + deltaf
                    p1msg = makeMsg("/note/2", l[2])
                    bundle.append(p1msg)
                    p1freq =  makeMsg("/dfreq/2", deltaf)
                    bundle.append(p1freq)
                    p2vol = makeMsg("/vol/2", vol[1])
                    bundle.append(p2vol)

                if(l[5] == 3):              
                    freq = midiToFrequency(l[2]) + deltaf
                    p1msg = makeMsg("/note/3", l[2])
                    bundle.append(p1msg)
                    p1freq =  makeMsg("/deltaf/3", deltaf)
                    bundle.append(p1freq)
                    p3vol = makeMsg("/vol/3", vol[2])
                    bundle.append(p3vol)
                    
                #msg.append(0x90 + (l[5]-1))   # Note on + midi channel
                #p1msg.append(int(l[2]))
                 
               # if int(l[3])>0:
                   # print l[5]-1, vol[l[5]-1], l[2]
                    #msg.append(int(vol[l[5]-1]))   # midi.message( 0x90, int(l[2]), int(vol[1]) )
                #else:
                    #msg.append(int(0))        # midi.message( 0x90, int(l[2]), int(l[3]) )
                midiEvents.pop(iEvent)

                if len(bundle)>0:
                    client.send(bundle)

    except KeyboardInterrupt:
        break

    mytime = time() - zerotime

# Stop the mocap thread, and wait for it to complete (close the socket)
getMocap = 0
t1.join()
