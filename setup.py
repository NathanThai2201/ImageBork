import subprocess
import sys


packages = ['numpy', 'scikit-image', 'matplotlib', 'scipy','scikit-learn']

#test install
for package in packages:
    try:
        __import__(package)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
