#!/usr/bin/env python3
import os
import sys
import random
import string
from datetime import datetime

# Set PYTHONPATH to include bin
os.environ['PYTHONPATH'] = os.environ.get('PYTHONPATH', '') + ':' + os.path.dirname(os.path.abspath(__file__))

try:
    from lib.ConfigLoader import ConfigLoader
    from lib.objects.Forums import Forum
    from lib.objects.Pgps import Pgp
except ImportError:
    import sys
    sys.path.append(os.path.join(os.getcwd(), 'bin'))
    from lib.ConfigLoader import ConfigLoader
    from lib.objects.Forums import Forum
    from lib.objects.Pgps import Pgp

def generate_random_id(length=32):
    chars = string.ascii_lowercase + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def populate_forums(count=50):
    print(f"Generating {count} random forums...")
    forum_types = ['general', 'hacking', 'leaks', 'crypto', 'tech']

    for i in range(count):
        f_id = generate_random_id(16)
        f_type = random.choice(forum_types)
        f_name = f"Random Forum {f_id}"
        f_url = f"http://{f_id}.onion/forum"
        f_info = f"This is a randomly generated forum of type {f_type}"

        Forum(f_id).create(f_type, name=f_name, url=f_url, info=f_info)
        if (i + 1) % 10 == 0:
            print(f"Processed {i + 1}/{count}...")
    print(f"Successfully populated {count} forums.")

def populate_pgps(count=50):
    print(f"Generating {count} random PGP entries...")
    subtypes = ['key', 'mail', 'name']
    date = datetime.now().strftime("%Y%m%d")

    for i in range(count):
        subtype = random.choice(subtypes)
        if subtype == 'mail':
            p_id = f"{generate_random_id(8)}@example.com"
        elif subtype == 'name':
            p_id = f"User_{generate_random_id(8)}"
        else: # key
            p_id = generate_random_id(40)

        Pgp(p_id, subtype).add(date)
        if (i + 1) % 10 == 0:
            print(f"Processed {i + 1}/{count}...")
    print(f"Successfully populated {count} PGP entries.")

if __name__ == '__main__':
    # Default counts
    forum_count = 50
    pgp_count = 50

    if len(sys.argv) > 1:
        try:
            count = int(sys.argv[1])
            forum_count = count
            pgp_count = count
        except ValueError:
            pass

    populate_forums(forum_count)
    populate_pgps(pgp_count)
