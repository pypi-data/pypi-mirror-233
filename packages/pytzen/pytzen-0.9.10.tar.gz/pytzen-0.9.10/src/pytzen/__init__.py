from pytzen.data import DataStore, update_config
from pytzen.log import LogBuild
from pytzen.doc import DocGen
from abc import ABCMeta
import re

class MetaType(ABCMeta):

    def __new__(cls, name, bases, class_dict):
        if bases and '__init__' in class_dict:
            derived_init = class_dict['__init__']
            def init(self, **kwargs):
                ProtoType.__init__(self, **kwargs)
                derived_init(self, **kwargs)
            class_dict['__init__'] = init
        return super().__new__(cls, name, bases, class_dict)

class ProtoType(metaclass=MetaType):
    
    def __init__(self, **kwargs) -> None:
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.class_name: str = re.search(
            r"<class '(.*?)'>", str(self.__class__)).group(1)
        self.log_level: str = kwargs.get('log_level', 'INFO')
        self.log = LogBuild(name=self.class_name, level=self.log_level)
        if not hasattr(ProtoType, 'data'):
            ProtoType.data = DataStore()
        doc_gen = DocGen({**self.__dict__, **self.__class__.__dict__})
        update_config(doc=doc_gen.doc, 
                      class_name=self.class_name, 
                      data=ProtoType.data)
    @staticmethod
    def close():
        class CaptureNewData(ProtoType):
            def __init__(self):
                   ...
        CaptureNewData()