#!/usr/bin/env python

import pypar

rank = pypar.rank()
size = pypar.size()

print "I am rank=", rank,"size=",size 
