#ifndef __HDF5DATASET__
#define __HDF5DATASET__

#include <string>
#include <vector>
#include <hdf5.h>
#include "hdf5/types/hid_gc.h"
#include "hdf5/types/h5exception.h"
#include "hdf5/HDF5GroupBase.h"

namespace DAL {

/*!
 * \class HDF5DatasetBase
 *
 * Provides generic functionality for HDF5 Datasets.
 */
template<typename T> class HDF5DatasetBase: public HDF5GroupBase {
public:
  enum Endianness { NATIVE = 0, LITTLE, BIG };

  HDF5DatasetBase( const hid_gc &parent, const std::string &name ): HDF5GroupBase(parent, name) {}

  /*!
   * Creates a new dataset with dimensions sized `dims` and can be scaled up to `maxdims`. The
   * rank of the dataset is dims.size() == maxdims.size(). A maximum of -1 represents an unbounded dimension.
   *
   * If a `filename` is given, that file will be used to store the data. The file can be provided by
   * the user, or will be created upon the first write. Note that the filename cannot be changed
   * after the dataset has been created (HDF5 1.8.7), so providing absolute paths will make the
   * dataset difficult to copy or move across systems.
   *
   * If no `filename' is given, dims == maxdims is required due to limitations of HDF5.
   *
   * `endianness` toggles whether the data is in big-endian format. Typically:
   *  NATIVE: use the endianness of the current machine
   *  LITTLE: use little-endian: ARM, x86, x86_64
   *  BIG:    use big-endian:    MIPS, POWER, PowerPC, SPARC
   */
  void create( const std::vector<ssize_t> &dims, const std::vector<ssize_t> &maxdims, const std::string &filename = "", enum Endianness endianness = NATIVE );
  virtual void create() { throw HDF5Exception("create() not supported on a dataset"); }

  /*!
   * Returns the rank of the dataset.
   */
  size_t ndims();

  /*!
   * Returns the dimension sizes.
   */
  std::vector<ssize_t> dims();

  /*!
   * Returns the maximum dimension sizes to which this dataset can grow;
   * elements of -1 represent unbounded dimensions.
   */
  std::vector<ssize_t> maxdims();

  /*!
   * Changes the dimensionality of the dataset. Elements of -1 represent unbounded dimensions.
   * If this dataset uses internal storage (i.e. externalFiles() is empty), dimensions
   * cannot be unbounded due to limitations of HDF5.
   *
   * For now, resizing is only supported if external files are used.
   */
  void resize( const std::vector<ssize_t> &newdims );

  /*!
   * Returns a list of the external files containing data for this dataset.
   */
  std::vector<std::string> externalFiles();

  /*!
   * Retrieves any matrix of data of sizes `size` from position `pos`.
   * `buffer` must point to a memory block large enough to hold the result.
   *
   * Requires:
   *    pos.size() == size.size() == ndims()
   */
  void getMatrix( const std::vector<size_t> &pos, const std::vector<size_t> &size, T *buffer );

  /*!
   * Stores any matrix of data of sizes `size` at position `pos`.
   *
   * Requires:
   *    pos.size() == size.size() == ndims()
   */
  void setMatrix( const std::vector<size_t> &pos, const std::vector<size_t> &size, const T *buffer );

  /*!
   * Retrieves a 2D matrix of data from a 2D dataset from position `pos`.
   * `buffer` must point to a memory block large enough to hold the result.
   *
   * pos:                       position of the first sample
   * dim1, dim2, outbuffer2:    2D array, the size of which determines the amount of data to retrieve
   * dim1index, dim2index:      indices of the dimensions to query
   *
   * Requires:
   *    ndims() >= 2
   *    pos.size() == ndims()
   *    dim1index < dim2index < ndims()
   */
  void get2D( const std::vector<size_t> &pos, size_t dim1, size_t dim2, T *outbuffer2, unsigned dim1index = 0, unsigned dim2index = 1 );

  /*!
   * Stores a 2D matrix of data from a 2D dataset at position `pos`.
   *
   * pos:                       position of the first sample
   * dim1, dim2, outbuffer2:    2D array, the size of which determines the amount of data to write
   * dim1index, dim2index:      indices of the dimensions to query
   *
   * Requires:
   *    ndims() >= 2
   *    pos.size() == ndims()
   *    dim1index < dim2index < ndims()
   */
  void set2D( const std::vector<size_t> &pos, size_t dim1, size_t dim2, const T *inbuffer2, unsigned dim1index = 0, unsigned dim2index = 1 );

  /*!
   * Retrieves a 1D matrix of data from a 1D dataset from position `pos`.
   * `buffer` must point to a memory block large enough to hold the result.
   *
   * pos:                       position of the first sample
   * dim1, outbuffer1:          1D array, the size of which determines the amount of data to write
   * dim1index:                 index of the dimension to query
   *
   * Requires:
   *    ndims() >= 1
   *    pos.size() == ndims()
   *    dim1index < ndims()
   */
  void get1D( const std::vector<size_t> &pos, size_t dim1, T *outbuffer1, unsigned dim1index = 0 );

  /*!
   * Stores a 1D matrix of data from a 1D dataset at position `pos`.
   *
   * pos:                       position of the first sample
   * dim1, outbuffer1:          1D array, the size of which determines the amount of data to write
   * dim1index:                 index of the dimension to query
   *
   * Requires:
   *    ndims() >= 1
   *    pos.size() == ndims()
   *    dim1index < ndims()
   */
  void set1D( const std::vector<size_t> &pos, size_t dim1, const T *inbuffer1, unsigned dim1index = 0 );

  /*!
   * Retrieves a single value from the dataset from position `pos`.
   *
   * Requires:
   *    pos.size() == ndims()
   */
  T getScalar( const std::vector<size_t> &pos );

  /*!
   * Stores a single value into the dataset at position `pos`.
   *
   * Requires:
   *    pos.size() == ndims()
   */
  void setScalar( const std::vector<size_t> &pos, const T &value );

protected:
  virtual hid_gc *open( hid_t parent, const std::string &name ) const {
    return new hid_gc(H5Dopen2(parent, name.c_str(), H5P_DEFAULT), H5Dclose, "Could not open dataset");
  }

  bool bigEndian( enum Endianness endianness ) const;

  // if the strides vector is empty, a continuous array is assumed
  void matrixIO( const std::vector<size_t> &pos, const std::vector<size_t> &size, const std::vector<size_t> &strides, T *buffer, bool read );
};

}

#include "hdf5/HDF5DatasetBase.tcc"

#endif

