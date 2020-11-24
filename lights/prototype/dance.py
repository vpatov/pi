import subprocess
import time

for i in range(0,50):
	subprocess.run('./lights.sh on',shell=True)
	time.sleep(0.05)
	subprocess.run('./lights.sh off',shell=True)
	time.sleep(0.05)

