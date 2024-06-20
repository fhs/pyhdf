/*
 * $Id: hdfext.i,v 1.7 2008-06-30 02:41:44 gosselin_a Exp $
 * $Log: not supported by cvs2svn $
 * Revision 1.6  2005/07/14 01:36:41  gosselin_a
 * pyhdf-0.7-3
 * Ported to HDF4.2r1.
 * Support for SZIP compression on SDS datasets.
 * All classes are now 'new-style' classes, deriving from 'object'.
 * Update documentation.
 *
 * Revision 1.5  2004/11/02 21:33:39  gosselin
 * *** empty log message ***
 *
 * Revision 1.3  2004/08/02 15:36:04  gosselin
 * pyhdf-0.7-1
 *
 * Revision 1.2  2004/08/02 15:22:59  gosselin
 * pyhdf-0.6-1
 *
 * Revision 1.1  2004/08/02 15:00:34  gosselin
 * Initial revision
 *
 */

%module hdfext


%include "typemaps.i"
%include "cstring.i"
%include "carrays.i"

/* ********************************************************************* */
/* HDF type info codes */
/* ******************* */

#define DFNT_NONE        0  /* indicates that number type not set */
#define DFNT_QUERY       0  /* use this code to find the current type */
#define DFNT_VERSION     1  /* current version of NT info */

#define DFNT_FLOAT32     5
#define DFNT_FLOAT       5  /* For backward compat; don't use */
#define DFNT_FLOAT64     6
#define DFNT_DOUBLE      6  /* For backward compat; don't use */
#define DFNT_FLOAT128    7  /* No current plans for support */

#define DFNT_INT8       20
#define DFNT_UINT8      21

#define DFNT_INT16      22
#define DFNT_UINT16     23
#define DFNT_INT32      24
#define DFNT_UINT32     25
#define DFNT_INT64      26
#define DFNT_UINT64     27
#define DFNT_INT128     28  /* No current plans for support */
#define DFNT_UINT128    30  /* No current plans for support */

#define DFNT_UCHAR8      3  /* 3 chosen for backward compatibility */
#define DFNT_UCHAR       3  /* uchar=uchar8 for backward compatibility */
#define DFNT_CHAR8       4  /* 4 chosen for backward compatibility */
#define DFNT_CHAR        4  /* uchar=uchar8 for backward compatibility */
#define DFNT_CHAR16     42  /* No current plans for support */
#define DFNT_UCHAR16    43  /* No current plans for support */

#define SD_UNLIMITED     0
#define SD_FILL          0
#define SD_NOFILL      256

#define CHAR_BUFFER_SIZE 4096
#define ATTRIB_BUFFER_SIZE 128

/* ********************************************************************* */
/* internal file access codes */

#define DFACC_READ 1
#define DFACC_WRITE 2
#define DFACC_CREATE 4
#define DFACC_ALL 7

#define DFACC_RDONLY 1
#define DFACC_RDWR 3
#define DFACC_CLOBBER 4

/* New file access codes (for Hstartaccess only, currently) */
#define DFACC_BUFFER 8  /* buffer the access to this AID */
#define DFACC_APPENDABLE 0x10 /* make this AID appendable */
#define DFACC_CURRENT 0x20 /* start looking for a tag/ref from the current */
                           /* location in the DD list (useful for continued */
                           /* searching ala findfirst/findnext) */

/* External Element File access mode */
/* #define DFACC_CREATE 4       is for creating new external element file */
#define DFACC_OLD       1       /* for accessing existing ext. element file */

/* Compression codes */
#define COMP_CODE_NONE    0
#define COMP_CODE_RLE     1
#define COMP_CODE_NBIT    2
#define COMP_CODE_SKPHUFF 3
#define COMP_CODE_DEFLATE 4
#define COMP_CODE_SZIP    5

/* Tags */
#define  DFTAG_NDG  720
#define  DFTAG_VH  1962
#define  DFTAG_VG  1965

/* limits */
%constant int H4_MAX_VAR_DIMS = H4_MAX_VAR_DIMS;

