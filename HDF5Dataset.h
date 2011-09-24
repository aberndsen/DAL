#ifndef __HDF5DATASET__
#define __HDF5DATASET__

#include <string>
#include <vector>
#include <hdf5.h>
#include "HDF5Group.h"
#include "hdf5core/hid_gc.h"
#include "hdf5core/h5typemap.h"

template<typename T> class HDF5Dataset: public HDF5Group {
public:
  enum Endianness { NATIVE = 0, LITTLE, BIG };

  /*
   * Creates a new dataset with dimensions sized `dims` and can be scaled up to `maxdims`. The
   * rank of the dataset is dims.size() <= maxdims.size(). Any dimension d not mentioned in maxdims
   * has its maximum set by dims[d]. A maximum of -1 represents an unbounded dimension.
   *
   * If a filename is given, that file will be used to store the data. The file can be provided by
   * the user, or will be created upon the first write.
   *
   * `bigEndian` toggles whether the data is in big-endian format. Typically:
   *  big-endian:    MIPS, POWER, PowerPC, SPARC
   *  little-endian: ARM, x86, x86_64
   */
  void create( const std::vector<ssize_t> &dims, const std::vector<ssize_t> &maxdims, const std::string &filename = "", enum Endianness endianness = NATIVE );
  virtual void create() const { throw HDF5Exception("create() not supported on a dataset"); }

  size_t ndims();
  std::vector<ssize_t> dims();
  std::vector<ssize_t> maxdims();
  std::vector<std::string> externalFiles();

  void getMatrix( const std::vector<size_t> &pos, const std::vector<size_t> &size, T *buffer );
  T getScalar( const std::vector<size_t> &pos );

protected:
  HDF5Dataset( const hid_gc &parent, const std::string &name ): HDF5Group(parent, name) {}

  virtual hid_gc *open( hid_t parent, const std::string &name ) const {
    return new hid_gc(H5Dopen2(parent, name.c_str(), H5P_DEFAULT), H5Dclose, "Could not open dataset");
  }

private:
  bool bigEndian( enum Endianness endianness ) const {
    switch (endianness) {
      union {
        char c[sizeof (unsigned)];
        unsigned i;
      } checker;

      case LITTLE:
        return false;

      case BIG:
        return true;

      default:
        // we don't actually know sizeof unsigned, so check for little-endianness
        checker.i = 1;
        return checker.c[0] != 1;
    };
  }
};

template<typename T> void HDF5Dataset<T>::create( const std::vector<ssize_t> &dims, const std::vector<ssize_t> &maxdims, const std::string &filename, enum Endianness endianness ) {

  const size_t rank = dims.size();

  // convert from ssize_t -> hsize_t
  std::vector<hsize_t> hdims(rank), hmaxdims(rank);

  for (size_t i = 0; i < rank; i++) {
    hdims[i] = dims[i];
    hmaxdims[i] = i < maxdims.size()
                    ? (maxdims[i] == -1 ? H5S_UNLIMITED : maxdims[i])
                    : dims[i];
  }

  // define the layout and the location of the data
  hid_gc_noref filespace(H5Screate_simple(rank, &hdims[0], &hmaxdims[0]), H5Sclose, "Could not create simple dataspace");

  hid_gc_noref dcpl(H5Pcreate(H5P_DATASET_CREATE), H5Pclose, "Could not create dataset creation property list (dcpl)");
  H5Pset_layout(dcpl, H5D_CONTIGUOUS);
  if (filename != "") {
    if (H5Pset_external(dcpl, filename.c_str(), 0, H5F_UNLIMITED) < 0)
      throw HDF5Exception("Could not add external file to dataset");
  }

  // create the dataset
  delete _group; _group = 0;
  _group = new hid_gc(H5Dcreate2(parent, _name.c_str(), h5dataType<T>(bigEndian(endianness)), filespace, H5P_DEFAULT, dcpl, H5P_DEFAULT), H5Dclose, "Could not create dataset");
}

