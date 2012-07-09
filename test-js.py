from os import killpg, setsid
import random
import signal
from subprocess import Popen, PIPE
import sys
from time import sleep

if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-v", "--verbose", dest="verbose", action="store_true",
        help="Verbose output")
    options, args = parser.parse_args()

    port = random.randint(10000, 60000)

    cmd = ['python', 'admin.py', '--host', '127.0.0.1', '-d', 'sqlite:///:memory:', '-p', str(port), '--noauth']
    if options.verbose:
        cmd.append('-v')
    balrog = Popen(cmd, stdout=PIPE, stderr=PIPE, preexec_fn=setsid)
    testsUrl = 'http://127.0.0.1:%d/tests.html' % port
    success = True
    attempts = 5
    n = 1
    while n <= attempts:
        tests_cmd = Popen(['phantomjs', 'scripts/run-qunit.js', testsUrl], stdout=PIPE)
        tests_cmd.wait()
        if tests_cmd.returncode != 0:
            output = tests_cmd.stdout.read()
            if 'Unable to access network' in output:
                if n == 5:
                    print "Balrog still not initialized, bailing..."
                    success = False
                else:
                    print "Balrog not initialized, sleeping and trying again..."
                    sleep(1)
            # Tests failed or something went wrong in phantom
            else:
                break
        n += 1
    print output
    killpg(balrog.pid, signal.SIGKILL)
    balrog.wait()
    if not success:
        sys.exit(1)
