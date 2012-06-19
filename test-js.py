import logging
from os import path
import random
import site
from subprocess import check_call, Popen, PIPE, STDOUT
from time import sleep

if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-v", "--verbose", dest="verbose", action="store_true",
        help="Verbose output")
    options, args = parser.parse_args()

    port = random.randint(10000, 60000)

    cmd = ['python', 'admin.py', '--host', '127.0.0.1', '-d', 'sqlite:///:memory:', '-p', str(port)]
    if options.verbose:
        cmd.append('-v')
    balrog = Popen(cmd)
    sleep(1)
    testsUrl = 'http://127.0.0.1:%d/tests.html' % port
    check_call(['phantomjs', 'scripts/run-qunit.js', testsUrl])
