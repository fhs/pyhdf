#!/usr/bin/env python
#
# $Id: mpy.pyx,v 1.6 2005-02-13 01:51:14 gosselin_a Exp $
# $Name: not supported by cvs2svn $
# $Log: not supported by cvs2svn $
# Revision 1.5  2005/02/12 03:55:59  gosselin_a
# Fixed comments in the header of MPY_Scatter().
#
# Revision 1.4  2005/02/12 02:31:38  gosselin_a
# Added support for Numeric array datatype inside MPY_Scatter().
#
# Revision 1.3  2005/02/11 04:09:47  gosselin_a
# Support for Numeric arrays in function MPY_Gather().
#
# Revision 1.2  2005/02/10 23:11:04  gosselin_a
# Fixed comments in front of old logs generated when "mpy" was hosted at
# the Maurice-Lamontagne Institute.
#
# Revision 1.1.1.1  2005/02/10 22:54:06  gosselin_a
# Initial import of the mpy package
#
# Following logs refer to an earlier CVS repository used
# to manage "mpy" at the Maurice-Lamontagne Institute.
#
# Revision 1.14  2005/02/10 04:04:00  gosselin_a
# Added support for Numeric arrays inside MPY_Bcast().
#
# Revision 1.13  2005/02/09 03:35:58  gosselin_a
# Added support for Numeric arrays in Mpy_Sendrecv() and
# MPY_Sendrecv_replace().
# Removed parameter 'ctrl' in most functions where a probe can be
# performed to obtain the receive count.
#
# Revision 1.12  2005/02/08 04:15:30  gosselin_a
# Updated comments in function MPY_Start().
#
# Revision 1.11  2005/02/08 04:04:05  gosselin_a
# Finished support for numeric arrays in the MPY_xxx_init() routines.
#
# Revision 1.10  2005/01/25 03:04:35  gosselin_a
# Support for numeric arrays insde MPY_Ixxx series().
# Started support for numeric arrays inside MPY_Ixx-init() series.
#
# Revision 1.9  2005/01/24 04:01:25  gosselin_a
# Started to implement support for Numeric arrays.
#
# Revision 1.8  2005/01/15 03:51:55  gosselin_a
# Added support for environmental functions.
#
# Revision 1.7  2005/01/14 03:35:35  gosselin_a
# Added support for graph topology functions.
#
# Revision 1.6  2005/01/13 04:01:19  gosselin_a
# dded remaining cartesian topology functions.
#
# Revision 1.5  2005/01/12 03:29:27  gosselin_a
# Started addition of functions dealing with communicator topology.
#
# Revision 1.4  2005/01/11 03:31:02  gosselin_a
# Sdded support for attribute caching functions.
#
# Revision 1.3  2005/01/10 03:30:52  gosselin_a
# Added support for inter-communicator functions.
#
# Revision 1.2  2005/01/09 02:33:17  gosselin_a
# Support de toutes les fonctions relatives aux intra-communicateurs.
#
# Revision 1.1  2005/01/08 18:13:44  gosselin_a
# First version of the mpy package.
# Supports almost all functions in the point-to-point and collective
# message passing category, plus those for group manipulation.
#

import sys
import cPickle
import types
import Numeric

cdef extern from "Python.h":

    char  *PyString_AsString(object o)
    object PyString_FromStringAndSize(char *s, int len)
    void  *PyMem_Malloc(int nBytes)
    void   PyMem_Free(void *buf)

cdef extern from "string.h":

    char *memcpy (char *dest, char *src, int n)
    char *memmove(char *dest, char *src, int n)
    char *strncpy(char *dest, char *src, int n)

cdef extern from "Numeric/arrayobject.h":
        struct PyArray_Descr:
                int type_num, elsize
                char type

        ctypedef class Numeric.ArrayType [object PyArrayObject]:
                cdef int ob_refcnt
                cdef char *data
                cdef int nd
                cdef int *dimensions, *strides
                cdef object base
                cdef PyArray_Descr *descr
                cdef int flags

        int PyArray_ISCONTIGUOUS (ArrayType numArray)
        ArrayType PyArray_ContiguousFromObject(object numArray, int, int, int)
        int PyArray_NOTYPE
        int PyArray_CHAR
        int PyArray_UBYTE
        int PyArray_SBYTE
        int PyArray_SHORT
        int PyArray_USHORT
        int PyArray_INT
        int PyArray_UINT
        int PyArray_LONG
        int PyArray_FLOAT
        int PyArray_DOUBLE
        int PyArray_CFLOAT
        int PyArray_CDOUBLE
        int PyArray_NTYPES
        void import_array()

cdef extern from "mpi.h":

    # MPI handle types
    ctypedef void * MPI_Comm
    MPI_Comm        MPI_COMM_WORLD
    MPI_Comm        MPI_COMM_SELF
    MPI_Comm        MPI_COMM_NULL
    
    ctypedef void * MPI_Datatype
    MPI_Datatype    MPI_BYTE
    MPI_Datatype    MPI_CHAR
    MPI_Datatype    MPI_DOUBLE
    MPI_Datatype    MPI_FLOAT
    MPI_Datatype    MPI_INT
    MPI_Datatype    MPI_LONG
    MPI_Datatype    MPI_LONG_LONG
    MPI_Datatype    MPI_SHORT
    MPI_Datatype    MPI_UNSIGNED
    MPI_Datatype    MPI_UNSIGNED_CHAR
    MPI_Datatype    MPI_UNSIGNED_SHORT
    
    ctypedef void * MPI_Group
    MPI_Group       MPI_GROUP_EMPTY
    MPI_Group       MPI_GROUP_NULL
    
    ctypedef void * MPI_Op
    MPI_Op          MPI_BAND
    MPI_Op          MPI_BOR
    MPI_Op          MPI_BXOR
    MPI_Op          MPI_LAND
    MPI_Op          MPI_LOR
    MPI_Op          MPI_LXOR
    MPI_Op          MPI_MAX
    MPI_Op          MPI_MIN
    MPI_Op          MPI_PROD
    MPI_Op          MPI_SUM

# Not supported yet
#   MPI_Op          MPI_MINLOC
#   MPI_Op          MPI_MAXLOC
    
    ctypedef void * MPI_Request
    MPI_Request     MPI_REQUEST_NULL

    ctypedef struct MPI_Status:
        int     MPI_SOURCE
        int     MPI_TAG
        int     MPI_ERROR
        int     st_length
        
    int             MPI_MAX_PROCESSOR_NAME
    int             MPI_SUCCESS
    int             MPI_ANY_SOURCE
    int             MPI_PROC_NULL
    int             MPI_CANCEL_SOURCE
    int             MPI_ROOT
    int             MPI_ANY_TAG
    int             MPI_UNDEFINED

    int             MPI_IDENT
    int             MPI_CONGRUENT
    int             MPI_SIMILAR
    int             MPI_UNEQUAL

    int             MPI_CART
    int             MPI_GRAPH

    int             MPI_TAG_UB
    int             MPI_HOST
    int             MPI_IO
    int             MPI_WTIME_IS_GLOBAL

    int             MPI_KEYVAL_INVALID
    

# Attribute callbacks.

    ctypedef int MPI_Copy_function(MPI_Comm comm, int keyval, void *extraState,
                                     void *valIn, void *valOut, int *flag)
    MPI_Copy_function MPI_NULL_COPY_FN
    MPI_Copy_function MPI_DUP_FN

    ctypedef int MPI_Delete_function(MPI_Comm comm, int keyval, void *val,
                                     void *extraState)
    MPI_Delete_function MPI_NULL_DELETE_FN

# Error codes.
    int MPI_ERR_BUFFER
    int MPI_ERR_COUNT
    int MPI_ERR_TYPE
    int MPI_ERR_TAG
    int MPI_ERR_COMM
    int MPI_ERR_RANK
    int MPI_ERR_REQUEST
    int MPI_ERR_ROOT
    int MPI_ERR_GROUP
    int MPI_ERR_OP
    int MPI_ERR_TOPOLOGY
    int MPI_ERR_DIMS
    int MPI_ERR_ARG
    int MPI_ERR_UNKNOWN
    int MPI_ERR_TRUNCATE
    int MPI_ERR_OTHER
    int MPI_ERR_INTERN
    int MPI_ERR_IN_STATUS
    int MPI_ERR_PENDING
    int MPI_ERR_SYSRESOURCE
    int MPI_ERR_LOCALDEAD
    int MPI_ERR_REMOTEDEAD
    int MPI_ERR_VALUE
    int MPI_ERR_FLAGS
    int MPI_ERR_SERVICE
    int MPI_ERR_NAME
    int MPI_ERR_SPAWN
    int MPI_ERR_KEYVAL
    int MPI_ERR_INFO_NOKEY
    int MPI_ERR_WIN
    int MPI_ERR_EPOCH
    int MPI_ERR_TYPENOTSUP
    int MPI_ERR_INFO_KEY
    int MPI_ERR_INFO_VALUE
    int MPI_ERR_NO_MEM
    int MPI_ERR_BASE
    int MPI_ERR_LASTCODE
    

# Error handlers.
    
    ctypedef void *  MPI_Errhandler
    MPI_Errhandler   MPI_ERRORS_ARE_FATAL
    MPI_Errhandler   MPI_ERRORS_RETURN
    
    
    int MPI_Abort                  (MPI_Comm comm, int errCode)
    int MPI_Allgather              (void *sendBuf, int sendCount,
                                    MPI_Datatype sendType,
                                    void *recvBuf, int recvCount,
                                    MPI_Datatype recvType,
                                    MPI_Comm comm)
    int MPI_Allgatherv             (void *sendBuf, int sendCount,
                                    MPI_Datatype sendType,
                                    void *recvBuf, int *recvCounts, int *displ,
                                    MPI_Datatype recvType,
                                    MPI_Comm comm)
    int MPI_Allreduce              (void *sendBuf, void *recvBuf, int count,
                                    MPI_Datatype datatype, MPI_Op op,
                                    MPI_Comm comm)
    int MPI_Alltoall               (void *sendBuf, int sendCount,
                                    MPI_Datatype sendType,
                                    void *recvBuf, int recvCount,
                                    MPI_Datatype recvType,
                                    MPI_Comm comm)
    int MPI_Alltoallv              (void *sendBuf, int *sendCounts, int *sDispls,
                                    MPI_Datatype sendType,
                                    void *recvBuf, int *recvCounts, int *rDispls,
                                    MPI_Datatype recvType,
                                    MPI_Comm comm)
    int MPI_Attr_delete            (MPI_Comm comm, int keyval)
    int MPI_Attr_get               (MPI_Comm comm, int keyval, void *val, int *flag)
    int MPI_Attr_put               (MPI_Comm comm, int keyval, void *val)
    int MPI_Barrier                (MPI_Comm comm)
    int MPI_Bcast                  (void *buf, int count,
                                    MPI_Datatype datatype, int root,
                                    MPI_Comm comm)
    int MPI_Bsend                  (void *sendBuf, int count,
                                    MPI_Datatype datatype, int dest, int tag,
                                    MPI_Comm comm)
    int MPI_Bsend_init             (void *sendBuf, int count,
                                    MPI_Datatype datatype, int dest, int tag,
                                    MPI_Comm comm, MPI_Request *request)
    int MPI_Buffer_attach          (void *buffer, int size)
    int MPI_Buffer_detach          (void **bufAddr, int *size)
    int MPI_Cancel                 (MPI_Request *request)
    int MPI_Cart_coords            (MPI_Comm comm, int rank, int maxdims,
                                    int *coords)
    int MPI_Cart_create            (MPI_Comm comm, int ndims, int *dims,
                                    int *periodic, int reorder,
                                    MPI_Comm *newComm)
    int MPI_Cartdim_get            (MPI_Comm comm, int *nDims)
    int MPI_Cart_get               (MPI_Comm comm, int ndims, int *size,
                                    int *period,
                                    int *coord)
    int MPI_Cart_map               (MPI_Comm comm, int ndims, int *dims,
                                    int *periodic, int *newRank)
    int MPI_Cart_rank              (MPI_Comm comm, int *coords, int *rank)
    int MPI_Cart_shift             (MPI_Comm comm, int dimension,
                                    int direction, int *src, int *dest)
    int MPI_Cart_sub               (MPI_Comm comm, int *remainDims,
                                    MPI_Comm *newComm)
    int MPI_Comm_compare           (MPI_Comm comm1, MPI_Comm com2, int *result)
    int MPI_Comm_create            (MPI_Comm comm, MPI_Group group,
                                    MPI_Comm *newComm)
    int MPI_Comm_dup               (MPI_Comm comm, MPI_Comm *new)
    int MPI_Comm_free              (MPI_Comm *comm)
    int MPI_Comm_group             (MPI_Comm comm, MPI_Group *group)
    int MPI_Comm_rank              (MPI_Comm comm, int *rank)
    int MPI_Comm_remote_group      (MPI_Comm comm, MPI_Group *group)
    int MPI_Comm_remote_size       (MPI_Comm comm, int *size)
    int MPI_Comm_size              (MPI_Comm comm, int *size)
    int MPI_Comm_split             (MPI_Comm oldComm, int partition,
                                    int newRank, MPI_Comm *newComm)
    int MPI_Comm_test_inter        (MPI_Comm comm, int *flag)
    int MPI_Dims_create            (int nNodes, int nDims, int *dims)
    int MPI_Errhandler_get         (MPI_Comm, MPI_Errhandler *handler)
    int MPI_Errhandler_set         (MPI_Comm comm, MPI_Errhandler handler)
    int MPI_Error_class            (int errCode, int *errClass)
    int MPI_Error_string           (int errCode, char *string, int *resultLen)
    int MPI_Finalize               ()
    int MPI_Finalized              (int *flag)
    int MPI_Gather                 (void *sendBuf, int sendCount,
                                    MPI_Datatype sendType,
                                    void *recvBuf, int recvCount,
                                    MPI_Datatype recvType,
                                    int root, MPI_Comm comm)
    int MPI_Gatherv                (void *sendBuf, int sendCount,
                                    MPI_Datatype sendType,
                                    void *recvBuf, int *recvCounts, int *displ,
                                    MPI_Datatype recvType,
                                    int root, MPI_Comm comm)
    int MPI_Get_count              (MPI_Status *status, MPI_Datatype dataType,
                                    int *count)
    int MPI_Get_processor_name     (char *name, int *length)
    int MPI_Get_version            (int *major, int *minor)
    int MPI_Graph_create           (MPI_Comm comm, int nNodes, int *index,
                                    int *edges, int reorder, MPI_Comm *newComm)
    int MPI_Graphdims_get          (MPI_Comm comm, int *nNodes, int *nEdges)
    int MPI_Graph_get              (MPI_Comm comm, int maxindex,int maxedges,
                                    int *index, int *edges)
    int MPI_Graph_map              (MPI_Comm comm, int nNodes, int *index,
                                    int *edges, int *newRank)
    int MPI_Graph_neighbors        (MPI_Comm comm, int rank, int maxNeighbors,
                                    int *neighbors)
    int MPI_Graph_neighbors_count  (MPI_Group comm, int rank, int *nNeighbors)
    int MPI_Group_compare          (MPI_Group group1, MPI_Group group2,
                                    int *result)
    int MPI_Group_difference       (MPI_Group group1, MPI_Group group2,
                                    MPI_Group *new)
    int MPI_Group_excl             (MPI_Group group, int excl_num,
                                    int *excl_ranks, MPI_Group *new)
    int MPI_Group_free             (MPI_Group *group)
    int MPI_Group_incl             (MPI_Group group, int incl_num,
                                    int *incl_ranks, MPI_Group *new)
    int MPI_Group_intersection     (MPI_Group group1, MPI_Group group2,
                                    MPI_Group *new)
    int MPI_Group_range_excl       (MPI_Group group, int n, int ranges[][3],
                                    MPI_Group *new)
    int MPI_Group_range_incl       (MPI_Group group, int n, int ranges[][3],
                                    MPI_Group *new)
    int MPI_Group_rank             (MPI_Group group, int *rank)
    int MPI_Group_size             (MPI_Group group, int *size)
    int MPI_Group_translate_ranks  (MPI_Group group1, int n, int *rank1,
                                    MPI_Group group2, int *rank2)
    int MPI_Group_union            (MPI_Group group1, MPI_Group group2,
                                    MPI_Group *new)
    int MPI_Ibsend                 (void *sendBuf, int count,
                                    MPI_Datatype datatype, int dest, int tag,
                                    MPI_Comm comm, MPI_Request *request)
    int MPI_Init                   (int *argc, char ***argv)
    int MPI_Initialized            (int *flag)
    int MPI_Intercomm_create       (MPI_Comm localComm, int localLeader,
                                    MPI_Comm peerComm,  int remoteLeader,
                                    int tag, MPI_Comm *newIntercomm)
    int MPI_Intercomm_merge        (MPI_Comm intercomm, int high,
                                    MPI_Comm *newComm)
    int MPI_Iprobe                 (int source, int tag,
                                    MPI_Comm comm, int *flag, MPI_Status *status)
    int MPI_Irecv                  (void *recvBuf, int count,
                                    MPI_Datatype datatype, int source, int tag,
                                    MPI_Comm comm, MPI_Request *request)
    int MPI_Irsend                 (void *sendBuf, int count,
                                    MPI_Datatype datatype, int dest, int tag,
                                    MPI_Comm comm, MPI_Request *request)
    int MPI_Isend                  (void *sendBuf, int count,
                                    MPI_Datatype datatype, int dest, int tag,
                                    MPI_Comm comm, MPI_Request *request)
    int MPI_Issend                 (void *sendBuf, int count,
                                    MPI_Datatype datatype, int dest, int tag,
                                    MPI_Comm comm, MPI_Request *request)
    int MPI_Keyval_create          (MPI_Copy_function *copy_fn,
                                    MPI_Delete_function *delete_fn,
                                    int *keyval, void *extraState)
    int MPI_Keyval_free            (int *keyval)
    int MPI_Probe                  (int source, int tag,
                                    MPI_Comm comm, MPI_Status *status)
    int MPI_Recv                   (void *recvBuf, int count,
                                    MPI_Datatype datatype, int source, int tag,
                                    MPI_Comm comm, MPI_Status *status)
    int MPI_Recv_init              (void *sendBuf, int count,
                                    MPI_Datatype datatype, int source, int tag,
                                    MPI_Comm comm, MPI_Request *request)
    int MPI_Reduce                 (void *sendBuf, void *recvBuf, int count,
                                    MPI_Datatype datatype, MPI_Op op, int root,
                                    MPI_Comm comm)
    int MPI_Reduce_scatter         (void *sendBuf, void *recvBuf, int *recvCounts,
                                    MPI_Datatype datatype, MPI_Op op,
                                    MPI_Comm comm)
    int MPI_Request_free           (MPI_Request *request)
    int MPI_Rsend                  (void *sendBuf, int count,
                                    MPI_Datatype datatype, int dest, int tag,
                                    MPI_Comm comm)
    int MPI_Rsend_init             (void *sendBuf, int count,
                                    MPI_Datatype datatype, int dest, int tag,
                                    MPI_Comm comm, MPI_Request *request)
    int MPI_Scan                   (void *sendBuf, void *recvBuf, int count,
                                    MPI_Datatype datatype, MPI_Op op,
                                    MPI_Comm comm)
    int MPI_Scatter                (void *sendBuf, int sendCount,
                                    MPI_Datatype sendType,
                                    void *recvBuf, int recvCount,
                                    MPI_Datatype recvType, int root,
                                    MPI_Comm comm)
    int MPI_Scatterv               (void *sendBuf, int *sendCounts, int *displ,
                                    MPI_Datatype sendType,
                                    void *recvBuf, int recvCount,
                                    MPI_Datatype recvType, int root,
                                    MPI_Comm comm)
    int MPI_Send                   (void *sendBuf, int count,
                                    MPI_Datatype datatype, int dest, int tag,
                                    MPI_Comm comm)
    int MPI_Send_init              (void *sendBuf, int count,
                                    MPI_Datatype datatype, int dest, int tag,
                                    MPI_Comm comm, MPI_Request *request)
    int MPI_Sendrecv               (void *sendBuf, int sendCount,
                                    MPI_Datatype sendDatatype, int dest,
                                    int sendTag,
                                    void *recvBuf, int recvCount,
                                    MPI_Datatype recvDatatype, int src,
                                    int recvTag,
                                    MPI_Comm comm, MPI_Status *status)
    int MPI_Sendrecv_replace       (void *buf, int count,
                                    MPI_Datatype datatype, int dest,
                                    int sendTag, int source, int recvTag, 
                                    MPI_Comm comm, MPI_Status *status)
    int MPI_Ssend                  (void *sendBuf, int count,
                                    MPI_Datatype datatype, int dest, int tag,
                                    MPI_Comm comm)
    int MPI_Ssend_init             (void *sendBuf, int count,
                                    MPI_Datatype datatype, int dest, int tag,
                                    MPI_Comm comm, MPI_Request *request)
    int MPI_Start                  (MPI_Request *request)
    int MPI_Startall               (int count, MPI_Request *reqArr)
    int MPI_Test                   (MPI_Request *request, int *flag,
                                    MPI_Status *status)
    int MPI_Testall                (int count, MPI_Request *arr, int *flag,
                                    MPI_Status *status)
    int MPI_Testany                (int count, MPI_Request *arr, int *index,
                                    int *flag, MPI_Status *status)
    int MPI_Test_cancelled         (MPI_Status *status, int *flag)
    int MPI_Testsome               (int count, MPI_Request *arr, int *outCount,
                                    int *indexArr, MPI_Status *statusArr)
    int MPI_Topo_test              (MPI_Comm comm, int *status)
    int MPI_Wait                   (MPI_Request *request, MPI_Status *status)
    int MPI_Waitall                (int count, MPI_Request *arr,
                                    MPI_Status *status)
    int MPI_Waitany                (int count, MPI_Request *arr, int *index,
                                    MPI_Status *status)
    int MPI_Waitsome               (int count, MPI_Request *arr, int *outCount,
                                    int *indexArr, MPI_Status *statusArr)
    double MPI_Wtick               ()
    double MPI_Wtime               ()

# Create Python variables equivalent to the C MPI vars.
# Cast them to long so as to allow their use as python arguments.

# MPI Communicators
MPY_COMM_WORLD  = <long>MPI_COMM_WORLD
MPY_COMM_SELF   = <long>MPI_COMM_SELF
MPY_COMM_NULL   = <long>MPI_COMM_NULL

# MPI Groups
MPY_GROUP_EMPTY = <long>MPI_GROUP_EMPTY
MPY_GROUP_NULL  = <long>MPI_GROUP_NULL

# MPI basic datatypes
MPY_BYTE              = <long>MPI_BYTE
MPY_CHAR              = <long>MPI_CHAR
MPY_DOUBLE            = <long>MPI_DOUBLE
MPY_FLOAT             = <long>MPI_FLOAT
MPY_INT               = <long>MPI_INT
MPY_LONG              = <long>MPI_LONG
MPY_LONG_LONG         = <long>MPI_LONG_LONG
MPY_SHORT             = <long>MPI_SHORT
MPY_UNSIGNED          = <long>MPI_UNSIGNED
MPY_UNSIGNED_CHAR     = <long>MPI_UNSIGNED_CHAR
MPY_UNSIGNED_SHORT    = <long>MPI_UNSIGNED_SHORT

# Additions to the basic datatypes, to suit Python environment :
MPY_PYTHON_OBJ        = <long>-1
MPY_PYTHON_STR        = <long>-2
MPY_PYTHON_ARRAY      = <long>-3

# MPI operators
MPY_BAND              = <long>MPI_BAND
MPY_BOR               = <long>MPI_BOR
MPY_BXOR              = <long>MPI_BXOR
MPY_LAND              = <long>MPI_LAND
MPY_LOR               = <long>MPI_LOR
MPY_LXOR              = <long>MPI_LXOR
MPY_MAX               = <long>MPI_MAX
MPY_MIN               = <long>MPI_MIN
MPY_PROD              = <long>MPI_PROD
MPY_SUM               = <long>MPI_SUM

# Not supported yet
#MPY_MAXLOC            = <long>MPI_MAXLOC
#MPY_MINLOC            = <long>MPI_MINLOC

# MPI Requests
MPY_REQUEST_NULL      = <long>MPI_REQUEST_NULL


MPY_MAX_PROCESSOR_NAME = MPI_MAX_PROCESSOR_NAME

MPY_SUCCESS            = MPI_SUCCESS
MPY_ANY_SOURCE         = MPI_ANY_SOURCE
MPY_PROC_NULL          = MPI_PROC_NULL
MPY_CANCEL_SOURCE      = MPI_CANCEL_SOURCE
MPY_ROOT               = MPI_ROOT
MPY_ANY_TAG            = MPI_ANY_TAG

MPY_UNDEFINED          = MPI_UNDEFINED
MPY_SUCCESS            = MPI_SUCCESS
MPY_ANY_SOURCE         = MPI_ANY_SOURCE
MPY_PROC_NULL          = MPI_PROC_NULL
MPY_CANCEL_SOURCE      = MPI_CANCEL_SOURCE
MPY_ROOT               = MPI_ROOT
MPY_ANY_TAG            = MPI_ANY_TAG

MPY_UNDEFINED          = MPI_UNDEFINED

MPY_IDENT              = MPI_IDENT
MPY_CONGRUENT          = MPI_CONGRUENT
MPY_SIMILAR            = MPI_SIMILAR
MPY_UNEQUAL            = MPI_UNEQUAL

MPY_CART               = MPI_CART
MPY_GRAPH              = MPI_GRAPH

