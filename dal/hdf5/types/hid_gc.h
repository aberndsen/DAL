#ifndef DAL_HID_GC_H
#define DAL_HID_GC_H

#include <hdf5.h>
#include "dal/hdf5/exceptions/exceptions.h"

namespace DAL {

// Autocloses hid_t types using closefunc() on destruction, and keeps a reference count.
class hid_gc
{
public:
  // allow deference of actual construction to operator=
  hid_gc(): hid(0), closefunc(0) {}

  hid_gc(hid_t hid, hid_t (*closefunc)(hid_t) = 0, const std::string &errordesc = ""): hid(hid), closefunc(closefunc) {
    // checking for success here greatly reduces the code base
    if (hid <= 0)
      throw HDF5Exception(errordesc);

    H5Iinc_ref(hid);
  }

  hid_gc( const hid_gc &other ): hid(other.hid), closefunc(other.closefunc) {
    if (isset()) {
      H5Iinc_ref(hid);
    }  
  }

  ~hid_gc() {
    if (isset() && H5Idec_ref(hid) == 1 && closefunc) {
      closefunc(hid);
    }
  }

  hid_gc &operator=( hid_gc other ) {
    std::swap(hid, other.hid);
    std::swap(closefunc, other.closefunc);

    return *this;
  }

  operator hid_t() const { return hid; }

  /*!
   * Returns true if this object wraps a hid.
   */
  bool isset() const { return hid > 0; }

private:
  hid_t hid;
  hid_t (*closefunc)(hid_t);
};

// Autocloses hid_t types using closefunc() on destruction, without using reference counting.
//
// This variant is faster than hid_gc, but cannot be copied.
class hid_gc_noref
{
public:
  hid_gc_noref(hid_t hid, hid_t (*closefunc)(hid_t) = 0, const std::string &errordesc = ""): hid(hid), closefunc(closefunc) {
    // checking for success here greatly reduces the code base
    if (hid <= 0)
      throw HDF5Exception(errordesc);
  }

  ~hid_gc_noref() {
    if (isset() && closefunc) {
      closefunc(hid);
    }  
  }

  operator hid_t() const { return hid; }

  /*!
   * Returns true if this object wraps a hid.
   */
  bool isset() const { return hid > 0; }

private:
  hid_gc_noref( const hid_gc &other );
  hid_gc_noref &operator=( const hid_gc & );

  const hid_t hid;
  hid_t (*const closefunc)(hid_t);
};

}

#endif

