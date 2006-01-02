/*
 * $Id: pycdfext.i,v 1.1 2006-01-02 18:51:15 gosselin_a Exp $
 * $Name: not supported by cvs2svn $
 * $Log: not supported by cvs2svn $
 *
 * SWIG directives for generating the pycdfext module for use with Numeric.
 */

%module pycdfext


%include "typemaps.i"
%include "cstring.i"
%include "carrays.i"
%include "cpointer.i"

/*
 * Define new typemaps to deal with output args of non standard type:
 *   size_t   (4 bits on Intel, 8 on Alpha)
 *
 * The definitions are adapted from the `typemaps.i' file.
 */

%typemap(in,numinputs=0) size_t *OUTPUT($*1_ltype temp), size_t &OUTPUT($*1_ltype temp) "$1 = &temp;";
%typemap(argout,fragment="t_output_helper") size_t *OUTPUT, size_t &OUTPUT {
   PyObject *o = PyInt_FromLong((long) (*$1));
   $result = t_output_helper($result,o);
   }

/*
 * For passing arrays to C routines.
 */

%array_class(unsigned char, array_byte);
%array_class(short, array_int16);
%array_class(unsigned short, array_uint16);
%array_class(int, array_int);
%array_class(float, array_float);
%array_class(double, array_double);
%array_class(size_t, array_size_t);


/* ********************************************************************* */
/* netCDF type codes */
/* ***************** */

#define NC_NOERR        0

#define NC_NOWRITE      0       /* default is read only */
#define NC_WRITE        0x1     /* read & write */
#define NC_CLOBBER      0
#define NC_NOCLOBBER    0x4     /* Don't destroy existing file on create */
#define NC_64BIT_OFFSET 0x0200  /* Use large (64-bit) file offsets */
#define NC_FILL         0       /* argument to ncsetfill to clear NC_NOFILL */
#define NC_NOFILL       0x0100  /* Don't fill data section an records */
#define NC_LOCK         0x0400  /* Use locking if available */
#define NC_SHARE        0x0800  /* Share updates, limit cacheing */

#define NC_NAT          0       /* Not a Type */
#define NC_BYTE         1       /* Signed 1 byte integer */
#define NC_CHAR         2       /* ISO/ASCII character */
#define NC_SHORT        3       /* signed 2 byte integer */
#define NC_INT          4       /* signed 4 byte integer */
#define NC_FLOAT        5       /* single precision floating point number */
#define NC_DOUBLE       6       /* double precision floating point number */

#define NC_GLOBAL      -1       /* global attribute id */
#define NC_UNLIMITED    0       /* unlimited dimension */

                             /* Simpler names for Python user */
#define NOERR        0

#define NOWRITE      0       /* default is read only */
#define WRITE        0x1     /* read & write */
#define CLOBBER      0
#define NOCLOBBER    0x4     /* Don't destroy existing file on create */
#define BIT64_OFFSET  0x0200  /* Use large (64-bit) file offsets */
#define FILL         0       /* argument to ncsetfill to clear NC_NOFILL */
#define NOFILL       0x0100  /* Don't fill data section an records */
#define LOCK         0x0400  /* Use locking if available */
#define SHARE        0x0800  /* Share updates, limit cacheing */

#define NAT          0       /* Not a Type */
#define BYTE         1       /* Signed 1 byte integer */
#define CHAR         2       /* ISO/ASCII character */
#define SHORT        3       /* signed 2 byte integer */
#define INT          4       /* signed 4 byte integer */
#define FLOAT        5       /* single precision floating point number */
#define DOUBLE       6       /* double precision floating point number */

#define GLOBAL      -1       /* global attribute id */
#define UNLIMITED    0       /* unlimited dimension */


/*
 * Interface to Numeric, which is used to read and write
 * array data.
 */

%init %{
  /* Init Numeric. Mandatory, otherwise the extension will bomb. */
  import_array();
  %}

