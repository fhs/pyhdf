from numpy import *
from pycdf import *

print "Running with pycdf configured for: %s" % pycdfArrayPkg()

try:
    # Create a test dataset. Raise the automode flag, so that
    # we do not need to worry about setting the define/data mode.
    d = CDF('test.nc', NC.WRITE|NC.CREATE|NC.TRUNC)
    d.automode()
    # Create 2 global attributes, one holding a string,
    # and the other one 2 floats.
    d.title = 'This is a test dataset'
    d.cal_coeff = (-0.5, 2.8)
    # We want to create a "record" variable to store a matrix
    # with 5 columns and a variable number of rows.
    # We thus create 2 netCDF dimensions:
    #   -one named `bin_number' of length 5 (NCOLS) for the number
    #    of columns;
    #   -one named `rec_num' of unlimited length (NROWS) for the number
    #    of rows.
    NROWS = NC.UNLIMITED
    NCOLS = 5
    rec_num    = d.def_dim('rec_num',    NROWS)
    bin_number = d.def_dim('bin_number', NCOLS)
    # Create a netCDF record variable named `obs_table', of type
    # integer. Note that the unlimited dimension must come first
    # (must be the slowest varying index).
    obs_table = d.def_var('obs_table', NC.INT, (rec_num, bin_number))
    # Specify valid data range by setting a variable attribute.
    obs_table.valid_range = (-40, 200)
    # Switch to data mode.
    # Initialize variable with a few records
    recs = ((1,3,-4,5,10),
            (0,10,8,7,4),
            (-1,4,5,9,13))
    obs_table[0:len(recs)] = recs
    
    print "\nstep 1, obs_table"
    print obs_table[:]
    print "should be"
    print array(recs)
    
    # Change value at row 1 and col 3
    #obs_table.put_1((1,3),45)
    v = 45
    obs_table[1,3] = v      
    print "\nstep 2, obs_table with element [1,3] modified"
    print obs_table[:]
    print "element [1,3] should be"
    print v
    
    # Get the current number of records in the table,
    # and append 2 new records to the table.
    nrecs = len(rec_num)    # equiv to rec_num.inq_len()
    newrecs = ((12,-45,13, 0, 8),
               (0,56,-10,16,13))
    #obs_table.put(newrecs,               # data
    #         (nrecs,0),             # start
    #         (len(newrecs),NCOLS))  # count
    obs_table[nrecs:nrecs+len(newrecs)] = newrecs
    print "\nstep 3, obs_table with 2 rows appended"
    print obs_table[:]
    print "last 2 rows should be"
    print array(newrecs)

    # Get values of column 2. col_2 is a Numeric array.
    nrecs = len(rec_num)
    col_2 = obs_table[:,2]
    print "\nstep 4, col 2 of obs_table"
    print array(col_2)[:,newaxis]
    print "column 2 values should be"
    print array([-4, 8, 5, 13, -10])[:,newaxis]

    # Bump column values by 5 and write column back to the netCDF
    # variable. We take advantage of Numeric capacity to operate
    # directly on arrays.
    #obs_table.put(col_2+5, start=(0,2), count=(nrecs,1))
    obs_table[:,2] = col_2+5
    print "\nstep 5, column 2 values incremented by 5"
    print obs_table[:]
    print "column 2 values should be"
    print array([1, 13, 10, 18, -5])[:,newaxis]

    # Create a second variable named `obs_table_copy', this time of
    # type double, and initialize it with the first 3 records of
    # variable `obs_table'.
    # Create 2nd variable and copy to it attribute `valid_range' of
    # first variable.
    obs_table_copy = d.def_var('obs_table_copy', NC.DOUBLE,
                               (rec_num, bin_number))
    obs_table.attr('valid_range').copy(obs_table_copy)
    # Since obs_table_copy was defined using the same dimensions as 
    # obs_table (rec_num, bin_number) and the length of rec_num is
    # currently > 3, obs_table_copy will have uninitialized rows at
    # its end (since we transfer only first 3 records from obs_table).
    # Those rows will be filled with the default fill value. This
    # default does not suit us, so we redefine it to a more convenient
    # one.
    obs_table_copy._FillValue = -9999.0
    # Transfer first 3 records from obs_table to obs_table_copy, first
    # dividing values by 10.
    obs_table_copy[:3] = obs_table[:3]/10.0
    print "\nstep 6, obs_table_copy"
    print array2string(obs_table_copy[:], precision=3,
                       suppress_small=1)
    print "First 3 rows should be equal to those of 'obs_table'"
    print "divided by 10. Last 2 rows should be set to _FillValue",\
          obs_table_copy._FillValue

    d.close()                     # Close dataset
except CDFError, msg:
    print "CDF error occured: ",msg
