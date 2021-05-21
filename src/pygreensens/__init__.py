"""pygreensens"""
__version__ = "0.3.6"

if __name__ != '__main__':
    from .api import GreensensApi
else:
    from api import GreensensApi


