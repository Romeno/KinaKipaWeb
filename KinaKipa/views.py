from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from pip.operations import freeze
import sys

def test_view(req):
   return HttpResponse("Hello World!")

def freeze_info(req):
   x = freeze.freeze()
   #for p in x:
   print (str(x)+"\n")
   return HttpResponse(x)
def  sistem_info(req):
   i =sys.version
   print(i)
   return HttpResponse(i)

"""
import os
def freeze_info(req):
   p1 = '''pip freeze
            '''
   print(os.system(p1))
   return HttpResponse(p1)
"""