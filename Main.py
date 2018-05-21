#!/usr/bin/python -tt

from daemon import Daemon
import sys,time
import RPi.GPIO as GPIO
import requests

FRONT_MOTION_CHANNEL = 16
BACK_MOTION_CHANNEL = 19
DEBOUNCE_TIME = 15000
SPRINKLER_RUN_TIME = 4
FRONT_ZONE = 3
BACK_ZONE=1
PASSWORD=""
SPRINKLER_URL = "http://localhost/cm"

class MotionDaemon(Daemon):

    def run(self):
        read_password()
        GPIO.cleanup() # may cause a warning but safer than the callback not getting set up correctly
        GPIO.setmode(GPIO.BCM)
        GPIO.setup([FRONT_MOTION_CHANNEL, BACK_MOTION_CHANNEL], GPIO.IN)
        GPIO.add_event_detect(FRONT_MOTION_CHANNEL, GPIO.FALLING, callback=self.activate_sprinkler, bouncetime=DEBOUNCE_TIME)
        GPIO.add_event_detect(BACK_MOTION_CHANNEL , GPIO.FALLING, callback=self.activate_sprinkler, bouncetime=DEBOUNCE_TIME)
        while True:
            time.sleep(10000);
            
    def read_password():
        f = open("password.txt")
        PASSWORD=f.readline()
        f.close()
        print(PASSWORD)
        
    def activate_sprinkler(self, channel):
        log("channel: " + `channel` + " activated\n")
        if channel==FRONT_MOTION_CHANNEL:
            run_sprinkler(FRON_ZONE)
        elif channel==BACK_MOTION_CHANNEL:
            run_sprinkler(BACK_ZONE)

    def run_sprinkler(self,zone):
        querystring = {"sid" : zone, "en" : "1", "t" : SPRINKLER_RUN_TIME, "pw" : PASSWORD}
        response = requests.request("GET", url, params=querystring)
        log(response.text)
        
    log(self,message):
        f = open("/var/log/motionDaemonOutput.txt", "a")
        f.write(message)
        f.close()
        
#(pidfile, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null')
if __name__ == "__main__":
    daemon = MotionDaemon( '/var/run/MotionDaemon.pid',"/dev/null","/var/log/Motion_daemon.log","/var/log/Motion_daemon_error.log")
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)
