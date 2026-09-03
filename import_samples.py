import os
import sys

# Set environment variables
AIL_HOME = os.getcwd()
AIL_BIN = os.path.join(AIL_HOME, 'bin')
os.environ['AIL_HOME'] = AIL_HOME
os.environ['AIL_BIN'] = AIL_BIN

# Add AIL_BIN to sys.path
sys.path.append(AIL_BIN)

try:
    from importer.FileImporter import DirImporter
    print("Successfully imported DirImporter")
    
    importer = DirImporter()
    sample_path = os.path.join(AIL_HOME, 'samples/2021/01/01')
    
    if os.path.isdir(sample_path):
        print(f"Importing data from {sample_path}...")
        importer.importer(sample_path)
        print("Import completed successfully.")
    else:
        print(f"Error: {sample_path} is not a directory.")

except Exception as e:
    print(f"An error occurred: {e}")
