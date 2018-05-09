#!/usr/bin/python -tt

from daemon import Daemon
import sys,time
import RPi.GPIO as GPIO

FRONT_MOTION_CHANNEL = 16
BACK_MOTION_CHANNEL = 19
DEBOUNCE_TIME = 15000
class MotionDaemon(Daemon):

    def run(self):
        GPIO.cleanup() # may cause a warning but safer than the callback not getting set up correctly
        GPIO.setmode(GPIO.BCM)
        GPIO.setup([FRONT_MOTION_CHANNEL, BACK_MOTION_CHANNEL], GPIO.IN)
        GPIO.add_event_detect(FRONT_MOTION_CHANNEL, GPIO.FALLING, callback=self.activate_sprinkler, bouncetime=DEBOUNCE_TIME)
        GPIO.add_event_detect(BACK_MOTION_CHANNEL , GPIO.FALLING, callback=self.activate_sprinkler, bouncetime=DEBOUNCE_TIME)
        while True:
            time.sleep(10000);

    def activate_sprinkler(self, channel):
        # todo actually turn on the correct sprinkler zone here
        f = open("/var/log/motionDaemonOutput.txt", "a")
        f.write("channel: " + `channel` + " activated\n")
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