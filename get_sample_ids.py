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
    r_crawler = config_loader.get_db_conn("Kvrocks_Crawler")

    # Get a few samples from the full sets
    up_domains = r_crawler.srandmember('full_onion_up', 5)
    down_domains = r_crawler.srandmember('full_onion_down', 5)

    print("--- Sample UP Domains ---")
    if up_domains:
        for d in up_domains:
            print(d.decode() if isinstance(d, bytes) else d)
    else:
        print("No UP domains found.")

    print("\n--- Sample DOWN Domains ---")
    if down_domains:
        for d in down_domains:
            print(d.decode() if isinstance(d, bytes) else d)
    else:
        print("No DOWN domains found.")

if __name__ == '__main__':
    get_samples()
