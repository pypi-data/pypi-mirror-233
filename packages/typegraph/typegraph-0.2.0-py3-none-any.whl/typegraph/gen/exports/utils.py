from ..intrinsics import _clamp, _decode_utf8, _encode_utf8, _load, _store
from ..types import Err, Ok, Result
import ctypes
from dataclasses import dataclass
from typing import List, Optional
import wasmtime

from typing import TYPE_CHECKING
if TYPE_CHECKING:
  from .. import Root

Error = str
TypeId = int
@dataclass
class ApplyValue:
    inherit: bool
    payload: Optional[str]

@dataclass
class ApplyPath:
    path: List[str]
    value: ApplyValue

@dataclass
class Apply:
    paths: List[ApplyPath]

class Utils:
    component: 'Root'
    
    def __init__(self, component: 'Root') -> None:
        self.component = component
    def gen_applyb(self, caller: wasmtime.Store, supertype_id: TypeId, data: Apply) -> Result[TypeId, Error]:
        record = data
        field = record.paths
        vec15 = field
        len17 = len(vec15)
        result16 = self.component._realloc0(caller, 0, 0, 4, len17 * 24)
        assert(isinstance(result16, int))
        for i18 in range(0, len17):
            e = vec15[i18]
            base0 = result16 + i18 * 24
            record1 = e
            field2 = record1.path
            field3 = record1.value
            vec = field2
            len7 = len(vec)
            result = self.component._realloc0(caller, 0, 0, 4, len7 * 8)
            assert(isinstance(result, int))
            for i8 in range(0, len7):
                e4 = vec[i8]
                base5 = result + i8 * 8
                ptr, len6 = _encode_utf8(e4, self.component._realloc0, self.component._core_memory0, caller)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base5, 4, len6)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base5, 0, ptr)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, base0, 4, len7)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, base0, 0, result)
            record9 = field3
            field10 = record9.inherit
            field11 = record9.payload
            _store(ctypes.c_uint8, self.component._core_memory0, caller, base0, 8, int(field10))
            if field11 is None:
                _store(ctypes.c_uint8, self.component._core_memory0, caller, base0, 12, 0)
            else:
                payload12 = field11
                _store(ctypes.c_uint8, self.component._core_memory0, caller, base0, 12, 1)
                ptr13, len14 = _encode_utf8(payload12, self.component._realloc0, self.component._core_memory0, caller)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base0, 20, len14)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base0, 16, ptr13)
        ret = self.component.lift_callee62(caller, _clamp(supertype_id, 0, 4294967295), result16, len17)
        assert(isinstance(ret, int))
        load = _load(ctypes.c_uint8, self.component._core_memory0, caller, ret, 0)
        expected: Result[TypeId, Error]
        if load == 0:
            load19 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 4)
            expected = Ok(load19 & 0xffffffff)
        elif load == 1:
            load20 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 4)
            load21 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 8)
            ptr22 = load20
            len23 = load21
            list = _decode_utf8(self.component._core_memory0, caller, ptr22, len23)
            expected = Err(list)
        else:
            raise TypeError("invalid variant discriminant for expected")
        self.component._post_return0(caller, ret)
        return expected
