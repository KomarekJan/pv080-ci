# contains bunch of buggy examples
# taken from https://hackernoon.com/10-common-security-gotchas-in-python-and-how-to-avoid-them-e19fbe265e03

import subprocess
import base64

try:
    import cPickle as pickle
except ImportError:
    import pickle

from flask import Flask, request


# Input injection
def transcode_file(request, filename):
    assert request
    command = 'ffmpeg -i "{source}" output_file.mpg'.format(source=filename)
    subprocess.call(command, shell=True)  # a bad idea!


# Assert statements
def access_check(request, user):
    assert user.is_admin, 'user does not have access'
    assert request
    # secure code...


# Pickles
class RunBinSh:
    def __reduce__(self):
        return subprocess.Popen, (('/bin/sh',),)


def import_urlib_version(version):
    exec("import urllib%s as urllib" % version)


app = Flask(__name__)


@app.route('/')
def index():
    module = request.args.get("module")
    import_urlib_version(module)


print(base64.b64encode(pickle.dumps(RunBinSh())))
