from __future__ import annotations
from dataclasses import dataclass, field
from functools import partial
from inspect import signature
from typing import Any, Callable
from typing_extensions import Protocol

import numpy as np
from ipag_core.define import DataProcessor, DataContainerProtocol, DataTuple, MetaSetter, MetadataLike
from ipag_core.metadata import new_metadata


def data_processor(obj)->DataProcessor:
    """ parse input to a processor 
    
    Accepted input are: 
        - A Processor, returned as it is 
        - A Callable with signature `f(data)` , encapsulated in a FuncProc 
        - An iterable containing a valid processor input, encapsulated in a ProcessChain 

    Exemple:
        from functools import partial 

        processor( np.squeeze )
        processor( partial(np.mean, axis=0) )
        # equivalent to : 
        procfunc( np.mean, axis=0) 

        processor( [ procfunc(np.mean, axis=0), lambda x: x-256] ) 
        
    """
    if isinstance(obj, DataProcessor):
        return obj 
    if hasattr(obj, "__call__"):
        return FuncProc( obj )
    if hasattr( obj, "__iter__"):
        return ProcessChain( *(data_processor(child) for child in obj) )
    raise ValueError(f"{type(obj)} is not a processor")


def procfunc(func, *args, **kwargs):
    return FuncProc( partial(func, *args, **kwargs))

@dataclass
class FuncProc:
    """ Simple data process to encapsulate any function `f(data)` as process 

    see proc func 
    """
    func: Callable
    def process_data(self, data, metadata=None):
        return DataTuple(self.func(data), metadata)


class ProcessChain:
    """ Processor using  several processor and execute them in cascade """
    def __init__(self, *processors):
        self.processors = [data_processor(proc) for proc in processors]
    
    def process_data(self, data, metadata=None):
        for proc in self.processors:
            data, metadata = proc.process_data(data, metadata)
        return DataTuple(data, metadata)

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

    def process_data(self, data, metadata=None):
        return DataTuple(self.reducer(np.asarray(data), axis=self.axis), metadata)

@dataclass 
class DarkSubstractor:
    """ Processor substracted a Dark to data """
    dark: DataTuple | float | np.ndarray 
    
    def process_data(self, data, metadata=None):
        return DataTuple( np.asarray(data)-np.asarray(self.dark), metadata )

def _modulo_take( a:np.ndarray, index: int, axis: int =0):
    l = a.shape[axis]
    return np.take( a, index%l , axis)


@dataclass
class AxisLooper(DataProcessor):
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
class MetadataAdder(DataProcessor):
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
    def process_data(self, data, metadata=None) -> DataTuple:
        if not self.enabled:
            return DataTuple( data, metadata)

        if metadata is not None:
            if self.copy:
                metadata = metadata.copy()
            self.setter.set_to_metadata( metadata, self.state, prefix=self.prefix )
        return DataTuple( data, metadata )
    
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