MPY_TAG_UB             = MPI_TAG_UB
MPY_HOST               = MPI_HOST
MPY_IO                 = MPI_IO
MPY_WTIME_IS_GLOBAL    = MPI_WTIME_IS_GLOBAL

MPY_NULL_COPY_FN       = <long>MPI_NULL_COPY_FN
MPY_DUP_FN             = <long>MPI_DUP_FN
MPY_NULL_DELETE_FN     = <long>MPI_NULL_DELETE_FN
MPY_KEYVAL_INVALID     = MPI_KEYVAL_INVALID

MPY_ERRORS_ARE_FATAL   = <long>MPI_ERRORS_ARE_FATAL
MPY_ERRORS_RETURN      = <long>MPI_ERRORS_RETURN

MPY_ERR_BUFFER = MPI_ERR_BUFFER
MPY_ERR_COUNT = MPI_ERR_COUNT
MPY_ERR_TYPE = MPI_ERR_BUFFER
MPY_ERR_TAG = MPI_ERR_BUFFER
MPY_ERR_COMM = MPI_ERR_COMM
MPY_ERR_RANK = MPI_ERR_RANK 
MPY_ERR_REQUEST = MPI_ERR_REQUEST
MPY_ERR_ROOT = MPI_ERR_ROOT
MPY_ERR_GROUP = MPI_ERR_GROUP
MPY_ERR_OP = MPI_ERR_OP
MPY_ERR_TOPOLOGY   = MPI_ERR_TOPOLOGY
MPY_ERR_DIMS       = MPI_ERR_DIMS
MPY_ERR_ARG       = MPI_ERR_ARG
MPY_ERR_UNKNOWN    = MPI_ERR_UNKNOWN
MPY_ERR_TRUNCATE   = MPI_ERR_TRUNCATE
MPY_ERR_OTHER      = MPI_ERR_OTHER
MPY_ERR_INTERN     = MPI_ERR_INTERN
MPY_ERR_IN_STATUS  = MPI_ERR_IN_STATUS
MPY_ERR_PENDING    = MPI_ERR_PENDING
MPY_ERR_SYSRESOURE = MPI_ERR_SYSRESOURCE
MPY_ERR_LOCALDEAD  = MPI_ERR_LOCALDEAD
MPY_ERR_REMOTEDEAD = MPI_ERR_REMOTEDEAD
MPY_ERR_VALUE      = MPI_ERR_VALUE
MPY_ERR_FLAGS      = MPI_ERR_FLAGS
MPY_ERR_SERVICE    = MPI_ERR_SERVICE
MPY_ERR_NAME       = MPI_ERR_NAME
MPY_ERR_SPAWN      = MPI_ERR_SPAWN
MPY_ERR_KEYVAL     = MPI_ERR_KEYVAL
MPY_ERR_INFO_NOKEY = MPI_ERR_INFO_NOKEY
MPY_ERR_WIN        = MPI_ERR_WIN
MPY_ERR_EPOCH      = MPI_ERR_EPOCH
MPY_ERR_TYPENOTSUP = MPI_ERR_TYPENOTSUP
MPY_ERR_INFO_KEY   = MPI_ERR_INFO_KEY
MPY_ERR_INFO_VALUE = MPI_ERR_INFO_VALUE
MPY_ERR_NO_MEM     = MPI_ERR_NO_MEM
MPY_ERR_BASE       = MPI_ERR_BASE
MPY_ERR_LASTCODE   = MPI_ERR_LASTCODE

# Buffer space
cdef int _bufSpace
_bufSpace = 0

# Null pointer
cdef void *NULLPT
NULLPT                 = <void *>0


cdef int controlTag
controlTag             = 32766

# Private communicator holding all processes.
cdef MPI_Comm    priv_comm
cdef MPI_Group   priv_group

# For Numeric. Calling import_array() is mandatory to use Numeric.
import_array()
# Info about array properties.
cdef class numArrInfo:
    cdef char *data               # internal buffer address
    cdef int  nElem               # total number of elements
    cdef long mpi_datatype        # equivalent MPI datatype

# For testing Numeric types
_arrayType = type(Numeric.zeros(0))
# To convert from Numeric data types to MPI datatypes.
numArrToMPI_types = {
    PyArray_CHAR   : MPY_CHAR,
    PyArray_UBYTE  : MPY_UNSIGNED_CHAR,
    PyArray_SBYTE  : MPY_CHAR,
    PyArray_SHORT  : MPY_SHORT,
    PyArray_USHORT : MPY_UNSIGNED_SHORT,
    PyArray_INT    : MPY_INT,
    PyArray_UINT   : MPY_UNSIGNED,
    PyArray_LONG   : MPY_LONG,
    PyArray_FLOAT  : MPY_FLOAT,
    PyArray_DOUBLE : MPY_DOUBLE
    #PyArray_CFLOAT :
    #PyArray_CDOUBLE:
    }

class MPY_Error(Exception):

    def __init__(self, args=None):
        self.args = args
    
class Status(object):
    """Status object returned by functions when 'retStatus' parameter
    is set to True."""

    def __init__(self, source, tag, error, length):
        self.source = source
        self.tag    = tag
        self.error  = error
        self.length = length

    def __repr__(self):
        return "source=%s tag=%s error=%s length=%s" \
               % (self.source, self.tag, self.error, self.length)

class Request(object):
    """Object returned by 'isend()' and 'irecv()' functions.
                                                                """

    def __init__(self, mpi_request, buf, receive, dataType=MPY_PYTHON_OBJ,
                 array=None, permanent=False):
        """
        Initialize a Request instance.

        Params:
          mpi_request      MPI request, as returned by a call to MPI_Isend, etc
          buf              buffer holding message data
          receive          boolean indicating if the request implies a receive
                           (== True) or a send (==False) operation
          dataType         type of the data elements
          array            This parameter should be set only when dataType==
                           MPY_PYTHON_ARRAY, indicating that the buffer belongs
                           to numeric array 'array'. This object is passed to avoid
                           the garbage collection of the numeric array, which would
                           make 'buf' invalid.
          permanent        Boolean indicating if the request belongs to a permanent
                           request (MPY_Isend_init, etc).
                                                                         """

        self.mpi_request = mpi_request
        self.buf         = buf
        self.receive     = receive
        self.length      = 0
        self.dataType    = dataType
        self.array       = array
        self.permanent   = permanent

    def __str__(self):
        return "%x %x %d %d" % (self.mpi_request, self.buf, self.receive,
                                self.length)


# Message transfer mode : as a python object, or as an array of MPI datatypes.
#
# A message can be exchanged between process using two different modes : as a Python
# object, or as an array of MPI datatypes.
#
# When exchanged as a Python object, the message is encapsulated inside an array of
# bytes in such a way that the receiver can recover the message with absolutely
# no loss of information. This mode is the most simple, powerfull and versatile
# to use. With it, almost any Python object can be exchanged, whathever its
# complexity : lists, sequences, multi-level sequences, dictionnaries, etc. To
# exchange any object, just give it to a sending function on the sending side, and 
# and recover the output of a receiving function on the receiving side : there is
# nothing more to do. It cannot be any simpler. Use of this mode however comes
# with a cost : the encapsulation process somewhat increases
# the size of the message. Also, the message becomes python specific, and cannot
# be properly interpreted by a non-python process.
#
# This mode is the default. To use this mode in a message exchanging function,
# omit parameter 'dataType', or set it to 'MPY_PYTHON_OBJ'. 
#
# The other transmission mode consists of assembling the message inside conventional
# arrays regrouping values of a basic MPI type. To use this mode in a message
# exchanging function, set parameter 'dataType' to one of the basic MPI
# datatypes : MPI_SHORT (short integer), MPI_INT (integer), MPI_FLOAT
# (32 bits float), MPI_DOUBLE (double), etc. Messages sent in this mode must
# be either scalars, or sequences (list or tuple) of scalars. When assembling
# the message, type conversion can occur. For ex., If a sending routine is
# passed a list of integers and the datatype is set to 'MPI_FLOAT', the integers
# will be sent as 32 bit floating point numbers. This transmission mode produces
# the most compact messages (no encapsulation overhead compared to first mode),
# and the messages can be read by any process conforming to the MPI standard.
# However, this mode is convenient only for messages whose structure is relatively
# "simple", eg homogeneous regular arrays. Exchanging objects like dictionnaries,
# mixed-type tables or multi-level lists can easily become a nightmare.
#
# Steps a message goes through during data exchange
#
# Since we start from a python environment and MPI was developped for more
# traditional environments (C, C++, Fortran), every message exchange implies
# copying the python data inside a C-style array during a send, and converting
# the contents of a C-style array to a python object during a receive.
#
# The first step when sending a message is to allocate a C-style array where
# the message is copied. This array is then handed over to the proper MPI data
# exchange routine. The array is then freed (there are exceptions to this in
# the case of immediate or permanent requests, where the array may freed later).
#
# On the receiving side, we must allocate a buffer to receive the message. To do
# that, the message size is needed, and the buffer size must be at least equal to
# the message size. If a Numeric array is used by the receiver (datatype ==
# MPY_PYTHON_ARRAY), the message size is given by the array size.
# Otherwise, receiver can set parameter nElem to the message size. Otherwise,
# the receiver will probe the message queue to obtain the message length, and
# allocate the buffer accordingly.
#
#
#
# Number of data elements
#
# Most of the message-exchanging functions take an 'nElem' parameter which
# gives the number of data elements composing the message. This number is in
# units of 'dataType', not bytes. For ex., if the datatype is MPI_INT, 'nElem'
# gives the number of integers in the message. How this translates to bytes
# is platform dependent. For the MPY_PYTHON_OBJ datatype, 'nElem' is counted
# in bytes, and is interpreted as the length of the string needed to encapsulate
# the python object.
#
# On a send operation, Python can automatically deduce the number of data elements
# from the object about to be sent. Parameter 'nElem' can always be omitted here.
# However, if 'nElem' is set and the transmission mode uses MPI datatypes,
# a check is made that its value is equal to the number of elements inside
# the message to transmit. If 'nElem' is set and the message is transmitted as
# a python object, a check is made that its value is >= that of the string
# that would be used to encapsulate the object. A mismatch will raise an exception.
# 
# On a receive operation, 'nElem' can be omitted if the receive is blocking,
# in which case the message size will be obtained by probing the message
# queue, unless the datatype is MPY_PYTHON_ARRAY. In that last case, the number of
# elements is given by the product of the array dimensions.
# 

# Notes of the relative efficiency of messages passed as Python objects
# vs basic MPI datatypes.
#
# A message passed as a Python object is picked inside a string on the
# sender side, then unpickled on the receiver side. This may or may
# not incur a penalty on the message size.
#
# Examples
#   object          msg size when pickling    msg size using MPI datatypes
#   range(100,150)        106                       200 (50 * 4 bytes per int)
#   range(1000,1100)      306                       400
#   range(100000,100100)  506                       400
#   [1000.0,...,1099.0]   906                       800 (using MPI_DOUBLE)
#   'X'*100               105                       100
#
# It does not seem that pickling significantly increase message size.
# It however tremendously increase the versatility of the message
# passing routines.
#
# When receiving a message broadcasted as an object (eg: a pickled object)
# the receiving buffer can be oversized. Ths wastes space, but does
# not prevent the received message from being properly unpickled.
# This is because the pickled string starts with a header telling
# where the valid part of the string ends. If the message is broadcasted
# using the basic MPI datatype, the buffer size on the receiver side must
# match that on the sender side, otherwise the message will be followed by
# junk. No status accompanies a broadcast, nor is it possible to probe
# a broadcast to obtain its length.
#
# Notes on MPI_CHAR
#  MPI supports no string type per se. When exchanging messages using the 
#  basic MPI datatypes, MPI_CHAR can be used to send an array either 
#  of characters or of small signed integers (-128, 127). On the receiving side
#  however, one will get an array of numbers, and must be prepared to
#  convert it to a Python string if a string is wanted instead.
#  To avoid this chore, this package offers a new datatype MPI_PYTHON_STR.
#  When used by a receiving function, this datatype will force the return
#  of a python string whose components are the values of the array elements.
#
#  Of course, all this trouble can be avoided by sending messages as
#  python objects : the structure and contents of the messages will then
#  totally preserved.

######################################################################
# MPI functions
######################################################################

def MPY_Abort(long comm=MPY_COMM_WORLD, int errCode=32767):
    """
    Python wrapper around MPI_Abort() .

    Params:
      comm          Communicator of tasks to abort.
      errCode       Error code to return to invoking environment.

    Returns:
      None
                                                                         """

    res = MPI_Abort(<MPI_Comm>comm, errCode)
    checkErr(res, "MPY_Abort")
    

def MPY_Allgather(msg, dataType=MPY_PYTHON_OBJ,
                  long comm=MPY_COMM_WORLD):
    """
    Python wrapper around MPI_Allgather() .

    MPY_Allgather() and MPY_Allgatherv() have the same calling sequence.
    They differ from each other in that, with MPY_Allgather(), all participating
    processes must send the same number of data elements, whereas MPY_Allgatherv()
    allows each process to send a different number of data elements.

    When gathering messages sent as python objects, MPY_Allgatherv() should
    be called rather than MPY_Allgather() since it can be hard to predict
    the exact size of the string used to encapsulate a python object.
    Even if the objects contain the same number of elements of the same
    type, the magnitude of the element values may generate strings
    of different length. For example, lists [1,2,3] and [10001,10002,10002]
    each contain 3 integers, but their encapsulated length is different
    because of the magnitude of their respective values.

    Params:
      msg           Message which will be sent to other processes. The number of
                    data elements is automaticaly determined. All messages
                    sent by participating processes must be of the same length.
                    If this is not the case, call MPY_Allgatherv() instead.
      dataType      Message datatype.
      comm          Communicator handle.

    Returns:
        List holding the gathered messages, one per process inside the
        communicator. 

                                                                 """
    cdef long r, s, mpi_datatype
    cdef int size, rank, chunkSize
    cdef long adr

    size = MPY_Comm_size(comm)
    rank = MPY_Comm_rank(comm)

    # Allocate buffer to store message sent by all processes.
    s, nElem, mpi_datatype = obj2CArray(msg, dataType, NULLPT)

    # Allocate a receive buffer for all processes. The buffer will be divided
    # into chunks of size 'nElem' data elements. Each value returned by member of rank
    # 'n' will be written to chunk number 'n'.
    chunkSize = nElem * dataTypeSize(dataType)
    r, mpi_datatype = prepRecv(nElem * size, dataType)
            
    # Do the gather.
    res = MPI_Allgather(<void *>s, nElem, <MPI_Datatype>mpi_datatype,
                        <void *>r, nElem, <MPI_Datatype>mpi_datatype,
                        <MPI_Comm>comm)
    checkErr(res, "MPY_Allgather")

    # Dispose of the C source buffer.
    PyMem_Free(<void *>s)

    # Convert the receive buffer to a Python list.
    adr = r
    res = []
    for k in range(size):
        # Convert the contents of chunk 'k' to a Python
        # object, and append this object to the output list.
        res.append(CArray2Obj(<void *>adr, dataType, nElem, False))
        # Compute the offset of next chunk.
        adr = adr + chunkSize

    # Free receive buffer.
    PyMem_Free(<void *>r)

    # Return list
    return res


def MPY_Allgatherv(buffer, dataType=MPY_PYTHON_OBJ,
                   long comm=MPY_COMM_WORLD):
    """
    Python wrapper around MPI_Allgatherv() .

    MPY_Allgather() and MPY_Allgatherv() have the same calling sequence.
    They differ from each other in that, with MPY_Allgather(), all participating
    processes must send the same number of data elements, whereas MPY_Allgatherv()
    allows each process to send a different number of data elements.

    When gathering messages sent as python objects, MPY_Allgatherv() should
    be called rather than MPY_Allgather() since it can be hard to predict
    the exact size of the string used to encapsulate a python object.
    Even if the objects contain the same number of elements of the same
    type, the magnitude of the element values may generate strings
    of different length. For example, lists [1,2,3] and [10001,10002,10002]
    each contain 3 integers, but their encapsulated length is different
    because of the magnitude of their respective values.

    Params:
      buffer        Message which will be sent to other processes.
                    The number of data elements is automatically determined.
                    Each participating process does not need
                    to send the same number of data elements, countrary to
                    function MPY_Allgather() where each participant needs to send the
                    same number of data elements.
      dataType      Message datatype.
      comm          Communicator handle.

    Returns:
        list holding the gathered messages

                                                                                 """
    cdef long r, s, mpi_datatype
    cdef int size, rank
    cdef long adr
    cdef int nElem, *nElemArr, *displArr, i, totalElem, elemSize

    size = MPY_Comm_size(comm)
    rank = MPY_Comm_rank(comm)

    # Allocate buffer to store message to be sent.
    s, nElem, mpi_datatype = obj2CArray(buffer, dataType, NULLPT)

    # Allocate element and displacement arrays.
    nElemArr = <int *>PyMem_Malloc(size * sizeof(int))
    displArr = <int *>PyMem_Malloc(size * sizeof(int))

    # Since the number of data elements can vary between participants,
    # we need to gather the size of the message that each is about to send.
    MPI_Allgather(&nElem, 1, MPI_INT, nElemArr, 1, MPI_INT, <MPI_Comm>comm)

    # Compute total number of data elements, and initialize displacement array.
    totalElem = 0
    for i from 0 <= i < size:
        totalElem = totalElem + nElemArr[i]
        if i == 0:
            displArr[i] = 0
        else:
            displArr[i] = displArr[i-1] + nElemArr[i-1]

    # Allocate a receive buffer. The buffer will be divided
    # into chunks of size 'nElemArr[i]' data elements.
    # Each value returned by member of rank 'n' will be written
    # to chunk number 'n'.
    r, mpi_datatype = prepRecv(totalElem, dataType)
            
    # Do the gather.
    res = MPI_Allgatherv(<void *>s, nElem, <MPI_Datatype>mpi_datatype,
                         <void *>r, nElemArr, displArr, <MPI_Datatype>mpi_datatype,
                         <MPI_Comm>comm)
    checkErr(res, "MPY_Allgather")

    # Dispose of the C source buffer.
    PyMem_Free(<void *>s)

    # Convert the receive buffer to a Python list.
    adr = <long>r
    res = []
    elemSize = dataTypeSize(dataType)
    for k in range(size):
        # Convert the contents of chunk 'k' to a Python
        # object, and append this object to the output list.
        res.append(CArray2Obj(<void *>adr, dataType, nElemArr[k], False))
        # Compute the offset of next chunk.
        adr = adr + nElemArr[k] * elemSize

    # Free receive buffer, element array and displacement array.
    PyMem_Free(<void *>r)
    PyMem_Free(<void *>nElemArr)
    PyMem_Free(<void *>displArr)
    
    # Return list
    return res


def MPY_Allreduce(buf, long op, dataType=MPY_PYTHON_OBJ,
                  long comm=MPY_COMM_WORLD):
    """
    Python wrapper around MPI_Allreduce() .

    Params:
      buf           Data element(s) submitted to the reduce operation.
                    Either a single numeric value, or a sequence of numeric
                    values. All processes must send the same number of elements
                    to the reduce operator.
      op            Reduction operator. MINLOC and MAXLOC are not supported yet.
      dataType      Data elements type.
      comm          Communicator handle.

    Returns:
      One or more reduced values
    
                                                               """
    cdef int i, nElem, rank
    cdef long s, r, mpi_datatype


    rank = MPY_Comm_rank(comm)
    
    # If a python object is passed in, try to deduce the MPI datatype.
    if dataType == MPY_PYTHON_OBJ:
        if type(buf) in [types.TupleType, types.ListType]:
            t = type(buf[0])
        else:
            t = type(buf)
        if t == type(1):
            dataType = MPY_INT
        elif t == type(1.0):
            dataType = MPY_DOUBLE
        elif t == type(long(1)):
            dataType = MPY_LONG_LONG
        else:
            raise MPY_Error, "bad value type passed to MPY_reduce"

    # Allocate buffer where to store the data elements.
    s, nElem, mpi_datatype = obj2CArray(buf, dataType, NULLPT)

    # Allocate buffer to receive the reduced results.
    r, mpi_datatype = prepRecv(nElem, dataType)

    # Execute the reduce operation.
    res = MPI_Allreduce(<void *>s, <void *>r, nElem, <MPI_Datatype>mpi_datatype,
                        <MPI_Op>op, <MPI_Comm>comm)
    checkErr(res, "MPY_Allreduce")

    # Return result and free receive buffer.
    obj = CArray2Obj(<void *>r, dataType, nElem, False)
    PyMem_Free(<void *>r)
    
    # Free source buffer.
    PyMem_Free(<void *>s)

    return obj


def MPY_Alltoall(msgSeq, dataType=MPY_PYTHON_OBJ,
                 long comm=MPY_COMM_WORLD):
    """
    Python wrapper around MPI_Alltoall() .

    MPY_Alltoall() and MPY_Alltoallv() have the same calling sequence.
    They differ from each other in that, with MPY_Alltoall(), all participating
    processes must send the same number of data elements to each other,
    whereas MPY_Alltoallv() allows each process to send a different number of
    data elements to each process.

    Params:
      msgSeq        Sequence of messages to scatter.
                    The length of this sequence must match the number of processes
                    inside the communicator, message at index 'i' being sent to
                    process of rank 'i'. Messages must be of the same length among
                    all processes inside the communicator.
      dataType      Message datatype.
      comm          Communicator handle.

    Returns:
        List holding the gathered messages, one per process inside the
        communicator. 

                                                                 """
    cdef long r, s, mpi_datatype, adr, adr0
    cdef int nElem, mxElem, chunkSize, size, rank

    size = MPY_Comm_size(comm)
    rank = MPY_Comm_rank(comm)

    # Compute the maximum number of elements among the messages to send.
    # Each proces will we sent a message with this number of elements.
    mxElem = 0
    for obj in msgSeq:
        if dataType == MPY_PYTHON_OBJ:
            nElem = lenPickle(obj)
        else:
            # Sequence
            if type(obj) in [types.TupleType, types.ListType, types.StringType]:
                nElem = len(obj)
            # Scalar.
            else:
                nElem = 1
        if nElem > mxElem:
            mxElem = nElem

    # Allocate a buffer to store the messages to send.
    s, mpi_datatype = prepRecv(mxElem * size, dataType)

    # Copy messages to this buffer, one per chunk.
    adr = s
    chunkSize = mxElem * dataTypeSize(dataType)   # in bytes
    for obj in msgSeq:
        adr0, nElem, mpi_datatype = obj2CArray(obj, dataType, <void *>adr)
        adr = adr + chunkSize

    # Allocate a receive buffer for all processes. The buffer will be divided
    # into chunks of size 'mxElem' data elements. Each value returned by member of rank
    # 'n' will be written to chunk number 'n'.
    r, mpi_datatype = prepRecv(mxElem * size, dataType)
            
    # Do the gather.
    res = MPI_Alltoall(<void *>s, nElem, <MPI_Datatype>mpi_datatype,
                       <void *>r, nElem, <MPI_Datatype>mpi_datatype,
                       <MPI_Comm>comm)
    checkErr(res, "MPY_Alltoall")

    # Dispose of the C source buffer.
    PyMem_Free(<void *>s)

    # Convert the receive buffer to a Python list.
    adr = r
    res = []
    for k in range(size):
        # Convert the contents of chunk 'k' to a Python
        # object, and append this object to the output list.
        res.append(CArray2Obj(<void *>adr, dataType, nElem, False))
        # Compute the offset of next chunk.
        adr = adr + chunkSize

    # Free receive buffer.
    PyMem_Free(<void *>r)

    # Return list
    return res


