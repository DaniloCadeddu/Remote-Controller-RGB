import RPi.GPIO as GPIO # The module for controlling the Raspberry Pi GPIO extension board
from http.server import BaseHTTPRequestHandler, HTTPServer
import time

host_name = '192.168.1.***' # Change this to your Raspberry Pi IP address
host_port = 8000
PINS = [17,18,27] # The pins that controls the output
class MyServer(BaseHTTPRequestHandler):
	# A special implementation of BaseHTTPRequestHander for reading data from and control GPIO of a Raspberry Pi
	
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
		# Put here your template html
		html = '''html_template'''
		
		self.do_HEAD()
		self.wfile.write(html.format().encode("utf-8"))
	
	
	
	def do_POST(self):
		content_length = int(self.headers['Content-Length']) # Get the size of data
		post_data = self.rfile.read(content_length).decode("utf-8") # Get the data
		post_data = post_data.split("=")[1] # Only keep the value
		# GPIO setup
		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(False)
		GPIO.setup(PINS,GPIO.OUT) # Put the three PINS define above as output
		
		# Function that makes the LED blink, just a finite loop that alternates the color we pass to the function and the led off.
		def blink (pincolor, pin2, pin3):
			for _ in range(3):
				GPIO.output(17, GPIO.HIGH)
				GPIO.output(18, GPIO.HIGH)
				GPIO.output(27, GPIO.HIGH)
				time.sleep(0.3)
				GPIO.output(pincolor, GPIO.LOW)
				GPIO.output(pin2, GPIO.HIGH)
				GPIO.output(pin3, GPIO.HIGH)
				time.sleep(0.3)
		
		# Makes the led red
		if post_data == 'R':
			GPIO.output(17, GPIO.LOW)
			GPIO.output(18, GPIO.HIGH)
			GPIO.output(27, GPIO.HIGH)
		# Makes the led green
		elif post_data == 'G':
			GPIO.output(17, GPIO.HIGH)
			GPIO.output(18, GPIO.LOW)
			GPIO.output(27, GPIO.HIGH)
		# Makes the led blue
		elif post_data == 'B':
			GPIO.output(17, GPIO.HIGH)
			GPIO.output(18, GPIO.HIGH)
			GPIO.output(27, GPIO.LOW)
		
		# Blink red
		elif post_data == 'B-R':
			blink(17, 18, 27)
		# Blink green
		elif post_data == 'B-G':
			blink(18, 17, 27)
		# Blink blue
		elif post_data == 'B-B':
			blink(27, 18, 17)
		
		# Makes the led white (on)
		elif post_data == 'On':
			GPIO.output(17, GPIO.LOW)
			GPIO.output(18, GPIO.LOW)
			GPIO.output(27, GPIO.LOW)
		# Makes the led off
		elif post_data == 'Off':
			GPIO.output(17, GPIO.HIGH)
			GPIO.output(18, GPIO.HIGH)
			GPIO.output(27, GPIO.HIGH)
		# Makes the led explode
		elif post_data == 'Secret':
			GPIO.output(17, GPIO.LOW)
			GPIO.output(18, GPIO.HIGH)
			GPIO.output(27, GPIO.LOW)
				
		self._redirect('/') # Redirect back to the root url

# Run the server
if __name__ == '__main__':
	http_server = HTTPServer((host_name, host_port), MyServer)
	print("Server Starts - %s:%s" % (host_name, host_port))
	try:
		http_server.serve_forever()
	except KeyboardInterrupt:
		http_server.server_close()
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
