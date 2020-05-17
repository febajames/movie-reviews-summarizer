import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))

ABS_PATH = os.path.abspath(os.path.dirname(sys.argv[0]))
CONFIG_PATH = os.path.join(ABS_PATH, './config.json')  #replace './config.json' with your filename