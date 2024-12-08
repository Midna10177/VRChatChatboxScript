#!/usr/bin/python3

import argparse
import pythonosc.udp_client
import sys
from time import sleep

parser = argparse.ArgumentParser(
 prog="VRChat OSC Chatbox Sender",
 description="will send data from stdin to your chatbox in vrchat!"
)

parser.add_argument( "IPAddress", default="127.0.0.1" )
parser.add_argument( "-p", "--port", type=int, default=9000 )
parser.add_argument( "-v", "--verbose", action="store_true")

args = parser.parse_args()
'''
def tryconnect( address, port ):
 client = None
 
 try:
  client = pythonosc.udp_client.SimpleUDPClient( address, port )
 
 except:
  if args.verbose: print("failed to connect, retrying...")
  sleep(0.5)
  tryconnect( address, port )
 
 if args.verbose: print("connected! to vrchat!")
 return client
'''
def tryconnect( ip, port ):
 return pythonosc.udp_client.SimpleUDPClient( ip, port )

class VRChatOSCSenderHelper:
 def __init__( self, address, port ):
  self.address = address
  self.port    = port
  #try to connect...
  self.client = tryconnect( address, port )
  #-----
  self.client.send_message( "/chatbox/typing", False ) #disable typing indicator
  
 def send( self, data, hideBackground=True ):
  data = self.trimData( data )
  if hideBackground:
   self.client.send_message("/chatbox/input", [data + '\x03\x1f', True, False])
  else:
   self.client.send_message("/chatbox/input", [data, True, False])
 
 def trimData( self, data ):
  #You will be limited to 144 characters for chatbox text, and a maximum of 9 lines will be displayed, including new lines and word wrap.
  #we save 9+2 characters for newlines and the special 2-byte-code that hides the chatbox background
  data=data[:144-11]
  return data



def main():
 VRChatOSCSender = VRChatOSCSenderHelper( args.IPAddress, args.port )
 
 VRChatOSCSender.send( sys.stdin.read() )

main()
