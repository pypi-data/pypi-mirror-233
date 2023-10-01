from typing import List, Literal, Optional, Union

from .authorization import Authorization
from .balance import Balance
from .base import LikeObject, MutableLikeObject
from .collection import Collection
from .collection_element import CollectionElement
from .file import File
from .hand import Hand
from .input_file import BufferedInputFile, FileSystemInputFile, InputFile
from .user import User

__all__ = (
    "Authorization",
    "Balance",
    "BufferedInputFile",
    "Collection",
    "CollectionElement",
    "File",
    "FileSystemInputFile",
    "Hand",
    "InputFile",
    "LikeObject",
    "MutableLikeObject",
    "User",
)

for _entity_name in __all__:
    _entity = globals()[_entity_name]
    if not hasattr(_entity, "model_rebuild"):
        continue
    _entity.model_rebuild(
        _types_namespace={
            "List": List,
            "Optional": Optional,
            "Union": Union,
            "Literal": Literal,
            **{k: v for k, v in globals().items() if k in __all__},
        }
    )

del _entity
del _entity_name
