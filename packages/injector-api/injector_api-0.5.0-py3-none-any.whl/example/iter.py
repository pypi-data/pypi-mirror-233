import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from example.iinterfa import *
# Agrega el directorio padre al sys.path
#from injector_api import inject


class ExampleServiceImpl2(IExampleService):
    #@inject()
    def __init__(self,se:Se) -> None:
        pass
    
    def do_something(self):
        return "Service Implementation 2"
    
class ExampleServiceImpl1(IExampleService):
    def do_something(self):
        return "Service Implementation 1"
    
class SeA(Se):
    def do_something(self):
        return "Service Implementation SeA"