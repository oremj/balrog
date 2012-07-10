import atexit
from os import killpg, remove, setsid
import random
import signal
from subprocess import Popen, PIPE, STDOUT
import sys
from tempfile import mkstemp
from time import sleep

if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("--auth", dest="auth", default="bob:bob")
    parser.add_option("-v", "--verbose", dest="verbose", action="store_true",
        help="Verbose output")
    options, args = parser.parse_args()
    username, password = options.auth.split(':')

    port = random.randint(10000, 60000)

    db = mkstemp()[1]
    cmd = ['python', 'admin.py', '--host', '127.0.0.1', '-d', 'sqlite:///' + db, '-p', str(port), '--auth', options.auth]
    if options.verbose:
        cmd.append('-v')
    balrog = Popen(cmd, stdout=PIPE, stderr=STDOUT, preexec_fn=setsid)
    @atexit.register
    def killbalrog():
        killpg(balrog.pid, signal.SIGKILL)
        balrog.wait()
        remove(db)
        print balrog.stdout.read()

    testsUrl = 'http://%s:%s@127.0.0.1:%d/tests.html' % (username, password, port)
    success = True
    attempts = 5
    n = 1
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
        n += 1
    print output
    if not success:
        sys.exit(1)
