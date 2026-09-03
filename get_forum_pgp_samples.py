#!/usr/bin/env python3
import os
import sys

# Set PYTHONPATH to include bin
os.environ['PYTHONPATH'] = os.environ.get('PYTHONPATH', '') + ':' + os.path.dirname(os.path.abspath(__file__))

try:
    from lib.ConfigLoader import ConfigLoader
except ImportError:
    import sys
    sys.path.append(os.path.join(os.getcwd(), 'bin'))
    from lib.ConfigLoader import ConfigLoader

def get_samples():
    config_loader = ConfigLoader()
    r_object = config_loader.get_db_conn("Kvrocks_Objects")

    print("--- Sample Forums ---")
    forums = r_object.smembers('forum:all')
    if forums:
        for f in list(forums)[:5]:
            print(f.decode() if isinstance(f, bytes) else f)
    else:
        print("No forums found.")

    print("\n--- Sample PGP Entries ---")
    # PGP has subtypes: key, mail, name
    subtypes = ['key', 'mail', 'name']
    for st in subtypes:
        pgps = r_object.zrange(f'pgp_all:{st}', 0, 4)
        if pgps:
            print(f"Subtype {st}:")
            for p in pgps:
                print(f"  {p.decode() if isinstance(p, bytes) else p}")
        else:
            print(f"No PGP entries found for subtype {st}.")

if __name__ == '__main__':
    get_samples()