def MPY_Alltoallv(msgSeq, dataType=MPY_PYTHON_OBJ,
                  long comm=MPY_COMM_WORLD):
    """
    Python wrapper around MPI_Alltoallv() .

    MPY_Alltoall() and MPY_Alltoallv() have the same calling sequence.
    They differ from each other in that, with MPY_Alltoall(), all participating
    processes must send the same number of data elements to each other,
    whereas MPY_Alltoallv() allows each process to send a different number of
    data elements to each process.

    Params:
      msgSeq        Sequence of messages to scatter.
                    The length of this sequence must match the number of processes
                    inside the communicator, message at index 'i' being sent to
                    process of rank 'i'.
      dataType      Message datatype.
      comm          Communicator handle.

    Returns:
        list holding the gathered messages

                                                                                 """
    cdef long r, s, mpi_datatype, adr, adr0
    cdef int nElem, totElem, chunkSize, size, rank, p, dSize
    cdef int *sendCounts, *displ
    cdef int *nElemArr, *displArr, i

    size = MPY_Comm_size(comm)
    rank = MPY_Comm_rank(comm)

    # Compute the total number of elements among the messages to send.
    totElem = 0
    for obj in msgSeq:
        if dataType == MPY_PYTHON_OBJ:
            nElem = lenPickle(obj)
        else:
            # Sequence
            if type(obj) in [types.TupleType, types.ListType, types.StringType]:
                nElem = len(obj)
            # Scalar.
            else:
                nElem = 1
        totElem = totElem + nElem

    # Allocate a buffer to store the messages to send, their lengths and
    # their offsets.
    s, mpi_datatype = prepRecv(totElem, dataType)
    sendCounts = <int *>PyMem_Malloc(size * sizeof(int))
    displ      = <int *>PyMem_Malloc(size * sizeof(int))

    # Copy messages to this buffer. Setup length and offset arrays.
    adr = s
    p = 0
    dSize = dataTypeSize(dataType)
    for obj in msgSeq:
        adr0, nElem, mpi_datatype = obj2CArray(obj, dataType, <void *>adr)
        sendCounts[p] = nElem
        displ[p] = (adr - s) / dSize
        adr = adr + nElem * dSize
        p = p + 1

    # Allocate element and displacement arrays for the receive buffer.
    nElemArr = <int *>PyMem_Malloc(size * sizeof(int))
    displArr = <int *>PyMem_Malloc(size * sizeof(int))

    # Since the number of data elements can vary between participants,
    # we need to gather the size of the message that each is about to send.
    MPI_Alltoall(sendCounts, 1, MPI_INT, nElemArr, 1, MPI_INT, <MPI_Comm>comm)

    # Compute total number of data elements, and initialize displacement array.
    totElem = 0
    for i from 0 <= i < size:
        totElem = totElem + nElemArr[i]
        if i == 0:
            displArr[i] = 0
        else:
            displArr[i] = displArr[i-1] + nElemArr[i-1]

    # Allocate a receive buffer. The buffer will be divided
    # into chunks of size 'nElemArr[i]' data elements.
    # Each value returned by member of rank 'n' will be written
    # to chunk number 'n'.
    r, mpi_datatype = prepRecv(totElem, dataType)
            
    # Do the gather.
    res = MPI_Alltoallv(<void *>s, sendCounts, displ, <MPI_Datatype>mpi_datatype,
                        <void *>r, nElemArr, displArr, <MPI_Datatype>mpi_datatype,
                        <MPI_Comm>comm)
    checkErr(res, "MPY_Alltoallv")

    # Dispose of the C source buffer.
    PyMem_Free(<void *>s)
    PyMem_Free(<void *>sendCounts)
    PyMem_Free(<void *>displ)

    # Convert the receive buffer to a Python list.
    adr = <long>r
    res = []
    for k in range(size):
        # Convert the contents of chunk 'k' to a Python
        # object, and append this object to the output list.
        res.append(CArray2Obj(<void *>adr, dataType, nElemArr[k], False))
        # Compute the offset of next chunk.
        adr = adr + nElemArr[k] * dSize

    # Free receive buffer, element array and displacement array.
    PyMem_Free(<void *>r)
    PyMem_Free(<void *>nElemArr)
    PyMem_Free(<void *>displArr)
    
    # Return list
    return res

def MPY_Attr_delete(long comm, int keyval):
    """
    Python wrapper around MPI_Attr_delete() .

    Params:
      comm          Communicator handle.
      keyval        Key which identifyes the attribute. The attribute value
                    disappears, but the key remains.

    Returns:
      None
                                                                  """

    res = MPI_Attr_delete(<MPI_Comm>comm, keyval)
    checkErr(res, "MPY_Attr_delete")
    

def MPY_Attr_get(long comm, int keyval):
    """
    Python wrapper around MPI_Attr_get() .

    Params:
      comm          Communicator handle.
      keyval        Key which identifyes the attribute.

    Returns:
      2-elem tuple holding: boolean indicating if the attribute
      was set or not, followed by the attribute value (None if not set).
                                                                           """
    cdef int *val, flag
    
    res = MPI_Attr_get(<MPI_Comm>comm, keyval, &val, &flag)
    checkErr(res, "MPY_Attr_get")
    if flag:
        flag = True
    else:
        flag = False
    return flag, val[0]
    

def MPY_Attr_put(long comm, int keyval, int val):
    """
    Python wrapper around MPI_Attr_put() .

    Params:
      comm          Communicator handle
      keyval        Key which identifyes the attribute.
      val           Value to associate with the attribute.

    Returns:
      None
                                                             """

    res = MPI_Attr_put(<MPI_Comm>comm, keyval, &val)
    checkErr(res, "MPY_Attr_put")
    

def MPY_Barrier(long comm=MPY_COMM_WORLD):
    """
    Python wrapper around MPI_Barrier() .

    Params:
      comm          Communicator handle

    Returns:
      None

    Blocks until all communicator members have gone through the call to
    barrier().

                                                                             """

    res = MPI_Barrier(<MPI_Comm>comm)
    checkErr(res, "MPY_Barrier")


def MPY_Bcast(int root, msg=None, int nElem=0, dataType=MPY_PYTHON_OBJ, array=None,
              long comm=MPY_COMM_WORLD):
    """
    Python wrapper around MPI_Bcast()
    
    Params :
      root          Rank inside the communicator of the process issuing the
                    broadcast.
      msg           Message to broadcast, meaningfull only on the root process.
                    Ignored on a non-root process where this parameter can be
                    set to None (or simply omitted).
      nElem         Number of data elements in the broadcast. This parameter is
                    ignored when the message is broadcasted through a numeric
                    array (dataType==MPY_PYTHON_ARRAY), because the size of the
                    array automatically determines the number of data elements.
                    The sender and receiver must then use a compatible array
                    (same shape and type). Otherwise, omitting parameter 'nElem'
                    (or setting it to 0) on both the sender and the receiver sides
                    asks the sender to broadcast the number of data elements prior
                    to the broadcast of the message. Conversely, the receiver is
                    requested to acknowledge this broadcast prior to that of the
                    message itself. 
      dataType      Message transmission mode.
      array         Meaningfull only when dataType == MPY_PYTHON_ARRAY.
                    'array' then gives the Numeric array where
                    the broadcasted message is copied. On the sender side, this
                    parameter can be omitted, as the received message is always
                    identical to the sent message 'msg'.
      comm          Communicator handle
    
    Returns :
      Object broadcasted by root. Note that the message is broadcasted to every
      process inside the communicator, including the root itself.

                                     """
    cdef long s, mpi_datatype
    cdef int size, p
    cdef ArrayType arrayObj

    rank = MPY_Comm_rank(comm)
    # Remember if message size is omitted.
    size = nElem

    # Prepare buffer holding the message to broadcast.
    if rank == root:
        if msg is None:
            raise MPY_Error, "P%d bcast(): msg cannot be omitted " \
                  " on the sender side" % rank
        # Allocate and initialize send buffer. 'arrayObj' is meaningful only
        # when the object is to be sent using the MPY_PYTHON_ARRAY datatype.
        # It is returned to avoid the garbage collection of the array object
        # from which the internal buffer address 's' comes from. Simply ignore
        # 'arrayObj' and the object will be garbage collected when the function
        # returns.
        s, nElem, mpi_datatype, arrayObj = obj2CArray2(msg, dataType, NULLPT)
        
    # Broadcast/receive the message size if nElem was originally 0, unless
    # datatype is Numeric array.
    if size == 0 and dataType != MPY_PYTHON_ARRAY:
        res = MPI_Bcast(&nElem, 1, MPI_INT, root, <MPI_Comm>comm)
        
    # Allocate buffer to store message.
    if rank != root:
        # 'arrayObj' serves only when dataType==MPY_PYTHON_ARRAY, to avoid
        # the garbage collection of the python object to which buffer 's' belongs.
        if dataType == MPY_PYTHON_ARRAY and array is None:
            raise MPY_Error, "array parameter cannot be None on the receiver side " \
                             "when dataType == MPY_PYTHON_ARRAY"
        s, mpi_datatype, nElem, arrayObj = prepRecv2(nElem, array, dataType)
            
    # Broadcast or receive from a broadcast.
    res = MPI_Bcast(<void *>s, nElem, <MPI_Datatype>mpi_datatype,
                    root, <MPI_Comm>comm)
    checkErr(res, "MPY_Bcast")

    # Convert result to a python object and free C array, unless the output buffer
    # is a Numeric array.
    if dataType != MPY_PYTHON_ARRAY:
        obj = CArray2Obj(<void *>s, dataType, nElem, False)
        PyMem_Free(<void *>s)
    elif rank == root:
        obj = msg
    else:
        obj = array
        
    return obj


def MPY_Bsend(msg, int dest, dataType=MPY_PYTHON_OBJ,
              int tag=1, long comm=MPY_COMM_WORLD):
    """
    Python wrapper around MPI_Bsend()

    Params :
      msg           Message to send
      dest          Rank inside the communicator of the process to which the
                    message is sent
      dataType      Message transmission mode.
      tag           Numeric tag which can be used to identify this message.
      comm          Communicator handle

    Returns:
      None

                                     """

    cdef int nElem
    cdef long s, mpi_datatype
    cdef ArrayType arrayObj

    # Allocate and initialize send buffer. 'arrayObj' is meaningful only when the
    # object is to be sent using the MPY_PYTHON_ARRAY datatype. It is returned
    # to avoid the garbage collection of the array object from which the
    # internal buffer address 's' comes from. Simply ignore 'arrayObj' and the
    # object will be garbage collected when the function returns.
    s, nElem, mpi_datatype, arrayObj = obj2CArray2(msg, dataType, NULLPT)

    # Send message, buffered mode.
    res = MPI_Bsend(<void *>s, nElem, <MPI_Datatype>mpi_datatype,
                    dest, tag, <MPI_Comm>comm)

    if dataType != MPY_PYTHON_ARRAY:  # Do not free Numeric array internal buffer
        PyMem_Free(<void *>s)
        
    checkErr(res, "MPY_Bsend")


def MPY_Bsend_init(int dest, int nElem=0, dataType=MPY_PYTHON_OBJ, array=None,
               int tag=1, long comm=MPY_COMM_WORLD):
    """
    Python wrapper around MPI_Bsend_init().

    Params:
      dest          Rank inside the communicator of the process to which the
                    request will send messages.
      nElem         Number of data elements to send through the persistent request.
                    All messages sent with this request must be of the same size
                    (or less or equal to this size for dataType MPY_PYTHON_OBJ.
                    This parameter should be omitted if dataType==MPY_PYTHON_ARRAY,
                    since the size of the array determines the number of elements.
      dataType      Message transmission mode.
      array         If dataType==MPY_PYTHON_ARRAY, parameter 'array' must identify
                    the Numeric array which will hold the data to be sent.
      tag           Numeric tag which can be used to identify this message.
      comm          Communicator handle

    Returns:
      Persistent request handle. Pass this handle to requestLoad() to load
      a message inside the request buffer, unless dataType == MPY_PYTHON_ARRAY.
      In that case, simply load the data inside 'array'. Then call MPY_Start()
      to launch the send.
      Assert completion of the request by a call to a function of the MPY_Test() or
      MPY_Wait() family. Free request resources by calling MPY_Request_free().
                                                                               """

    cdef long s, mpi_datatype
    cdef MPI_Request request

    # Allocate buffer to store message.
    # 'arrayObj' serves only when dataType==MPY_PYTHON_ARRAY, to avoid the garbage
    # collection of the python object to which buffer 's' belongs. 
    s, mpi_datatype, nElem, arrayObj = prepRecv2(nElem, array, dataType)

    # Create permanent request.
    res = MPI_Bsend_init(<void *>s, nElem, <MPI_Datatype>mpi_datatype,
                         dest, tag, <MPI_Comm>comm, &request)
    checkErr(res, "MPY_Bsend_init")

    return Request(<long>request, s, receive=False, dataType=dataType,
                   array=arrayObj)
    
def MPY_Buffer_attach(int size):
    """
    Python wrapper around MPI_Buffer_attach().

    Params:
      size          Buffer size, in bytes

    Returns:
      None

    Allocates a buffer of size 'size' for buffered mode send operations.
    To free the bufer, call buffer_detach().

                                                                           """
    global _bufSpace
    cdef long l
    cdef void *buf

    # Buffer already attached : MPI will trap this as an error.
    # But at least free the memory we allocated.
    if _bufSpace != 0 :
        l = _bufSpace
        PyMem_Free(<void *>l)
    
    buf = <void *>PyMem_Malloc(size)
    _bufSpace = <long>buf
    res = MPI_Buffer_attach(buf, size)
    checkErr(res, "MPY_Buffer_attach")
    
    
def MPY_Buffer_detach():
    """
    Python wrapper around MPI_Buffer_detach()

    Params:
      None

    Returns:
      None

    Release the buffer allocated through buffer_attach().
                                                                         """

    cdef void *bufAddr
    cdef int size

    res = MPI_Buffer_detach(&bufAddr, &size)
    checkErr(res, "MPY_Buffer_detach")

    _bufSpace = 0

def MPY_Cancel(object request):
    """
    Python wrapper around MPI_Cancel() .

    Params:
      request       Request (persistent or non-persistent) identifying the
                    non-blocking operation to cancel. This operation can be
                    either a send or a receive.

    Returns:
      None

                                                 """

    cdef long l
    cdef MPI_Request mpi_request

    l = request.mpi_request
    mpi_request = <MPI_Request>l
    res = MPI_Cancel(&mpi_request)
    checkErr(res, "MPY_Cancel")

    # Update request object.
    request.mpi_request = <long>mpi_request

    # Free send buffer.
    if not request.receive and request.buf != 0:
        l = request.buf
        PyMem_Free(<char*>l)
        request.buf = <long>0
    

def MPY_Cart_coords(long comm, int rank):
    """
    Python wrapper around MPI_cart_coords() .

    Params:
      comm           Communicator
      rank           Process rank inside the communicator

    Returns:
      Sequence holding the corresponding process coordinates inside the
      cartesian topology.
                                                                 """

    cdef int *coords
    cdef int i, n, nDims

    nDims = MPY_Cartdim_get(comm)
    coords = <int *>PyMem_Malloc(nDims * sizeof(int))
    res = MPI_Cart_coords(<MPI_Comm>comm, rank, nDims, coords)
    checkErr(res, "MPY_Cart_coords")

    c = CArray2Obj(coords, MPY_INT, nDims, False)
    PyMem_Free(coords)

    return c

def MPY_Cart_create(long oldComm, object dims, object periodic=None,
                    object reorder=True):
    """
    Python wrapper around MPI_Cart_create() .

    Params:
      oldComm        Communicator on which to apply a cartesian topology
                     in order to create a new communicator.
      dims           Sequence of integers giving the size of each dimension
                     in the topology
      periodic       Sequence of booleans indicating if each dimension is
                     periodic or not. Defaults to True on all dimensions.
      reorder        Boolean indicating if processes can be reordered or not
                     in the new communicator. Defaults to True.

    Returns:
      New communicator.
    
                                                                  """

    cdef long dimsArr, perArr
    cdef int i,n
    cdef MPI_Comm newComm

    nDims = len(dims)
    if not periodic:
        periodic = (True,) * nDims
    dimsArr = obj2CArray(dims, MPY_INT, NULLPT)[0]
    perArr  = obj2CArray(periodic, MPY_INT, NULLPT)[0]
    res = MPI_Cart_create(<MPI_Comm>oldComm, nDims, <int *>dimsArr, <int *>perArr,
                          reorder, &newComm)
    checkErr(res, "MPY_Cart_create")

    PyMem_Free(<void *>dimsArr)
    PyMem_Free(<void *>perArr)

    return <long>newComm

def MPY_Cartdim_get(long comm):
    """
    Python wrapper around MPI_Cartdim_get() .

    Params:
      comm           Communicator.

    Returns:
      Number of dimensions in the cartesian topology
                                                             """

    cdef int nDims

    res = MPI_Cartdim_get(<MPI_Comm>comm, &nDims)
    checkErr(res, "MPY_Cartdim_get")

    return nDims
    

def MPY_Cart_get(long comm):
    """
    Python wapper around MPI_Cart_get() .

    Params:
      comm           Communicator.
    
    Returns:
      Tuple composed of the following 3 elements
        tuple of the dimension sizes
        tuple of the dimensions periodicity
        tuple of calling process coordinates in the cartesian topology

                                                            """

    cdef int *size, *period, *coord
    cdef int i, n, nDims

    nDims = MPY_Cartdim_get(comm)
    
    n = nDims * sizeof(int)
    size   = <int *>PyMem_Malloc(n)
    period = <int *>PyMem_Malloc(n)
    coord  = <int *>PyMem_Malloc(n)
    res = MPI_Cart_get(<MPI_Comm>comm, nDims, size, period, coord)
    checkErr(res, "MPY_Cart_get")

    sizeLst   = CArray2Obj(<void *>size,   MPY_INT, nDims, False)
    periodLst = CArray2Obj(<void *>period, MPY_INT, nDims, False)
    coordLst  = CArray2Obj(<void *>coord,  MPY_INT, nDims, False)
    
    PyMem_Free(size)
    PyMem_Free(period)
    PyMem_Free(coord)

    return sizeLst, periodLst, coordLst

def MPY_Cart_map(long comm, object dims, object periodic=None):
    """
    Python wrapper around MPI_Cart_map() .

    Params:
      comm           Input communicator.
      dims           Sequence of integers giving the size of each dimension
                     in the topology
      periodic       Sequence of booleans indicating if each dimension is
                     periodic or not. Defaults to True on all dimensions.

    Returns:
      Optimal rank of the calling process on the physical machine, or
      MPI_UNDEFINED if the calling process does not belong to the grid.
    
                                                                  """

    cdef long dimsArr, perArr
    cdef int i, n, newRank

    nDims = len(dims)
    if not periodic:
        periodic = (True,) * nDims
    dimsArr = obj2CArray(dims, MPY_INT, NULLPT)[0]
    perArr  = obj2CArray(periodic, MPY_INT, NULLPT)[0]
    res = MPI_Cart_map(<MPI_Comm>comm, nDims, <int *>dimsArr, <int *>perArr,
                       &newRank)
    checkErr(res, "MPY_Cart_map")

    PyMem_Free(<void *>dimsArr)
    PyMem_Free(<void *>perArr)

    return newRank


def MPY_Cart_rank(long comm, object coords):
    """
    Python wrapper around MPI_Cart_rank() .

    Params:
      comm           Communicator.
      coords         Sequence of integers giving the process coordinates in the
                     cartesian topology

    Returns:
      Rank of the process in the communicator.
                                                                  """

    cdef int rank
    cdef long arr

    arr = obj2CArray(coords, MPY_INT, NULLPT)[0]
    res = MPI_Cart_rank(<MPI_Comm>comm, <int *>arr, &rank)
    checkErr(res, "MPY_Cart_rank")
    
    PyMem_Free(<void *>arr)

    return rank
    

def MPY_Cart_shift(long comm, int dimension, int direction):
    """
    Python wrapper around MPI_Cart_shift() .

    Params:
      comm           Communicator.
      dimension      Cartesian dimension along which the shift is taking place.
      direction      Number of cells by which to shift along 'dimension'.

    Returns:
      2-elem tuple, giving the rank of the cell to shift data from,
      and the rank of the cell to shift data to. If wraparound is disabled
      along 'dimension', the source and destination ranks are set to MPI_NULL_PROC
      if the shift is outside of the grid.
                                                                     """

    cdef int src, dest
    
    res = MPI_Cart_shift(<MPI_Comm>comm, dimension, direction, &src, &dest)
    checkErr(res, "MPY_Cart_shift")

    return src, dest


def MPY_Cart_sub(long comm, object remainDims):
    """
    Python wrapper around MPI_Cart_sub() .

    Params:
      comm           Communicator.
      remainDims     Sequence of booleans indicating which dimension to keep
                     in the new communicator. The length of this sequence must equal
                     the number of dimensions in the cartesian communicator.
                     Element i of this sequence is true if the dimension must be
                     kept.

    Returns:
      New communicator to which the calling process belongs.
                                                                   """

    cdef long arr
    cdef MPI_Comm newComm

    arr = obj2CArray(remainDims, MPY_INT, NULLPT)[0]
    res = MPI_Cart_sub(<MPI_Comm>comm, <int *>arr, &newComm)
    checkErr(res, "MPY_Cart_sub")
    PyMem_Free(<void *>arr)

    return <long>newComm


def MPY_Comm_compare(long comm1, long comm2):
    """
    Python wrapper around MPI_Comm_compare() .

    Params:
      comm1          First communicator to compare.
      comm2          Second communicator to compare

    Returns:
      MPY_IDENT      if the comunicators are identical (same members in the same
                     order, and same context)
      MPY_CONGRUENT  if the communicators have the same members in the same order,
                     but not the same context
      MPY_SIMILAR    if the communicators have the same members, but not in the
                     same order
      MPY_UNEQUAL    otherwise
                                                                  """

    cdef int result

    res = MPI_Comm_compare(<MPI_Comm>comm1, <MPI_Comm>comm2, &result)
    checkErr(res, "MPY_Comm_compare")

    return result
    

def MPY_Comm_create(long comm, long group):
    """
    Python wrapper around MPI_Comm_create() .

    Params:
      comm           Communicator from which to create the new communicator.
      group          Group of processes belonging to 'comm' which are to become
                     members of the new communicator.

    Returns:
      Handle of the new communicator. The new communicator defines a new context
      for the processes contained inside 'group'.
    
    IMPORTANT: MPY_Comm_create is a collective communication operation. All processes
               belonging to 'comm' must call it. MPI_COMM_NULL is returned for
               processes that do not belong to the group.
                                                      """

    cdef MPI_Comm newComm
    
    res = MPI_Comm_create(<MPI_Comm>comm, <MPI_Group>group, &newComm)
    checkErr(res, "MPY_Comm_create")
    
    return <long>newComm


def MPY_Comm_dup(long comm):
    """
    Python wrapper around MPI_Comm_dup() .

    Params:
      comm           Communicator to duplicate.

    Returns:
      New communicator which duplicates 'comm', in a new context.

    IMPORTANT : MPY_Comm_dup is a collective call. Every member of the source
                communicator must call it.
                                                                            """

    cdef MPI_Comm new
    
    res = MPI_Comm_dup(<MPI_Comm>comm, &new)
    checkErr(res, "MPY_Comm_dup")

    return <long>new
    

def MPY_Comm_free(long comm):
    """
    Python wrapper around MPI_Comm_free() .

    Params:
      comm           Communicator to free. Upon return, the communicator
                     is invalid.

    Returns:
      MPY_COMM_NULL
    
                                                      """

    res = MPI_Comm_free(<MPI_Comm *>&comm)
    checkErr(res, "MPY_Comm_free")

    return comm
    

def MPY_Comm_group(long comm=MPY_COMM_WORLD):
    """
    Python wrapper around MPI_Comm_group() .

    Params:
      comm          Communicator handle.

    Returns:
      Group handle .
    
                                                      """

    cdef MPI_Group group
    cdef int res

    res = MPI_Comm_group(<MPI_Comm>comm, &group)
    checkErr(res, "MPY_Comm_group")
    
    return <long>group

def MPY_Comm_rank(long comm=MPY_COMM_WORLD):
    """
    Python wrapper around MPI_Comm_rank() .

    Params:
      comm          Communicator handle.

    Returns:
      Process rank inside the communicator .
    
                                                       """

    cdef int rank

    res = MPI_Comm_rank(<MPI_Comm>comm, &rank)
    checkErr(res, "MPY_Comm_rank")

    return rank


def MPY_Comm_remote_group(long comm=MPY_COMM_WORLD):
    """
    Python wrapper around MPI_Comm_remote_group() .

    Params:
      comm          Inter-communicator.

    Returns:
      Group at the remote side of the communicator.
    
                                                      """

    cdef MPI_Group group
    cdef int res

    res = MPI_Comm_remote_group(<MPI_Comm>comm, &group)
    checkErr(res, "MPY_Comm_remote_group")
    
    return <long>group


def MPY_Comm_remote_size(long comm=MPY_COMM_WORLD):
    """
    Python wrapper around MPI_Comm_remote_size() .

    Params:
      comm          Intra-communicator.

    Returns:
      Number of processes inside the group at the remote side of the communicator.
    
                                                          """

    cdef int size

    res = MPI_Comm_remote_size(<MPI_Comm>comm, &size)
    checkErr(res, "MPY_Comm_remote_size")
    
    return size


def MPY_Comm_size(long comm=MPY_COMM_WORLD):
    """
    Python wrapper around MPI_Comm_size() .

    Params:
      comm          Communicator handle.

    Returns:
      Number of processes inside the communicator group.
    
                                                          """

    cdef int size

    res = MPI_Comm_size(<MPI_Comm>comm, &size)
    checkErr(res, "MPY_Comm_size")
    
    return size

def MPY_Comm_split(long oldComm, partition, newRank):
    """
    Python wrapper around MPI_Comm_split() .

    Params:
      oldComm          Communicator handle.
      partition        Create a communicator for each distinct value of
                       'partition'. Set to MPY_UNDEFINED if the calling process
                       must not be assigned to a communicator.
      newRank          Within each communicator, order processes by the value
                       of 'newRank'.

    Returns:
      New communiator.

    IMPORTANT : MPY_Comm_split is a collective call. Every member of the source
                communicator must call it.
      
                                                     """
    cdef MPI_Comm newComm

    res = MPI_Comm_split(<MPI_Comm>oldComm, partition, newRank, &newComm)
    checkErr(res, "MPY_Comm_split")

    return <long>newComm

def MPY_Comm_test_inter(long comm):
    """
    Python wrappr around MPI_Comm_test_inter()  .

    Params:
      comm          Communicator

    Returns:
      True if 'comm' is an inter-communicator, false otherwise.
                                                                         """

    cdef int flag

    res = MPI_Comm_test_inter(<MPI_Comm>comm, &flag)
    checkErr(res, "MPY_Comm_test_inter")

    return flag


def MPY_Dims_create(int nNodes, object dims):
    """
    Python wrapper around MPI_Dims_create() .

    Params:
      nNodes        Number of nodes to allocate in a cartesian grid.
      dims          Sequence of integers constraining the suggested grid dimensions.
                    The length of this sequence gives the grid number of dimensions.
                    The suggested grid dimensions will be set to dims[i] wherever
                    dims[i] > 0. Where dims[i] == 0, the function will compute
                    an optimal value for dimension i.

    Returns:
      Tuple of integers listing the proposed grid dimensions.
                                                                             """

    cdef int nDims
    cdef long arr

    arr = obj2CArray(dims, MPY_INT, NULLPT)[0]
    nDims = len(dims)
    res = MPI_Dims_create(nNodes, nDims, <int *>arr)
    checkErr(res, "MPY_Dims_create")
    
    obj = CArray2Obj(<void *>arr, MPY_INT, nDims, False)
    PyMem_Free(<void *>arr)

    return obj