%{

#include <stddef.h>     /* ptrdiff_t */
#include "Numeric/arrayobject.h"

#define NC_BYTE         1       /* Signed 1 byte integer */
#define NC_CHAR         2       /* ISO/ASCII character */
#define NC_SHORT        3       /* signed 2 byte integer */
#define NC_INT          4       /* signed 4 byte integer */
#define NC_FLOAT        5       /* single precision floating point number */
#define NC_DOUBLE       6       /* double precision floating point number */


extern       int   nc_get_vars_text(int ncid, int varid, 
                                    const size_t *start,
                                    const size_t *count, 
                                    const ptrdiff_t *stride,
                                    void *value);
extern       int   nc_get_vars_schar(int ncid, int varid, 
                                     const size_t *start,
                                     const size_t *count, 
                                     const ptrdiff_t *stride,
                                     void *value);
extern       int   nc_get_vars_uchar(int ncid, int varid, 
                                     const size_t *start,
                                     const size_t *count, 
                                     const ptrdiff_t *stride,
                                     void *value);
extern       int   nc_get_vars_int(int ncid, int varid, 
                                   const size_t *start,
                                   const size_t *count, 
                                   const ptrdiff_t *stride,
                                   void *value);
extern       int   nc_get_vars_short(int ncid, int varid, 
                                     const size_t *start,
                                     const size_t *count, 
                                     const ptrdiff_t *stride,
                                     void *value);
extern       int   nc_get_vars_float(int ncid, int varid, 
                                     const size_t *start,
                                     const size_t *count, 
                                     const ptrdiff_t *stride,
                                     void *value);
extern       int   nc_get_vars_double(int ncid, int varid, 
                                      const size_t *start,
                                      const size_t *count, 
                                      const ptrdiff_t *stride,
                                      void *value);

extern       int   nc_get_varm_text(int ncid, int varid, 
                                    const size_t *start,
                                    const size_t *count, 
                                    const ptrdiff_t *stride,
                                    const ptrdiff_t *map, 
                                    void *value);
extern       int   nc_get_varm_schar(int ncid, int varid, 
                                     const size_t *start,
                                     const size_t *count, 
                                     const ptrdiff_t *stride,
                                     const ptrdiff_t *map, 
                                     void *value);
extern       int   nc_get_varm_uchar(int ncid, int varid, 
                                     const size_t *start,
                                     const size_t *count, 
                                     const ptrdiff_t *stride,
                                     const ptrdiff_t *map, 
                                     void *value);
extern       int   nc_get_varm_int(int ncid, int varid, 
                                   const size_t *start,
                                   const size_t *count, 
                                   const ptrdiff_t *stride,
                                   const ptrdiff_t *map, 
                                   void *value);
extern       int   nc_get_varm_short(int ncid, int varid, 
                                     const size_t *start,
                                     const size_t *count, 
                                     const ptrdiff_t *stride,
                                     const ptrdiff_t *map, 
                                     void *value);
extern       int   nc_get_varm_float(int ncid, int varid, 
                                     const size_t *start,
                                     const size_t *count, 
                                     const ptrdiff_t *stride,
                                     const ptrdiff_t *map, 
                                     void *value);
extern       int   nc_get_varm_double(int ncid, int varid, 
                                      const size_t *start,
                                      const size_t *count, 
                                      const ptrdiff_t *stride,
                                      const ptrdiff_t *map, 
                                      void *value);

extern       int   nc_put_vars_text(int ncid, int varid, 
                                    const size_t *start,
                                    const size_t *count, 
                                    const ptrdiff_t *stride,
                                    const void *value);
extern       int   nc_put_vars_schar(int ncid, int varid, 
                                     const size_t *start,
                                     const size_t *count, 
                                     const ptrdiff_t *stride,
                                     const void *value);
extern       int   nc_put_vars_uchar(int ncid, int varid, 
                                     const size_t *start,
                                     const size_t *count, 
                                     const ptrdiff_t *stride,
                                     const void *value);
extern       int   nc_put_vars_int(int ncid, int varid, 
                                   const size_t *start,
                                   const size_t *count, 
                                   const ptrdiff_t *stride,
                                   const void *value);
extern       int   nc_put_vars_short(int ncid, int varid, 
                                     const size_t *start,
                                     const size_t *count, 
                                     const ptrdiff_t *stride,
                                     const void *value);
extern       int   nc_put_vars_float(int ncid, int varid, 
                                     const size_t *start,
                                     const size_t *count, 
                                     const ptrdiff_t *stride,
                                     const void *value);
extern       int   nc_put_vars_double(int ncid, int varid, 
                                      const size_t *start,
                                      const size_t *count, 
                                      const ptrdiff_t *stride,
                                      const void *value);

extern       int   nc_put_varm_text(int ncid, int varid, 
                                    const size_t *start,
                                    const size_t *count, 
                                    const ptrdiff_t *stride,
                                    const ptrdiff_t *map, 
                                    const void *value);
extern       int   nc_put_varm_schar(int ncid, int varid, 
                                     const size_t *start,
                                     const size_t *count, 
                                     const ptrdiff_t *stride,
                                     const ptrdiff_t *map, 
                                     const void *value);
extern       int   nc_put_varm_uchar(int ncid, int varid, 
                                     const size_t *start,
                                     const size_t *count, 
                                     const ptrdiff_t *stride,
                                     const ptrdiff_t *map, 
                                     const void *value);
extern       int   nc_put_varm_int(int ncid, int varid, 
                                   const size_t *start,
                                   const size_t *count, 
                                   const ptrdiff_t *stride,
                                   const ptrdiff_t *map, 
                                   const void *value);
extern       int   nc_put_varm_short(int ncid, int varid, 
                                     const size_t *start,
                                     const size_t *count, 
                                     const ptrdiff_t *stride,
                                     const ptrdiff_t *map, 
                                     const void *value);
extern       int   nc_put_varm_float(int ncid, int varid, 
                                     const size_t *start,
                                     const size_t *count, 
                                     const ptrdiff_t *stride,
                                     const ptrdiff_t *map, 
                                     const void *value);
extern       int   nc_put_varm_double(int ncid, int varid, 
                                      const size_t *start,
                                      const size_t *count, 
                                      const ptrdiff_t *stride,
                                      const ptrdiff_t *map, 
                                      const void *value);

static int CDFtoNumericType(int cdf, int ubyte)    {

    int num;

    switch (cdf)   {
        case NC_FLOAT:   num = PyArray_FLOAT; break;
        case NC_DOUBLE:  num = PyArray_DOUBLE; break;
        case NC_BYTE:    num = ubyte ? PyArray_UBYTE : PyArray_SBYTE; break;
        case NC_SHORT:   num = PyArray_SHORT; break;
        case NC_INT:     num = PyArray_INT; break;
        case NC_CHAR:    num = PyArray_CHAR; break;
        default:
            num = -1;
            break;
        }
    return num;
    }

static PyObject * _nc_get_var_0(int ncid, int varid, int data_type,
                                PyObject *start,
                                PyObject *edges, 
                                PyObject *stride,
                                PyObject *map,
                                      int ubyte)    {

    /*
     * A value of -1 in 'edges' indicates that the dimension 
     * is indexed, not sliced. This dimension should be removed from
     * the output array.
     */

    PyArrayObject *array;
    PyObject *o;
    int n, rank, outRank, num_type, status, useMap;
    int (*fct) (int ncid, int varid, 
                const size_t *start, 
                const size_t *count, 
                const ptrdiff_t *stride,
                void *val);
    int (*fct1)(int ncid, int varid, 
                const size_t *start, 
                const size_t *count, 
                const ptrdiff_t *stride,
                const ptrdiff_t *map, 
                void *val);
        /*
         * Allocate those arrays on the stack for simplicity.
         * 80 dimensions should be more than enough!
         */
    size_t startArr[80], edgesArr[80];
    ptrdiff_t strideArr[80], mapArr[80];
    int dims[80];
    float f32;
    double f64;
    int   i32;

        /*
         * Load arrays. Caller has guaranteed that all 4 arrays have the
         * same dimensions.
         */
    rank = PyObject_Length(start);
    outRank = 0;
    dims[0] = 0;
    useMap = 0;
    for (n = 0; n < rank; n++)    {
        o = PySequence_GetItem(start, n);
        if (!PyInt_Check(o))    {
            PyErr_SetString(PyExc_ValueError, "arg start contains a non-integer");
            return NULL;
            }
        startArr[n] = PyInt_AsLong(o);

        o = PySequence_GetItem(edges, n);
        if (!PyInt_Check(o))    {
            PyErr_SetString(PyExc_ValueError, "arg edges contains a non-integer");
            return NULL;
            }
            /*
             * Do as Numeric when a dimension is indexed (indicated by
             * a count of -1).
             * This dimension is then dropped from the output array,
             * producing a subarray. For ex., if m is a 3x3 array, m[0]
             * is a 3 element vector holding the first row of `m'.
             * Variables `outRank' and `dims' store the resulting array
             * rank and dimension lengths, resp.
             */
        edgesArr[n] = PyInt_AsLong(o);
        if (edgesArr[n] != -1)    {
            dims[outRank++] = abs(edgesArr[n]);
            }
        else
            edgesArr[n] = 1;

        o = PySequence_GetItem(stride, n);
        if (!PyInt_Check(o))    {
            PyErr_SetString(PyExc_ValueError, "arg stride contains a non-integer");
            return NULL;
            }
        strideArr[n] = PyInt_AsLong(o);

        o = PySequence_GetItem(map, n);
        if (!PyInt_Check(o))    {
            PyErr_SetString(PyExc_ValueError, "arg map contains a non-integer");
            return NULL;
            }
        if ((mapArr[n] = PyInt_AsLong(o)) != 0)
            useMap = 1;
        }

        /*
         * Create output Numeric array.
         */
    if ((num_type = CDFtoNumericType(data_type, ubyte)) < 0)    {
        PyErr_SetString(PyExc_ValueError, 
                        "data type not compatible with Numeric");
        return NULL;
        }
    if ((array = (PyArrayObject *) 
                 PyArray_FromDims(outRank, dims, num_type)) == NULL)
        return NULL;
        /*
         * Load it from the netCDF variable.
         */
    if (useMap)    {
        switch (num_type)    {
            case PyArray_FLOAT:    fct1 = nc_get_varm_float; break;
            case PyArray_DOUBLE:   fct1 = nc_get_varm_double; break;
            case PyArray_SBYTE:    fct1 = nc_get_varm_schar; break;
            case PyArray_UBYTE:    fct1 = nc_get_varm_uchar; break;
            case PyArray_SHORT:    fct1 = nc_get_varm_short; break;
            case PyArray_INT:      fct1 = nc_get_varm_int; break;
            case PyArray_CHAR:     fct1 = nc_get_varm_text; break;
            }
        status = fct1(ncid, varid, startArr, edgesArr, strideArr, 
                      mapArr, array -> data);
        }
    else    {
        switch (num_type)    {
            case PyArray_FLOAT:    fct = nc_get_vars_float; break;
            case PyArray_DOUBLE:   fct = nc_get_vars_double; break;
            case PyArray_SBYTE:    fct = nc_get_vars_schar; break;
            case PyArray_UBYTE:    fct = nc_get_vars_uchar; break;
            case PyArray_SHORT:    fct = nc_get_vars_short; break;
            case PyArray_INT:      fct = nc_get_vars_int; break;
            case PyArray_CHAR:     fct = nc_get_vars_text; break;
            }
        status = fct(ncid, varid, startArr, edgesArr, strideArr, 
                     array -> data);
        }
    if (status < 0)    {
        char msg[80];
        sprintf (msg, "%d", status);
        PyErr_SetString(PyExc_ValueError, msg);
        Py_DECREF(array);  /* Free array */
        return NULL;
        }
        /*
         * Return array.
         * PyArray_Return() does not seem to work ok. 
         * Deal ourselves with the 0 rank case.
         */
    /* return PyArray_Return(array); */
    if (outRank > 0)
        return (PyObject *) array;
    switch (num_type)    {
        case PyArray_FLOAT:
            f32 = *(float *) array->data;
            o = PyFloat_FromDouble((double) f32);
            break;
        case PyArray_DOUBLE:
            f64 = *(double *) array->data;
            o = PyFloat_FromDouble(f64);
            break;
        case PyArray_CHAR:
        case PyArray_SBYTE:
            i32 = *(char *) array->data;
            o = PyInt_FromLong((long) i32);
            break;
        case PyArray_UBYTE:
            i32 = *(unsigned char *) array->data;
            o = PyInt_FromLong((long) i32);
            break;
        case PyArray_SHORT:
            i32 = *(short *) array->data;
            o = PyInt_FromLong((long) i32);
            break;
        case PyArray_INT:
            i32 = *(int *) array->data;
            o = PyInt_FromLong((long) i32);
            break;
        }
    Py_DECREF(array);  /* Free array */
    return o;
    }

static PyObject * _nc_put_var_0(int ncid, int varid, int data_type,
                                PyObject *data,
                                PyObject *start,
                                PyObject *edges, 
                                PyObject *stride,
                                PyObject *map,
                                      int ubyte)    {

    PyArrayObject *array;
    PyObject *o;
    int n, rank, num_type, status, useMap;
    int (*fct) (int ncid, int varid,
                const size_t *start, 
                const size_t *count, 
                const ptrdiff_t *stride,
                const void *val);
    int (*fct1)(int ncid, int varid,
                const size_t *start, 
                const size_t *count, 
                const ptrdiff_t *stride,
                const ptrdiff_t *map, 
                const void *val);

        /*
         * Allocate those arrays on the stack for simplicity.
         * 80 dimensions should be more than enough!
         */
    size_t startArr[80], edgesArr[80];
    ptrdiff_t strideArr[80], mapArr[80];

        /*
         * Load arrays. Caller has guaranteeded that all 4 arrays have the
         * same dimensions.
         */
    rank = PyObject_Length(start);
    useMap = 0;
    for (n = 0; n < rank; n++)    {
        o = PySequence_GetItem(start, n);
        if (!PyInt_Check(o))    {
            PyErr_SetString(PyExc_ValueError, "arg start contains a non-integer");
            return NULL;
            }
        startArr[n] = PyInt_AsLong(o);

        o = PySequence_GetItem(edges, n);
        if (!PyInt_Check(o))    {
            PyErr_SetString(PyExc_ValueError, "arg edges contains a non-integer");
            return NULL;
            }
            /*
             * A value of -1 indicates that an index, not a slice, was applied
             * to the dimension. This difference is significant only for a
             * `get' operation. So ignore it here.
             */
        edgesArr[n] = abs(PyInt_AsLong(o));

        o = PySequence_GetItem(stride, n);
        if (!PyInt_Check(o))    {
            PyErr_SetString(PyExc_ValueError, "arg stride contains a non-integer");
            return NULL;
            }
        strideArr[n] = PyInt_AsLong(o);

        o = PySequence_GetItem(map, n);
        if (!PyInt_Check(o))    {
            PyErr_SetString(PyExc_ValueError, "arg map contains a non-integer");
            return NULL;
            }
        if ((mapArr[n] = PyInt_AsLong(o)) != 0)
            useMap = 1;
        }

        /*
         * Convert input to a contiguous Numeric array (no penalty if
         * input already in this format). Do not do that for char type,
         * `PyArray_ContiguousFromObject()' does not seem to work with that
         * type. Caller must convert characters to ascii codes before.
         */
    if ((num_type = CDFtoNumericType(data_type, ubyte)) < 0)    {
        PyErr_SetString(PyExc_ValueError, "data_type not compatible with Numeric");
        return NULL;
        }
    if ((array = (PyArrayObject *) 
                 PyArray_ContiguousFromObject(data, num_type, 
                                              rank - 1, rank)) == NULL)
        return NULL;
        /*
         * Store in the netCDF variable.
         */
    if (useMap)    {
        switch (num_type)    {
            case PyArray_FLOAT:    fct1 = nc_put_varm_float; break;
            case PyArray_DOUBLE:   fct1 = nc_put_varm_double; break;
            case PyArray_UBYTE:    fct1 = nc_put_varm_uchar; break;
            case PyArray_SBYTE:    fct1 = nc_put_varm_schar; break;
            case PyArray_SHORT:    fct1 = nc_put_varm_short; break;
            case PyArray_INT:      fct1 = nc_put_varm_int; break;
            case PyArray_CHAR:     fct1 = nc_put_varm_text; break;
            }
        status = fct1(ncid, varid, startArr, edgesArr, strideArr, 
                      mapArr, array -> data);
        }
    else    {
        switch (num_type)    {
            case PyArray_FLOAT:    fct = nc_put_vars_float; break;
            case PyArray_DOUBLE:   fct = nc_put_vars_double; break;
            case PyArray_UBYTE:    fct = nc_put_vars_uchar; break;
            case PyArray_SBYTE:    fct = nc_put_vars_schar; break;
            case PyArray_SHORT:    fct = nc_put_vars_short; break;
            case PyArray_INT:      fct = nc_put_vars_int; break;
            case PyArray_CHAR:     fct = nc_put_vars_text; break;
            }
        status = fct(ncid, varid, startArr, edgesArr, strideArr, array -> data);
        }
    Py_DECREF(array);      /* Free array */
    if (status < 0)    {
        char msg[80];
        sprintf (msg, "%d", status);
        PyErr_SetString(PyExc_ValueError, msg);
        return NULL;
        }
        /*
         * Return None.
         */
    Py_INCREF(Py_None); 
    return Py_None;
    }

%}


