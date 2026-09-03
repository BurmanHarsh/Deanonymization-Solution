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

def check_pgp_meta():
    config_loader = ConfigLoader()
    r_object = config_loader.get_db_conn("Kvrocks_Objects")

    # Let's check one of the IDs we generated
    # Subtype key: 0naq6unx4lkl1rkaqlb6zn5z55oywn2pcr12h8ok
    test_id = '0naq6unx4lkl1rkaqlb6zn5z55oywn2pcr12h8ok'
    subtype = 'key'
    key = f'meta:pgp:{subtype}:{test_id}'

    print(f"Checking key: {key}")
    exists = r_object.exists(key)
    print(f"Exists: {exists}")
    if exists:
        print(f"Meta: {r_object.hgetall(key)}")

if __name__ == '__main__':
    check_pgp_meta()
