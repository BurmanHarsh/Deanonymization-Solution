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

def test_exists():
    obj_type = 'pgp'
    subtype = 'key'
    obj_id = '0naq6unx4lkl1rkaqlb6zn5z55oywn2pcr12h8ok'

    print(f"Testing exists_obj({obj_type}, {subtype}, {obj_id})")
    result = ail_objects.exists_obj(obj_type, subtype, obj_id)
    print(f"Result: {result}")

if __name__ == '__main__':
    test_exists()
