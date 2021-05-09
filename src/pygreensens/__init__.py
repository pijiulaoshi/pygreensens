"""pygreensens"""
__version__ = "0.3.1"

if __name__ != '__main__':
    from .pygreensens import GreenSens
    from .const import *
else:
    from pygreensens import GreenSens
    from const import *