/*
 * Following two routines are defined above, and interface to the `nc_get_var...' and
 * `nc_put_var...' series.
 */

extern PyObject * _nc_get_var_0(int ncid, int varid, int data_type,
                                PyObject *start,
                                PyObject *edges,
                                PyObject *stride,
                                PyObject *map,
                                int      ubyte);

extern PyObject * _nc_put_var_0(int ncid, int varid, int data_type,
                                PyObject *data,
                                PyObject *start,
                                PyObject *edges,
                                PyObject *stride,
                                PyObject *map,
                                int      ubyte);

/*
 * Routines defined in the netcdf library.
 */

extern const char *nc_inq_libvers(void);
extern const char *nc_strerror(int ncerr);
extern       int   nc_create(const char *path, int cmode, int *OUTPUT);
extern       int   nc_open(const char *path, int omode, int *OUTPUT);
extern       int   nc_close(int ncid);
extern       int   nc_redef(int ncid);
extern       int   nc_enddef(int ncid);

extern       int   nc_inq(int ncid, int *OUTPUT, int *OUTPUT,
                          int *OUTPUT, int *OUTPUT);
extern       int   nc_inq_ndims(int ncid, int *OUTPUT);
extern       int   nc_inq_nvars(int ncid, int *OUTPUT);
extern       int   nc_inq_natts(int ncid, int *OUTPUT);
extern       int   nc_inq_unlimdim(int ncid, int *OUTPUT);