%array_class(unsigned char, array_byte);
%array_class(signed char, array_int8);
%array_class(short, array_int16);
%array_class(unsigned short, array_uint16);
%array_class(int, array_int32);
%array_class(unsigned int, array_uint32);
%array_class(float, array_float32);
%array_class(double, array_float64);
%array_functions(void *, array_voidp);

typedef int           int32;
typedef int           intn;
typedef int          uint32;
typedef short         int16;
typedef unsigned char uint8;

%{
#include "hdf.h"
#include "mfhdf.h"
%}

/*
 ***************
 * Basic HDF API
 ***************
 */

/*
 * Opening and closing HDF file.
 */

extern int32 Hopen(const char *filename,
                   intn        access_mode,
                   int         num_dds_blocks);
extern intn  Hclose(int32      file_id);

/*
 * Library version.
 */

%cstring_bounded_output(char *string, CHAR_BUFFER_SIZE);
extern intn Hgetlibversion(uint32 *OUTPUT,     /* major_v */
                           uint32 *OUTPUT,     /* minor_v */
                           uint32 *OUTPUT,     /* release */
                           char   *string);
extern intn Hgetfileversion(int32  file_id,
                            uint32 *OUTPUT,    /* major_v */
                            uint32 *OUTPUT,     /* minor_v */
                            uint32 *OUTPUT,     /* release */
                            char   *string);
%clear char *string;

/*
 * Inquiry.
 */

extern intn Hishdf(const char *filename);

/*
 ***********
 * Error API
 ***********
 */

%{
#include <stdio.h>
void _HEprint(void)   {

    HEprint(stderr,0);
    }
%}

extern int32 HEvalue(int32 error_stack_offset);
extern const char *HEstring(int32 error_code);
extern void _HEprint(void);


/*
 ********
 * SD API
 ********
 */

/*
 * Interface to numpy, which is used to read and write
 * SD array data.
 */

%init %{
  /* Init numpy. Mandatory, otherwise the extension will bomb. */
  import_array();
  %}


