from ..exports import core
from ..intrinsics import _clamp, _decode_utf8, _encode_utf8, _load
from ..types import Err, Ok, Result
import ctypes
from dataclasses import dataclass
from typing import Optional
import wasmtime

from typing import TYPE_CHECKING
if TYPE_CHECKING:
  from .. import Root

Error = core.Error
RuntimeId = core.RuntimeId
MaterializerId = core.MaterializerId
@dataclass
class S3RuntimeData:
    host_secret: str
    region_secret: str
    access_key_secret: str
    secret_key_secret: str
    path_style_secret: str

@dataclass
class S3PresignGetParams:
    bucket: str
    expiry_secs: Optional[int]

@dataclass
class S3PresignPutParams:
    bucket: str
    expiry_secs: Optional[int]
    content_type: Optional[str]

class Aws:
    component: 'Root'
    
    def __init__(self, component: 'Root') -> None:
        self.component = component
    def register_s3_runtime(self, caller: wasmtime.Store, data: S3RuntimeData) -> Result[RuntimeId, Error]:
        record = data
        field = record.host_secret
        field0 = record.region_secret
        field1 = record.access_key_secret
        field2 = record.secret_key_secret
        field3 = record.path_style_secret
        ptr, len4 = _encode_utf8(field, self.component._realloc0, self.component._core_memory0, caller)
        ptr5, len6 = _encode_utf8(field0, self.component._realloc0, self.component._core_memory0, caller)
        ptr7, len8 = _encode_utf8(field1, self.component._realloc0, self.component._core_memory0, caller)
        ptr9, len10 = _encode_utf8(field2, self.component._realloc0, self.component._core_memory0, caller)
        ptr11, len12 = _encode_utf8(field3, self.component._realloc0, self.component._core_memory0, caller)
        ret = self.component.lift_callee63(caller, ptr, len4, ptr5, len6, ptr7, len8, ptr9, len10, ptr11, len12)
        assert(isinstance(ret, int))
        load = _load(ctypes.c_uint8, self.component._core_memory0, caller, ret, 0)
        expected: Result[RuntimeId, Error]
        if load == 0:
            load13 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 4)
            expected = Ok(load13 & 0xffffffff)
        elif load == 1:
            load14 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 4)
            load15 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 8)
            ptr16 = load14
            len17 = load15
            list = _decode_utf8(self.component._core_memory0, caller, ptr16, len17)
            expected = Err(list)
        else:
            raise TypeError("invalid variant discriminant for expected")
        self.component._post_return0(caller, ret)
        return expected
    def s3_presign_get(self, caller: wasmtime.Store, runtime: RuntimeId, data: S3PresignGetParams) -> Result[MaterializerId, Error]:
        record = data
        field = record.bucket
        field0 = record.expiry_secs
        ptr, len1 = _encode_utf8(field, self.component._realloc0, self.component._core_memory0, caller)
        if field0 is None:
            variant = 0
            variant3 = 0
        else:
            payload2 = field0
            variant = 1
            variant3 = _clamp(payload2, 0, 4294967295)
        ret = self.component.lift_callee64(caller, _clamp(runtime, 0, 4294967295), ptr, len1, variant, variant3)
        assert(isinstance(ret, int))
        load = _load(ctypes.c_uint8, self.component._core_memory0, caller, ret, 0)
        expected: Result[MaterializerId, Error]
        if load == 0:
            load4 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 4)
            expected = Ok(load4 & 0xffffffff)
        elif load == 1:
            load5 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 4)
            load6 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 8)
            ptr7 = load5
            len8 = load6
            list = _decode_utf8(self.component._core_memory0, caller, ptr7, len8)
            expected = Err(list)
        else:
            raise TypeError("invalid variant discriminant for expected")
        self.component._post_return0(caller, ret)
        return expected
    def s3_presign_put(self, caller: wasmtime.Store, runtime: RuntimeId, data: S3PresignPutParams) -> Result[MaterializerId, Error]:
        record = data
        field = record.bucket
        field0 = record.expiry_secs
        field1 = record.content_type
        ptr, len2 = _encode_utf8(field, self.component._realloc0, self.component._core_memory0, caller)
        if field0 is None:
            variant = 0
            variant4 = 0
        else:
            payload3 = field0
            variant = 1
            variant4 = _clamp(payload3, 0, 4294967295)
        if field1 is None:
            variant9 = 0
            variant10 = 0
            variant11 = 0
        else:
            payload6 = field1
            ptr7, len8 = _encode_utf8(payload6, self.component._realloc0, self.component._core_memory0, caller)
            variant9 = 1
            variant10 = ptr7
            variant11 = len8
        ret = self.component.lift_callee65(caller, _clamp(runtime, 0, 4294967295), ptr, len2, variant, variant4, variant9, variant10, variant11)
        assert(isinstance(ret, int))
        load = _load(ctypes.c_uint8, self.component._core_memory0, caller, ret, 0)
        expected: Result[MaterializerId, Error]
        if load == 0:
            load12 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 4)
            expected = Ok(load12 & 0xffffffff)
        elif load == 1:
            load13 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 4)
            load14 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 8)
            ptr15 = load13
            len16 = load14
            list = _decode_utf8(self.component._core_memory0, caller, ptr15, len16)
            expected = Err(list)
        else:
            raise TypeError("invalid variant discriminant for expected")
        self.component._post_return0(caller, ret)
        return expected
    def s3_list(self, caller: wasmtime.Store, runtime: RuntimeId, bucket: str) -> Result[MaterializerId, Error]:
        ptr, len0 = _encode_utf8(bucket, self.component._realloc0, self.component._core_memory0, caller)
        ret = self.component.lift_callee66(caller, _clamp(runtime, 0, 4294967295), ptr, len0)
        assert(isinstance(ret, int))
        load = _load(ctypes.c_uint8, self.component._core_memory0, caller, ret, 0)
        expected: Result[MaterializerId, Error]
        if load == 0:
            load1 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 4)
            expected = Ok(load1 & 0xffffffff)
        elif load == 1:
            load2 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 4)
            load3 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 8)
            ptr4 = load2
            len5 = load3
            list = _decode_utf8(self.component._core_memory0, caller, ptr4, len5)
            expected = Err(list)
        else:
            raise TypeError("invalid variant discriminant for expected")
        self.component._post_return0(caller, ret)
        return expected
    def s3_upload(self, caller: wasmtime.Store, runtime: RuntimeId, bucket: str) -> Result[MaterializerId, Error]:
        ptr, len0 = _encode_utf8(bucket, self.component._realloc0, self.component._core_memory0, caller)
        ret = self.component.lift_callee67(caller, _clamp(runtime, 0, 4294967295), ptr, len0)
        assert(isinstance(ret, int))
        load = _load(ctypes.c_uint8, self.component._core_memory0, caller, ret, 0)
        expected: Result[MaterializerId, Error]
        if load == 0:
            load1 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 4)
            expected = Ok(load1 & 0xffffffff)
        elif load == 1:
            load2 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 4)
            load3 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 8)
            ptr4 = load2
            len5 = load3
            list = _decode_utf8(self.component._core_memory0, caller, ptr4, len5)
            expected = Err(list)
        else:
            raise TypeError("invalid variant discriminant for expected")
        self.component._post_return0(caller, ret)
        return expected
    def s3_upload_all(self, caller: wasmtime.Store, runtime: RuntimeId, bucket: str) -> Result[MaterializerId, Error]:
        ptr, len0 = _encode_utf8(bucket, self.component._realloc0, self.component._core_memory0, caller)
        ret = self.component.lift_callee68(caller, _clamp(runtime, 0, 4294967295), ptr, len0)
        assert(isinstance(ret, int))
        load = _load(ctypes.c_uint8, self.component._core_memory0, caller, ret, 0)
        expected: Result[MaterializerId, Error]
        if load == 0:
            load1 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 4)
            expected = Ok(load1 & 0xffffffff)
        elif load == 1:
            load2 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 4)
            load3 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 8)
            ptr4 = load2
            len5 = load3
            list = _decode_utf8(self.component._core_memory0, caller, ptr4, len5)
            expected = Err(list)
        else:
            raise TypeError("invalid variant discriminant for expected")
        self.component._post_return0(caller, ret)
        return expected