def MPY_Errhandler_get(long comm):
    """
    Python wrapper around MPI_Errhandler_get() .

    Params:
      comm          Communicator.

    Returns:
      Error handler associated with the communicator (handle).
                                                                         """
    cdef MPI_Errhandler handler

    res = MPI_Errhandler_get(<MPI_Comm>comm, &handler)
    checkErr(res, "MPY_Errhandler_get")

    return <long>handler

def MPY_Error_class(int errCode):
    """
    Python wrapper around MPI_Error_class() .

    Params:
      errCode          MPI error code.

    Returns
      Error class associated with given error code.
                                                                     """
    cdef int errClass

    res = MPI_Error_class(errCode, &errClass)
    checkErr(res, "MPY_Error_class")

    return errClass


def MPY_Errhandler_set(long comm, long handler):
    """
    Python wrapper around MPI_Errhandler_set() .

    Params:
      comm          Communicator.
      handler       Error handler : one of MPY_ERRORS_ARE_FATAL, MPY_ERRORS_RETURN.

    Returns:
      None
                                                                         """

    res = MPI_Errhandler_set(<MPI_Comm>comm, <MPI_Errhandler>handler)
    checkErr(res, "MPY_Errhandler_set")
    

def MPY_Error_string(int errCode):
    """
    Python wrapper around MPI_Error_string() .

    Params:
      errCode       MPI error code

    Returns:
      Error string associated with the given error code.
                                                                          """

    cdef char  str[256]
    cdef int   strLen

    res = MPI_Error_string(errCode, str, &strLen)
    checkErr(res, "MPY_Error_string")

    # Strip 'MPI_Error_string: ' header
    return PyString_FromStringAndSize(str, strLen).replace('MPI_Error_string: ', '')
    

def MPY_Finalize():
    """
    Python wrapper around MPI_Finalize() .

    Params:
      None

    Returns:
      None

    Put an end to the MPI environment.
                                                      """

    cdef int res

    res = MPI_Finalize()
    checkErr(res, "MPY_Finalize")
    

def MPY_Finalized():
    """
    Python wrapper around MPI_Finalized() .

    Params:
      None

    Returns:
      boolean indicating if a finalize() call has been executed to
      put an end to the MPI environment.
                                                                         """

    cdef int res, flag
    
    res = MPI_Finalized(&flag)
    checkErr(res, "MPY_Finalized")
    return flag

def MPY_Gather(msg, int root, dataType=MPY_PYTHON_OBJ, array=None,
               long comm=MPY_COMM_WORLD):
    """
    Python wrapper around MPI_Gather() .

    MPY_Gather() and MPY_Gatherv() have the same calling sequence. They differ
    from each other in that, with MPY_Gather(), all participating processes
    must send the same number of data elements, whereas MPY_Gatherv() allows
    each process to send a different number of data elements.

    When gathering messages sent as python objects, MPY_Gatherv() should
    be called rather than MPY_Gather() since it can be hard to predict
    the exact size of the string used to encapsulate a python object.
    Even if the objects contain the same number of elements of the same
    type, the magnitude of the element values may generate strings
    of different length. For example, lists [1,2,3] and [10001,10002,10002]
    each contain 3 integers, but their encapsulated length is different
    because of the magnitude of their respective values.

    Params:
      msg           Message which will be sent to root process. Note that
                    root itself sends this message. The number of data elements
                    is automatically determined. All messages sent by
                    participating processes must be of the same length.
                    If this is not the case, call MPY_Gatherv() instead.
                    If 'msg' is a Numeric array (dataType==MPY_PYTHON_ARRAY)
                    the message is made of the array elements sent in row major
                    order.
      root          Rank inside the communicator of the process which
                    gathers the messages.
      dataType      Message datatype.
      array         Significant only when dataType==MPY_PYTHON_ARRAY.
                    It then identifies the numeric array where the messages will
                    be gathered. Gathered messages will then be stored one after
                    another in rank order inside the array. The caller must
                    guarantee that the array type agrees with that of the
                    messages sent by the processes, and that the array size is
                    at least equal to the total number of data elements to be
                    gathered. If parameter 'array' is None, an output array
                    will be allocated whose shape will be (size, sh0, ...).
                    'size' is the number of processes in the communicator, and
                    'sh0, ...' is the shape of the gathered messages (all
                    messages are required to be of equal shape). The type of
                    the output array wil be set to that of the gathered messages.
      comm          Communicator handle.

    Returns:
      On the root process:
        If dataType==MPY_PYTHON_ARRAY, numeric array storing the gathered
        messages. Otherwise, List holding the gathered messages, one per
        process inside the communicator. Remember that the root process
        participates in the gather and thus sends a message to itself.

      On the non-root processes:
        None
      
                                                                 """
    cdef long r, s, mpi_datatype
    cdef int nElem, size, rank, chunkSize
    cdef ArrayType sendArrayObj, recvArrayObj
    cdef long adr

    size = MPY_Comm_size(comm)
    rank = MPY_Comm_rank(comm)

    # Allocate buffer to store message sent by all processes (root included).
    # 'sendArrayObj' is meaningful only when the message is to be sent using the
    # MPY_PYTHON_ARRAY datatype. It is returned to avoid the garbage collection
    # of the array object from which the internal buffer address 's' comes from.
    # Simply ignore 'arrayObj' and the object will be garbage collected when
    # the function returns.
    s, nElem, mpi_datatype, sendArrayObj = obj2CArray2(msg, dataType, NULLPT)

    # Allocate a receive buffer for root. The buffer will be divided
    # into chunks of size 'nElem' data elements. Each value returned by member
    # of rank 'n' will be written to chunk number 'n'.
    # 'recvArrayObj' serves only when dataType==MPY_PYTHON_ARRAY, to avoid
    # the garbage collection of the python object to which buffer 'r' belongs. 
    if rank == root:
        if dataType == MPY_PYTHON_ARRAY:
            # Allocate an output if array if none given. The shape of the output
            # array is (size, sh0) where 'size' is the communicator size, and
            # 'sh0' is the shape of the input messages (which must be identical).
            if array is None:
                array = Numeric.zeros((size,) + msg.shape, msg.typecode())
        else:
            chunkSize = nElem * dataTypeSize(dataType)   # CHECK
        r, mpi_datatype, dum, recvArrayObj = prepRecv2(nElem * size,
                                                       array, dataType)
            
    # The receive buffer is meaningless for non-root members.
    else:
        r = <long>NULLPT

    # Do the gather.
    res = MPI_Gather(<void *>s, nElem, <MPI_Datatype>mpi_datatype,
                     <void *>r, nElem, <MPI_Datatype>mpi_datatype,
                     root, <MPI_Comm>comm)
    checkErr(res, "MPY_Gather")

    # Simply return the array arg if a Numeric array was used to
    # send the message.
    if dataType == MPY_PYTHON_ARRAY:
        return array

    # Dispose of the C source buffer.
    PyMem_Free(<void *>s)

    # If root, convert the receive buffer to a Python list.
    if rank == root:
        adr = r
        res = []
        for k in range(size):
            # Convert the contents of chunk 'k' to a Python
            # object, and append this object to the output list.
            res.append(CArray2Obj(<void *>adr, dataType, nElem, False))
            # Compute the offset of next chunk.
            adr = adr + chunkSize

        # Free receive buffer.
        PyMem_Free(<void *>r)

        # Return list
        return res

    # Non-root processes receive nothing.

def MPY_Gatherv(msg, int root, dataType=MPY_PYTHON_OBJ, array=None,
                long comm=MPY_COMM_WORLD):
    """ 
    Python wrapper around MPI_Gatherv() .

    MPY_Gather() and MPY_Gatherv() have the same calling sequence. They differ from
    each other in that, with MPY_Gather(), all participating processes must send
    the same number of data elements, whereas MPY_Gatherv() allows each process to
    send a different number of data elements.

    When gathering messages sent as python objects, MPY_Gatherv() should
    be called rather than MPY_Gather() since it can be hard to predict
    the exact size of the string used to encapsulate a python object.
    Even if the objects contain the same number of elements of the same
    type, the magnitude of the element values may generate strings
    of different length. For example, lists [1,2,3] and [10001,10002,10002]
    each contain 3 integers, but their encapsulated length is different
    because of the magnitude of their respective values.

    Params:
      msg           Message which will be sent to root process. Note that
                    root itself sends this message. The number of data elements
                    is automatically determined. Each participant does not need
                    to send the same number of data elements, countrary to
                    function MPY_Gather() where each participant needs to send the
                    same number of data elements.
                    If 'msg' is a Numeric array (dataType==MPY_PYTHON_ARRAY)
                    the message is made of the array elements sent in row major
                    order.
      root          Rank inside the communicator of the process which
                    gathers the messages.
      dataType      Message datatype.
      array         Significant only when dataType==MPY_PYTHON_ARRAY.
                    It then identifies the numeric array where the messages will
                    be gathered. Gathered messages will then be stored one after
                    another in rank order inside the array. The caller must
                    guarantee that the array type agrees with that of the
                    messages sent by the processes, and that the array size is
                    at least equal to the total number of data elements to be
                    gathered. If parameter 'array' is None, an output array
                    will be allocated whose shape will be (size, sh0, ...).
                    'size' is the number of processes in the communicator, and
                         CHECK!!!
                    'sh0, ...' is the shape of the gathered messages (all
                    messages are required to be of equal shape). The type of
                    the output array wil be set to that of the gathered messages.
      comm          Communicator handle.

    Returns:
      On the root process:
        list holding the gathered messages

      On the non-root processes:
        None
      
                                                                 """
    cdef long r, s, mpi_datatype
    cdef int nElem, size, rank
    cdef long adr
    cdef ArrayType sendArrayObj, recvArrayObj
    cdef int *nElemArr, *displArr, i, totalElem, elemSize

    size = MPY_Comm_size(comm)
    rank = MPY_Comm_rank(comm)

    # Allocate buffer to store message sent by all processes (root included).
    # 'sendArrayObj' is meaningful only when the message is to be sent using the
    # MPY_PYTHON_ARRAY datatype. It is returned to avoid the garbage collection
    # of the array object from which the internal buffer address 's' comes from.
    # Simply ignore 'arrayObj' and the object will be garbage collected when
    # the function returns.
    s, nElem, mpi_datatype, sendArrayObj = obj2CArray2(msg, dataType, NULLPT)

    # On root, allocate element and displacement arrays.
    if rank == root:
        nElemArr = <int *>PyMem_Malloc(size * sizeof(int))
        displArr = <int *>PyMem_Malloc(size * sizeof(int))
    # Those arrays are meaningless on non-root processes.
    else:
        nElemArr = <int *>NULLPT
        displArr = <int *>NULLPT

    # Since the number of data elements can vary between participants,
    # we need to gather the size of the message that each is about to send.
    MPI_Gather(&nElem, 1, MPI_INT, nElemArr, 1, MPI_INT,
               root, <MPI_Comm>comm)

    # On root, compute total number of data elements, and initialize
    # displacement array.
    if rank == root:
        totalElem = 0
        for i from 0 <= i < size:
            totalElem = totalElem + nElemArr[i]
            if i == 0:
                displArr[i] = 0
            else:
                displArr[i] = displArr[i-1] + nElemArr[i-1]

    # Allocate a receive buffer for root. The buffer will be divided
    # into chunks of size 'nElemArr[i]' data elements.
    # Each value returned by member of rank 'n' will be written
    # to chunk number 'n'.
    # 'recvArrayObj' serves only when dataType==MPY_PYTHON_ARRAY, to avoid
    # the garbage collection of the python object to which buffer 'r' belongs. 
    if rank == root:
        if dataType == MPY_PYTHON_ARRAY:
            # Allocate an output if array if none given. The array is allocated
            # as one-dimensional, its size beingequal to the total number of elements
            # gathered. The calling program can reshape it later.
            if array is None:
                array = Numeric.zeros(totalElem, msg.typecode())
        r, mpi_datatype, dum, recvArrayObj = prepRecv2(totalElem, array, dataType)
            
    # The receive buffer is meaningless for non-root processes.
    else:
        r = <long>NULLPT

    # Do the gather.
    res = MPI_Gatherv(<void *>s, nElem, <MPI_Datatype>mpi_datatype,
                      <void *>r, nElemArr, displArr, <MPI_Datatype>mpi_datatype,
                      root, <MPI_Comm>comm)
    checkErr(res, "MPY_Gatherv")

    # Simply return the array arg if a Numeric array was used to
    # send the message.
    if dataType == MPY_PYTHON_ARRAY:
        return array
    
    # Dispose of the C source buffer.
    PyMem_Free(<void *>s)

    # If root, convert the receive buffer to a Python list.
    if rank == root:
        adr = r
        res = []
        elemSize = dataTypeSize(dataType)
        for k in range(size):
            # Convert the contents of chunk 'k' to a Python
            # object, and append this object to the output list.
            res.append(CArray2Obj(<void *>adr, dataType, nElemArr[k], False))
            # Compute the offset of next chunk.
            adr = adr + nElemArr[k] * elemSize

        # Free receive buffer, element array and displacement array.
        PyMem_Free(<void *>r)
        PyMem_Free(<void *>nElemArr)
        PyMem_Free(<void *>displArr)

        # Return list
        return res

    # Non-root processes receive nothing.

def MPY_Get_count(status, dataType=MPY_PYTHON_OBJ):
    """
    Python wrapper around MPI_Get_count() .

    Params:
      status        Status object returned by a receive operation
      dataType      Data transmission mode

    Returns:
      Number of data elements returned by the receive operation

    For a message exchanged as a python object, the length represents
    the length of the encapsulated message. It does not mean much, except when
    one wants to tune the size of a receive buffer.
                                                                               """
    cdef int nElem, sizeElem

    # NOTE: We cannot call MPI_Get_count(). For an unknown reason, it seems
    # impossible to recreate an MPI_Status struct from a Status python object,
    # even if all the fields look the same.
    
    # Obtain element size.
    sizeElem = dataTypeSize(dataType)

    # Compute number of elements. If the length is not an exact multiple
    # of the element size, return MPY_UNDEFINED.
    nElem = status.length / sizeElem
    if nElem * sizeElem != status.length:
        nElem = MPY_UNDEFINED

    return nElem
      

def MPY_Get_processor_name():
    """
    Python wrapper around MPI_Get_processor_name() .

    Params:
      None

    Returns:
      Name of the processor executing the call.
                                                       """

    cdef char name[256]
    cdef int l, res
        
    res = MPI_Get_processor_name(name, &l)
    checkErr(res, "MPY_Get_processor_name")
    nm = name[:l]

    return nm


def MPY_Get_version():
    """
    Python wrapper around MPI_Get_version() .

    Params:
      None

    Returns:
      2-elem tuple holding the major and minor MPI version numbers.
                                                                        """
    cdef int major, minor

    res = MPI_Get_version(&major, &minor)
    checkErr(res, "MPY_Get_version")

    return major, minor


def MPY_Graph_create(long oldComm, object index, object edges,
                     object reorder=True):
    """
    Python wrapper around MPI_Graph_create() .

    Params:
      oldComm        Communicator on which to apply a graph topology
                     in order to create a new communicator.
      index          Sequence of integers whose length gives the number of nodes
                     in the graph. Element i gives the total number of neighbors
                     if the first i graph nodes.
      edges          Sequence of integers listing the neightbors of each nodes,
                     in node order.
      reorder        Boolean indicating if processes can be reordered or not
                     in the new communicator. Defaults to True.

    Returns:
      New communicator.


    To find the neighbors of node i, obtain j=index[i]-1 and k=index[i-1],
    and extract edges[n] where j <= n <= k
    
                                                                  """

    cdef long idxArr, edgArr
    cdef int nNodes
    cdef MPI_Comm newComm

    nNodes  = len(index)
    idxArr  = obj2CArray(index, MPY_INT, NULLPT)[0]
    edgArr  = obj2CArray(edges, MPY_INT, NULLPT)[0]
    res = MPI_Graph_create(<MPI_Comm>oldComm, nNodes, <int *>idxArr, <int *>edgArr,
                          reorder, &newComm)
    checkErr(res, "MPY_Graph_create")

    PyMem_Free(<void *>idxArr)
    PyMem_Free(<void *>edgArr)

    return <long>newComm


def MPY_Graphdims_get(long comm):
    """
    Python wrapper around MPI_Graphdims_get() .

    Params:
      comm           Communicator with a graph topology applied.

    Returns:
      2-elem tuple, with the graph number of nodes and the graph number of
      edges.
                                                                 """

    cdef int nNodes, nEdges

    res = MPI_Graphdims_get(<MPI_Comm>comm, &nNodes, &nEdges)
    checkErr(res, "MPY_Graphdims_get")
    
    return nNodes, nEdges


def MPY_Graph_map(long oldComm, object index, object edges):
    """
    Python wrapper around MPI_Graph_map() .

    Params:
      oldComm        Communicator on which to apply a graph topology.
      index          Sequence of integers whose length gives the number of nodes
                     in the graph. Element i gives the total number of neighbors
                     if the first i graph nodes.
      edges          Sequence of integers listing the neighbors of each nodes,
                     in node order.

    Returns:
      Optimal rank of the calling process in the graph topology.


    Parameters'index' and 'edges' are as for MPY_Graph_create().
                                                                  """

    cdef long idxArr, edgArr
    cdef int nNodes, newRank

    nNodes  = len(index)
    idxArr  = obj2CArray(index, MPY_INT, NULLPT)[0]
    edgArr  = obj2CArray(edges, MPY_INT, NULLPT)[0]
    res = MPI_Graph_map(<MPI_Comm>oldComm, nNodes, <int *>idxArr, <int *>edgArr,
                        &newRank)
    checkErr(res, "MPY_Graph_map")

    PyMem_Free(<void *>idxArr)
    PyMem_Free(<void *>edgArr)

    return newRank


def MPY_Graph_neighbors(long comm, int rank):
    """
    Python wrapper around MPI_Graph_neighbors() .

    Params:
      comm           Communicator with a graph topology applied.
      rank           Rank of the process for which the neighbor list
                     is requested.

    Returns:
      List holding the ranks of the neighbors of process 'rank'.
                                                                            """

    cdef int count, *neighbors

    count = MPY_Graph_neighbors_count(comm, rank)
    neighbors = <int *>PyMem_Malloc(count * sizeof(int))
    res = MPI_Graph_neighbors(<MPI_Comm>comm, rank, count, neighbors)
    checkErr(res, "MPY_Graph_neighbors")

    obj = CArray2Obj(neighbors, MPY_INT, count, False)
    PyMem_Free(neighbors)

    return obj


def MPY_Graph_neighbors_count(long comm, int rank):
    """
    Python wrapper around MPI_Graph_Neighbors_count() .

    Params:
      comm           Communicator with a graph topology applied.
      rank           Rank of the process for which the count of neighbors
                     is requested.

    Returns:
      Number of neighbors.
                                                                                """

    cdef int nNeighbors

    res = MPI_Graph_neighbors_count(<MPI_Comm>comm, rank, &nNeighbors)
    checkErr(res, "MPY_Graph_neighbors_count")
    
    return nNeighbors
    

def MPY_Graph_get(long comm):
    """
    Python wrapper around MPI_Graph_get() .

    Params:
      comm           Communicator with a graph topology applied.

    Returns:
      2-elem tuple. First element is a tuple with the graph 'index' values.
      Second element is a tupel with the graph 'edges' values.
      'index' and 'edges' are as defined in the MPY_Graph_create() call.
                                                                              """
    cdef int maxIndex, maxEdges, n
    cdef int  *index, *edges

    maxIndex, maxEdges = MPY_Graphdims_get(comm)
    index = <int *>PyMem_Malloc(maxIndex * sizeof(int))
    edges = <int *>PyMem_Malloc(maxEdges * sizeof(int))

    res = MPI_Graph_get(<MPI_Comm>comm, maxIndex, maxEdges, index, edges)
    checkErr(res, "MPY_Graph_get")

    idxObj = CArray2Obj(index, MPY_INT, maxIndex, False)
    edgObj = CArray2Obj(edges, MPY_INT, maxEdges, False)

    PyMem_Free(index)
    PyMem_Free(edges)

    return idxObj, edgObj


def MPY_Group_compare(long group1, long group2):
    """
    Python wrapper around MPI_Group_compare() .

    Params:
      group1        Group handle of first group to compare.
      group2        Group handle of second group to compare.

    Returns:
      MPY_IDENT     if the group members and the group order are identical
      MPY_SIMILAR   if the group members are similar, but their order is different
      MPY_UNEQUAL   otherwise
                                                                           """

    cdef int result
    
    res = MPI_Group_compare(<MPI_Group>group1, <MPI_Group>group2, &result)
    checkErr(res, "MPY_Group_compare")

    return result

def MPY_Group_difference(long group1, long group2):
    """
    Python wrapper around MPI_Group_difference() .

    Params:
      group1        Handle of group from which to remove members.
      group2        Handle of group holding members to remove

    Returns:
      New group composed of all members of group1 that are not in group2.
      Members are ordered as in group1.
                                                                           """

    cdef MPI_Group new
    
    res = MPI_Group_difference(<MPI_Group>group1, <MPI_Group>group2, &new)
    checkErr(res, "MPY_Group_difference")

    return <long>new


def MPY_Group_excl(long group, object ranks):
    """
    Python wrapper around MPI_Group_excl() .

    Params:
      group         Handle of the group to which the ranks refer.
      ranks         Sequence of ranks inside group.

    Returns:
      New group whose members are the processes inside 'group', minus
      the ranks listed in sequence 'ranks'.
    
                                                   """
    cdef int n, i
    cdef int *a
    cdef MPI_Group new

    n = len(ranks)
    a = <int *>PyMem_Malloc(n * sizeof(int))
    for i from 0 <= i < n:
        a[i] = ranks[i]
    res = MPI_Group_excl(<MPI_Group>group, n, a, &new)
    checkErr(res, "MPY_Group_excl")

    PyMem_Free(a)

    return <long>new

def MPY_Group_free(long group):
    """
    Python wrapper around MPI_Group_free() .

    Params:
      group         Group to free (handle). Upon return, the value of
                    'group' is invalid.
    
    Returns:
      MPI_GROUP_NULL
                                                      """

    res = MPI_Group_free(<MPI_Group *>&group)
    checkErr(res, "MPI_Group_free")
    
    return group
    

def MPY_Group_incl(long group, object ranks):
    """
    Python wrapper around MPI_Group_incl() .

    Params:
      group         Handle of the group to which the ranks refer.
      ranks         Sequence of ranks inside group.

    Returns:
      New group whose members are the processes listed in sequence 'ranks'.
    
                                                   """

    cdef int n, i
    cdef int *a
    cdef MPI_Group new

    n = len(ranks)
    a = <int *>PyMem_Malloc(n * sizeof(int))
    for i from 0 <= i < n:
        a[i] = ranks[i]
    res = MPI_Group_incl(<MPI_Group>group, n, a, &new)
    checkErr(res, "MPY_Group_incl")

    PyMem_Free(a)

    return <long>new

def MPY_Group_intersection(long group1, long group2):
    """
    Python wrapper around MPI_Group_intersection() .

    Params:
      group1        Handle of first group.
      group2        Handle of second group.

    Returns:
      New group composed of all members both in group1 and group2.
      Members are ordered as in group1.
                                                                           """

    cdef MPI_Group new
    
    res = MPI_Group_intersection(<MPI_Group>group1, <MPI_Group>group2, &new)
    checkErr(res, "MPY_Group_intersection")

    return <long>new


def MPY_Group_range_excl(long group, object ranges):
    """
    Python wrapper around MPI_Group_range_excl() .
    
    Params:
      group         Group handle.
      ranges        Sequences of sequences. Each level-2 sequence holds 3 integers
                    defining a subset of members of 'group' to exclude from the
                    new group. Those 3 ints are : starting rank, ending rank,
                    and stride between successive ranks to exclude. The stride can be
                    < 0, allowing the starting rank to be greater than the
                    ending rank.

    Returns :
      New group.
                                                                                """

    cdef int n, *rnks
    cdef long adr, chunkSize
    cdef MPI_Group new

    if not type(ranges) in [types.ListType, types.TupleType]:
        raise MPY_Error, "MPY_Groupe_range_excl : ranges arg not a sequence"
    for triplet in ranges:
        if not type(triplet) in [types.ListType, types.TupleType] or \
               len(triplet) != 3:
            raise MPY_Error, "MPY_Group_range_excl : 'ranges' elems must be triplets"
        
    n = len(ranges)        # number of triplets
    chunkSize = 3 * sizeof(int *)
    rnks = <int *>PyMem_Malloc(n * chunkSize)

    # Copy triplets inside C array.
    adr = <long>rnks
    for triplet in ranges:
        obj2CArray(triplet, MPY_INT, <void *>adr)
        adr = adr + chunkSize

    # Call MPI
    res = MPI_Group_range_excl(<MPI_Group>group, n, <int (*)[3]>rnks, &new)
    checkErr(res, "MPY_Group_range_excl")

    # Free allocated memory.
    PyMem_Free(rnks)

    return <long>new
    
