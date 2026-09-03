#!/usr/bin/env python3
import os
import sys
import time
from datetime import datetime

# Set PYTHONPATH to include bin
os.environ['PYTHONPATH'] = os.environ.get('PYTHONPATH', '') + ':' + os.path.dirname(os.path.abspath(__file__))
# If we are running from root, we need to add bin
sys.path.append(os.path.join(os.getcwd(), 'bin'))

try:
    from lib.ConfigLoader import ConfigLoader
    from lib.objects import Domains
except ImportError:
    import sys
    sys.path.append(os.path.join(os.getcwd(), 'bin'))
    from lib.ConfigLoader import ConfigLoader
    from lib.objects import Domains

def force_up(domain_name):
    config_loader = ConfigLoader()
    r_crawler = config_loader.get_db_conn("Kvrocks_Crawler")

    date = datetime.now().strftime("%Y%m%d")
    epoch = int(time.time())
    domain_type = 'onion' if domain_name.endswith('.onion') else 'web'

    print(f"Forcing {domain_name} to UP status for date {date}...")

    # 1. Add to daily and full UP sets
    r_crawler.sadd(f'{domain_type}_up:{date}', domain_name)
    r_crawler.sadd(f'full_{domain_type}_up', domain_name)

    # 2. Remove from DOWN sets
    r_crawler.srem(f'{domain_type}_down:{date}', domain_name)
    r_crawler.srem(f'full_{domain_type}_down', domain_name)

    # 3. Update domain history to show it was UP
    # Domain.is_up() checks if the latest history entry is NOT an integer.
    # We use a dummy item ID 'forced_up_item_123'
    dummy_item_id = 'forced_up_item_123'
    r_crawler.zadd(f'domain:history:{domain_name}', {dummy_item_id: epoch})

    # 4. Update meta
    r_crawler.hset(f'domain:meta:{domain_name}', 'first_seen', date)
    r_crawler.hset(f'domain:meta:{domain_name}', 'last_check', date)

    print(f"Successfully marked {domain_name} as UP.")

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        # Default to the one we found
        target = 'eswpccgr5xyovsahffkehgleqthrasfpfdblwbs4lstd345dwq5qumqd.onion'
    else:
        target = sys.argv[1]
    force_up(target)
