
import os, os.path

def check_saved():
	DIR = 'Capture'
	return len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])

print(check_saved())