%{
#include "hdf.h"      /* declares int32, float32, etc */

#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
#include "numpy/ndarraytypes.h"
#include "numpy/ndarrayobject.h"

#define DFNT_FLOAT32     5
#define DFNT_FLOAT       5  /* For backward compat; don't use */
#define DFNT_FLOAT64     6
#define DFNT_DOUBLE      6  /* For backward compat; don't use */
#define DFNT_FLOAT128    7  /* No current plans for support */

#define DFNT_INT8       20
#define DFNT_UINT8      21

#define DFNT_INT16      22
#define DFNT_UINT16     23
#define DFNT_INT32      24
#define DFNT_UINT32     25
#define DFNT_INT64      26
#define DFNT_UINT64     27

#define DFNT_UCHAR8      3  /* 3 chosen for backward compatibility */
#define DFNT_UCHAR       3  /* uchar=uchar8 for backward compatibility */
#define DFNT_CHAR8       4  /* 4 chosen for backward compatibility */
#define DFNT_CHAR        4  /* uchar=uchar8 for backward compatibility */

static int HDFtoNumericType(int hdf)    {

    int num;

    switch (hdf)   {
        case DFNT_FLOAT32: num = NPY_FLOAT; break;
        case DFNT_FLOAT64: num = NPY_DOUBLE; break;
        case DFNT_INT8   : num = NPY_BYTE; break;
        case DFNT_UINT8  : num = NPY_UBYTE; break;
        case DFNT_INT16  : num = NPY_SHORT; break;
#ifndef NOUINT
        case DFNT_UINT16 : num = NPY_USHORT; break;
#endif
        case DFNT_INT32  : num = NPY_INT; break;
#ifndef NOUINT
        case DFNT_UINT32 : num = NPY_UINT; break;
#endif
        case DFNT_CHAR8  : num = NPY_STRING; break;
        case DFNT_UCHAR8 : num = NPY_UBYTE; break;
        default:
            num = -1;
            break;
        }
    return num;
    }

static PyObject * _SDreaddata_0(int32 sds_id, int32 data_type,
                                PyObject *start,
                                PyObject *edges,
                                PyObject *stride)    {

    /*
     * A value of -1 in 'edges' indicates that the dimension
     * is indexed, not sliced. This dimension should be removed from
     * the output array.
     */

    PyArrayObject *array;
    PyObject *o;
    int n, rank, outRank, num_type, status;
        /*
         * Allocate those arrays on the stack for simplicity.
         * 80 dimensions should be more than enough!
         */
    int startArr[80], strideArr[80], edgesArr[80];
    npy_intp dims[80];
    float f32;
    double f64;
    int   i32;

        /*
         * Load arrays. Caller has guaranteeded that all 3 arrays have the
         * same dimensions.
         */
    rank = PyObject_Length(start);
    outRank = 0;
    dims[0] = 0;
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
             * Do as numpy when a dimension is indexed (indicated by
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
        }

        /*
         * Create output numpy array. We provide 1 for the itemsize argument to
         * PyArray_New to handle to case when num_type is NPY_STRING. All other
         * num_type possibilities are fixed-size types, so itemsize is ignored.
         */
    if ((num_type = HDFtoNumericType(data_type)) < 0)    {
        PyErr_SetString(PyExc_ValueError, "data_type not compatible with numpy");
        return NULL;
        }
    array = (PyArrayObject *)PyArray_New(&PyArray_Type, outRank, dims, num_type,
                                         NULL, NULL, 1, 0, NULL);
    if (array == NULL)
        return NULL;
        /*
         * Load it from the SDS.
         */
    status = SDreaddata(sds_id, startArr, strideArr, edgesArr,
                        PyArray_DATA(array));
    if (status < 0)    {
        PyErr_SetString(PyExc_ValueError, "SDreaddata failure");
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
        case NPY_FLOAT:
            f32 = *(float *) PyArray_DATA(array);
            o = PyFloat_FromDouble((double) f32);
            break;
        case NPY_DOUBLE:
            f64 = *(double *) PyArray_DATA(array);
            o = PyFloat_FromDouble(f64);
            break;
        case NPY_STRING:
        case NPY_BYTE:
            i32 = *(char *) PyArray_DATA(array);
            o = PyInt_FromLong((long) i32);
            break;
        case NPY_UBYTE:
            i32 = *(unsigned char *) PyArray_DATA(array);
            o = PyInt_FromLong((long) i32);
            break;
        case NPY_SHORT:
            i32 = *(short *) PyArray_DATA(array);
            o = PyInt_FromLong((long) i32);
            break;
        case NPY_INT:
            i32 = *(int *) PyArray_DATA(array);
            o = PyInt_FromLong((long) i32);
            break;
        }
    Py_DECREF(array);  /* Free array */
    return o;
    }

static PyObject * _SDwritedata_0(int32 sds_id, int32 data_type,
                                 PyObject *start,
                                 PyObject *edges,
                                 PyObject *data,
                                 PyObject *stride)    {

    PyArrayObject *array;
    PyObject *o;
    int n, rank, num_type, status;
        /*
         * Allocate those arrays on the stack for simplicity.
         * 80 dimensions should be more than enough!
         */
    int startArr[80], strideArr[80], edgesArr[80];

        /*
         * Load arrays. Caller has guaranteeded that all 3 arrays have the
         * same dimensions.
         */
    rank = PyObject_Length(start);
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
        }

        /*
         * Convert input to a contiguous numpy array (no penalty if
         * input already in this format).
         */
    if ((num_type = HDFtoNumericType(data_type)) < 0)    {
        PyErr_SetString(PyExc_ValueError, "data_type not compatible with numpy");
        return NULL;
        }
    if ((array = (PyArrayObject *)
                 PyArray_ContiguousFromObject(data, num_type, rank - 1, rank)) == NULL)
        return NULL;
        /*
         * Store in the SDS.
         */
    status = SDwritedata(sds_id, startArr, strideArr, edgesArr,
                         PyArray_DATA(array));
    Py_DECREF(array);      /* Free array */
    if (status < 0)    {
        PyErr_SetString(PyExc_ValueError, "SDwritedata failure");
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
 * Following two routines are defined above, and interface to the
 * `SDreaddata()' and `SDwritedata()' hdf functions.
 */

extern PyObject * _SDreaddata_0(int32 sds_id, int32 data_type,
                                PyObject *start,
                                PyObject *edges,
                                PyObject *stride);

extern PyObject * _SDwritedata_0(int32 sds_id, int32 data_type,
                                 PyObject *start,
                                 PyObject *edges,
                                 PyObject *data,
                                 PyObject *stride);

/*
 * Access
 */

extern int32 SDstart(const char *filename, int32 access_mode);

extern int32 SDcreate(int32 sd_id, const char *sds_name, int32 data_type,
                      int32 rank, const int32 *dim_sizes);

extern int32 SDselect(int32 sd_id, int32 sds_index);

extern int32 SDendaccess(int32 sds_id);

extern int32 SDend(int32 sd_id);

/*
 * General inquiry.
 */

extern int32 SDfileinfo(int32 sd_id, int32 *OUTPUT, int32 *OUTPUT);

%cstring_bounded_output(char *sds_name, H4_MAX_NC_NAME);
extern int32 SDgetinfo(int32 sds_id, char *sds_name, int32 *OUTPUT, void *buf,
                 int32 *OUTPUT, int32 *OUTPUT);
%clear char *sds_name;

extern int32 SDcheckempty(int32 sds_id, int32 *OUTPUT);

extern int32 SDidtoref(int32 sds_id);

extern int32 SDiscoordvar(int32 sds_id);

extern int32 SDisrecord(int32 sds_id);

extern int32 SDnametoindex(int32 sd_id, const char *sds_name);

extern int32 SDreftoindex(int32 sd_id, int32 sds_ref);

/*
 * Dimensions
 */

%cstring_bounded_output(char *dim_name, CHAR_BUFFER_SIZE);
extern int32 SDdiminfo(int32 dim_id, char *dim_name,
                       int32 *OUTPUT, int32 *OUTPUT, int32 *OUTPUT);
%clear char *dim_name;

extern int32 SDgetdimid(int32 sds_id, int32 dim_index);

extern int32 SDsetdimname(int32 dim_id, const char *dim_name);

/*
 * Dimension scales
 */

extern int32 SDgetdimscale(int32 dim_id, void *buf);

extern int32 SDsetdimscale(int32 dim_id, int32 n_values, int32 data_type,
                           const void *buf);

/*
 * User-defined attributes
 */

%cstring_bounded_output(char *attr_name, CHAR_BUFFER_SIZE);
extern int32 SDattrinfo(int32 obj_id, int32 attr_index,
                        char *attr_name, int32 *OUTPUT, int32 *OUTPUT);
%clear char *attr_name;

extern int32 SDfindattr(int32 obj_id, char *attr_name);

extern int32 SDreadattr(int32 obj_id, int32 attr_index, void *buf);

extern int32 SDsetattr(int32 obj_id, const char *attr_name, int32 data_type,
                       int32 n_values, const void *values);


/*
 * Predefined attributes
 */

extern int32 SDgetcal(int32 sds_id, double *OUTPUT, double *OUTPUT,
                     double *OUTPUT, double *OUTPUT, int32 *OUTPUT);

%cstring_bounded_output(char *label, ATTRIB_BUFFER_SIZE);
%cstring_bounded_output(char *unit, ATTRIB_BUFFER_SIZE);
%cstring_bounded_output(char *format, ATTRIB_BUFFER_SIZE);
%cstring_bounded_output(char *coord_system, ATTRIB_BUFFER_SIZE);
extern int32 SDgetdatastrs(int32 sds_id, char *label, char *unit, char *format,
                           char *coord_system, int32 len);
%clear char *label;
%clear char *unit;
%clear char *format;
%clear char *coord_system;

%cstring_bounded_output(char *label, ATTRIB_BUFFER_SIZE);
%cstring_bounded_output(char *unit, ATTRIB_BUFFER_SIZE);
%cstring_bounded_output(char *format, ATTRIB_BUFFER_SIZE);
extern int32 SDgetdimstrs(int32 sds_id, char *label, char *unit, char *format,
                          int32 len);
%clear char *label;
%clear char *unit;
%clear char *format;

extern int32 SDgetfillvalue(int32 sds_id, void *buf);

extern int32 SDgetrange(int32 sds_id, void *buf1, void *buf2);

extern int32 SDsetcal(int32 sds_id, double cal, double cal_error,
                      double offset, double offset_err, int32 data_type);

extern int32 SDsetdatastrs(int32 sds_id, const char *label, const char *unit,
                           const char *format, const char *coord_system);

extern int32 SDsetdimstrs(int32 sds_id, const char *label, const char *unit,
                          const char *format);

extern int32 SDsetfillmode(int32 sd_id, int32 fill_mode);

extern int32 SDsetfillvalue(int32 sds_id, const void *fill_val);

extern int32 SDsetrange(int32 sds_id, const void *max, const void *min);

/*
 * Compression
 */

%{

#include "hcomp.h"

static int32 _SDgetcompress(int32 sds_id, int32 *comp_type, int32 *value,
                            int32 *v2, int32 *v3, int32 *v4, int32 *v5)    {

    comp_info c_info;
    int32 status;

#ifdef NOCOMPRESS
    status = -1;
#else
    status = SDgetcompress(sds_id, comp_type, &c_info);
    switch (*comp_type)  {
        case COMP_CODE_NONE:
        case COMP_CODE_RLE :
            break;
        case COMP_CODE_SKPHUFF:
            *value = c_info.skphuff.skp_size;
            break;
        case COMP_CODE_DEFLATE:
            *value = c_info.deflate.level;
            break;
#ifndef NOSZIP
        case COMP_CODE_SZIP:
            *value = c_info.szip.options_mask;
            *v2 =    c_info.szip.pixels_per_block;
            *v3 =    c_info.szip.pixels_per_scanline;
            *v4 =    c_info.szip.bits_per_pixel;
            *v5 =    c_info.szip.pixels;
            break;
#endif
        }
#endif

    return status;
    }

static int32 _SDsetcompress(int32 sds_id, int32 comp_type, int32 value,
                            int32 v2)    {

    comp_info c_info;
    int32 status;

#ifdef NOCOMPRESS
    status = -1;
#else
    switch (comp_type)  {
        case COMP_CODE_NONE:
        case COMP_CODE_RLE :
            break;
        case COMP_CODE_SKPHUFF:
            c_info.skphuff.skp_size = value;
            break;
        case COMP_CODE_DEFLATE:
            c_info.deflate.level = value;
            break;
#ifndef NOSZIP
        case COMP_CODE_SZIP:
            c_info.szip.options_mask = value;
            c_info.szip.pixels_per_block = v2;
            break;
#endif
        }
    status = SDsetcompress(sds_id, comp_type, &c_info);
#endif
    return status;
    }
%}

extern int32 _SDgetcompress(int32 sds_id, int32 *OUTPUT, int32 *OUTPUT,
                            int32 *OUTPUT, int32 *OUTPUT, int32 *OUTPUT,
                            int32 *OUTPUT);
extern int32 _SDsetcompress(int32 sds_id, int32 comp_type, int32 value,
                            int32 v2);

/*
 * Misc
 */

extern int32 SDsetexternalfile(int32 sds_id, const char *filename,
                               int32 offset);

/*
 ********
 * VS API
 ********
 */


/*
 * Access / Create
 *****************
 */

extern intn    Vinitialize(int32 file_id);     /* Vstart is a macro */

extern int32   VSattach(int32 file_id,
                        int32 vdata_ref,
                        const char * vdata_access_mode);

extern int32   VSdetach(int32 vdata_id);

extern intn    Vfinish(int32 file_id);         /* Vend is a macro */

/*
 * Creating one-field vdata.
 */

extern int32  VHstoredata(int32 file_id,
                          const char *fieldname,
                          void *buf,
                          int32 n_records,
                          int32 data_type,
                          const char *vdata_name,
                          const char *vdata_class);

extern int32  VHstoredatam(int32 file_id,
                           const char *fieldname,
                           void *buf,
                           int32 n_records,
                           int32 data_type,
                           const char *vdata_name,
                           const char *vdata_class,
                           int32 order);

/*
 * Defining vdata structure.
 */

extern intn  VSfdefine(int32 vdata_id,
                       const char *fieldname,
                       int32 data_type,
                       int32 order);

extern intn  VSsetfields(int32 vdata_id,
                         const char *fieldname_list);

/*
 * Reading / writing vdata.
 */

int32 VSseek(int32 vdata_id,
             int32 record_index);

int32 VSread(int32 vdata_id,
             void *databuf,
             int32 n_records,
             int32 interlace_mode);

int32 VSwrite(int32 vdata_id,
              void *databuf,
              int32 n_records,
              int32 interlace_mode);

intn  VSfpack(int32 vdata_id,
              intn  action,    /* 0: PACK, 1: UNPACK */
              const char *fields_in_buf,
              void *buf,
              intn buf_size,
              intn n_records,
              const char *fieldname_list,
              void **bufptrs);

/*
 * Inquiry.
 */

extern int32 VSelts(int32 vdata_id);

%cstring_bounded_output(char *vdata_class, CHAR_BUFFER_SIZE);
extern intn  VSgetclass(int32 vdata_id,
                        char *vdata_class);
%clear char *vdata_class;

%cstring_bounded_output(char *fieldname_list, CHAR_BUFFER_SIZE);
extern int32 VSgetfields(int32 vdata_id,
                         char *fieldname_list);
%clear char *fieldname_list;

extern intn  VSgetinterlace(int32 vdata_id);

%cstring_bounded_output(char *vdata_name, CHAR_BUFFER_SIZE);
extern intn  VSgetname(int32 vdata_id,
                       char *vdata_name);
%clear char *vdata_name;

extern intn  VSsizeof(int32 vdata_id,
                      const char *fieldname_list);

%cstring_bounded_output(char *fieldname_list, CHAR_BUFFER_SIZE);
%cstring_bounded_output(char *vdata_name, CHAR_BUFFER_SIZE);
extern intn  VSinquire(int32 vdata_id,
                       int32 *OUTPUT,         /* n_records */
                       int32 *OUTPUT,         /* interlace_mode */
                       char  *fieldname_list,
                       int32 *OUTPUT,         /* vdata_size */
                       char *vdata_name);
%clear char *fieldname_list;
%clear char *vdata_name;

extern int32  VSQuerytag(int32 vdata_id);

extern int32  VSQueryref(int32 vdata_id);

extern intn   VSfindex(int32 vdata_id,
                       const char *field_name,
                       int32 *OUTPUT);         /* field_index */

extern intn   VSisattr(int32 vdta_id);

extern int32  VFnfields(int32 vdata_id);

extern int32  VFfieldtype(int32 vdata_id,
                          int32 field_index);

extern const char *VFfieldname(int32 vdata_id,
                               int32 field_index);

extern int32  VFfieldesize(int32 vdata_id,
                           int32 field_index);

extern int32  VFfieldisize(int32 vdata_id,
                           int32 field_index);

extern int32  VFfieldorder(int32 vdata_id,
                           int32 field_index);


/*
 * Searching
 */

extern int32  VSfind(int32 file_id,
                     const char *vdata_name);

extern int32  VSgetid(int32 file_id,
                      int32 vdata_ref);

extern intn   VSfexist(int32 vdata_id,
                       const char *fieldname_list);

/*
 * Attributes.
 */

extern int32 VSsetclass(int32 vdata_id,
                        const char *vdata_class);

extern int32 VSsetname(int32 vdata_id,
                       const char *vdata_name);

extern intn  VSsetinterlace(int32 vdata_id,
                            int32 interlace_mode);

extern intn  VSsetattr(int32 vdata_id,
                       int32 field_index,
                       const char *attr_name,
                       int32 data_type,
                       int32 n_values,
                       const void *values);

extern intn  VSgetattr(int32 vdata_id,
                       int32 field_index,
                       intn  attr_index,
                       void *buf);

extern int32 VSfnattrs(int32 vdata_id,
                       int32 field_index);

extern int32 VSnattrs(int32 vdata_id);

%cstring_bounded_output(char *attr_name, CHAR_BUFFER_SIZE);
extern intn  VSattrinfo(int32 vdata_id,
                        int32 field_index,
                        intn  attr_index,
                        char  *attr_name,
                        int32 *OUTPUT,     /* data_type */
                        int32 *OUTPUT,     /* n_values */
                        int32 *OUTPUT);    /* size */
%clear char *attr_name;

extern intn  VSfindattr(int32 vdata_id,
                        int32 field_index,
                        const char *attr_name);

/*********
 * V API *
 *********/

/*
 * Access vgroup
 */

extern int32  Vattach(int32 file_id,
                      int32 vgroup_ref,
                      const char *vg_access_mode);

extern int32 Vdetach(int32 vgroup_id);

%cstring_bounded_output(char *name, CHAR_BUFFER_SIZE);
extern int32 Vgetname(int32 vgroup_id,
                      char *name);
%clear char *name;

extern int32 Vsetname(int32 vgroup_id,
                      const char *vgroup_name);

%cstring_bounded_output(char *name, CHAR_BUFFER_SIZE);
extern int32 Vgetclass(int32 vgroup_id,
                       char *name);
%clear char *name;

extern int32 Vsetclass(int32 vgroup_id,
                       const char *vgroup_class);

extern int32 Vfind(int32 file_id,
                   const char *vgroup_name);

extern int32 Vfindclass(int32 file_id,
                        const char *vgroup_class);

extern int32 Vinsert(int32 vgroup_id,
                     int32 v_id);

extern int32 Vaddtagref(int32 vgroup_id,
                        int32 obj_tag,
                        int32 obj_ref);

extern int32 Vdeletetagref(int32 vgroup_id,
                           int32 obj_tag,
                           int32 obj_ref);

extern int32 Vdelete(int32 file_id,
                     int32 vgroup_id);

extern int32 VQueryref(int32 vgroup_id);

extern int32 VQuerytag(int32 vgroup_id);

extern int32 Vntagrefs(int32 vgroup_id);

extern int32 Vgettagref(int32 vgroup_id,
                        int32 index,
                        int32 *OUTPUT,       /* obj_tag */
                        int32 *OUTPUT);      /* obj_ref */

extern int32 Vgetversion(int32 vgroup_id);

extern int32 Vgettagrefs(int32 vgroup_id,
                         void  *tag_attay,
                         void  *ref_array,
                         int32  maxsize);

extern int32 Vgetid(int32 file_id,
                    int32 vgroup_ref);

extern intn  Vinqtagref(int32 vgroup_id,
                        int32 tag,
                        int32 ref);

extern intn  Visvg(int32 vgroup_id,
                   int32 obj_ref);

extern intn  Visvs(int32 vgroup_id,
                   int32 obj_ref);

extern int32 Vnrefs(int32 vgroup_id,
                    int32 tag_type);

/*
 * Attributes
 */

extern intn  Vfindattr(int32 vgroup_id,
                       const char *attr_name);

extern intn  Vgetattr(int32 vdata_id,
		      intn  attr_index,
		      void *buf);

extern intn  Vsetattr(int32 vgroup_id,
                      const char *attr_name,
                      int32 data_type,
                      int32 n_values,
                      const void *values);

%cstring_bounded_output(char *attr_name, CHAR_BUFFER_SIZE);
extern intn  Vattrinfo(int32 vgroup_id,
		       intn  attr_index,
		       char  *attr_name,
		       int32 *OUTPUT,     /* data_type */
		       int32 *OUTPUT,     /* n_values */
		       int32 *OUTPUT);    /* size */
%clear char *attr_name;

extern intn  Vnattrs(int32 vgroup_id);