extern       int   nc_sync(int ncid);
extern       int   nc_abort(int ncid);

extern       int   nc_set_fill(int ncid, int fillmode, int *OUTPUT);

extern       int   nc_def_dim(int ncid, const char *name, size_t len, 
                              int *OUTPUT);
extern       int   nc_inq_dimid(int ncid, const char *name, 
                                int *OUTPUT);
%cstring_bounded_output(char *name, 256);
extern       int   nc_inq_dim(int ncid, int dimid, char *name, size_t *OUTPUT);
extern       int   nc_inq_dimname(int ncid, int dimid, char *name);
extern       int   nc_inq_dimlen(int ncid, int dimid, size_t *OUTPUT);
%clear char *name;

extern       int   nc_rename_dim(int ncid, int dimid, const char *name);

extern       int   nc_def_var(int ncid, const char *name, int xtype,
                              int ndims, const int *dimids, int *OUTPUT);
extern       int   nc_inq_varid(int ncid, const char *name, int *OUTPUT);

%cstring_bounded_output(char *name, 256);
extern       int   nc_inq_var(int ncid, int varid, char *name, int *OUTPUT,
                              int *OUTPUT, int *dimids, int *OUTPUT);
extern       int   nc_inq_varname(int ncid, int varid, char *name);
extern       int   nc_inq_vartype(int ncid, int varid, int *OUTPUT);
extern       int   nc_inq_varndims(int ncid, int varid, int *OUTPUT);
extern       int   nc_inq_vardimid(int ncid, int varid, int *dimids);
extern       int   nc_inq_varnatts(int ncid, int varid, int *OUTPUT);
%clear char *name;