def MPY_Group_range_incl(long group, object ranges):
    """
    Python wrapper around MPI_Group_range_incl() .
    
    Params:
      group         Group handle.
      ranges        Sequences of sequences. Each level-2 sequence holds 3 integers
                    defining a subset of members of 'group' to include in the
                    new group. Those 3 ints are : starting rank, ending rank,
                    and stride between successive ranks to include. The stride can be
                    < 0, allowing the starting rank to be greater than the
                    ending rank.

    Returns :
      New group.
                                                                                """

    cdef int n, *rnks
    cdef long adr, chunkSize
    cdef MPI_Group new

    if not type(ranges) in [types.ListType, types.TupleType]:
        raise MPY_Error, "MPY_Groupe_range_incl : ranges arg not a sequence"
    for triplet in ranges:
        if not type(triplet) in [types.ListType, types.TupleType] or \
               len(triplet) != 3:
            raise MPY_Error, "MPY_Group_range_incl : 'ranges' elems must be triplets"
        
    n = len(ranges)        # number of triplets
    chunkSize = 3 * sizeof(int *)
    rnks = <int *>PyMem_Malloc(n * chunkSize)

    # Copy triplets inside C array.
    adr = <long>rnks
    for triplet in ranges:
        obj2CArray(triplet, MPY_INT, <void *>adr)
        adr = adr + chunkSize

    # Call MPI
    res = MPI_Group_range_incl(<MPI_Group>group, n, <int (*)[3]>rnks, &new)
    checkErr(res, "MPY_Group_range_incl")

    # Free allocated memory.
    PyMem_Free(rnks)

    return <long>new
    
def MPY_Group_rank(long group):
    """
    Python wrapper around MPI_Group_rank() .

    Params:
      group         Group handle.

    Returns :
      Rank of the calling process inside the group, or MPY_UNDEFINED
      if the process is not a member.
                                                                        """
    cdef int rank
    
    res = MPI_Group_rank(<MPI_Group>group, &rank)
    checkErr(res, "MPY_Group_rank")

    return rank

def MPY_Group_size(long group):
    """
    Python wrapper around MPI_Group_size() .

    Params:
      group         Group handle.

    Returns :
      Number of processes inside the group.
                                                                        """
    cdef int size
    
    res = MPI_Group_size(<MPI_Group>group, &size)
    checkErr(res, "MPY_Group_size")

    return size

def MPY_Group_translate_ranks(long group1, object rank1, long group2):
    """
    Python wrapper around MPI_Group_translate_ranks() .

    Params:
      group1        Group to which refer the ranks listed inside 'rank1'.
      rank1         Sequence of ranks inside group 'group1'
      group2        Group for which we want to compute the corresponding ranks.

    Returns:
      List of ranks inside 'group2' corresponding to ranks listed
      inside sequence 'rank1'. If a rank of 'group1' has no correspondence
      inside 'group2', MPY_UNDEFINED is stored in the returned list.
                                                                            """

    cdef int i, n
    cdef int *a1, *a2
    
    n = len(rank1)
    a1 = <int *>PyMem_Malloc(n * sizeof(int))
    a2 = <int *>PyMem_Malloc(n * sizeof(int))
    for i from 0 <= i < n:
        a1[i] = rank1[i]
    res = MPI_Group_translate_ranks(<MPI_Group>group1, n, a1,
                                    <MPI_Group>group2, a2)
    checkErr(res, "MPY_Group_translate_ranks")

    l = CArray2Obj(a2, MPY_INT, n, False)

    PyMem_Free(a1)
    PyMem_Free(a2)
    
    return l

def MPY_Group_union(long group1, long group2):
    """
    Python wrapper around MPI_Group_union() .

    Params:
      group1        Handle of first group.
      group2        Handle of second group.

    Returns:
      New group composed of all members in group1 followed by those of
      group2 not in group1.
                                                                           """

    cdef MPI_Group new
    
    res = MPI_Group_union(<MPI_Group>group1, <MPI_Group>group2, &new)
    checkErr(res, "MPY_Group_union")

    return <long>new

def MPY_Ibsend(msg, int dest, dataType=MPY_PYTHON_OBJ,
               int tag=1, long comm=MPY_COMM_WORLD):
    """
    Python wrapper around MPI_Ibsend() .

    Params:
      msg           Message to send
      dest          Rank inside communicator of the process to which to send
                    the message
      dataType      Message transmission mode.
      tag           Numeric tag which can be used to identify this message.
      comm          Communicator handle.

    Returns:
      Request handle. This object can be passed to a function of the test()
      or wait() family to monitor the call completion.
      
                                                                               """

    cdef int nElem
    cdef long s, mpi_datatype
    cdef ArrayType arrayObj
    cdef MPI_Request request

    # Allocate and initialize send buffer. 'arrayObj' is meaningful only when the
    # object is to be sent using the MPY_PYTHON_ARRAY datatype. It is returned
    # to avoid the garbage collection of the array object from which the
    # internal buffer address 's' comes from. Simply ignore 'arrayObj' and the
    # object will be garbage collected when the function returns.
    s, nElem, mpi_datatype, arrayObj = obj2CArray2(msg, dataType, NULLPT)

    # Send message, immediate buffered mode
    res = MPI_Ibsend(<void *>s, nElem, <MPI_Datatype>mpi_datatype,
                     dest, tag, <MPI_Comm>comm, &request)
    checkErr(res, "MPY_Ibsend")

    return Request(<long>request, s, receive=False, dataType=dataType,
                   array=arrayObj)
    
def MPY_Init(argv=sys.argv):
    """
    Python wrapper around MPI_Init() .

    Params:
      argv          List of command line arguments.

    Returns:
      None

                                                 """

    cdef char **a
    cdef int k, n
    cdef MPI_Group group

    # Allocate arg buffer.
    n = len(argv)
    a = <char **>PyMem_Malloc((n + 1) * sizeof(char *)) # +1 for trailing NULL
    # Recreate command string inside arg buffer.
    for k from 0 <= k < n:
        x = argv[k]         # This assignment avoids a warning
        a[k] = x
    a[k] = NULL

    # Initialize MPI function.
    res = MPI_Init(&n, &a)

    # Test for error.
    checkErr(res, "MPY_Init")

    # Create private communicator.
    MPI_Comm_group(MPI_COMM_WORLD, &group)
    MPI_Comm_create(MPI_COMM_WORLD, group, &priv_comm)
    MPI_Comm_group(priv_comm, &priv_group)
    MPI_Group_free(&group)
    

def MPY_Initialized():
    """
    Python wrapper around MPI_Initialized() .

    Params:
      None

    Returns:
      Boolean indicating if the MPI environment has been initialized
      through a call to init().
                                                 """

    cdef int res, flag
    
    res = MPI_Initialized(&flag)
    checkErr(res, "MPY_Initialized")

    return flag


def MPY_Intercomm_create(long localComm, int localLeader,
                         long peerComm, int remoteLeader, int tag):
    """
    Python wrapper around MPI_Intercomm_create() .

    Params:
      localComm     Local intra-communicator (handle). The two intra-communicators
                    joined in an inter-communicator must be disjoint.
      localLeader   Rank inside 'localComm' of a process which can act as as a
                    leader for the local group, eg communicate with a process of
                    the remote communicator through 'peerCom'.
      peerComm      Communicator used to enable communication between  remote leaders
                    on both sides.
      remoteLeader  Rank inside 'peerComm' of a process which can act as a leader
                    for the remote group. 'remoteLeader' must be a member of
                    'peerCom'.

    Returns:
      Inter-communicator.

    To create an inter-communicator, a common communicator ('peerComm')
    must be given that contains a member of each intra-communicator side.
    MPY_COMM_WORLD can always be used here. A local leader is then selected
    among the members of each side. The rank of the local leader is then
    then translated to the corresponding rank inside 'peerCom'. This is the
    value to use for param 'remoteLeader' when calling MPY_Intercomm_create()
    on the opposite side.

    Suppose for ex. that MPY_COMM_WORLD holds 4 processes, and that
    we create two intra-communicators containing even (0, 2) and odd (1, 3) processes.
    We could do the following to create an inter-communicator connecting the
    two intra-communicators.

      rank = MPY_Comm_rank()
      comm = MPY_Comm_split(MPY_COMM_WORLD, rank % 2 == 0, rank)
      if rank % 2 == 0:
          # local leader maps to 0 in MPY_COMM_WORLD, so use that
          # rank as the remote leader in the second call
          # Rank 1 is used as the local leader in the second call.
          # This maps to 3 in MPY_COMM_WORLD, so use that rank as the
          # value of remote leader in the first call.
          interComm = MPY_Intercomm_create(comm, 0, MPY_COMM_WORLD, 3, tag)
      else:
          interComm = MPY_Intercomm_create(comm, 1, MPY_COMM_WORLD, 0, tag)

                                                                       """

    cdef MPI_Comm newIntercomm

    res = MPI_Intercomm_create(<MPI_Comm>localComm, localLeader,
                               <MPI_Comm>peerComm, remoteLeader,
                               tag, &newIntercomm)
    checkErr(res, "MPY_Intercomm_create")
                    
    return <long>newIntercomm

def MPY_Intercomm_merge(long intercomm, int high):
    """
    Python wrapper around MPI_Intercomm_merge() .

    Params:
      intercomm     Inter-communicator (handle).
      high          True to order members of the group to which the calling
                    process belongs at the end of the merged group.

    Returns:
      New intracommunicator which merges the members of the two groups forming the
      inter-communicator.
                                                                        """

    cdef MPI_Comm newComm

    res = MPI_Intercomm_merge(<MPI_Comm> intercomm, high, &newComm)
    checkErr(res, "MPY_Intercomm_merge")
                    
    return <long>newComm
    

def MPY_Iprobe(int source=MPY_ANY_SOURCE, int tag=MPY_ANY_TAG,
               long comm=MPY_COMM_WORLD, retStatus=False):
    """
    Python wrapper around MPI_Iprobe() .

    Params:
      source        Rank inside the communicator of the process which sent the
                    message to probe, or MPY_ANY_SOURCE to probe messages
                    from any source.
      tag           Numeric tag identifying the message to probe, or MPY_ANY_TAG
                    to ignore message tags.
      comm          Communicator handle.
      retStatus     True to have the function return a Status object in addition
                    to its normal result. This object tells additional info
                    about the probed message.

    Returns:
      Boolean indicating if a message is waiting, but without consuming it.
      If 'retStatus' is true, the function returns a tuple whose 2nd element
      is a Status object holding the operation status. If the first tuple element
      is false (no message waiting), then the contents of Status are undefined. 

    probe() blocks until a message is waiting, but without consuming it.
    iprobe() serves same purpose, but does not block if no message is waiting.
                                                                                 """

    cdef MPI_Status status
    cdef int flag

    res = MPI_Iprobe(source, tag, <MPI_Comm>comm, &flag, &status)
    chekErr(res, "MPY_Iprobe")

    ret = [flag]
    if retStatus:
        ret.append(Status(status.MPI_SOURCE, status.MPI_TAG, 
                          status.MPI_ERROR, status.st_length))
    if len(ret) == 1:
        return ret[0]
    else:
        return tuple(ret)


def MPY_Irecv(int source, int nElem=0, dataType=MPY_PYTHON_OBJ, array=None,
              int tag=MPY_ANY_TAG, long comm=MPY_COMM_WORLD):
    """
    Python wrapper around MPI_Irecv() .

    Params:
      source        Rank inside communicator of the process from which to receive
                    the message.
      nElem         Maximum number of data elements inside the message to receive.
                    Neeeded only when dataType != MPY_PYTHON_ARRAY.
                    When passed the request object created by irecv(),
                    function requestExtract() will determine the effective length.
      dataType      Message transmission mode.
      array         If dataType==MPY_PYTHON_ARRAY, parameter 'array' must identify
                    the Numeric array into which to store the received data.
                    The caller must make sure that this array is compatible
                    with the one to be received (size and datatype); its shape can
                    always be modified afterwards.
      tag           Numeric tag identifying the message to receive, or MPY_ANY_TAG
                    to ignore message tags.
      comm          Communicator handle.
                    
    Returns:
      Request handle. This object can be passed to a function of the test()
      or wait() family to monitor the call completion. Once the operation has
      completed, call requestExtract() to retrieve the message contents, except if
      the message is received inside a numeric array. In that case, simply access
      the array instead.

                                                                                """
    cdef long s, mpi_datatype
    cdef ArrayType arrayObj
    cdef MPI_Request request

    # Allocate buffer to store message
    # 'arrayObj' serves only when dataType==MPY_PYTHON_ARRAY, to avoid the garbage
    # collection of the python object to which buffer 's' belongs. 
    s, mpi_datatype, nElem, arrayObj = prepRecv2(nElem, array, dataType)

    # Receive message, immediate mode
    res = MPI_Irecv(<void *>s, nElem, <MPI_Datatype>mpi_datatype,
                    source, tag, <MPI_Comm>comm, &request)
    checkErr(res, "MPY_Irecv")

    return Request(<long>request, s, receive=True, dataType=dataType, array=arrayObj)


def MPY_Irsend(msg, int dest, dataType=MPY_PYTHON_OBJ,
               int tag=1, long comm=MPY_COMM_WORLD):
    """
    Python wrapper around MPI_Irsend() .

    Params:
      msg           Message to send.
      dest          Rank inside communicator of the process to which to send
                    the message.
      dataType      Message transmission mode.
      tag           Numeric tag which can be used to identify the message.
      comm          Communicator handle.

    Returns:
      Request handle. This object can be passed to a function of the test()
      or wait() family to monitor the call completion.
                
                                                                                """

    cdef int nElem
    cdef long s, mpi_datatype
    cdef ArrayType arrayObj
    cdef MPI_Request request

    # Allocate and initialize send buffer. 'arrayObj' is meaningful only when the
    # object is to be sent using the MPY_PYTHON_ARRAY datatype. It is returned
    # to avoid the garbage collection of the array object from which the
    # internal buffer address 's' comes from. Simply ignore 'arrayObj' and the
    # object will be garbage collected when the function returns.
    s, nElem, mpi_datatype, arrayObj = obj2CArray2(msg, dataType, NULLPT)

    # Send message, ready mode
    res = MPI_Irsend(<void *>s, nElem, <MPI_Datatype>mpi_datatype,
                     dest, tag, <MPI_Comm>comm, &request)
    checkErr(res, "MPY_Irsend")

    return Request(<long>request, s, receive=False, dataType=dataType,
                   array=arrayObj)


def MPY_Isend(msg, int dest, dataType=MPY_PYTHON_OBJ,
              int tag=1, long comm=MPY_COMM_WORLD):
    """
    Python wrapper around MPI_Isend() .

    Params:
      msg           Message to send
      dest          Rank inside communicator of the process to which to send
                    the message
      dataType      Message transmission mode.
      tag           Numeric tag which can be used to identify this message.
      comm          Communicator handle.

    Returns:
      Request handle. This object can be passed to a function of the test()
      or wait() family to monitor the call completion.

                                                                               """

    cdef int nElem
    cdef long s, mpi_datatype
    cdef ArrayType arrayObj
    cdef MPI_Request request

    # Allocate and initialize send buffer. 'arrayObj' is meaningful only when the
    # object is to be sent using the MPY_PYTHON_ARRAY datatype. It is returned
    # to avoid the garbage collection of the array object from which the
    # internal buffer address 's' comes from. Simply ignore 'arrayObj' and the
    # object will be garbage collected when the function returns.
    s, nElem, mpi_datatype, arrayObj = obj2CArray2(msg, dataType, NULLPT)

    # Send message, immediate mode.
    res = MPI_Isend(<void *>s, nElem, <MPI_Datatype>mpi_datatype,
                    dest, tag, <MPI_Comm>comm, &request)
    checkErr(res, "MPY_Isend")

    return Request(<long>request, s, receive=False, dataType=dataType,
                   array=arrayObj)
    

def MPY_Issend(msg, int dest, dataType=MPY_PYTHON_OBJ,
               int tag=1, long comm=MPY_COMM_WORLD):
    """
    Python wrapper around MPI_Issend()

    Params:
      msg           Message to send
      dest          Rank inside communicator of the process to which to send
                    the message
      dataType      Message transmission mode.
      tag           Numeric tag which can be used to identify this message.
      comm          Communicator handle.

    Returns:
      Request handle. This object can be passed to a function of the test()
      or wait() family to monitor the call completion.

                                                                               """

    cdef int nElem
    cdef long s, mpi_datatype
    cdef ArrayType arrayObj
    cdef MPI_Request request

    # Allocate and initialize send buffer. 'arrayObj' is meaningful only when the
    # object is to be sent using the MPY_PYTHON_ARRAY datatype. It is returned
    # to avoid the garbage collection of the array object from which the
    # internal buffer address 's' comes from. Simply ignore 'arrayObj' and the
    # object will be garbage collected when the function returns.
    s, nElem, mpi_datatype, arrayObj = obj2CArray2(msg, dataType, NULLPT)

    # Send message, synchronous mode
    res = MPI_Issend(<void *>s, nElem, <MPI_Datatype>mpi_datatype,
                     dest, tag, <MPI_Comm>comm, &request)
    checkErr(res, "MPY_Issend")

    return Request(<long>request, s, receive=False, dataType=dataType,
                   array=arrayObj)
    

def MPY_Keyval_create(copy_fn=MPY_NULL_COPY_FN, delete_fn=MPY_NULL_DELETE_FN,
                      extra_state=0):
    """
    Python wrapper around MPI_Keyval_create() .

    Params:
      copy_fn       Callback when the communicator is duplicated by a call to
                    MPY_Comm_dup(). One of MPY_NULL_COPY_FN or MPY_DUP_FN
      delete_fn     Callback when the communicator is deleted, or the
                    attribute is deleted. Can only be MPY_NULL_DELETE_FN
      extra_state   Extra state value passed to the callback.

    Returns:
      Key identifying the attribute.
                                                                 """

    cdef int  keyval, extra
    cdef long copyFunc, delFunc

    copyFunc = copy_fn
    delFunc  = delete_fn
    extra = extra_state
    res = MPI_Keyval_create(<MPI_Copy_function *>copyFunc,
                            <MPI_Delete_function *>delFunc,
                            &keyval, <void *>extra)
    checkErr(res, "MPY_Keyval_create")

    return keyval

def MPY_Keyval_free(int keyval):
    """
    Python wrapper around MPI_Keyval_free() .

    Params:
      keyval        Key value. Upon return, the key value is invalid.

    Returns:
      MPI_KEYVAL_INVALID
                                                             """

    res = MPI_Keyval_free(&keyval)
    checkErr(res, "MPY_Keyval_free")

    return keyval
    

def MPY_Probe(int source=MPY_ANY_SOURCE, int tag=MPY_ANY_TAG,
              long comm=MPY_COMM_WORLD, retStatus=False):
    """
    Python request around MPI_Probe() .

    Params:
      source        Rank inside the communicator of the process which sent the
                    message to probe, or MPY_ANY_SOURCE to probe messages
                    from any source.
      tag           Numeric tag identifying the message to probe, or MPY_ANY_TAG
                    to ignore message tags.
      comm          Communicator handle.
      retStatus     True to have the function return a Status object telling
                    additional info about the probed message.

    Returns:
      None if 'retStatus' is false, Status object otherwise.

    probe() blocks until a message is waiting, but without consuming it.
    iprobe() serves same purpose, but does not block if no message is waiting.
                                                                                """

    cdef MPI_Status status

    res = MPI_Probe(source, tag, <MPI_Comm>comm, &status)
    checkErr(res, "MPY_Probe")

    if retStatus:
        ret = Status(status.MPI_SOURCE, status.MPI_TAG, 
                     status.MPI_ERROR, status.st_length)
    else:
        ret = None

    return ret

    
def MPY_Recv(int source, int nElem=0, dataType=MPY_PYTHON_OBJ, array=None,
             int tag=MPY_ANY_TAG,
             long comm=MPY_COMM_WORLD, retStatus=False):
    """
    Python wrapper around MPI_Recv() .

    Params:
      source        Rank inside communicator of the process from which to receive
                    the message.
      nElem         Maximum number of data elements inside the message to receive.
                    If omitted or 0, function will probe the message queue to
                    obtain the message length. 
      dataType      Message transmission mode.
      array         If dataType==MPY_PYTHON_ARRAY, parameter 'array' must identify
                    the Numeric array into which to store the received data.
                    The caller must make sure that this array is compatible
                    with the one to be received (size and datatype); its shape can
                    always be modified afterwards.
      tag           Numeric tag identifying the message to receive, or MPY_ANY_TAG
                    to ignore message tags.
      comm          Communicator handle.
      retStatus     True to have the function return a Status object in addition
                    to the message contents.

    Returns:
      Received message. If the message was received as a python object,
      this object is returned. In the case where dataType specifies a Numeric array,
      the returned object is identical to the value of parameter 'array'.
      Otherwise, function returns a scalar or a list of scalars
      representing the basic MPI datatype chosen. If 'retStatus' is true,
      function returns a tuple whose 1st element is the message, and the second
      one is the Status object caracterising the operation.
    
                                                                                 """
    cdef long s, mpi_datatype
    cdef MPI_Status status
    cdef ArrayType arrayObj
    cdef int nBytes

    # Probe message queue to get the message length.
    if dataType != MPY_PYTHON_ARRAY:
        if nElem == 0:
            res = MPI_Probe(source, tag, <MPI_Comm>comm, &status)
            checkErr(res, "MPY_Recv/MPI_Probe")
            nElem = status.st_length / dataTypeSize(dataType)

    else:
        if array is None:
            raise MPY_Error, "MPY_Recv : parameter 'array' cannot be None " \
                  "if dataType == MPY_PYTHON_ARRAY"

    # Allocate buffer to store message.
    # 'arrayObj' serves only when dataType==MPY_PYTHON_ARRAY, to avoid the
    # garbage collection of the python object to which buffer 's' belongs. 
    s, mpi_datatype, nElem, arrayObj = prepRecv2(nElem, array, dataType)

    # Receive message
    res = MPI_Recv(<void *>s, nElem, <MPI_Datatype>mpi_datatype,
                   source, tag, <MPI_Comm>comm, &status)
    checkErr(res, "MPY_Recv")

    # Convert to Python object and free C array, unless the output buffer is
    # a Numeric array.
    if dataType != MPY_PYTHON_ARRAY:
        obj = CArray2Obj(<void *>s, dataType, status.st_length, True)
        PyMem_Free(<void *>s)
    else:
        obj = array
        
    if not retStatus:
        return obj
    else:
        return (obj, Status(status.MPI_SOURCE, status.MPI_TAG, 
                            status.MPI_ERROR, status.st_length))

def MPY_Recv_init(int source, int nElem=0, dataType=MPY_PYTHON_OBJ, array=None,
                  int tag=1, long comm=MPY_COMM_WORLD):
    """
    Python wrapper around MPI_Recv_init() .

    Params:
      source        Rank inside the communicator of the process from which the
                    messages will originate.
      nElem         Maximum number of data elements to receive through the
                    persistent request. All messages received through this request
                    must have no more than this number of data elements.
                    This parameter should be omitted if dataType==MPY_PYTHON_ARRAY,
                    since the size of the array determines the number of elements.
      dataType      Message transmission mode.
      array         If dataType==MPY_PYTHON_ARRAY, parameter 'array' must identify
                    the Numeric array which will hold the data to be received.
      tag           Numeric tag which can be used to select the message to receive.
      comm          Communicator handle.

    Returns:
      Persistent request handle. Pass this handle to start() to launch the receive.
      Assert operation completion by calling a function of the test() or wait()
      family. Once the operation is complete, call requestExtract() to obtain
      the message contents, unless dataType == MPY_PYTHON_ARRAY. In that last case,
      just access the array directly. Once the request object is no more usefull,
      free resources by calling request_free().
                                                                                    """

    cdef long s, mpi_datatype
    cdef ArrayType arrayObj
    cdef MPI_Request request

    # Allocate buffer to store message.
    # 'arrayObj' serves only when dataType==MPY_PYTHON_ARRAY, to avoid the garbage
    # collection of the python object to which buffer 's' belongs. 
    s, mpi_datatype, nElem, arrayObj = prepRecv2(nElem, array, dataType)

    # Create permanent request.
    res = MPI_Recv_init(<void *>s, nElem, <MPI_Datatype>mpi_datatype,
                        source, tag, <MPI_Comm>comm, &request)
    checkErr(res, "MPY_Recv_init")

    return Request(<long>request, <long>s, receive=True, dataType=dataType,
                   permanent=True, array=arrayObj)
    
def MPY_Reduce(buf, long op, root, dataType=MPY_PYTHON_OBJ,
               long comm=MPY_COMM_WORLD):
    """
    Python wrapper around MPI_Reduce() .

    Params:
      buf           Data element(s) submitted to the reduce operation.
                    Either a single numeric value, or a sequence of numeric
                    values. All processes must send the same number of elements
                    to the reduce operator.
      op            Reduction operator. MINLOC and MAXLOC are not supported yet.
      root          Rank of the process to which reduced values are sent.
      dataType      Data elements type.
      comm          Communicator handle.

    Returns:
      root process :     One or more reduced values
      non-root process : None
    
                                                               """
    cdef int i, nElem, rank
    cdef long s, r, mpi_datatype


    rank = MPY_Comm_rank(comm)
    
    # If a python object is passed in, try to deduce the MPI datatype.
    if dataType == MPY_PYTHON_OBJ:
        if type(buf) in [types.TupleType, types.ListType]:
            t = type(buf[0])
        else:
            t = type(buf)
        if t == type(1):
            dataType = MPY_INT
        elif t == type(1.0):
            dataType = MPY_DOUBLE
        elif t == type(long(1)):
            dataType = MPY_LONG_LONG
        else:
            raise MPY_Error, "bad value type passed to MPY_reduce"

    # Allocate buffer where to store the data elements.
    s, nElem, mpi_datatype = obj2CArray(buf, dataType, NULLPT)

    # Allocate buffer where root receives the reduced results.
    if rank == root:
        r, mpi_datatype = prepRecv(nElem, dataType)
    else:
        r = 0

    # Execute the reduce operation.
    res = MPI_Reduce(<void *>s, <void *>r, nElem, <MPI_Datatype>mpi_datatype,
                     <MPI_Op>op, root, <MPI_Comm>comm)
    checkErr(res, "MPY_Reduce")

    # Return result to root process and free receive buffer.
    if rank == root:
        obj = CArray2Obj(<void *>r, dataType, nElem, False)
        PyMem_Free(<void *>r)
    else:
        obj = None
    
    # Free source buffer.
    PyMem_Free(<void *>s)

    return obj

