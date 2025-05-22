#!/usr/bin/env python3

from gpiozero import Servo
import os
from http.server import BaseHTTPRequestHandler, HTTPServer

host_name = '10.178.202.171'  # IP Address of Raspberry Pi
host_port = 7000

def getTemperature():
    temp = os.popen("vcgencmd measure_temp").read()
    return temp

class MyServer(BaseHTTPRequestHandler):

    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def _redirect(self, path):
        self.send_response(303)
        self.send_header('Content-type', 'text/html')
        self.send_header('Location', path)
        self.end_headers()

    def do_GET(self):
        html = '''
           <html>
           <body style="width:960px; margin: 20px auto;">
           <h1 style="text-align:center;">Rover Control</h1>
           <p>Current GPU temperature is {}</p>
           
           <p style="width:300px; height:300px" id="myP" onmousedown=document.getElementById("myP").style.color = "red"; onmouseup=document.getElementById("myP").style.color = "blue";>A</p>
           
           </body>
           </html>
        '''
        
        temp = getTemperature()
        self.do_HEAD()
        self.wfile.write(html.format(temp[5:]).encode("utf-8"))
# # # # # Main # # # # #

if __name__ == '__main__':
    http_server = HTTPServer((host_name, host_port), MyServer)
    print("Server Starts - %s:%s" % (host_name, host_port))

    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        http_server.server_close()

