import atexit
from os import killpg, remove, setsid
import random
import signal
from subprocess import Popen, PIPE, STDOUT
import sys
from tempfile import mkstemp
from time import sleep

import code, traceback, signal

def debug(sig, frame):
    """Interrupt running process, and provide a python prompt for
    interactive debugging."""
    d={'_frame':frame}         # Allow access to frame object.
    d.update(frame.f_globals)  # Unless shadowed by global
    d.update(frame.f_locals)

    i = code.InteractiveConsole(d)
    message  = "Signal recieved : entering python shell.\nTraceback:\n"
    message += ''.join(traceback.format_stack(frame))
    i.interact(message)

def listen():
    signal.signal(signal.SIGUSR1, debug)  # Register handler


if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-v", "--verbose", dest="verbose", action="store_true",
        help="Verbose output")
    options, args = parser.parse_args()

    port = random.randint(10000, 60000)

    db = mkstemp()[1]
    cmd = ['python', 'admin.py', '--host', '127.0.0.1', '-d', 'sqlite:///' + db, '-p', str(port), '--auth', 'bob:bob']
    if options.verbose:
        cmd.append('-v')
    balrog = Popen(cmd, stdout=PIPE, stderr=STDOUT, preexec_fn=setsid)

    testsUrl = 'http://bob:bob@127.0.0.1:%d/tests.html' % port
    success = True
    attempts = 5
    n = 1

    @atexit.register
    def killbalrog():
        killpg(balrog.pid, signal.SIGKILL)
        balrog.wait()
        remove(db)
        if not success:
            print balrog.stdout.read()

    while n <= attempts:
        tests_cmd = Popen(['phantomjs', 'scripts/run-qunit.js', testsUrl], stdout=PIPE, stderr=STDOUT)
        tests_cmd.wait()
        output = tests_cmd.stdout.read()
        if tests_cmd.returncode != 0:
            if 'Unable to access network' in output:
                if n == attempts:
                    print "Balrog still not initialized, bailing..."
                    success = False
                else:
                    print "Balrog not initialized, sleeping and trying again..."
                    sleep(1)
            # Tests failed or something went wrong in phantom
            else:
                break
        else:
            break
        n += 1
    print output
    if not success:
        sys.exit(1)
