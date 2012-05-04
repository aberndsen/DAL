#ifndef __COMMONTUPLES__
#define __COMMONTUPLES__

#include "hdf5/types/h5tuple.h"

namespace DAL {

/*!
 * Coordinate3D<T> is a 3-dimensional coordinate with fields x, y, z.
 */
template<typename T> class Coordinate3D: public TupleBase<T,3> {
public:
  T x, y, z;
};

}

#endif

