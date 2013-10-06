import threading
import math
import OSC
from MidiInFile import MidiInFile
from MidiToList import MidiToList # the event handler


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

#thread that gets information from mo-cap server
import re
# import midi
import OSC
from time import time

# The following are global variables, used by threads
#tempo lower is faster! default 1.5
timeScale = 1.5

# get data

midiList = formMidiList()

zerotime = time()
mytime = 0.0
client = OSC.OSCClient()
send_address = '127.0.0.1', 9002
recieve_address = '127.0.0.1', 9001
client.connect( send_address )
s = OSC.OSCServer( recieve_address )
s.addDefaultHandlers()

midiEvents = midiList.events

def timehandler(addr, tags, stuff, source):
    #global timeScale
    timeScale = stuff[0]#change tempo
    print timeScale

s.addMsgHandler("/tempo", timehandler)

st =threading.Thread( target = s.serve_forever )
st.start()
print "Starting"

while mytime < timeScale*76.0:
    
    try:
        bundle = OSC.OSCBundle()              # Bundle all events that have occurred 

        mylist = midiEvents
        
        for iEvent,l in enumerate(mylist):

            if (timeScale*(float(l[4])/1000.0)) < mytime:

                if(l[5] == 1):              
                    p1msg = makeMsg("/note/1", l[2])
                    bundle.append(p1msg)
                if(l[5] == 2):              
                    p2msg = makeMsg("/note/2", l[2])
                    bundle.append(p2msg)
                if(l[5] == 3):              
                    p1msg = makeMsg("/note/3", l[2])
                    bundle.append(p1msg)
                    

                midiEvents.pop(iEvent)

                if len(bundle)>0:
                    client.send(bundle)
                    print "sent"

    except KeyboardInterrupt:
        break

mytime = time() - zerotime

# Stop the mocap thread, and wait for it to complete (close the socket)


