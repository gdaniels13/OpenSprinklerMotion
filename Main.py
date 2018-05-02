#!/usr/bin/python -tt

from daemon import Daemon
import sys,time



class MotionDaemon(Daemon):
    def run(self):
        counter = 0
        while True:
            print("hello: " + counter)
            counter += counter+1
            time.sleep(10)






if __name__ == "__main__":
    daemon = MotionDaemon('/var/run/MotionDaemon.pid')
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