def MPY_Reduce_scatter(buf, recvCounts, long op, dataType=MPY_PYTHON_OBJ,
                       long comm=MPY_COMM_WORLD):
    """
    Python wrapper around MPI_Reduce_scatter() .

    Params:
      buf           Data element(s) submitted to the reduce operation.
                    Either a single numeric value, or a sequence of numeric
                    values. All processes must send the same number of elements
                    to the reduce operator.
      op            Reduction operator. MINLOC and MAXLOC are not supported yet.
      recvCounts    Sequence of integers, whose length is equal to the number
                    of processes inside the communicator. The sum of the integers
                    must equal the number of data elements submitted to the reduce
                    operation. Process 'i' will receive 'recvCounts[i]' values
                    from the set of reduced values.
      dataType      Data elements type.
      comm          Communicator handle.

    Returns:
      Process of rank 'i' receives a list of 'recvCounts[i]' values.
    
                                                               """
    cdef int i, nElem, rank, size, n
    cdef long s, r, counts, mpi_datatype


    rank = MPY_Comm_rank(comm)
    size = MPY_Comm_size(comm)

    # If a python object is passed in, try to deduce the MPI datatype.
    if dataType == MPY_PYTHON_OBJ:
        if type(buf) in [types.TupleType, types.ListType]:
            t = type(buf[0])
        else:
            t = type(buf)
        if t == type(1):
            dataType = MPY_INT
        elif t == type(1.0):
            dataType = MPY_DOUBLE
        elif t == type(long(1)):
            dataType = MPY_LONG_LONG
        else:
            raise MPY_Error, "bad value type passed to MPY_reduce"

    # Allocate buffer where to store the data elements.
    s, nElem, mpi_datatype = obj2CArray(buf, dataType, NULLPT)

    # Validate recvCounts.
    if not type(recvCounts) in [types.TupleType, types.ListType] or \
           len(recvCounts) != size or \
           type(recvCounts[rank]) != types.IntType:
        raise MPY_Error, "MPY_Reduce_scatter : bad 'recvCounts' parameter"
    n = 0
    for i from 0 <= i < size:
        n = n + recvCounts[i]
    if n != nElem:
        raise MPY_Error, "MPY_Reduce_scatter : total number of values is bad"

    # Allocate buffer where to receive the reduced results.
    r, mpi_datatype = prepRecv(recvCounts[rank], dataType)

    # Allocate buffer to store counts.
    counts = obj2CArray(recvCounts, MPY_INT, NULLPT)[0]

    # Execute the reduce operation.
    res = MPI_Reduce_scatter(<void *>s, <void *>r, <int *>counts,
                             <MPI_Datatype>mpi_datatype, <MPI_Op>op,
                             <MPI_Comm>comm)
    checkErr(res, "MPY_Reduce_scatter")

    # Return results.
    obj = CArray2Obj(<void *>r, dataType, recvCounts[rank], False)
    
    # Free memory.
    PyMem_Free(<void *>s)
    PyMem_Free(<void *>r)
    PyMem_Free(<void *>counts)

    return obj

def requestExtract(request):
    """
    requestExtract() is not part of the MPI specification, but
    is special to he 'mpy' package.

    requestExtract() is called to obtain the message received through a
    request object, either an immediate receive or a persistent receive
    request, except if the message datatype is MPY_PYTHON_ARRAY. In that
    later case, one simply reads the array to get the message contents,

    Params:
      request       Request object created by a call to a non-blocking
                    receive (persistent or non-persistent).

    Returns:
      Message contents.
      
    The request object passed to requestExtract() is created by a call to a
    function that creates a persistent or immediate receive request (recv_init(),
    irecv() ).
    
    Following a wait() on that request, or a test() on that request that returned
    true, requestExtract() is called to obtain the contents of the just read message.
    If the request is not persistent, requestExtract() deallocates the private
    buffer where the message was stored. Thus, requestExtract() can only be called
    once for a non-persistent request.
    
                                                              """
    cdef long l
    cdef void *s
    
    if request.receive:
        if request.array:
            obj = request.array
        else:
            l = request.buf
            obj = CArray2Obj(<void *>l, request.dataType, request.length, True)
        request.length = 0
        
    # Free internal object, except if the request is permanent or if
    # the request implies a numeric array.
    if not request.permanent:
        # Free reference to numeric array.
        if request.array:
            request.array = None
        # Free internal C buffer, except if the request is permament.
        elif request.buf != 0:
            l = request.buf
            PyMem_Free(<char *>l)
            request.buf = <long>0

    # Return python object
    return obj


def MPY_Request_free(request):
    """
    Python wrapper around MPI_Request_free()

    Params:
      request       Persistent request object created by a call to a function of
                    the '*_init()' family.

    Returns:
      None

    request_free() is called to free the resources allocated to a persistent request,
    particularly the private buffers used to store messages sent/received
    through this request. Calling request_free() assures that memory will not be
    wasted once the persistent request is not needed any more.
                                                                                   """

    cdef long l
    cdef MPI_Request mpi_request

    l = request.mpi_request
    mpi_request = <MPI_Request>l
    res = MPI_Request_free(&mpi_request)
    checkErr(res, "MPY_Request_free")

    request.mpi_request = <long>mpi_request   # Update
    request.length = 0

    # Free underlying array object.
    if request.array:
        request.array = None
    elif request.buf != 0:
        l = request.buf
        PyMem_Free(<char *>l)
        request.buf = <long>0


def requestLoad(request, obj):
    """
    requestLoad() is not part of the MPI specification, but is special to this
    Python implementation.

    requestLoad() is called to load a message in the buffer of a persistent
    send request, except if the message datatype is MPY_PYTHON_ARRAY.
    In that later case, simply write to the array directly.

    Params:
      request       Persistent send request created by a call to bsend_init(),
                    rsend_init(), send_init() or ssend_init() .
      obj           Data to load in the private request buffer and which will
                    be sent by the next call to start(). The number of data elements
                    inside 'obj' must not exceed the 'nElem' value used when
                    the persistent request was created.


    Call start() to send the message just loaded in the request buffer.
                                                                             """

    cdef int count
    cdef long l

    l = request.buf
    obj2CArray(obj, request.dataType, <void *>l)


def MPY_Rsend(msg, int dest, dataType=MPY_PYTHON_OBJ,
              int tag=1, long comm=MPY_COMM_WORLD):
    """
    Python wrapper around MPI_Rsend() .

    Params:
      msg           Message to send
      dest          Rank inside the communicator of the process to which the
                    message is sent
      dataType      Message transmission mode.
      tag           Numeric tag which can be used to identify this message.
      comm          Communicator handle

    Returns:
      None
                                                                                    """

    cdef int nElem
    cdef long s, mpi_datatype
    cdef ArrayType arrayObj

    # Allocate and initialize send buffer. 'arrayObj' is meaningful only when the
    # object is to be sent using the MPY_PYTHON_ARRAY datatype. It is returned
    # to avoid the garbage collection of the array object from which the
    # internal buffer address 's' comes from. Simply ignore 'arrayObj' and the
    # object will be garbage collected when the function returns.
    s, nElem, mpi_datatype, arrayObj = obj2CArray2(msg, dataType, NULLPT)

    # Send message, ready mode.
    res = MPI_Rsend(<void *>s, nElem, <MPI_Datatype>mpi_datatype,
                    dest, tag, <MPI_Comm>comm)

    if dataType != MPY_PYTHON_ARRAY:  # Do not free Numeric array internal buffer
        PyMem_Free(<void *>s)
        
    checkErr(res, "MPY_Rsend")

def MPY_Rsend_init(int dest, int nElem=0, dataType=MPY_PYTHON_OBJ, array=None,
                   int tag=1, long comm=MPY_COMM_WORLD):
    """
    Python wrapper around MPI_Rsend_init() .
    
    Params:
      dest          Rank inside the communicator of the process to which the
                    request will send messages.
      nElem         Number of data elements to send through the persistent request.
                    All messages sent with this request must be of the same size
                    (or less or equal to this size for dataType MPY_PYTHON_OBJ.
                    This parameter should be omitted if dataType==MPY_PYTHON_ARRAY,
                    since the size of the array determines the number of elements.
      dataType      Message transmission mode.
      array         If dataType==MPY_PYTHON_ARRAY, parameter 'array' must identify
                    the Numeric array which will hold the data to be sent.
      tag           Numeric tag which can be used to identify this message.
      comm          Communicator handle

    Returns:
      Persistent request handle. Pass this handle to requestLoad() to load
      a message inside the request buffer, unless dataType == MPY_PYTHON_ARRAY.
      In that case, simply load the data inside 'array'. Then call MPY_Start()
      to launch the send.
      Assert completion of the request by a call to a function of the MPY_Test() or
      MPY_Wait() family. Free request resources by calling MPY_Request_free().

                                                                                  """

    cdef long s, mpi_datatype
    cdef ArrayType arrayObj
    cdef MPI_Request request

    # Allocate buffer to store messages.
    # 'arrayObj' serves only when dataType==MPY_PYTHON_ARRAY, to avoid the garbage
    # collection of the python object to which buffer 's' belongs. 
    s, mpi_datatype, nElem, arrayObj = prepRecv2(nElem, array, dataType)

    # Create permanent request.
    res = MPI_Rsend_init(<void *>s, nElem, <MPI_Datatype>mpi_datatype,
                         dest, tag, <MPI_Comm>comm, &request)
    checkErr(res, "MPY_Rsend_init")

    return Request(<long>request, s, receive=False, dataType=dataType,
                   array=arrayObj)


def MPY_Scan(buf, long op, dataType=MPY_PYTHON_OBJ,
             long comm=MPY_COMM_WORLD):
    """
    Python wrapper around MPI_Scan() .

    Params:
      buf           Data element(s) submitted to the scan operation.
                    Either a single numeric value, or a sequence of numeric
                    values. All processes must send the same number of elements
                    to the scan operator.
      op            Reduction operator. MINLOC and MAXLOC are not supported yet.
      dataType      Data elements type.
      comm          Communicator handle.

    Returns:
      One or more reduced values
    
                                                               """
    cdef int i, nElem, rank
    cdef long s, r, mpi_datatype


    rank = MPY_Comm_rank(comm)
    
    # If a python object is passed in, try to deduce the MPI datatype.
    if dataType == MPY_PYTHON_OBJ:
        if type(buf) in [types.TupleType, types.ListType]:
            t = type(buf[0])
        else:
            t = type(buf)
        if t == type(1):
            dataType = MPY_INT
        elif t == type(1.0):
            dataType = MPY_DOUBLE
        elif t == type(long(1)):
            dataType = MPY_LONG_LONG
        else:
            raise MPY_Error, "bad value type passed to MPY_reduce"

    # Allocate buffer where to store the data elements.
    s, nElem, mpi_datatype = obj2CArray(buf, dataType, NULLPT)

    # Allocate buffer to receive the reduced results.
    r, mpi_datatype = prepRecv(nElem, dataType)

    # Execute the scan operation.
    res = MPI_Scan(<void *>s, <void *>r, nElem, <MPI_Datatype>mpi_datatype,
                   <MPI_Op>op, <MPI_Comm>comm)
    checkErr(res, "MPY_Scan")

    # Return result and free receive buffer.
    obj = CArray2Obj(<void *>r, dataType, nElem, False)
    PyMem_Free(<void *>r)
    
    # Free source buffer.
    PyMem_Free(<void *>s)

    return obj


def MPY_Scatter(int root, msg=None, int recvCount=0,
                dataType=MPY_PYTHON_OBJ, array=None, long comm=MPY_COMM_WORLD):
    """
    Python wrapper around MPI_Scatter() .

    Params:
      root          Rank inside the communicator of the process which
                    scatters the messages.
      msg           Message to scatter. This parameter is significant
                    only at root, and is ignored on non-root processes, where
                    it should be omitted (or set to the default None).
                    When dataType == MPY_PYTHON_ARRAY, 'msg' must by a Numeric
                    array, whose total number of elements must be a multiple
                    of the number of processes inside the communicator. The array
                    contents are divided into equal-sized "chunks", and a chunk is
                    sent to each process, in rank order.
                    For other datatypes, 'msg' must be a sequence whose length
                    must match the number of processes inside the communicator,
                    message at index 'i' being sent to process of rank 'i'.
                    Messages must be of the same length.
                    Remember that the root process participates in the scatter and
                    thus sends a message to itself.
      recvCount     Max number of data elements to receive. Must be greater or
                    equal to the message size. If set to 0 (default value), the
                    root process will first broadcast the number of data elements
                    scattered to the processes
      dataType      Message datatype.
      array         Significant only if dataType == MPY_PYTHON_ARRAY. This parameter
                    then identifies the array where the process will receive its 
                    "chunk". If this parameter is omitted, a one-dimensional array
                    is allocated to store the chunk elements. The array type is
                    taken from that of the array given to the root process.
      comm          Communicator handle.

    Returns:
      Message received from the root

    MPY_Scatter() is the inverse of MPY_Gather().
                                                                             """

    cdef long r, s, mpi_datatype, adr, adr0
    cdef int nElem, mxElem, chunkSize, size, rank, p
    cdef ArrayType sendArrayObj, recvArrayObj

    size = MPY_Comm_size(comm)
    rank = MPY_Comm_rank(comm)

    # Only root scatters messages.
    if rank == root:
        # Unless Numeric arrays are used, we must allocate a buffer
        # where all messages will be regrouped.
        if dataType != MPY_PYTHON_ARRAY:
            # Compute the maximum number of elements among the messages to send.
            # Each proces will we sent a message with this number of elements.
            mxElem = 0
            for obj in msg:
                if dataType == MPY_PYTHON_OBJ:
                    nElem = lenPickle(obj)
                else:
                    # Sequence
                    if type(obj) in [types.TupleType, types.ListType,
                                     types.StringType]:
                        nElem = len(obj)
                    # Scalar.
                    else:
                        nElem = 1
                if nElem > mxElem:
                    mxElem = nElem

            # Allocate a buffer to store the messages to send.
            s, mpi_datatype = prepRecv(mxElem * size, dataType)

            # Copy messages to this buffer, one per chunk.
            adr = s
            chunkSize = mxElem * dataTypeSize(dataType)   # in bytes
            for obj in msg:
                adr0, nElem, mpi_datatype = obj2CArray(obj, dataType, <void *>adr)
                adr = adr + chunkSize

        # A Numeric array is used. Divide the total number of elements inside
        # the array into chunks, one per process.
        else:
            s, nElem, mpi_datatype, sendArrayObj = obj2CArray2(msg, dataType, NULLPT)
            mxElem = nElem / size
            # Get the array typecode. We may need to broadcast it later.
            typeCode = msg.typecode()

    # If the receive count is omitted, broadcast the number of data elements
    # per chunk.
    if recvCount == 0:
        MPI_Bcast(&mxElem, 1, MPI_INT, root, <MPI_Comm>comm)
        recvCount = mxElem
                  
    # Allocate receive buffer, for everyone. If dataType == MPY_PYTHON_ARRAY,
    # use parameter 'array' as the buffer, unless it is None. In that case,
    # allocate a one-dimensional array of length 'mxElem', whose type is the same as
    # that of the array passed to the root process.
    if dataType == MPY_PYTHON_ARRAY and array is None:
        # Let root broadcast the array typecode (1 char string).
        typeCode = MPY_Bcast(root, typeCode, nElem=1, dataType=MPY_PYTHON_STR,
                             comm=comm)
        # Allocate the array.
        array = Numeric.zeros(mxElem, typeCode)
    r, mpi_datatype, dum, recvArrayObj = prepRecv2(recvCount, array, dataType)

    # Scatter data.
    res = MPI_Scatter(<void *>s, mxElem, <MPI_Datatype>mpi_datatype,
                      <void *>r, recvCount, <MPI_Datatype>mpi_datatype,
                      root, <MPI_Comm>comm)
    checkErr(res, "MPY_Scatter")

    # If Numeric array was used, simply return it.
    if dataType == MPY_PYTHON_ARRAY:
        obj = array
    
    # Otherwise, convert message to Python object and free allocated buffers.
    else:
        obj = CArray2Obj(<void *>r, dataType, mxElem, False)

        # Free allocated buffers.
        PyMem_Free(<void *>r)
        if rank == root:
            PyMem_Free(<void *>s)

    # Return results.
    return obj
            

def MPY_Scatterv(int root, msg=None, sendCount=None, int recvCount=0,
                 dataType=MPY_PYTHON_OBJ, array=None, long comm=MPY_COMM_WORLD):
    """
    Python wrapper around MPI_Scatterv() .

    MPY_Scatter() and MPY_Scatterv() have the same calling sequence. They differ from
    each other in that, with MPY_Scatter(), all participating processes receive
    the same number of data elements, whereas MPY_Scatterv() allows each process to
    receive a different number of data elements.


    Params:
      root          Rank inside the communicator of the process which
                    scatters the messages.
      msg           Message to scatter. This parameter is significant
                    only at root, and is ignored on non-root processes, where
                    it should be omitted (or set to the default None).
                    When dataType == MPY_PYTHON_ARRAY, 'msg' must by a Numeric
                    array. For other datatypes, 'msg' must be a sequence whose length
                    must match the number of processes inside the communicator,
                    message at index 'i' being sent to process of rank 'i'.
                    Remember that the root process participates in the scatter and
                    thus sends a message to itself.
      sendCount     Significant only when dataType == MPY_PYTHON_ARRAY. sendCount 
                    is then a sequence giving the number of data elements to send to
                    each process.
      recvCount     Max number of data elements to receive. Must be greater or
                    equal to the message size. If set to 0 (default value),
                    root process scatters the number of data elements sent to
                    each process.
      dataType      Message datatype.
      comm          Communicator handle.

    Returns:
      Message received from the root

    MPY_Scatterv() is the inverse of MPY_Gatherv().
                                                                             """
    cdef long r, s, mpi_datatype, adr, adr0
    cdef int nElem, totElem, chunkSize, size, rank, p, dSize
    cdef int *sendCounts, *displ

    size = MPY_Comm_size(comm)
    rank = MPY_Comm_rank(comm)

    # Only root scatters messages.
    if rank == root:
        sendCounts = <int *>PyMem_Malloc(size * sizeof(int))
        displ      = <int *>PyMem_Malloc(size * sizeof(int))

        # Unless Numeric arrays are used, we must allocate a buffer
        # where all messages will be regrouped.
        if dataType != MPY_PYTHON_ARRAY:
            # Compute the total number of elements among the messages to send.
            totElem = 0
            for obj in msg:
                if dataType == MPY_PYTHON_OBJ:
                    nElem = lenPickle(obj)
                else:
                    # Sequence
                    if type(obj) in [types.TupleType, types.ListType,
                                     types.StringType]:
                        nElem = len(obj)
                    # Scalar.
                    else:
                        nElem = 1
                totElem = totElem + nElem

            # Allocate a buffer to store the messages to send, their lengths and
            # their offsets.
            s, mpi_datatype = prepRecv(totElem, dataType)

            # Copy messages to this buffer. Setup length and offset arrays.
            adr = s
            p = 0
            dSize = dataTypeSize(dataType)
            for obj in msg:
                adr0, nElem, mpi_datatype = obj2CArray(obj, dataType, <void *>adr)
                sendCounts[p] = nElem
                displ[p] = (adr - s) / dSize
                adr = adr + nElem * dSize
                p = p + 1

        # A Numeric array is used.
        else:
            s, nElem, mpi_datatype, sendArrayObj = obj2CArray2(msg, dataType, NULLPT)
            for p in range(size):
                if sendCount is None:
                    sendCounts[p] = nElem / size
                else:
                    sendCounts[p] = sendCount[p]
                if p == 0:
                    displ[p] = 0
                else:
                    displ[p] = displ[p - 1] + sendCounts[p - 1]
            # Get the array typecode. We may need to broadcast it later.
            typeCode = msg.typecode()

    # Scatter the counts to each process if the receive count is not
    # specified.
    if recvCount == 0:
        MPI_Scatter(sendCounts, 1, MPI_INT, &recvCount, 1, MPI_INT,
                    root, <MPI_Comm>comm)

    # Allocate receive buffer, for everyone. If dataType == MPY_PYTHON_ARRAY,
    # use parameter 'array' as the buffer, unless it is None. In that case,
    # allocate a one-dimensional array of length 'recvCount', whose type is the same as
    # that of the array passed to the root process.
    if dataType == MPY_PYTHON_ARRAY and array is None:
        # Let root broadcast the array typecode (1 char string).
        typeCode = MPY_Bcast(root, typeCode, nElem=1, dataType=MPY_PYTHON_STR,
                             comm=comm)
        # Allocate the array.
        array = Numeric.zeros(recvCount, typeCode)
        
    r, mpi_datatype, dum, recvArrayObj = prepRecv2(recvCount, array, dataType)

    # Scatter data.
    res = MPI_Scatterv(<void *>s, sendCounts, displ, <MPI_Datatype>mpi_datatype,
                       <void *>r, recvCount, <MPI_Datatype>mpi_datatype,
                       root, <MPI_Comm>comm)
    checkErr(res, "MPY_Scatterv")
        
    # If Numeric array was used, simply return it.
    if dataType == MPY_PYTHON_ARRAY:
        obj = array

    # Otherwise, convert received message to Python object,
    # and free allocated buffers.
    else:
        obj = CArray2Obj(<void *>r, dataType, recvCount, False)

        # Free allocated buffers.
        PyMem_Free(<void *>r)
        if rank == root:
            PyMem_Free(<void *>s)
            PyMem_Free(<void *>sendCounts)
            PyMem_Free(<void *>displ)

    # Return results.
    return obj
            

def MPY_Send(msg, int dest, dataType=MPY_PYTHON_OBJ,
             int tag=1, long comm=MPY_COMM_WORLD):
    """
    Python wrapper around MPI_Send() .

    Parameters:
      msg           Message to send.
      dest          Rank inside the communicator of the process to which
                    the message is sent.
      dataType      Message transmission mode.
      tag           Numeric tag which can be used to identify the message
                    to receive.
      comm          Communicator handle.

    Returns:
      None
                                                                            """

    cdef int nElem
    cdef long s, mpi_datatype
    cdef ArrayType arrayObj

    # Allocate and initialize send buffer. 'arrayObj' is meaningful only when 
    # object is to be sent using the MPY_PYTHON_ARRAY datatype. It is returned
    # to avoid the garbage collection of the array object from which the
    # internal buffer address 's' comes from. Simply ignore 'arrayObj' and the
    # object will be garbage collected when the function returns.
    s, nElem, mpi_datatype, arrayObj = obj2CArray2(msg, dataType, NULLPT)

    # Send message
    res = MPI_Send(<void *>s, nElem, <MPI_Datatype>mpi_datatype,
                   dest, tag, <MPI_Comm>comm)
    
    # Free internal array, unless the message comes from a Numeric array.
    if dataType != MPY_PYTHON_ARRAY:
        PyMem_Free(<void *>s)
        
    checkErr(res, "MPY_Send")

def MPY_Send_init(int dest, int nElem=0, dataType=MPY_PYTHON_OBJ, array=None,
                  int tag=1, long comm=MPY_COMM_WORLD):
    """
    Python wrapper around MPI_Send_init() .

    Params:
      dest          Rank inside the communicator of the process to which the
                    request will send messages.
      nElem         Number of data elements to send through the persistent request.
                    All messages sent with this request must be of the same size
                    (or less or equal to this size for dataType MPY_PYTHON_OBJ).
                    This parameter should be omitted if dataType==MPY_PYTHON_ARRAY,
                    since the size of the array determines the number of elements.
      dataType      Message transmission mode.
      array         If dataType==MPY_PYTHON_ARRAY, parameter 'array' must identify
                    the Numeric array which will hold the data to be sent.
      tag           Numeric tag which can be used to identify this message.
      comm          Communicator handle

    Returns:
      Persistent request handle. Pass this handle to requestLoad() to load
      a message inside the request buffer, unless dataType == MPY_PYTHON_ARRAY.
      In that case, simply load the data inside 'array'. Then call MPY_Start()
      to launch the send.
      Assert completion of the request by a call to a function of the MPY_Test() or
      MPY_Wait() family. Free request resources by calling MPY_Request_free().

                                     """

    cdef long s, mpi_datatype
    cdef ArrayType arrayObj
    cdef MPI_Request request

    # Allocate buffer to store message.
    # 'arrayObj' serves only when dataType==MPY_PYTHON_ARRAY, to avoid the garbage
    # collection of the python object to which buffer 's' belongs. 
    s, mpi_datatype, nElem, arrayObj = prepRecv2(nElem, array, dataType)

    # Create permanent request.
    res = MPI_Send_init(<void *>s, nElem, <MPI_Datatype>mpi_datatype,
                        dest, tag, <MPI_Comm>comm, &request)
    checkErr(res, "MPY_Send_init")

    return Request(<long>request, s, receive=False, dataType=dataType,
                   array=arrayObj)
    
