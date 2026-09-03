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

def set_status(r_crawler, domain_name, status, date, epoch):
    domain_type = 'onion' if domain_name.endswith('.onion') else 'web'

    if status == 'UP':
        r_crawler.sadd(f'{domain_type}_up:{date}', domain_name)
        r_crawler.sadd(f'full_{domain_type}_up', domain_name)
        r_crawler.srem(f'{domain_type}_down:{date}', domain_name)
        r_crawler.srem(f'full_{domain_type}_down', domain_name)
        dummy_item_id = 'random_up_item_' + ''.join(random.choices(string.digits, k=5))
        r_crawler.zadd(f'domain:history:{domain_name}', {dummy_item_id: epoch})
    else: # DOWN
        r_crawler.sadd(f'{domain_type}_down:{date}', domain_name)
        r_crawler.sadd(f'full_{domain_type}_down', domain_name)
        r_crawler.srem(f'{domain_type}_up:{date}', domain_name)
        r_crawler.srem(f'full_{domain_type}_up', domain_name)
        r_crawler.zadd(f'domain:history:{domain_name}', {epoch: epoch})

    r_crawler.hset(f'domain:meta:{domain_name}', 'first_seen', date)
    r_crawler.hset(f'domain:meta:{domain_name}', 'last_check', date)

def populate_mixed(count=50):
    config_loader = ConfigLoader()
    r_crawler = config_loader.get_db_conn("Kvrocks_Crawler")

    date = datetime.now().strftime("%Y%m%d")
    epoch = int(time.time())

    print(f"Generating {count} random mixed targets...")
    for i in range(count):
        target = generate_random_onion()
        status = random.choice(['UP', 'DOWN'])
        set_status(r_crawler, target, status, date, epoch)
        if (i + 1) % 10 == 0:
            print(f"Processed {i + 1}/{count}...")

    print(f"Successfully populated {count} mixed targets.")

if __name__ == '__main__':
    count = 50
    if len(sys.argv) > 1:
        try:
            count = int(sys.argv[1])
        except ValueError:
            pass
    populate_mixed(count)