extern       int   nc_put_var1_text(int ncid, int varid, const size_t *index,
                                    const char *tp);
extern       int   nc_put_var1_uchar(int ncid, int varid, const size_t *index,
                                     const unsigned char *bytes);
extern       int   nc_put_var1_int(int ncid, int varid, const size_t *index,
                                    int *INPUT);
extern       int   nc_put_var1_double(int ncid, int varid, const size_t *index,
                                    double *INPUT);

%cstring_bounded_output(char *value, 1);
extern       int   nc_get_var1_text(int ncid, int varid, const size_t *index,
                                    char *value);
%clear char *value;
extern       int   nc_get_var1_uchar(int ncid, int varid, const size_t *index,
                                     unsigned char *bytes);
extern       int   nc_get_var1_int(int ncid, int varid, const size_t *index,
                                    int *OUTPUT);
extern       int   nc_get_var1_double(int ncid, int varid, const size_t *index,
                                    double *OUTPUT);

extern       int   nc_rename_var(int ncid, int varid, const char *name);

extern       int   nc_put_att_text(int ncid, int varid, const char *name, 
                                   size_t len, const char *tp);
extern       int   nc_put_att_uchar(int ncid, int varid, const char *name, 
                                    int xtype, size_t len, const unsigned char *up);
extern       int   nc_put_att_int(int ncid, int varid, const char *name, 
                                  int xtype, size_t len, const int *lp);