def MPY_Sendrecv(msg, int dest, sendDataType=MPY_PYTHON_OBJ, int sendTag=1,
                 int source=MPY_ANY_SOURCE, recvDataType=MPY_PYTHON_OBJ, array=None,
                 int recvTag=MPY_ANY_TAG, int recvCount=0,
                 long comm=MPY_COMM_WORLD, retStatus=False):
    """
    Python wrapper around MPI_Sendrecv() .

    Params:
      msg           Message to send.
      dest          Rank inside the communicator of the process to which to send
                    the message.
      sendDataType  Mode with which to send the message.
      sendTag       Numeric tag identifying the output message.
      source        Rank inside the communicator of the process from which
                    to receive a message. Defaults to MPY_ANY_SOURCE to accept
                    message from any source.
      recvDataType  Mode with which to receive the message.
      recvtag       Numeric tag identifying the input message.
      recvCount     Maximum number of data elements in the message to be received.
                    Can only be defaulted to 0 if a numeric array is used to
                    receive the message, in which case the number of elements inside
                    the array gives the number of data elements.
      comm          Communicator handle.
      retStatus     If true, function will append to its result the status of
                    the receive operation.

    Returns:
      Message received from 'source'. If 'retStatus' is true, function will
      return a 2-element tuple where the 2nd element will be the status of the
      receive operation.

    Note that we cannot probe the message queue to get at the message length. This
    could put the process in a deadlock if for ex. the received message is dependent
    (directly or indirectly) on the message sent.
                                                                  """

    cdef long s, r, send_mpi_datatype, recv_mpi_datatype
    cdef int nElemSend, nElemRecv
    cdef ArrayType sendArrayObj, recvArrayObj
    cdef MPI_Status status

    # Allocate and initialize send buffer. 'sendArrayObj' is meaningful only when the
    # object is to be sent using the MPY_PYTHON_ARRAY datatype. It is returned
    # to avoid the garbage collection of the array object from which the
    # internal buffer address 's' comes from. Simply ignore 'arrayObj' and the
    # object will be garbage collected when the function returns.
    s, nElemSend, send_mpi_datatype, sendArrayObj = \
       obj2CArray2(msg, sendDataType, NULLPT)

    # Obtain the receive count.
    if recvDataType != MPY_PYTHON_ARRAY:
        if recvCount > 0:
            nElemRecv = recvCount
        else:
            raise MPY_Error, "MPY_Sendrecv() : recvCount == 0"
    elif array is None:
        raise MPY_Error, "MPY_Sendrecv : parameter 'array' cannot be None " \
              "if dataType == MPY_PYTHON_ARRAY"
            
    # Allocate buffer to receive message.
    # 'recvArrayObj' serves only when dataType==MPY_PYTHON_ARRAY, to avoid the garbage
    # collection of the python object to which buffer 's' belongs. 
    r, recv_mpi_datatype, nElemRecv, recvArrayObj = \
       prepRecv2(nElemRecv, array, recvDataType)

    # Send and receive.
    res = MPI_Sendrecv(<void *>s, nElemSend, <MPI_Datatype>send_mpi_datatype,
                       dest, sendTag,
                       <void *>r, nElemRecv, <MPI_Datatype>recv_mpi_datatype,
                       source,  recvTag,
                       <MPI_Comm>comm, &status)
    checkErr(res, "MPY_Sendrecv")
    
    # Free internal array, unless the message comes from a Numeric array.
    if sendDataType != MPY_PYTHON_ARRAY:
        PyMem_Free(<void *>s)

    # Convert received message to python object and free C array, unless
    # output buffer is a Numeric array.
    if recvDataType != MPY_PYTHON_ARRAY:
        obj = CArray2Obj(<void *>r, recvDataType, status.st_length, True)
        PyMem_Free(<void *>r)
    else:
        obj = array
        
    if not retStatus:
        return obj
    else:
        return (obj, Status(status.MPI_SOURCE, status.MPI_TAG, 
                            status.MPI_ERROR, status.st_length))


def MPY_Sendrecv_replace(sendMsg, int dest, dataType=MPY_PYTHON_OBJ,
                         int source=MPY_ANY_SOURCE, int count=0,
                         int sendTag=1, int recvTag=MPY_ANY_TAG,
                         long comm=MPY_COMM_WORLD, retStatus=False):
    """
    Python wrapper around MPI_Sendrecv_replace() .

    Params:
      sendMsg       Message to send. Unless dataType MPY_PYTHON_OBJ is used to
                    transmit message, the length of the message to be sent
                    must equal that of the message to be received. 
      dest          Rank inside the communicator of the process to which to send
                    the message.
      dataType      Mode with which to send and receive the message.
      source        Rank inside the communicator of the process from which
                    to receive a message. Defaults to MPY_ANY_SOURCE to accept
                    message from any source.
      count         Number of data elements to send and receive.
                    If set to the default 0 value, 'count' is computed from
                    the size of 'msg'.
                    If > 0, must be > greater or equal to the length of the message
                    to be sent and to be received.
      sendTag       Numeric tag identifying the output message. Defaults to 1.
      recvtag       Numeric tag identifying the input message. Defaults to
                    MPY_ANY_TAG to accept any tag.
      comm          Communicator handle.
      retStatus     If true, function will append to its result the status of
                    the receive operation.

    Returns:
      Message received from 'source'. If 'retStatus' is true, function will
      return a 2-element tuple where the 2nd element will be the status of the
      receive operation.

    Equivalent to MPY_Sendrecv(), except that only one buffer is allocated
    to send and receive, and the dataType and count is the same for both.
    
                                                                  """
    cdef long s, mpi_datatype
    cdef int nElem, n
    cdef MPI_Status status
    
        
    # Allocate and init buffer.
    if dataType == MPY_PYTHON_ARRAY:
        s, nElem, mpi_datatype, arrayObj = \
           obj2CArray2(sendMsg, dataType, NULLPT)
    elif count > 0:
        nElem = count
        s, mpi_datatype = prepRecv(nElem, dataType)
        s, n, mpi_datatype = obj2CArray(sendMsg, dataType, <void *>s)
    else:
        s, nElem, mpi_datatype = obj2CArray(sendMsg, dataType, NULLPT)

    # Call MPI_Sendrecv_replace().
    res = MPI_Sendrecv_replace(<void *>s, nElem, <MPI_Datatype>mpi_datatype,
                               dest, sendTag, source,  recvTag,
                               <MPI_Comm>comm, &status)
    checkErr(res, "MPY_Sendrecv_replace")

    # Convert received message to python object.
    if dataType != MPY_PYTHON_ARRAY:
        recvMsg = CArray2Obj(<void *>s, dataType, nElem, False)
        PyMem_Free(<void *>s)
    else:
        recvMsg = sendMsg

    # Return results.
    if not retStatus:
        return recvMsg
    else:
        return (recvMsg, Status(status.MPI_SOURCE, status.MPI_TAG, 
                                status.MPI_ERROR, status.st_length))
    
def MPY_Ssend(msg, int dest, dataType=MPY_PYTHON_OBJ,
              int tag=1, long comm=MPY_COMM_WORLD):
    """
    Python wrapper around MPI_Ssend() .

    Params:
      msg           Message to send
      dest          Rank inside the communicator of the process to which the
                    message is sent
      nElem         Number of data elements to send. This number is automatically
                    computed from the length of the buffer object, so this
                    parameter is ignored and can be omitted. If set, it must be
                    coherent with 'buffer' and 'dataType'.
      dataType      Message transmission mode.
      tag           Numeric tag which can be used to identify this message.
      comm          Communicator handle

    Returns:
      None
                                                                                    """
    cdef int nElem
    cdef long s, mpi_datatype
    cdef ArrayType arrayObj

    # Allocate and initialize send buffer. 'arrayObj' is meaningful only when the
    # object is to be sent using the MPY_PYTHON_ARRAY datatype. It is returned
    # to avoid the garbage collection of the array object from which the
    # internal buffer address 's' comes from. Simply ignore 'arrayObj' and the
    # object will be garbage collected when the function returns.
    s, nElem, mpi_datatype, arrayObj = obj2CArray2(msg, dataType, NULLPT)

    # Send message, synchronous mode.
    res = MPI_Ssend(<void *>s, nElem, <MPI_Datatype>mpi_datatype,
                    dest, tag, <MPI_Comm>comm)

    if dataType != MPY_PYTHON_ARRAY:  # Do not free Numeric array internal buffer
        PyMem_Free(<void *>s)
        
    checkErr(res, "MPY_Ssend")

def MPY_Ssend_init(int dest, int nElem=0, dataType=MPY_PYTHON_OBJ, array=None,
                   int tag=1, long comm=MPY_COMM_WORLD
                   ):
    """
    Python wrapper around MPI_Ssend_init() .

    Params:
      dest          Rank inside the communicator of the process to which the
                    request will send messages.
      nElem         Number of data elements to send through the persistent request.
                    All messages sent with this request must be of the same size
                    (or less or equal to this size for dataType MPY_PYTHON_OBJ.
                    This parameter should be omitted if dataType==MPY_PYTHON_ARRAY,
                    since the size of the array determines the number of elements.
      dataType      Message transmission mode.
      array         If dataType==MPY_PYTHON_ARRAY, parameter 'array' must identify
                    the Numeric array which will hold the data to be sent.
      tag           Numeric tag which can be used to identify this message.
      comm          Communicator handle

    Returns:
      Persistent request handle. Pass this handle to requestLoad() to load
      a message inside the request buffer, unless dataType == MPY_PYTHON_ARRAY.
      In that case, simply load the data inside 'array'. Then call MPY_Start()
      to launch the send.
      Assert completion of the request by a call to a function of the MPY_Test() or
      MPY_Wait() family. Free request resources by calling MPY_Request_free().
                                     """

    cdef long s, mpi_datatype
    cdef ArrayType arrayObj
    cdef MPI_Request request

    # Allocate buffer to store messages.
    # 'arrayObj' serves only when dataType==MPY_PYTHON_ARRAY, to avoid the garbage
    # collection of the python object to which buffer 's' belongs. 
    s, mpi_datatype, nElem, arrayObj = prepRecv2(nElem, array, dataType)

    # Create permanent request.
    res = MPI_Ssend_init(<void *>s, nElem, <MPI_Datatype>mpi_datatype,
                         dest, tag, <MPI_Comm>comm, &request)
    checkErr(res, "MPY_Ssend_init")

    return Request(<long>request, s, receive=False, dataType=dataType,
                   array=arrayObj)
    
def MPY_Start(request):
    """
    Python request around MPI_Start() .

    Params:
      request       Persistent request created by a call to functions of the
                    '*_init()' family.

    Returns:
      None

    Call start() to launch a request. If the request is a send operation, the
    request data must have been previously loaded by a call to requestLoad(),
    unless the datatype is MPY_PYTHON_ARRAY. In that last case, directly initalize
    the array before the call.
    
    The request completion is monitored by calling a function of the test() or
    wait() family. For a receive operation, the message data are obtained by
    calling requestExtract(), except if the datatype is MPY_PYTHON_ARRAY.
    In that last case, directly access the array elements following the call.
                                                                                """

    cdef MPI_Request mpi_request
    cdef long l

    l = request.mpi_request
    mpi_request = <MPI_Request>l
    res = MPI_Start(&mpi_request)
    checkErr(res, "MPY_Start")

    request.mpi_request = <long>mpi_request   # Reset

def MPY_Startall(requests):
    """
    Python wrapper around MPI_Startall() .

    Params:
      requests      Sequence of persistent requests created by calls to functions
                    of the '*_init()' family. All those requests are launched
                    at once.

    Returns:
      None

    See function MPY_Start() for more information about the handling of each
    request.
                                                                               """

    cdef MPI_Request *reqArr
    cdef int n, count
    cdef long l

    # Allocate request array.
    reqArr = <MPI_Request *>PyMem_Malloc(count * sizeof(MPI_Request *))

    # Load C array
    count = len(requests)
    for n from 0 <= n < count:
        l = requests[n].mpi_request
        reqArr[n] = <MPI_Request>l

    # Call MPI_Startall.
    res = MPI_Startall(count, reqArr)
    checkErr(res, "MPY_Startall")

    # Update requests.
    for n from 0 <= n < count:
        requests[n].mpi_request = <long>reqArr[n]

    # Free allocated aray.
    PyMem_Free(<char *>reqArr)
    

def MPY_Test(request, retStatus=False):
    """
    Python wrapper around MPI_Test() .

    Params:
      request       Request (persistent or non-persistent) that is to be monitored.
      retStatus     If true, append to the return value a Status object holding
                    the operation status.

    Returns:
      Boolean indicating if the operation associated with the request has completed.
      If 'retStatus' is true, return a tuple whose 2nd element is a Status object
      holding the operation status.

    Note that the function is non-blocking, countrary to the corresponding
    wait() function.
    
    If the request represents a receive operation and the datatype is NOT
    MPY_PYTHON_ARRAY, call 'requestExtract()' to obtain the value of the just
    read message, and deallocate the private buffer used to store its value.
    Thus, 'requestExtract()' can only be called once for a given request.
    If the message datatype is MPY_PYTHON_ARRAY, simply read the array to get
    the message contents.
                                                                  """

    cdef MPI_Status status
    cdef long l
    cdef int flag
    cdef MPI_Request mpi_request
    
    # No-op if request has already been processed.
    l = request.mpi_request
    if l == MPY_REQUEST_NULL:
        # Return empty status.
        flag = True
        status.MPI_SOURCE = MPY_ANY_SOURCE
        status.MPI_TAG = MPY_ANY_TAG
        status.MPI_ERROR = 0
        status.st_length = 0

    # Test if operation complete
    else:
        mpi_request = <MPI_Request>l
        res = MPI_Test(&mpi_request, &flag, &status)
        checkErr(res, "MPY_Test")
        if flag:
            request.mpi_request = <long>mpi_request  # Reset
            request.length = status.st_length

    # Return results.
    res = [flag]
    if retStatus:
        res.append(Status(status.MPI_SOURCE, status.MPI_TAG, 
                          status.MPI_ERROR, status.st_length))

    if len(res) == 1:
        return res[0]
    else:
        return tuple(res)

def MPY_Testall(requests, retStatus=False):
    """
    Python wrapper around MPI_Testall() .

    Params:
      requests      Sequence of requests (persistent or non-persistent) created
                    by calls to immediate send/receive operations, or to functions
                    of the '*_init()' family. All those requests are tested at once.
      retStatus     If true, append to return value a tuple holding the Status
                    objects of all the tested operations.

    Returns:
      Boolean indicating if all requests have completed.
      If 'retStatus' is true and all requests have completed, function
      returns a tuple whose 2nd element is a tuple of Status objects,
      one for each request. If not all requests have completed, Nome is
      returned as 2nd element.

    Note that the function is non-blocking, countrary to the corresponding
    wait() function.

    For those requests that represent receive operations not based on datatype
    MPY_PYTHON_ARRAY, call 'requestExtract()' to obtain the value of the associated
    message, and deallocate the private buffer used to store its value.
    Thus, 'requestExtract()' can only be called once for a given request.
    If the message datatype is MPY_PYTHON_ARRAY, simply read the array to get
    the message contents.
                                                                """

    cdef int count, n, flag
    cdef long l
    cdef MPI_Request *reqArr
    cdef MPI_Status status, *statusArr

    # Allocate the request and status arrays.
    count = len(requests)
    reqArr = <MPI_Request *>PyMem_Malloc(count * sizeof(reqArr))
    statusArr = <MPI_Status *>PyMem_Malloc(count * sizeof(statusArr[0]))

    # Populate the request array.
    for n from 0 <= n < count:
        l = requests[n].mpi_request
        reqArr[n] = <MPI_Request>l

    # Call MPI_Testall()
    res = MPI_Testall(count, reqArr, &flag, statusArr)
    checkErr(res, "MPY_Testall")

    res = [flag]
    if flag:
        # Update request list.
        for n from 0 <= n < count:
            req = requests[n]
            req.mpi_request = <long>reqArr[n]
            req.length = statusArr[n].st_length
            requests[n] = req
    
        # Return results.
        if retStatus:
            st = []
            for n from 0 <= n < count:
                status = statusArr[n]
                st.append(Status(status.MPI_SOURCE, status.MPI_TAG, 
                                 status.MPI_ERROR, status.st_length))
            res.append(st)
        
    elif retStatus:
        res.append(None)

    # Free allocated arrays.
    PyMem_Free(reqArr)
    PyMem_Free(statusArr)

    # Pyrex has trouble with this statement, which otherwise seems OK...
    # return (len(res) == 1 and res[0]) or res
    if len(res) == 1:
        return res[0]
    else:
        return res

def MPY_Testany(requests, retStatus=False):
    """
    Python wrapper around MPI_Testany() .

    Params:
      requests      Sequence of requests (persistent or non-persistent) created
                    by calls to immediate send/receive operations, or to functions
                    of the '*_init()' family. All those requests are tested at once.
      retStatus     If true, append to return value a tuple holding the Status
                    object of the completed request, if any.

    Returns:
      Tuple whose 1st elem is a boolean indicating if any one of the requests has
      completed. 2nd element is the index of this request inside sequence
      'requests', or None if all requests had already completed at the time
      of the call. None is also returned here if 1st element is false.
      If 'retStatus' is true, the operation status is appended to the
      returned tuple; status is undefined if no operation has completed.

    Note that the function is non-blocking, countrary to the corresponding
    wait() function.
    
    For those requests that represent receive operations not based on datatype
    MPY_PYTHON_ARRAY, call 'requestExtract()' to obtain the value of the associated
    message, and deallocate the private buffer used to store its value.
    Thus, 'requestExtract()' can only be called once for a given request.
    If the message datatype is MPY_PYTHON_ARRAY, simply read the array to get
    the message contents.
                                                                """

    cdef int count, n, index, flag
    cdef long l
    cdef MPI_Request *reqArr
    cdef MPI_Status status

    # Allocate the request array.
    count = len(requests)
    reqArr = <MPI_Request *>PyMem_Malloc(count * sizeof(reqArr))

    # Populate the array.
    for n from 0 <= n < count:
        l = requests[n].mpi_request
        reqArr[n] = <MPI_Request>l

    # Call MPI_Testany()
    res = MPI_Testany(count, reqArr, &index, &flag, &status)
    checkErr(res, "MPY_Testany")

    # Check if one operation completed.
    if not flag:
        res = [False, None]
        # Return empty status.
        status.MPI_SOURCE = MPY_ANY_SOURCE
        status.MPI_TAG = MPY_ANY_TAG
        status.MPI_ERROR = 0
        status.st_length = 0

    # Check if all requests are complete.
    elif index == MPI_UNDEFINED:
        res = [True, None]
        # Return empty status.
        status.MPI_SOURCE = MPY_ANY_SOURCE
        status.MPI_TAG = MPY_ANY_TAG
        status.MPI_ERROR = 0
        status.st_length = 0
    else:
        req = requests[index]
        req.mpi_request = <long>reqArr[index]
        req.length = status.st_length
        requests[index] = req
        res = [True, index]
        
    # Free request array.
    PyMem_Free(reqArr)

    # Return results.
    if retStatus:
        res.append(Status(status.MPI_SOURCE, status.MPI_TAG, 
                          status.MPI_ERROR, status.st_length))
    return tuple(res)
        
def MPY_Test_cancelled(status):
    """
    Python wrapper around MPI_Test_cancelled() .

    Params:
      status      Status object returned by a send or receive operation applied to
                  a request object.

    Returns:
      True if the status indicates that the operation has been cancelled
      by a call to cancel().

                                                                    """
    cdef MPI_Status mpi_status
    cdef int flag

    mpi_status.MPI_SOURCE = status.source
    mpi_status.MPI_TAG    = status.tag
    mpi_status.MPI_ERROR  = status.error
    mpi_status.st_length  = status.length

    res = MPI_Test_cancelled(&mpi_status, &flag)
    checkErr(res, "MPY_Test_cancelled")
    
    status.source = mpi_status.MPI_SOURCE
    status.tag    = mpi_status.MPI_TAG
    status.error  = mpi_status.MPI_ERROR
    status.length = mpi_status.st_length

    return flag
    
def MPY_Testsome(requests, retStatus=False):
    """
    Python wrapper around MPI_Testsome() .

    Params:
      requests    Sequence (list or tuple) of request objects created by calls
                  to immediate send/receive functions, or to persistent request
                  creation functions (*_init() family).
      retStatus   If true, the function will append toits return value a tuple
                  holding the status of each completed request.

    Returns:
      List holding the indices inside array 'requests' of all the requests
      that have completed at the time of the call. If no request has completed,
      an empty list is returned. If all the requests have completed,
      None is returned.
      If 'retStatus' is true, the function returns a tuple where the
      2nd element is a tuple holding the status objects of the completed
      requests.

    Note that the function is non-blocking, countrary to the corresponding
    wait() function.
    
    For those requests that represent receive operations not based on datatype
    MPY_PYTHON_ARRAY, call 'requestExtract()' to obtain the value of the associated
    message, and deallocate the private buffer used to store its value.
    Thus, 'requestExtract()' can only be called once for a given request.
    If the message datatype is MPY_PYTHON_ARRAY, simply read the array to get
    the message contents.
                                                                """

    cdef int count, outCount, n, idx, *indexArr
    cdef long l
    cdef MPI_Request *reqArr
    cdef MPI_Status status, *statusArr

    # Allocate the request, index and status arrays.
    count = len(requests)
    reqArr = <MPI_Request *>PyMem_Malloc(count * sizeof(reqArr))
    indexArr = <int *>PyMem_Malloc(count * sizeof(indexArr[0]))
    statusArr = <MPI_Status *>PyMem_Malloc(count * sizeof(statusArr[0]))

    # Populate the request array.
    for n from 0 <= n < count:
        l = requests[n].mpi_request
        reqArr[n] = <MPI_Request>l

    # Call MPI_Testsome()
    res = MPI_Testsome(count, reqArr, &outCount, indexArr, statusArr)
    checkErr(res, "MPY_Testsome")

    # Build results.
    if outCount == MPI_UNDEFINED:
        res = [None]
        if retStatus:
            res.append(None)
    else:
        # Build indices sequence and update request list.
        indLst = []
        for n from 0 <= n < outCount:
            idx = indexArr[n]
            indLst.append(idx)
            req = requests[idx]
            req.mpi_request = <long>reqArr[idx]
            req.length = statusArr[n].st_length
            requests[idx] = req
        res = [indLst]

        # Return statuses sequence.
        if retStatus:
            statLst = []
            for n from 0 <= n < outCount:
                status = statusArr[n]
                statLst.append(Status(status.MPI_SOURCE, status.MPI_TAG, 
                                      status.MPI_ERROR, status.st_length))
            res.append(statLst)
        
    # Free allocated arrays.
    PyMem_Free(reqArr)
    PyMem_Free(indexArr)
    PyMem_Free(statusArr)

    # Return results.
    if len(res) == 1:
        return res[0]
    else:
        return tuple(res)
        
def MPY_Topo_test(long comm):
    """
    Python wrapper around MPI_Topo_test() .

    Params:
      comm          Communicator

    Returns:
      MPY_CART       if the communicator uses a cartesian topology
      MPY_GRAPH      if the communicator uses a graph topology
      MPY_UNDEFINED  if no topology is assigned to the communicator
                                                                           """

    cdef int status

    res = MPI_Topo_test(<MPI_Comm>comm, &status)
    checkErr(res, "MPY_Topo_test")

    return status
    

def MPY_Wait(request, retStatus=False):
    """
    Python wrapper around MPI_Wait() .

    Params:
      request       Request (persistent or non-persistent) that is to be monitored.
      retStatus     If true, return a Status object holding the operation status.

    Returns:
      If 'retStatus' is true, return a Status object holding the operation status.
      Otherwise return None.

    Note that the function is blocking, contrary to its test() counterpart :
    it does not return until the request has completed.
    
    If the request represents a receive operation and the datatype is NOT
    MPY_PYTHON_ARRAY, call 'requestExtract()' to obtain the value of the just
    read message, and deallocate the private buffer used to store its value.
    Thus, 'requestExtract()' can only be called once for a given request.
    If the messge datatype is MPY_PYTHON_ARRAY, simply read the array to get
    the message contents.

                                              """

    cdef MPI_Status status
    cdef long l
    cdef MPI_Request mpi_request
    
    # No-op if request has already been processed.
    l = request.mpi_request
    if l == MPY_REQUEST_NULL:
        # Return empty status.
        status.MPI_SOURCE = MPY_ANY_SOURCE
        status.MPI_TAG = MPY_ANY_TAG
        status.MPI_ERROR = 0
        status.st_length = 0

    else:
        mpi_request = <MPI_Request>l
        res = MPI_Wait(&mpi_request, &status)
        checkErr(res, "MPY_Wait")
        request.mpi_request = <long>mpi_request   # Update
        request.length = status.st_length

    # Return results.
    if retStatus:
        res = Status(status.MPI_SOURCE, status.MPI_TAG, 
                      status.MPI_ERROR, status.st_length)
    else:
        res = None
        
    return res

