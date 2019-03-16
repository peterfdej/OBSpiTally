#!/usr/bin/env python
# /etc/init.d/tally.py
### BEGIN INIT INFO
# Provides:             tally.py
# Required-Start:       $remote_fs $syslog
# Required-Stop:        $remote_fs $syslog
# Default-Start:        2 3 4 5
# Default-Stop:         0 1 6
# Short-Description:    Start daemon at boot time
# Description:          Enable service provided by daemon.
### END INIT INFO

# -*- coding: utf-8 -*-
#For Raspberry Pi
#

import sys
import time
import xml.etree.ElementTree as ET
import socket
import websocket
import hashlib
import base64
import json
from gpiozero import LED
try:
    import thread
except ImportError:
    import _thread as thread

tree = ET.parse('/home/pi/tally.xml')  
root = tree.getroot()
host = root[0].text
port = root[1].text
password = root[2].text
tallyscene = root[3].text

#ledgreen = LED(5)	#pin 29, 30 earth, R=330ohm
#ledred = LED(13)	#pin 33, 34 earth, R=330ohm

#pi V1
ledgreen = LED(23)	#pin 16, 14 earth, R=330ohm
ledred = LED(24)	#pin 18, 20 earth, R=330ohm

getauthrequired = {"request-type" : "GetAuthRequired" ,"message-id" : "1"};
GetSceneList = {"request-type" : "GetSceneList" , "message-id" : "getSceneList"}
GetStudioModeStatus = {"request-type" : "GetStudioModeStatus" , "message-id" : "GetStudioModeStatus"}
GetPreviewScene = {"request-type" : "GetPreviewScene" , "message-id" : "GetPreviewScene"}

while True:
	try:
		def on_message(ws, message):
			data = json.loads(message)
			#print (data["message-id"])
			#print (data)
			if "error" in data:
				if (data["error"] == "Authentication Failed."):
					print("Authentication Failed.")
					ws.keep_running = False
				else:
					print (data)
			elif "message-id" in data:
				if (data["message-id"] == "GetStudioModeStatus"):
					StudioMode = data["studio-mode"]
					if (StudioMode):
						ws.send(json.dumps(GetPreviewScene))
				elif (data["message-id"] == "getSceneList"):
					currentscene = data["current-scene"]
					print ("currentscene: %s" % currentscene)
					if (tallyscene == currentscene):
						print("Tallylight RED on: %s" % tallyscene)
						if ledgreen.is_lit:
							ledgreen.off()
						ledred.on()
				elif (data["message-id"] == "GetPreviewScene"):
					previewscene = data["name"]
					print ("previewscene: %s" % previewscene)
					if (tallyscene == previewscene):
						print("Tallylight GREEN on: %s" % tallyscene)
						if ledred.is_lit:
							ledred.off()
						ledgreen.on()
				elif (data["authRequired"]):
					print("Authentication required")
					secret = base64.b64encode(hashlib.sha256((password + data['salt']).encode('utf-8')).digest())
					auth = base64.b64encode(hashlib.sha256(secret + data['challenge'].encode('utf-8')).digest()).decode('utf-8')
					auth_payload = {"request-type": "Authenticate", "message-id": "2", "auth": auth}
					ws.send(json.dumps(auth_payload))
				else:
					print(data)
			elif "update-type" in message:
				if (data["update-type"] == "PreviewSceneChanged"):
					previewscene = data["scene-name"];
					print("previewscene: %s" % previewscene)
					if (tallyscene == previewscene):
						print("Tallylight GREEN on: %s" % tallyscene)
						if ledred.is_lit:
							ledred.off()
						ledgreen.on()
					else:
						print("Tallylight GREEN off: %s" % tallyscene)
						ledgreen.off()
					ws.send(json.dumps(GetSceneList))
					#when tallyscene is both preview and currentscene this will lit red also.
				elif (data["update-type"] == "SwitchScenes"):
					currentscene = data["scene-name"];
					print("currentscene: %s" % currentscene)
					if tallyscene == currentscene:
						print("Tallylight RED on: %s" % tallyscene)
						if ledgreen.is_lit:
							ledgreen.off()
						ledred.on()
					else:
						print("Tallylight RED off: %s" % tallyscene)
						ledred.off()

		def on_error(ws, error):
			print(error)
			ws.close()

		def on_close(ws):
			print("Connection error. Tally lights off")
			ledred.off()
			ledgreen.off()
			ws.keep_running = False
			time.sleep(30)

		def on_open(ws):
			def run(*args):
				ws.send(json.dumps(getauthrequired))
				time.sleep(2)
				if ws.sock:
					ws.send(json.dumps(GetStudioModeStatus))
					time.sleep(2)
					ws.send(json.dumps(GetSceneList))
			thread.start_new_thread(run, ())


		if __name__ == "__main__":
			#websocket.enableTrace(True)
			ws = websocket.WebSocketApp("ws://{}:{}".format(host, port),on_message = on_message,on_error = on_error,on_close = on_close)
			ws.on_open = on_open
			ws.run_forever()

	except Exception:
		print("Connection error. Tally lights off")
		ledred.off()
		ledgreen.off()
		time.sleep(30)