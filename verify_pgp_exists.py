#!/usr/bin/env python3
import os
import sys

# Set PYTHONPATH to include bin
os.environ['PYTHONPATH'] = os.environ.get('PYTHONPATH', '') + ':' + os.path.dirname(os.path.abspath(__file__))

try:
    from lib.ConfigLoader import ConfigLoader
    import lib.objects.ail_objects as ail_objects
except ImportError:
    import sys
    sys.path.append(os.path.join(os.getcwd(), 'bin'))
    from lib.ConfigLoader import ConfigLoader
    import lib.objects.ail_objects as ail_objects

def verify():
    config_loader = ConfigLoader()
    r_object = config_loader.get_db_conn("Kvrocks_Objects")

    # Get a few PGP IDs from the DB
    pgp_keys = r_object.zrange('pgp_all:key', 0, 4)
    if not pgp_keys:
        print("No PGP keys found in DB")
        return

    for pk in pgp_keys:
        pk = pk.decode() if isinstance(pk, bytes) else pk
        print(f"Testing {pk}:")
        print(f"  Direct DB exists: {r_object.exists(f'meta:pgp:key:{pk}')}")
        print(f"  ail_objects.exists_obj('pgp', 'key', {pk}): {ail_objects.exists_obj('pgp', 'key', pk)}")

if __name__ == '__main__':
    verify()
