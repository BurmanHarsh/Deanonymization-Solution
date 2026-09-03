#!/usr/bin/env python3
import os
import sys
import time
import random
import string
from datetime import datetime

# Set PYTHONPATH to include bin
os.environ['PYTHONPATH'] = os.environ.get('PYTHONPATH', '') + ':' + os.path.dirname(os.path.abspath(__file__))

try:
    from lib.ConfigLoader import ConfigLoader
except ImportError:
    import sys
    sys.path.append(os.path.join(os.getcwd(), 'bin'))
    from lib.ConfigLoader import ConfigLoader

def generate_random_onion():
    chars = string.ascii_lowercase + string.digits
    return ''.join(random.choice(chars) for _ in range(56)) + '.onion'

def force_down(domain_name):
    config_loader = ConfigLoader()
    r_crawler = config_loader.get_db_conn("Kvrocks_Crawler")

    date = datetime.now().strftime("%Y%m%d")
    epoch = int(time.time())
    domain_type = 'onion' if domain_name.endswith('.onion') else 'web'

    print(f"Forcing {domain_name} to DOWN status for date {date}...")

    # 1. Add to daily and full DOWN sets
    r_crawler.sadd(f'{domain_type}_down:{date}', domain_name)
    r_crawler.sadd(f'full_{domain_type}_down', domain_name)

    # 2. Remove from UP sets
    r_crawler.srem(f'{domain_type}_up:{date}', domain_name)
    r_crawler.srem(f'full_{domain_type}_up', domain_name)

    # 3. Update domain history to show it was DOWN
    # Domain.is_up() checks if the latest history entry is NOT an integer.
    # For DOWN, we use the epoch as the root_item (which is an integer).
    r_crawler.zadd(f'domain:history:{domain_name}', {epoch: epoch})

    # 4. Update meta
    r_crawler.hset(f'domain:meta:{domain_name}', 'first_seen', date)
    r_crawler.hset(f'domain:meta:{domain_name}', 'last_check', date)

    print(f"Successfully marked {domain_name} as DOWN.")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        # Generate 2 random ones if no arg provided
        for _ in range(2):
            target = generate_random_onion()
            force_down(target)
    else:
        target = sys.argv[1]
        force_down(target)
