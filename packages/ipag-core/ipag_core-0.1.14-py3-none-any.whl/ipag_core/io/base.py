from __future__ import annotations
from dataclasses import dataclass, field
import enum
from typing import Any

from ipag_core.define import DataReader, DataWriter, DataProcessor, DataTuple, MetadataLike, MetadataTransformer, Transformer

class PipelineType(enum.Enum):
    WRITER = enum.auto()
    DATAPROC = enum.auto()
    TRANSFORMER = enum.auto()
    FUNC = enum.auto()
    TRANSMETA = enum.auto()
_proc_callers = {
        PipelineType.DATAPROC: lambda proc,data,metadata:proc.process_data(data, metadata), 
        PipelineType.TRANSFORMER: lambda t, data, metadata: (t.transform(data), metadata), 
        PipelineType.FUNC: lambda f,data, metadata: (f(data), metadata), 
        PipelineType.TRANSMETA: lambda t, data, metadata: (data, t.transform_metadata(metadata))
}

def _parse_proc(proc):
    if isinstance( proc, DataProcessor):
        return PipelineType.DATAPROC , proc
    if isinstance( proc, Transformer):
        return  PipelineType.TRANSFORMER , proc 
    if isinstance( proc, MetadataTransformer):
        return  PipelineType.TRANSMETA , proc 

    if hasattr( proc, "__call__"):
        return PipelineType.FUNC , proc
    if hasattr( proc, "__iter__"):
        return PipelineType.DATAPROC, DataPipe( proc)
     
    raise ValueError(f"Element {proc} is not a valid processor or data writer")


class DataPipe(DataReader, DataWriter, DataProcessor):
    """ Create a pipeline of data 
    
    The pipeline can be made of: 
        - one DataReader (must be the first argument)
        - none, one or several data processors 
        - none one or several DataWriter 
    
    A processor in the pipeline  can be:
        - a DataProcessos with obj.process_data(data, metadata)->tuple[data, metadata] method
        - a Transformer with  obj.transfor(data)->data signature 
        - a callable with f(data)->data signature  
        - a list of one of the above
    
    """
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
        for ptype, obj in self._iter_pipe():
            if ptype == PipelineType.WRITER:
                obj.write_data( data, metadata)
            else:
                data, metadata = _proc_callers[ptype](obj, data, metadata)
        return DataTuple( data, metadata) 

    def read(self) -> Any:
        """ Same as read_data but return only data instead of (data, metadata) """
        data, _ = self.read_data()
        return data 

    def write_data(self, data: Any, metadata:MetadataLike|None = None):
        if not self._has_writer:
            raise ValueError( "This Data Pipe has no data_writer defined" )

        for ptype, obj in self._iter_pipe():
            if ptype == PipelineType.WRITER:
                obj.write_data( data, metadata)
            else:
                data, metadata = _proc_callers[ptype](obj, data, metadata)
    
    def process_data(self, data, metadata=None) -> DataTuple:
        for ptype, obj in self._iter_pipe():
            if ptype == PipelineType.WRITER: continue 
            data, metadata = _proc_callers[ptype](obj, data, metadata)
        return DataTuple(data, metadata)
    
    def transform(self, data) -> Any:
        for ptype, obj in self._iter_pipe():
            if ptype == PipelineType.WRITER: continue 
            if ptype == PipelineType.TRANSMETA: continue
            data, metadata = _proc_callers[ptype](obj, data, metadata)
        return data  
    
    def append(self, proc_or_writer: DataWriter | DataProcessor)->None:
        """ Append a new DataWriter or DataProcessor to the pipeline """
        if isinstance( proc_or_writer, DataWriter):
            self._pipeline.append(proc_or_writer)
            self._pipeline_types.append( PipelineType.WRITER ) 
            self._has_writer = True
        else:
            ptype, proc = _parse_proc(proc_or_writer)
            self._pipeline.append(proc)
            self._pipeline_types.append(ptype)
       
    def extend(self, proc_or_writer_list : list[ DataWriter|DataProcessor ] ):
        """ Extend a new DataWriters or DataProcessors to the pipeline """

        for obj in proc_or_writer_list:
            self.append( obj )

    def insert(self, index, proc_or_writer: DataWriter | DataProcessor)->None:
        """ Insert  a new DataWriter or DataProcessor to the pipeline at given index """
        if isinstance( proc_or_writer, DataWriter):
            self._pipeline.insert(index, proc_or_writer)
            self._pipeline_types.insert(index, True) 
            self._has_writer = True 
        else:
            ptype, proc = _parse_proc(proc_or_writer)
            self._pipeline.insert(index,  proc )
            self._pipeline_types.insert(index, ptype) 
    
    def purge(self, *types):
        """ remove all processor matching any of the given types """
        for obj in list(self._pipeline):
            if isinstance( obj, types):
                self.remove( obj )

    def pop(self, index=-1):
        """ Pop pipeline element at given index (default is the last one) """
        robj = self._pipeline.pop(index) 
        self._pipeline_types.pop(index)
        self._check_if_has_writer()
        return robj 
    
    def remove(self, obj):
        """ Remove a given object on the pipeline """
        i = self._pipeline.index(obj)
        self._pipeline.remove(obj)
        self._pipeline_types.pop(i) 
    
    def index(self, obj):
        """ Return pipeline index of the given object """
        return self._pipeline.index(obj)
    
    def clear(self):
        """ Clear the pipeline (The DataReader, if any, stays)"""
        self._pipeline.clear()
        self._pipeline_types.clear()

    def copy(self):
        """ copy this pipeline to a new one """
        if self._reader:
            return self.__class__(self._reader, *self._pipeline)
        else:
            return self.__class__( *self._pipeline)
    
    