def MPY_Waitall(requests, retStatus=False):
    """
    Python wrapper around MPI_Waitall() .

    Params:
      requests      Sequence of requests (persistent or non-persistent) created
                    by calls to immediate send/receive operations, or to functions
                    of the '*_init()' family. All those requests are tested at once.
      retStatus     If true, return a tuple holding the Status objects of all the
                    waited for operations.

    Returns:
      If 'retStatus' is true function returns a tuple of Status objects,
      one for each request. Otherwise, functions returns None.

    Note that the function is blocking, contrary to its test() counterpart :
    it does not return until all the requests have completed.

    For those requests that represent receive operations not based on datatype
    MPY_PYTHON_ARRAY, call 'requestExtract()' to obtain the value of the associated
    message, and deallocate the private buffer used to store its value.
    Thus, 'requestExtract()' can only be called once for a given request.
    If the message datatype is MPY_PYTHON_ARRAY, simply read the array to get
    the message contents.
                                                                """

    cdef int count, n, index
    cdef long l
    cdef MPI_Request *reqArr
    cdef MPI_Status status, *statusArr

    # Allocate the request and status arrays.
    count = len(requests)
    reqArr = <MPI_Request *>PyMem_Malloc(count * sizeof(reqArr))
    statusArr = <MPI_Status *>PyMem_Malloc(count * sizeof(statusArr[0]))

    # Populate the request array.
    for n from 0 <= n < count:
        l = requests[n].mpi_request
        reqArr[n] = <MPI_Request>l

    # Call MPI_Waitall()
    res = MPI_Waitall(count, reqArr, statusArr)
    checkErr(res, "MPY_Waitall")

    # Update request list.
    for n from 0 <= n < count:
        req = requests[n]
        req.mpi_request = <long>reqArr[n]
        req.length = statusArr[n].st_length
        requests[n] = req
    
    # Return results.
    if retStatus:
        res = []
        for n from 0 <= n < count:
            status = statusArr[n]
            res.append(Status(status.MPI_SOURCE, status.MPI_TAG, 
                              status.MPI_ERROR, status.st_length))
    else:
        res = None

    # Free allocated arrays.
    PyMem_Free(reqArr)
    PyMem_Free(statusArr)

    return res
        
def MPY_Waitany(requests, retStatus=False):
    """
    Python wrapper around MPI_Waitany() .

    Params:
      requests      Sequence of requests (persistent or non-persistent) created
                    by calls to immediate send/receive operations, or to functions
                    of the '*_init()' family. All those requests are tested
                    at once.
      retStatus     If true, append to the return value a tuple holding the Status
                    objects of all the requests that have completed.

    Returns:
      Function returns the index inside array 'requests' of any one
      request that has completed, or None if all the requests had
      already completed at the time of the call.
      If 'retStatus' is true, function appends a tuple holding the status of the
      the corresponding completed requests.

    Note that the function is blocking, countrary to the corresponding
    test() function : function does not return until at least one request
    has completed, or all had already completed.

    For those requests that represent receive operations not based on datatype
    MPY_PYTHON_ARRAY, call 'requestExtract()' to obtain the value of the associated
    message, and deallocate the private buffer used to store its value.
    Thus, 'requestExtract()' can only be called once for a given request.
    If the message datatype is MPY_PYTHON_ARRAY, simply read the array to get
    the message contents.
                                                                               """

    cdef int count, n, index
    cdef long l
    cdef MPI_Request *reqArr
    cdef MPI_Status status

    # Allocate the request array.
    count = len(requests)
    reqArr = <MPI_Request *>PyMem_Malloc(count * sizeof(reqArr))

    # Populate the array.
    for n from 0 <= n < count:
        l = requests[n].mpi_request
        reqArr[n] = <MPI_Request>l

    # Call MPI_Waitany()
    res = MPI_Waitany(count, reqArr, &index, &status)
    checkErr(res, "MPY_Waitany")

    if index == MPI_UNDEFINED:
        req = None
        # Return empty status.
        status.MPI_SOURCE = MPY_ANY_SOURCE
        status.MPI_TAG = MPY_ANY_TAG
        status.MPI_ERROR = 0
        status.st_length = 0
    else:
        req = requests[index]
        req.mpi_request = <long>reqArr[index]
        req.length = status.st_length
        requests[index] = req
        req = index
        
    # Free request array.
    PyMem_Free(reqArr)

    # Return results.
    res = [req]
    if retStatus:
        res.append(Status(status.MPI_SOURCE, status.MPI_TAG, 
                          status.MPI_ERROR, status.st_length))
    if len(res) == 1:
        return res[0]
    else:
        return tuple(res)
        
def MPY_Waitsome(requests, retStatus=False):
    """
    Python wrapper around MPI_Waitsome() .

    Params:
      requests      Sequence of requests (persistent or non-persistent) created
                    by calls to immediate send/receive operations, or to functions
                    of the '*_init()' family. All those requests are tested
                    at once.
      retStatus     If true, append to the return value a tuple holding the Status
                    objects of all the requests that have completed.

    Returns:
      Function returns a tuple holding the indices inside array 'requests' of
      all the requests that have completed, or None if all requests had
      completed at the time of the call.
      request that have completed, or None if all the requests had
      already completed at the time of the call.
      If 'retStatus' is true, function appends a tuple holding the status of the
      the completed requests.

    Note that the function is blocking, countrary to the corresponding
    test() function : function does not return until at least one request
    has completed, or all had already completed.

    For those requests that represent receive operations not based on datatype
    MPY_PYTHON_ARRAY, call 'requestExtract()' to obtain the value of the associated
    message, and deallocate the private buffer used to store its value.
    Thus, 'requestExtract()' can only be called once for a given request.
    If the message datatype is MPY_PYTHON_ARRAY, simply read the array to get
    the message contents.
                                                                """

    cdef int count, outCount, n, idx, *indexArr
    cdef long l
    cdef MPI_Request *reqArr
    cdef MPI_Status status, *statusArr

    # Allocate the request, index and status arrays.
    count = len(requests)
    reqArr = <MPI_Request *>PyMem_Malloc(count * sizeof(reqArr))
    indexArr = <int *>PyMem_Malloc(count * sizeof(indexArr[0]))
    statusArr = <MPI_Status *>PyMem_Malloc(count * sizeof(statusArr[0]))

    # Populate the request array.
    for n from 0 <= n < count:
        l = requests[n].mpi_request
        reqArr[n] = <MPI_Request>l

    # Call MPI_Waitsome()
    res = MPI_Waitsome(count, reqArr, &outCount, indexArr, statusArr)
    checkErr(res, "MPY_Waitsome")

    # Build results.
    if outCount == MPI_UNDEFINED:
        res = [None]
        if retStatus:
            res.append(None)
    else:
        # Build indices sequence and update request list.
        indLst = []
        for n from 0 <= n < outCount:
            idx = indexArr[n]
            indLst.append(idx)
            req = requests[idx]
            req.mpi_request = <long>reqArr[idx]
            req.length = statusArr[n].st_length
            requests[idx] = req
        res = [indLst]

        # Return statuses sequence.
        if retStatus:
            statLst = []
            for n from 0 <= n < outCount:
                status = statusArr[n]
                statLst.append(Status(status.MPI_SOURCE, status.MPI_TAG, 
                                      status.MPI_ERROR, status.st_length))
            res.append(statLst)
        
    # Free allocated arrays.
    PyMem_Free(reqArr)
    PyMem_Free(indexArr)
    PyMem_Free(statusArr)

    # Return results.
    if len(res) == 1:
        return res[0]
    else:
        return tuple(res)
        
def MPY_Wtick():
    """
    Python wrapper around MPI_Wtick() .

    Params:
      None

    Returns:
      Clock resolution, in seconds.
                                            """

    return MPI_Wtick()

def MPY_Wtime():
    """
    Python warpper around MPI_Wtime() .

    Params:
      None

    Returns:
      Time in seconds elapsed since a reference point in the past, guaranteed
      not to change during the life of a process.
                                                                                """

    return MPI_Wtime()

#################################################
# Utility routines
#################################################

cdef object unpickleCString(char *s, int n):
    """C 's' string contains a pickled object. Convert to a python string,
    and return the unpickled python object."""
    
    return cPickle.loads(PyString_FromStringAndSize(s, n))

cdef char * picklePyObject(object o, int *n):
    """Return a C string holding the pickled representation of
    python object 'o'. The caller is responsible of freeing the
    returned string.
                                                                """
    cdef char *s
    
    b = cPickle.dumps(o, 2)    # Pickle to python string using bin format
    count = len(b)
    s = <char *>PyMem_Malloc(count)  # Allocate C string of the same length
    # Copy python string to C string.
    # We could also write "memcpy(s,b,n)", but we feel it clearer
    # to explicitly call the Python to C conversion function.
    memcpy(s, PyString_AsString(b), count)
    
    n[0] = count
    return s

cdef char *picklePyObjectBuf(object o, int *n, char *buf):
    """Load into C array 'buf' a C string holding the pickled representation of
    python object 'o'. Returns value of 'buf'.
                                                                """

    b = cPickle.dumps(o, 2)    # Pickle to python string using bin format
    count = len(b)
    # Copy python string to C string.
    # We could also write "memcpy(s,b,n)", but we feel it clearer
    # to explicitly call the Python to C conversion function.
    memcpy(buf, PyString_AsString(b), count)
    
    n[0] = count
    return buf

cdef int lenPickle(object o):
    """Return the pickle length of object 'o'."""

    return len(cPickle.dumps(o,2))

cdef int recvCtrl(int source):
    """Receive a control message.
                                                     """
    cdef int bufSize
    cdef MPI_Status status
    
    MPI_Recv(&bufSize, 1, MPI_INT, source, 1, priv_comm, &status)

    return bufSize
    

cdef sendCtrl(int bufSize, int dest):
    """Send a control message.
                                                      """
    MPI_Send(&bufSize, 1, MPI_INT, dest, 1, priv_comm)


cdef validateDataType(dataType):
    """Validate dataType, raising an exception if invalid."""

    # Validate datatype.
    if dataType not in [MPY_PYTHON_OBJ,
                        MPY_PYTHON_STR,
                        MPY_PYTHON_ARRAY,
                        MPY_BYTE,
                        MPY_CHAR,
                        MPY_DOUBLE,
                        MPY_FLOAT,
                        MPY_INT,
                        MPY_LONG,
                        MPY_LONG_LONG,
                        MPY_SHORT,
                        MPY_UNSIGNED,
                        MPY_UNSIGNED_CHAR,
                        MPY_UNSIGNED_SHORT]:
        raise MPY_Error, "dataType must be 'MPY_PYTHON_OBJ' or one of "\
              "MPI datatypes"
    

cdef int dataTypeSize(long dataType):
    """Return the size in bytes of the given datatype."""

    cdef int sizeElem
    
    # Validate datatype.
    validateDataType(dataType)

    if dataType == MPY_PYTHON_OBJ:
        sizeElem = 1
    elif dataType in [MPY_CHAR, MPY_PYTHON_STR]:
        sizeElem = sizeof(char)
    elif dataType == MPY_BYTE:
        sizeElem = sizeof(unsigned char)
    elif dataType == MPY_SHORT:
        sizeElem = sizeof(short)
    elif dataType == MPY_UNSIGNED:
        sizeElem = sizeof(unsigned)
    elif dataType == MPY_UNSIGNED_CHAR:
        sizeElem = sizeof(unsigned char)
    elif dataType == MPY_UNSIGNED_SHORT:
        sizeElem = sizeof(unsigned short)
    elif dataType == MPY_INT:
        sizeElem = sizeof(int)
    elif dataType == MPY_LONG:
        sizeElem = sizeof(long)
    elif dataType == MPY_LONG_LONG:
        sizeElem = sizeof(long long)
    elif dataType == MPY_FLOAT:
        sizeElem = sizeof(float)
    elif dataType == MPY_DOUBLE:
        sizeElem = sizeof(double)

    return sizeElem

cdef obj2CArray(object obj, long dataType, void *arr):
    """Convert a python object to a C array before a send operation.
    If 'arr' is NULL, allocate buffer first, otherwise use this buffer. 

    Returns a 3-elem sequence:
      array address (as a long) caller must free it
      array len, in number of dataType elements
      mpi datatype of each element (as a long)
                                                                    """
    cdef int nElem, nBytes, i
    cdef ArrayType numArr   # cast warning
    cdef numArrInfo arrInfo
        
    # Validate datatype.
    validateDataType(dataType)

    # Pickle a general python object
    if dataType == MPY_PYTHON_OBJ:
        if arr == NULLPT:
            arr = picklePyObject(obj, &nElem)
        else:
            picklePyObjectBuf(obj, &nElem, <char *>arr)
        mpi_datatype = MPY_CHAR

    # Numeric array
    elif dataType == MPY_PYTHON_ARRAY:
       if type(obj) != _arrayType:
           raise MPY_Error, "array object expected, got %s" % type(obj)
       numArr = PyArray_ContiguousFromObject(obj, PyArray_NOTYPE, 0, 0) # cast warning
       arrInfo = getNumArrInfo(numArr)
       arr = <void *>arrInfo.data
       nElem = arrInfo.nElem
       mpi_datatype = arrInfo.mpi_datatype

    # MPI datatypes.
    else:
        # See if arg is a sequence.
        if type(obj) in [types.TupleType, types.ListType, types.StringType]:
            nElem = len(obj)
        # Scalar.
        else:
            nElem = 1
            obj = [obj]    # Convert it to sequence for ease of use.
        mpi_datatype = dataType
        # Allocate array if null.
        if arr == NULLPT:
            nBytes = nElem * dataTypeSize(dataType)
            arr = PyMem_Malloc(nBytes)
        try:
            if dataType in [MPY_CHAR, MPY_PYTHON_STR]:
                # Distinguish between a string and an array of small integers.
                if type(obj) == types.StringType:
                    memcpy(<char *>arr, PyString_AsString(obj), nElem)
                else:
                    for i from 0 <= i < nElem:
                        (<char *>arr)[i] = obj[i]
                mpi_datatype = MPY_CHAR
            elif dataType == MPY_BYTE:
                for i from 0 <= i < nElem:
                    (<unsigned char *>arr)[i] = obj[i]
            elif dataType == MPY_SHORT:
                for i from 0 <= i < nElem:
                    (<short *>arr)[i] = obj[i]
            elif dataType == MPY_UNSIGNED:
                for i from 0 <= i < nElem:
                    (<unsigned *>arr)[i] = obj[i]
            elif dataType == MPY_UNSIGNED_CHAR:
                for i from 0 <= i < nElem:
                    (<unsigned char *>arr)[i] = obj[i]
            elif dataType == MPY_UNSIGNED_SHORT:
                for i from 0 <= i < nElem:
                    (<unsigned short *>arr)[i] = obj[i]
            elif dataType == MPY_INT:
                for i from 0 <= i < nElem:
                    (<int *>arr)[i] = obj[i]
            elif dataType == MPY_LONG:
                for i from 0 <= i < nElem:
                    (<long *>arr)[i] = obj[i]
            elif dataType == MPY_LONG_LONG:
                for i from 0 <= i < nElem:
                    (<long long *>arr)[i] = obj[i]
            elif dataType == MPY_FLOAT:
                for i from 0 <= i < nElem:
                    (<float *>arr)[i] = obj[i]
            elif dataType == MPY_DOUBLE:
                for i from 0 <= i < nElem:
                    (<double *>arr)[i] = obj[i]
        except:
            raise MPY_Error, "python object cannot be converted to MPI datatype"

    return <long>arr, nElem, mpi_datatype

# Will eventually replace obj2CArray()
cdef obj2CArray2(object obj, long dataType, void *arr):
    """Convert a python object to a C array before a send operation.
    If obj is a Numeric array, us the internal buffer address.
    If 'arr' is NULL, allocate buffer first, otherwise use this buffer. 

    Returns a 4-elem sequence:
      array address (as a long) caller must free it (unless Numeric array)
      array len, in number of dataType elements
      mpi datatype of each element (as a long)
      numeric array object, returned to avoid making the array address invalid
      (the numeric array object may have been created here to make the
      array contiguous in memory, and must not be garbage collected!)
                                                                    """
    cdef int nElem, nBytes, i
    cdef ArrayType numArr   # cast warning
    cdef numArrInfo info
        
    # Validate datatype.
    validateDataType(dataType)

    # Pickle a general python object
    if dataType == MPY_PYTHON_OBJ:
        if arr == NULLPT:
            arr = picklePyObject(obj, &nElem)
        else:
            picklePyObjectBuf(obj, &nElem, <char *>arr)
        mpi_datatype = MPY_CHAR

    # Numeric array
    elif dataType == MPY_PYTHON_ARRAY:
        if type(obj) != _arrayType:
            raise MPY_Error, "array object expected, got %s" % type(obj)
        # Make the array contiguous. This may create a new object.
        numArr = PyArray_ContiguousFromObject(obj, PyArray_NOTYPE, 0, 0) # warning
        # Get the internal buffer address.
        info = getNumArrInfo(numArr)
        # IMPORTANT! PyArray_ContiguousFromObject() creates a python object,
        # associated with a reference count like all python objects.
        # Return 'numArr' so that its ref count is not decremented. Otherwise
        # 'numArr' ref count may go to 0 at function exit and the object will be
        # garbage collected. Consequently, the address of the internal buffer
        # which we extracted from 'numArr' and stored in 'info.data' will become
        # invalid. The caller simply has to ignore this 4th element: the associated
        # object will be garbage collected when the callr returns.
        return <long>info.data, info.nElem, info.mpi_datatype, numArr

    # MPI datatypes.
    else:
        # See if arg is a sequence.
        if type(obj) in [types.TupleType, types.ListType, types.StringType]:
            nElem = len(obj)
        # Scalar.
        else:
            nElem = 1
            obj = [obj]    # Convert it to sequence for ease of use.
        mpi_datatype = dataType
        # Allocate array if null.
        if arr == NULLPT:
            nBytes = nElem * dataTypeSize(dataType)
            arr = PyMem_Malloc(nBytes)
        try:
            if dataType in [MPY_CHAR, MPY_PYTHON_STR]:
                # Distinguish between a string and an array of small integers.
                if type(obj) == types.StringType:
                    memcpy(<char *>arr, PyString_AsString(obj), nElem)
                else:
                    for i from 0 <= i < nElem:
                        (<char *>arr)[i] = obj[i]
                mpi_datatype = MPY_CHAR
            elif dataType == MPY_BYTE:
                for i from 0 <= i < nElem:
                    (<unsigned char *>arr)[i] = obj[i]
            elif dataType == MPY_SHORT:
                for i from 0 <= i < nElem:
                    (<short *>arr)[i] = obj[i]
            elif dataType == MPY_UNSIGNED:
                for i from 0 <= i < nElem:
                    (<unsigned *>arr)[i] = obj[i]
            elif dataType == MPY_UNSIGNED_CHAR:
                for i from 0 <= i < nElem:
                    (<unsigned char *>arr)[i] = obj[i]
            elif dataType == MPY_UNSIGNED_SHORT:
                for i from 0 <= i < nElem:
                    (<unsigned short *>arr)[i] = obj[i]
            elif dataType == MPY_INT:
                for i from 0 <= i < nElem:
                    (<int *>arr)[i] = obj[i]
            elif dataType == MPY_LONG:
                for i from 0 <= i < nElem:
                    (<long *>arr)[i] = obj[i]
            elif dataType == MPY_LONG_LONG:
                for i from 0 <= i < nElem:
                    (<long long *>arr)[i] = obj[i]
            elif dataType == MPY_FLOAT:
                for i from 0 <= i < nElem:
                    (<float *>arr)[i] = obj[i]
            elif dataType == MPY_DOUBLE:
                for i from 0 <= i < nElem:
                    (<double *>arr)[i] = obj[i]
        except:
            raise MPY_Error, "python object cannot be converted to MPI datatype"

    # None is used as the last tuple element because no object is returned.
    return <long>arr, nElem, mpi_datatype, None

cdef prepRecv(int nElem, long dataType):
    """Prepare args for a receive.

    nElem      number of elements to receive
    dataType   element datatype

    Returns a 2-elem tuple:
      buffer address (cast to a long) caller must free it
      MPI datatype
                                                                  """
    cdef int sizeElem
    cdef void *arr

    # Validate datatype.
    validateDataType(dataType)
    
    # Allocate buffer where to receive message.
    if dataType == MPY_PYTHON_OBJ:
        mpi_datatype = MPY_BYTE
        sizeElem = 1
    else:
        mpi_datatype = dataType
        sizeElem = dataTypeSize(dataType)
        if dataType == MPY_PYTHON_STR:
            mpi_datatype = MPY_CHAR
    arr = <void *>PyMem_Malloc(nElem * sizeElem)
    return <long>arr, mpi_datatype

cdef prepRecv2(int nElem, object obj, long dataType):
    """Prepare args for a receive.

    nElem      Number of elements to receive
    obj        Numeric array, used only when dataType==MPY_PYTHON_ARRAY;
               represents the output buffer.
    dataType   Element datatype

    Returns a 4-elem tuple:
      buffer address (cast to a long) caller must free it (unless Numeric array)
      MPI datatype
      numeric array object, from which the buffer address comes from
      (see 'obj2CArray() for explanations)
      number of elements (only for Numeric arrays)
                                                                  """
    cdef int sizeElem
    cdef void *arr
    cdef ArrayType numArr
    cdef numArrInfo info

    # Validate datatype.
    validateDataType(dataType)
    
    # Allocate buffer where to receive message.
    if dataType == MPY_PYTHON_OBJ:
        mpi_datatype = MPY_BYTE
        sizeElem = 1

    # Numeric array.
    elif dataType == MPY_PYTHON_ARRAY:
        if type(obj) != _arrayType:
            raise MPY_Error, "array object expected, got %s" % type(obj)
        # Make the array contiguous. This may create a new object.
        numArr = PyArray_ContiguousFromObject(obj, PyArray_NOTYPE, 0, 0) # warning
        # Get the internal buffer address.
        info = getNumArrInfo(numArr)
        # See obj2CArray() for explanations on why 'numArr' is returned in the tuple.
        return <long>info.data, info.mpi_datatype, info.nElem, numArr

    # MPI datatypes.
    else:
        mpi_datatype = dataType
        sizeElem = dataTypeSize(dataType)
        if dataType == MPY_PYTHON_STR:
            mpi_datatype = MPY_CHAR
    arr = <void *>PyMem_Malloc(nElem * sizeElem)

    # Use None as the last tuple element because no object is returned.
    return <long>arr, mpi_datatype, nElem, None

cdef CArray2Obj(void *arr, long dataType, int msgSize, inBytes):
    """Convert a C array to a Python object following a receive operation.

    Params:
    
      msgSize     message length (in bytes if 'inBytes' is True)
      inBytes     True if 'msgSize' is measured in bytes, False if
                  measured in elements. This matters only for MPI types
                  represented on more than one byte.

    Returns:
      python object.
                                                                    """
    cdef int i, n
    cdef int sizeElem
    
    # Validate datatype.
    validateDataType(dataType)

    # Pickle a general python object
    if dataType == MPY_PYTHON_OBJ:
        # Convert to python string and unpickle to a python object.
        obj = unpickleCString(<char *>arr, msgSize)

    # Handle MPI datatypes.
    else:
        obj = []
        n = msgSize
        sizeElem = dataTypeSize(dataType)
        if inBytes:
            n = n / sizeElem

        # CHECK : any equivalent inside the python library ?
        
        if dataType == MPY_PYTHON_STR:
            obj = PyString_FromStringAndSize(<char *>arr, msgSize)
        elif dataType == MPY_CHAR:
            for i from 0 <= i < n:
                obj.append((<char *>arr)[i])
        elif dataType == MPY_BYTE:
            for i from 0 <= i < n:
                obj.append((<unsigned char *>arr)[i])
        elif dataType == MPY_SHORT:
            for i from 0 <= i < n:
                obj.append((<short *>arr)[i])
        elif dataType == MPY_UNSIGNED:
            for i from 0 <= i < n:
                obj.append((<unsigned *>arr)[i])
        elif dataType == MPY_UNSIGNED_CHAR:
            for i from 0 <= i < n:
                obj.append((<unsigned char *>arr)[i])
        elif dataType == MPY_UNSIGNED_SHORT:
            for i from 0 <= i < n:
                obj.append((<unsigned short *>arr)[i])
        elif dataType == MPY_INT:
            for i from 0 <= i < n:
                obj.append((<int *>arr)[i])
        elif dataType == MPY_LONG:
            for i from 0 <= i < n:
                obj.append((<long *>arr)[i])
        elif dataType == MPY_LONG_LONG:
            for i from 0 <= i < n:
                obj.append((<long long *>arr)[i])
        elif dataType == MPY_FLOAT:
            for i from 0 <= i < n:
                obj.append((<float *>arr)[i])
        elif dataType == MPY_DOUBLE:
            for i from 0 <= i < n:
                obj.append((<double *>arr)[i])

        # Do not return a one element sequence, except for a string.
        if dataType != MPY_CHAR:
            if n == 1:
                obj = obj[0]
                
    return obj

cdef numArrInfo getNumArrInfo(ArrayType numArr):
    """
    Return info about a Numeric array.
                                                                 """
    cdef numArrInfo info
    cdef int n, nElem

    info.data = numArr.data
    nElem = 1
    for n from 0 <= n < numArr.nd:
        nElem = nElem * numArr.dimensions[n]
    info.nElem = nElem
    info.mpi_datatype = numArrToMPI_types[numArr.descr.type_num]
    
    return info
    
cdef checkErr(int res, char *name):
    """
    Check an error code.

    Params:
      res         Error code from an MPI function.
      name        Function name

    Returns:
      None

    If the error code is not zero, raises an MPY_Error exception.

    NOTE: The function returns a Python object (None) so that exceptions can be
          propagated. Otherwise an 'except ...' clause would be needed.
                                                                          """
    if res != 0:
        raise MPY_Error, "%s:  error %d (%s)" % \
              (name, res, MPY_Error_string(res))

