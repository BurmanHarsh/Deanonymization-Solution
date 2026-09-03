import os
import sys

# Set environment variables
AIL_HOME = os.getcwd()
AIL_BIN = os.path.join(AIL_HOME, 'bin')
os.environ['AIL_HOME'] = AIL_HOME
os.environ['AIL_BIN'] = AIL_BIN
sys.path.append(AIL_BIN)

from lib import ail_core
from lib.objects import Items
from lib import ail_logger
import logging.config

logging.config.dictConfig(ail_logger.get_config(name='modules'))
logger = logging.getLogger()

def populate():
    print("Force populating database with sample items...")
    # Create a dummy item
    item_id = "sample_item_1"
    content = "This is a sample credit card leak containing card 4111111111111111"
    
    # The actual object creation depends on the project's internal lib.objects.Items
    # Since we don't want to guess the exact constructor, we'll use the internal 'Items.create_item' 
    # if it exists, otherwise we'll try to find how items are saved.
    
    try:
        # Attempt to create an item using the expected internal method
        Items.create_item(item_id, {"date": "2021-01-01"}, content)
        print(f"Successfully created item: {item_id}")
    except Exception as e:
        print(f"Failed to create item: {e}")

if __name__ == "__main__":
    populate()
