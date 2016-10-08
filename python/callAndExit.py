# call process from program and exit program
# source - http://stackoverflow.com/questions/6807102/python-run-system-command-and-then-exit-wont-exit

import subprocess
import sys

# to exit without return
subprocess.Popen(["C:/python27/python.exe", "D:/foo.py"])
sys.exit(0) 

# to exit after return like os.system(cmd)
p = subprocess.Popen(command)
p.wait()

