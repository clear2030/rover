#!/usr/bin/env python3

from gpiozero import Servo
import os
from http.server import BaseHTTPRequestHandler, HTTPServer

host_name = '10.178.202.171'  # IP Address of Raspberry Pi
host_port = 7000

leftMotor = Servo(3)
rightMotor = Servo(27)

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
           <style>
           </style>
           <body style="width:960px; margin: 20px auto;">
           <h1 style="text-align:center;">Rover Control</h1>
           <p style="color:white;">Current GPU temperature is {}</p>
           <form action="/" method="POST">
               
               <input type="submit" name="Stop" value="Stop" style="height:150px; width:150px; color:red;">
               <br>
               <input type="submit" name="Forward" value="Forward" style="height:300px; width:300px; margin:0 auto; display:flex;">
               <br>
               <input type="submit" name="Left" value="Left" style="height:300px; width:300px; margin:0 auto; display:inline;">
               <input type="submit" name="Right" value="Right" style="height:300px; width:300px; margin:0 auto; display:inline;">
               <br>
               <input type="submit" name="Backward" value="Backward" style="height:300px; width:300px; margin:0 auto; display:flex;">

           <button data-test="55" onclick="testFunction(this);">button1</button>
           
           <script>
              alert("scripts work");
           </script>
           
           
           
           </body>
           </html>
        '''
        temp = getTemperature()
        self.do_HEAD()
        self.wfile.write(html.format(temp[5:]).encode("utf-8"))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode("utf-8")
        post_data = post_data.split("=")[1]
        
        if post_data == 'Forward':
            leftMotor.value = 0.8
            rightMotor.value = 0.8
        elif post_data == 'Backward':
            leftMotor.value = -0.8
            rightMotor.value = -0.8
        elif post_data == 'Stop':
            leftMotor.value = 0
            rightMotor.value = 0
        elif post_data == 'Left':
            leftMotor.value = -0.8
            rightMotor.value = 0.8
        elif post_data == 'Right':
            leftMotor.value = 0.8
            rightMotor.value = -0.8

        print("Rover is {}".format(post_data))
        self._redirect('/')  # Redirect back to the root url


# # # # # Main # # # # #

if __name__ == '__main__':
    http_server = HTTPServer((host_name, host_port), MyServer)
    print("Server Starts - %s:%s" % (host_name, host_port))

    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        http_server.server_close()
