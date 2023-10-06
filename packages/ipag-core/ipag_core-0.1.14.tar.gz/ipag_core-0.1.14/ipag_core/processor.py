from __future__ import annotations
from dataclasses import dataclass, field
from functools import partial
from inspect import signature
from typing import Any, Callable
from typing_extensions import Protocol

import numpy as np
from ipag_core.define import DataProcessor, DataContainerProtocol, DataTuple, MetaSetter, MetadataLike, MetadataTransformer, Transformer
from ipag_core.metadata import new_metadata



@dataclass 
class DataReducer:
    """ Reduce data with a function f(data, axis=) as e.g. np.mean 

    Parameters:
        reducer: reduce function, default is np.mean 
        axis: axis number to reduce 'a la numpy'  
    """
    
    reducer: Callable = field( default= np.mean)# method to collapse the first cube dimension 
    """ method of signature f(a, axis=) to reduce the data. Default is np.mean  """
    
    axis: int | tuple = 0 
    """ Which axis is being reduced """

    def transform(self, data):
        return self.reducer(np.asarray(data), axis=self.axis)

@dataclass 
class DataSubstractor:
    """ Processor substracted a Dark to data """
    offset: DataTuple | float | np.ndarray 
    enabled: bool = True 
    def trasnform(self, data):
        if self.enabled:
            return np.asarray(data)-np.asarray(self.offset)
        return np.asarray(data)


def _modulo_take( a:np.ndarray, index: int, axis: int =0):
    l = a.shape[axis]
    return np.take( a, index%l , axis)


@dataclass
class AxisLooper:
    """ This processor is looping over one axis of the input array

    The returned array will have one dimension less. 
    When the axis length is exhausted it will restart from index 0
    """

    axis: int = 0
    """ axis number to iter on """

    _iteration = 0 
    def process_data(self, data:np.ndarray, metadata:MetadataLike|None =None) -> DataTuple:
        new_data =  _modulo_take(data, self._iteration, self.axis )
        self._iteration += 1
        return DataTuple(new_data, metadata)


@dataclass 
class MetadataAdder(MetadataTransformer):
    """ Transform the metadata by adding information from a state object 
    
    The metadata is copied unless copy is false 

    Args:
        state: A data structure 
        setter: a MetaSetter appropriate for the state data 
        prefix: optional prefix added to metadata keys
        copy: if True (default) the returned metadata is copied otherwise 
            it is transformed in place 
    """
    state: Any
    setter: MetaSetter
    prefix: str = ""
    copy: bool = True 
    enabled: bool = True 
    def transform_metadata(self, metadata:MetadataLike)->MetadataLike:
        if not self.enabled:
            return metadata
        if metadata is None:
            return self.new_metadata()
        if self.copy:
                metadata = metadata.copy()
        self.setter.set_to_metadata( metadata, self.state, prefix=self.prefix )
        return metadata
    
    def new_metadata(self):
        metadata = new_metadata()
        self.setter.set_to_metadata( metadata, self.state, prefix=self.prefix )
        return metadata

@dataclass 
class ImageTransformer(DataProcessor):
    """ A simple Image data processor to flip and transpose image 

    Args:
        flip_cols: if True, columns (second dimension) is flipped
        flip_rows: if True, rows (first diemnsion) is flipped 
        transpose: if True the table is transposed (after the flip !!)
        enabled:  set to False to disable the data process
    """
    flip_cols: bool = False 
    flip_rows: bool = False 
    transpose: bool = False 
    enabled: bool = True 

    def process_data(self, data, metadata=None) -> DataTuple:
        if not self.enabled:
            return DataTuple( data, metadata)
        if self.flip_cols:
            data = data[:,::-1]
        if self.flip_rows:
            data = data[::-1,:]
        if self.transpose:
            data = data.transpose()
        return DataTuple( data, metadata)




