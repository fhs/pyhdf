#!/usr/bin/env python

import sys
import math
import mpi

mpi.init()
rank = mpi.comm_rank()
size = mpi.comm_size()

root = 0
worldGroup = mpi.comm_group()

print "I am P%d of %d on node %s" % \
      (rank, size, mpi.get_processor_name())

mpi.barrier()

res = mpi.allreduce(rank*10, mpi.MPI_SUM)
print "P%d mpi.allreduce()=%d" % (rank, res)
mpi.barrier()

# MPI_Cart_create() returns MPI_COMM_NULL if the process does not
# belong to the cartesian grid.
# It seems that MPI_Cart_create() can return two different pointers
# for the same communicator. So, it seems to be incorrect to
# assume that two communicators are different if theit addresses differ.
cartComm = mpi.cart_create(mpi.MPI_COMM_WORLD, (3,2), (True, True),
                          True)
mpi.barrier()

if cartComm != mpi.MPI_COMM_NULL:
    rnk = mpi.comm_rank(cartComm)
    grp = mpi.comm_group(cartComm)
    print "P%d cartComm=%x rank in cartComm=%d" % (rank, cartComm, rnk)
    print "P%d group_translate_ranks()=" % rnk, \
          mpi.group_translate_ranks(grp, range(mpi.comm_size(cartComm)), grp)
    size, period, coord = mpi.cart_get(cartComm, 2)
    print "P%d cart_get  size=" % rank,size,"period=",period,"coord=",coord

    coords = mpi.cart_coords(cartComm, rnk, 2)
    print "P%d coords=%s" % (rnk, coords)

    print "P%d shift dim=0 dir=0"  % rank, mpi.cart_shift(cartComm, 0, 0)
    print "P%d shift dim=0 dir=1"  % rank, mpi.cart_shift(cartComm, 0, 1)
    print "P%d shift dim=0 dir=2"  % rank, mpi.cart_shift(cartComm, 0, 2)



sys.exit()


l = mpi.group_translate_ranks(worldGroup,
                              range(mpi.comm_size()),
                              worldGroup)
print "P%d original ranks=" % rank,l

# Create a new group.
excl = [0]                  # processes to exclude from newGroup
newGroup = mpi.group_excl(worldGroup, excl)

l = mpi.group_translate_ranks(worldGroup,
                              range(mpi.comm_size()),
                              newGroup)
print "P%d worldGroup ranks in newGroup" % rank, l

if not rank in excl:
    l = mpi.group_translate_ranks(newGroup,
                                  range(size - len(excl)),  # valid ranks in newGroup
                                  worldGroup)
    print "P%d newGroup ranks in worldGroup" % rank, l

# comm_create() is a collective communication operation. Every process
# must call it. MPI_COMM_NULL is returned for processes that do not belong
# to the group assigned to the communicator.
#
# process   rank in worldGroup  rank in newGroup
#   0             0                 ---
#   1             1                  0
#   2             2                 ---
#   3             3                  1

newComm  = mpi.comm_create(mpi.MPI_COMM_WORLD, newGroup)
if newComm != mpi.MPI_COMM_NULL:
    print "P%d newComm.comm_size()=" % rank,mpi.comm_size(newComm)
    print "P%d rank in newGroup=%d" % (rank, mpi.comm_rank(newComm))
    
newGroup = mpi.group_free(newGroup)

# Cannot free a communicator to which we do not belong.
if not rank in excl:
    newComm = mpi.comm_free(newComm)

sys.exit()
mpi.barrier()
t0 = mpi.wtime()

if rank == root:
    # Send arbitrary objects to process 1.
    # Note that we cannot pass a "live" var in the object (why?)
    for n in range(1):
        #k = n   # will not work
        k = n+1  # will work
        buf = [k,1,2,3,"andre gosselin",{1:'a',2:'b'}]
        print "sending #%d to 1" % n, buf
        mpi.send(buf, 1)
        
elif rank == 1:
    # Receive arbitrary objects from process 'root'
    for n in range(1):
        buf = mpi.recv(root)
        print "received #%d from root" % n, buf

mpi.barrier()

sys.exit()

for k in range(1,4):
    if rank == 0:
        b1 = mpi.bcast([k * 100000] * 3, root)
        b2 = mpi.bcast(k * 100000, root)
    else:
        # This works
        b1 = mpi.bcast([0,0,0], root)
        b2 = mpi.bcast(-1, root)
        # This fails, because data lengths do not match
        #b1 = mpi.bcast([1,2], root)
        # This fails, because data types do not match
        #b1 = mpi.bcast([1.0,2.0,3.0], root)
        # This returns spurious values after the first 3.
        #b1 = mpi.bcast([1,2,3,4,5], root)
    print "P%d b1=%s b2=%s" % (rank, b1, b2)
    mpi.barrier(mpi.MPI_COMM_WORLD)

print "elapsed on P%d" % rank,mpi.wtime() - t0
mpi.barrier()

buf = [[1,2,3],[4,5,6],(7,8,9), math.pi, 'foo bar']
if rank == 0:
    b = mpi.bcast(buf, root, mpi.MPI_COMM_WORLD)
else:
    # The buffer must be at least as long as the message
    # to be received. Otherwise, a "message truncated" error
    # will be raised.
    b = mpi.bcast(' '*100, root)
print "bcast at rank=%d" % rank,b
mpi.barrier()

x = mpi.reduce(10L, mpi.MPI_SUM, 0)
if rank == 0:
    print "***reduce=",x
mpi.finalize()