template<typename T> size_t HDF5Dataset<T>::ndims()
{
  hid_gc dataspace(H5Dget_space(group()), H5Sclose, "Could not obtain dataspace of dataset");

  int rank = H5Sget_simple_extent_ndims(dataspace);

  if (rank < 0)
    throw HDF5Exception("Could not obtain rank of dataspace");

  return rank;
}

template<typename T> std::vector<ssize_t> HDF5Dataset<T>::dims()
{
  const size_t rank = ndims();
  std::vector<hsize_t> dims(rank);
  std::vector<ssize_t> result(rank);

  hid_gc dataspace(H5Dget_space(group()), H5Sclose, "Could not obtain dataspace of dataset");

  if (H5Sget_simple_extent_dims(dataspace, &dims[0], NULL) < 0)
    throw HDF5Exception("Could not obtain dimensions of dataspace");

  for (size_t i = 0; i < rank; i++) {
    result[i] = dims[i];
  }

  return result;
}

template<typename T> std::vector<ssize_t> HDF5Dataset<T>::maxdims()
{
  const size_t rank = ndims();
  std::vector<hsize_t> maxdims(rank);
  std::vector<ssize_t> result(rank);

  hid_gc dataspace(H5Dget_space(group()), H5Sclose, "Could not obtain dataspace of dataset");

  if (H5Sget_simple_extent_dims(dataspace, &maxdims[0], NULL) < 0)
    throw HDF5Exception("Could not obtain maximum dimensions of dataspace");

  for (size_t i = 0; i < rank; i++) {
    result[i] = maxdims[i];
  }

  return result;
}

template<typename T> std::vector<std::string> HDF5Dataset<T>::externalFiles()
{
  hid_gc dcpl(H5Dget_create_plist(group()), H5Pclose, "Could not open dataset creation property list (dcpl)");

  int numfiles = H5Pget_external_count(dcpl);

  if (numfiles < 0)
    throw HDF5Exception("Could not obtain number of external files");

  std::vector<std::string> files(numfiles);

  for (int i = 0; i < numfiles; i++) {
    char buf[1024];
    if (H5Pget_external(dcpl, i, sizeof buf, buf, NULL, NULL) < 0)
      throw HDF5Exception("Could not obtain file name of external file");

    // null-terminate in case file name is >=1024 characters long
    buf[sizeof buf - 1] = 0;

    files[i] = buf;
  }

  return files;
}

template<typename T> void HDF5Dataset<T>::getMatrix( const std::vector<size_t> &pos, const std::vector<size_t> &size, T *buffer )
{
  const size_t rank = ndims();

  std::vector<hsize_t> offset(rank), count(rank);

  for (size_t i = 0; i < rank; i++) {
    offset[i] = pos[i];
    count[i]  = size[i];
  }

  hid_gc_noref dataspace(H5Dget_space(group()), H5Sclose, "Could not retrieve dataspace of group");

  if (H5Sselect_hyperslab(dataspace, H5S_SELECT_SET, &offset[0], NULL, &count[0], NULL) < 0)
    throw HDF5Exception("Could not select hyperslab in dataspace");

  for (size_t i = 0; i < rank; i++) {
    offset[i] = 0;
  }

  hid_gc_noref memspace(H5Screate_simple(rank, &count[0], NULL), H5Sclose, "Could not create simple dataspace");

  if (H5Sselect_hyperslab(memspace, H5S_SELECT_SET, &offset[0], NULL, &count[0], NULL) < 0)
    throw HDF5Exception("Could not select hyperslab in dataspace");

  if (H5Dread(group(), h5nativeType<T>(), memspace, dataspace, H5P_DEFAULT, buffer) < 0)
    throw HDF5Exception("Could not read data from dataset");
}

template<typename T> T HDF5Dataset<T>::getScalar( const std::vector<size_t> &pos )
{
  T value;
  std::vector<size_t> size(ndims(),1);

  getMatrix(pos, size, &value);

  return value;
}

#endif