extern       int   nc_put_att_float(int ncid, int varid, const char *name, 
                                    int xtype, size_t len, const float *dp);
extern       int   nc_put_att_double(int ncid, int varid, const char *name, 
                                     int xtype, size_t len, const double *dp);

extern       int   nc_inq_att(int ncid, int varid, const char *name,
                              int *OUTPUT, size_t *OUTPUT);
extern       int   nc_inq_atttype(int ncid, int varid, const char *name,
                                  int *OUTPUT);
extern       int   nc_inq_attlen(int ncid, int varid, const char *name,
                                 int *OUTPUT);
%cstring_bounded_output(char *name, 80);
extern       int   nc_inq_attname(int ncid, int varid, int attnum,
                                  char *name);
%clear char *name;
extern       int   nc_inq_attid(int ncid, int varid, const char *name,
                                int *OUTPUT);
%cstring_bounded_output(char *value, 256);
extern       int   nc_get_att_text(int ncid, int varid, const char *name,
                                   char *value);
%clear char *value;

extern       int   nc_get_att_uchar(int ncid, int varid, const char *name, 
                                    unsigned char *value);
extern       int   nc_get_att_int(int ncid, int varid, const char *name, 
                                  int *value);
extern       int   nc_get_att_double(int ncid, int varid, const char *name, 
                                     double *value);

extern       int   nc_copy_att(int ncid_in, int varid_in, const char *name,
                               int ncid_out, int varid_out);

extern       int   nc_del_att(int ncid, int varid, const char *name);

extern       int   nc_rename_att(int ncid, int varid, const char *name,
                                 const char *newname);
