#!/usr/bin/env python

import sys
from pycdf import *
from Numeric import *

typeTab = {NC.BYTE:   'BYTE',
           NC.CHAR:   'CHAR',
           NC.SHORT:  'SHORT',
           NC.INT:    'INT',
           NC.FLOAT:  'FLOAT',
           NC.DOUBLE: 'DOUBLE'}

printf = sys.stdout.write
ncFile = sys.argv[1]
try:
  nc = CDF(ncFile)
  attr = nc.attributes(full=1)
  dims = nc.dimensions(full=1)
  vars = nc.variables()

  # Dataset name, number of attributes, dimensions and variables.
  printf("DATASET INFO\n")
  printf("------------\n\n")
  printf("%-25s%s\n" % ("netCDF file:", ncFile))
  printf("%-25s%d\n" % ("  dataset attributes:", len(attr)))
  printf("%-25s%d\n" % ("  dimensions:", len(dims)))
  printf("%-25s%d\n" % ("  variables:", len(vars)))
  printf("\n");

  # Attribute table.
  if len(attr) > 0:
      printf("Dataset attributes\n\n")
      printf("  name                 idx type   len value\n")
      printf("  -------------------- --- ----   --- -----\n")
      attNames = attr.keys()
      attNames.sort()
      for a in attNames:
          t = attr[a]
          printf("  %-20s %3d %-6s %3d %s\n" %
                 (a, t[1], typeTab[t[2]], t[3], t[0]))
      printf("\n")

  # Dimensions table
  if len(dims) > 0:
      printf("Dataset dimensions\n\n")
      printf("  name                 idx length unlimited\n")
      printf("  -------------------- --- ------ ---------\n")
      dimNames = dims.keys()
      dimNames.sort()
      for d in dimNames:
          t = dims[d]
          printf ("  %-20s %3d %6d %3s\n" %
                  (d, t[1], t[0], t[2] and 'X' or ''))
      printf("\n")

  # Variables table
  if len(vars) > 0:
      printf("Dataset variables\n\n")
      printf("  name                 idx type   nattr dimension(s)\n")
      printf("  -------------------- --- ----   ----- ------------\n")
      varNames = vars.keys()
      varNames.sort()
      for v in varNames:
          vAttr = nc.var(v).attributes()
          t = vars[v]
          printf("  %-20s %3d %-6s %5d " %
                 (v, t[3], typeTab[t[2]], len(vAttr)))
          n = 0
          for d in t[0]:
              printf("%s%s(%d)" % (n > 0 and ', ' or '', d, t[1][n]))
              n += 1
          printf("\n")
      printf("\n")

  # Variables attributes
  if len(varNames) > 0:
      printf("VARIABLE INFO\n")
      printf("-------------\n\n")
      for v in varNames:
          vAttr = nc.var(v).attributes(full=1)
          if len(vAttr) > 0:
              printf("%s attributes\n\n" % v)
              printf("  name                 idx type   len value\n")
              printf("  -------------------- --- ----   --- -----\n")
              attNames = vAttr.keys()
              attNames.sort()
              for a in attNames:
                  t = vAttr[a]
                  printf("  %-20s %3d %-6s %3d %s\n" %
                         (a, t[1], typeTab[t[2]], t[3], t[0]))
              printf("\n")
      
except CDFError, msg:
    print "CDFError", msg
