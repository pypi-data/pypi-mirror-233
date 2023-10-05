from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any

from ipag_core.define import DataReader, DataWriter, DataProcessor, DataTuple, MetadataLike
from ipag_core.processor import data_processor


def _get_read_method( obj ):
    if hasattr(obj, "read_data"):
        return  obj.read_data 
    if hasattr(obj, "__call__"):
        return  obj 
    raise ValueError("input io must have a read_data() method or shall be callable")     

def _get_write_method( objs ):
    wrfuncs = []
    for io in objs:
        if hasattr(io, "write_data"):
            wrfuncs.append(io.write_data)
        elif hasattr(io, "__call__"):
            wrfuncs.append( io ) 
        else:
            raise ValueError("outputio must have a write_data() method or shall be callable")

    def write(data, metadata=None):
        for wr in wrfuncs:
            wr( data, metadata)
    return write 
    

class MergeDataIo(DataReader, DataWriter):
    """ Merge one 'input' io and one or more 'output' io 

    Args:
        io_in: A single io object or a callable with signature f() called at read_data
        *io_outs: A list of io object or functions with signature f(data,metadata). 
            They are executed with the same order when write method is called 

    Note the read and write function are built at init. Therefore the input and output 
    io(s) cannot be change after object creation. 
    """
    def __init__(self, io_in, *io_outs):
        self.read_data  = _get_read_method(io_in) 
        self.write_data = _get_write_method( io_outs)
    
    def read_data(self):
        raise ValueError("PipeIo wasn't initialised")

    def write_data(self, data:Any, metadata: MetadataLike | None = None):
        raise ValueError("PipeIo wasn't initialised")


class DataPipe(DataReader, DataWriter, DataProcessor):
    def __init__(self, *args: DataReader|DataWriter|DataProcessor):
        self._reader = None 
        self._pipeline = []
        self._pipeline_types = []

        if args:
            if isinstance( args[0], DataReader):
                self._reader = args[0]
                args = args[1:]
        self.extend( args ) 
    
    def _check_if_has_writer(self):
        self._has_writer = any( self._pipeline_types)
    
    def _iter_pipe(self):
        for is_writer, obj in zip(self._pipeline_types, self._pipeline):
            yield is_writer, obj
    
    def read_data(self) -> DataTuple:
        if self._reader is None:
            raise ValueError( "This Data Pipe has no data_reader ")
        
        data, metadata = self._reader.read_data()
        for is_writer, obj in self._iter_pipe():
            if is_writer:
                obj.write_data( data, metadata)
            else:
                data, metadata = obj.process_data( data, metadata)
        return DataTuple( data, metadata) 
    
    def write_data(self, data: Any, metadata:MetadataLike|None = None):
        if not self._has_writer:
            raise ValueError( "This Data Pipe has no data_writer defined" )

        for is_writer, obj in self._iter_pipe():
            if is_writer:
                obj.write_data( data, metadata)
            else:
                data, metadata = obj.process_data( data, metadata)
    
    def process_data(self, data, metadata=None) -> DataTuple:
        for is_writer, obj in self._iter_pipe():
            if not is_writer:
                data, metadata = obj.process_data( data, metadata)
        return DataTuple(data, metadata)
    
    def append(self, proc_or_writer: DataWriter | DataProcessor)->None:
        if isinstance( proc_or_writer, DataWriter):
            self._pipeline.append(proc_or_writer)
            self._pipeline_types.append( True) 
            self._has_writer = True 
        else:
            self._pipeline.append( data_processor(proc_or_writer) )
            self._pipeline_types.append( False) 

    def extend(self, proc_or_writer_list : list[ DataWriter|DataProcessor ] ):
        for obj in proc_or_writer_list:
            self.append( obj )

    def insert(self, index, proc_or_writer: DataWriter | DataProcessor)->None:
        if isinstance( proc_or_writer, DataWriter):
            self._pipeline.insert(index, proc_or_writer)
            self._pipeline_types.insert(index, True) 
            self._has_writer = True 
        else:
            self._pipeline.insert(index,  data_processor(proc_or_writer) )
            self._pipeline_types.insert(index, False) 
    
    def purge(self, *types):
        """ remove all processor matching any of the given types """
        for obj in list(self._pipeline):
            if isinstance( obj, types):
                self.remove( obj )

    def pop(self, index=-1):
        robj = self._pipeline.pop(index) 
        self._pipeline_types.pop(index)
        self._check_if_has_writer()
        return robj 
    
    def remove(self, obj):
        i = self._pipeline.index(obj)
        self._pipeline.remove(obj)
        self._pipeline_types.pop(i) 
    
    def index(self, obj):
        return self._pipeline.index(obj)
    
    def clear(self):
        self._pipeline.clear()
        self._pipeline_types.clear()

    def copy(self):
        if self._reader:
            return self.__class__(self._reader, *self._pipeline)
        else:
            return self.__class__( *self._pipeline)
    
    


class ProcessedDataIo(DataReader, DataWriter):
    """ An Io Processing data before returning it 

    Args:
        io: The Io object use to first retrieve the data 
        *procs: list of processor. can be 
            - a Process object 
            - a callable with signature  f(data) 
            - a list of one of these three types

    Exemple:
        
        import numpy as np 
        from ipag_core.ipag import ProcessedIo, FitsIo, procfunc 
        
        image_io = ProcessedIo( FitsIo("my_cube.fits"), procfunc(np.mean, axis=0) )
        data, metdata = image_io.read()     

    """
    def __init__(self, io: DataReader | DataWriter, *procs: DataProcessor):
        self.io = io 
        self.proc = data_processor(procs) 
    
    def write_data(self, data, metadata=None):
        self.io.write_data( data, metadata )

    def read_data(self):
        data, metadata = self.io.read_data() 
        data, metadata = self.proc.process_data( data, metadata)
        return DataTuple( data, metadata )

class ProcessAndWrite:
    def __init__(self, *args):
        *processes, writer = args 
        if not isinstance( writer, DataWriter):
            raise ValueError("Last argument must be  DataWriter compatible")
        self.io = writer 
        self.proc = data_processor(processes)

    def write_data(self, data, metadata=None):
        data, metadata = self.proc.process_data( data, metadata)
        self.io.write_data(data, metadata)

    def read_data(self):
        return self.io.read_data()
