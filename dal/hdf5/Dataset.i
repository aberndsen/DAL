// SWIG customisations for class Dataset

// member functions that return *this are problematic,
// because SWIG generates a new wrapper object and does not
// know how to do the memory management right between
// both wrapper objects. So we write our own further below.
%rename(_create) DAL::Dataset::create;

// -------------------------------
// Type marshalling
// -------------------------------

%{
  #define SWIG_FILE_WITH_INIT
%}

%include "external/numpy.i"

%init %{
  import_array();
%}

%define DATASETTYPE( datatype, numpytype, indextype )

// tell numpy which combinations of data types and index types we use
%numpy_typemaps(datatype, numpytype, indextype)

// Tell SWIG how we call our dimension and array parameters.
// The C++ arg order *and* identifiers in {(...)} must match exactly, but may be a sub-set of the args in the C++ code.
%apply (indextype DIM1, datatype* INPLACE_ARRAY1) {(indextype dim1, datatype *outbuffer1)}
%apply (indextype DIM1, indextype DIM2, datatype* INPLACE_ARRAY2) {(indextype dim1, indextype dim2, datatype *outbuffer2)}

%apply (indextype DIM1, datatype* IN_ARRAY1) {(indextype dim1, const datatype *inbuffer1)}
%apply (indextype DIM1, indextype DIM2, datatype* IN_ARRAY2) {(indextype dim1, indextype dim2, const datatype *inbuffer2)}

%enddef

// enumerate all the dataset types that we refer to (we use native types, so do not fix their size)
DATASETTYPE(short, NPY_SHORT, size_t);
DATASETTYPE(float, NPY_FLOAT, size_t);
DATASETTYPE(std::complex<float>, NPY_CFLOAT, size_t);

// -------------------------------
// Templates
// -------------------------------

// ignore functions that contain raw pointers that
// cannot be marshalled.
%ignore *::getMatrix;
%ignore *::setMatrix;

%include hdf5/Dataset.h

namespace DAL {
  %template(DatasetShort)        Dataset<short>;
  %template(DatasetFloat)        Dataset<float>;
  %template(DatasetComplexFloat) Dataset< std::complex<float> >;
}

// -------------------------------
// Class extensions for bindings
// -------------------------------

%pythoncode %{
  import numpy

  # record the numpy datatypes used in the various datasets
  DatasetShort.dtype = numpy.short
  DatasetFloat.dtype = numpy.single
  DatasetComplexFloat.dtype = numpy.csingle

  del numpy
%}

%extend DAL::Dataset {
  %pythoncode {
    def create(self):
      self._create()
      return self
  }    
}

