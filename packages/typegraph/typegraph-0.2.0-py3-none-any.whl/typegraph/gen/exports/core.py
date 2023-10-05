from ..intrinsics import _clamp, _decode_utf8, _encode_utf8, _list_canon_lower, _load, _store
from ..types import Err, Ok, Result
import ctypes
from dataclasses import dataclass
from typing import List, Optional, Tuple, Union
import wasmtime

from typing import TYPE_CHECKING
if TYPE_CHECKING:
  from .. import Root

Error = str
@dataclass
class Cors:
    allow_origin: List[str]
    allow_headers: List[str]
    expose_headers: List[str]
    allow_methods: List[str]
    allow_credentials: bool
    max_age_sec: Optional[int]

@dataclass
class AuthProtocolOauth2:
    pass

@dataclass
class AuthProtocolJwt:
    pass

@dataclass
class AuthProtocolBasic:
    pass

AuthProtocol = Union[AuthProtocolOauth2, AuthProtocolJwt, AuthProtocolBasic]

@dataclass
class Auth:
    name: str
    protocol: AuthProtocol
    auth_data: List[Tuple[str, str]]

@dataclass
class Rate:
    window_limit: int
    window_sec: int
    query_limit: int
    context_identifier: Optional[str]
    local_excess: int

@dataclass
class TypegraphInitParams:
    name: str
    dynamic: Optional[bool]
    folder: Optional[str]
    path: str
    prefix: Optional[str]
    cors: Cors
    auths: List[Auth]
    rate: Optional[Rate]

TypeId = int
@dataclass
class TypeBase:
    name: Optional[str]
    runtime_config: Optional[List[Tuple[str, str]]]
    as_id: bool

@dataclass
class TypeWithInjection:
    tpe: TypeId
    injection: str

@dataclass
class TypeProxy:
    name: str
    extras: List[Tuple[str, str]]

@dataclass
class TypeInteger:
    min: Optional[int]
    max: Optional[int]
    exclusive_minimum: Optional[int]
    exclusive_maximum: Optional[int]
    multiple_of: Optional[int]
    enumeration: Optional[List[int]]

@dataclass
class TypeFloat:
    min: Optional[float]
    max: Optional[float]
    exclusive_minimum: Optional[float]
    exclusive_maximum: Optional[float]
    multiple_of: Optional[float]
    enumeration: Optional[List[float]]

@dataclass
class TypeString:
    min: Optional[int]
    max: Optional[int]
    format: Optional[str]
    pattern: Optional[str]
    enumeration: Optional[List[str]]

@dataclass
class TypeFile:
    min: Optional[int]
    max: Optional[int]
    allow: Optional[List[str]]

@dataclass
class TypeArray:
    of: TypeId
    min: Optional[int]
    max: Optional[int]
    unique_items: Optional[bool]

@dataclass
class TypeOptional:
    of: TypeId
    default_item: Optional[str]

@dataclass
class TypeUnion:
    variants: List[TypeId]

@dataclass
class TypeEither:
    variants: List[TypeId]

@dataclass
class TypeStruct:
    props: List[Tuple[str, TypeId]]
    additional_props: bool
    min: Optional[int]
    max: Optional[int]
    enumeration: Optional[List[str]]

PolicyId = int
@dataclass
class PolicyPerEffect:
    none: Optional[PolicyId]
    create: Optional[PolicyId]
    update: Optional[PolicyId]
    delete: Optional[PolicyId]

@dataclass
class PolicySpecSimple:
    value: PolicyId

@dataclass
class PolicySpecPerEffect:
    value: PolicyPerEffect

PolicySpec = Union[PolicySpecSimple, PolicySpecPerEffect]

@dataclass
class TypePolicy:
    tpe: TypeId
    chain: List[PolicySpec]

@dataclass
class ContextCheckValue:
    value: str

@dataclass
class ContextCheckPattern:
    value: str

ContextCheck = Union[ContextCheckValue, ContextCheckPattern]

@dataclass
class TypeRenamed:
    tpe: TypeId
    name: str

RuntimeId = int
MaterializerId = int
@dataclass
class TypeFunc:
    inp: TypeId
    out: TypeId
    mat: MaterializerId
    rate_calls: bool
    rate_weight: Optional[int]

@dataclass
class Policy:
    name: str
    materializer: MaterializerId

@dataclass
class FuncParams:
    inp: TypeId
    out: TypeId
    mat: MaterializerId

class Core:
    component: 'Root'
    
    def __init__(self, component: 'Root') -> None:
        self.component = component
    def init_typegraph(self, caller: wasmtime.Store, params: TypegraphInitParams) -> Result[None, Error]:
        ptr = self.component._realloc0(caller, 0, 0, 4, 128)
        assert(isinstance(ptr, int))
        record = params
        field = record.name
        field0 = record.dynamic
        field1 = record.folder
        field2 = record.path
        field3 = record.prefix
        field4 = record.cors
        field5 = record.auths
        field6 = record.rate
        ptr7, len8 = _encode_utf8(field, self.component._realloc0, self.component._core_memory0, caller)
        _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 4, len8)
        _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 0, ptr7)
        if field0 is None:
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 8, 0)
        else:
            payload9 = field0
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 8, 1)
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 9, int(payload9))
        if field1 is None:
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 12, 0)
        else:
            payload11 = field1
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 12, 1)
            ptr12, len13 = _encode_utf8(payload11, self.component._realloc0, self.component._core_memory0, caller)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 20, len13)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 16, ptr12)
        ptr14, len15 = _encode_utf8(field2, self.component._realloc0, self.component._core_memory0, caller)
        _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 28, len15)
        _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 24, ptr14)
        if field3 is None:
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 32, 0)
        else:
            payload17 = field3
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 32, 1)
            ptr18, len19 = _encode_utf8(payload17, self.component._realloc0, self.component._core_memory0, caller)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 40, len19)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 36, ptr18)
        record20 = field4
        field21 = record20.allow_origin
        field22 = record20.allow_headers
        field23 = record20.expose_headers
        field24 = record20.allow_methods
        field25 = record20.allow_credentials
        field26 = record20.max_age_sec
        vec = field21
        len30 = len(vec)
        result = self.component._realloc0(caller, 0, 0, 4, len30 * 8)
        assert(isinstance(result, int))
        for i31 in range(0, len30):
            e = vec[i31]
            base27 = result + i31 * 8
            ptr28, len29 = _encode_utf8(e, self.component._realloc0, self.component._core_memory0, caller)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, base27, 4, len29)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, base27, 0, ptr28)
        _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 48, len30)
        _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 44, result)
        vec36 = field22
        len38 = len(vec36)
        result37 = self.component._realloc0(caller, 0, 0, 4, len38 * 8)
        assert(isinstance(result37, int))
        for i39 in range(0, len38):
            e32 = vec36[i39]
            base33 = result37 + i39 * 8
            ptr34, len35 = _encode_utf8(e32, self.component._realloc0, self.component._core_memory0, caller)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, base33, 4, len35)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, base33, 0, ptr34)
        _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 56, len38)
        _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 52, result37)
        vec44 = field23
        len46 = len(vec44)
        result45 = self.component._realloc0(caller, 0, 0, 4, len46 * 8)
        assert(isinstance(result45, int))
        for i47 in range(0, len46):
            e40 = vec44[i47]
            base41 = result45 + i47 * 8
            ptr42, len43 = _encode_utf8(e40, self.component._realloc0, self.component._core_memory0, caller)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, base41, 4, len43)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, base41, 0, ptr42)
        _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 64, len46)
        _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 60, result45)
        vec52 = field24
        len54 = len(vec52)
        result53 = self.component._realloc0(caller, 0, 0, 4, len54 * 8)
        assert(isinstance(result53, int))
        for i55 in range(0, len54):
            e48 = vec52[i55]
            base49 = result53 + i55 * 8
            ptr50, len51 = _encode_utf8(e48, self.component._realloc0, self.component._core_memory0, caller)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, base49, 4, len51)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, base49, 0, ptr50)
        _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 72, len54)
        _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 68, result53)
        _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 76, int(field25))
        if field26 is None:
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 80, 0)
        else:
            payload57 = field26
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 80, 1)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 84, _clamp(payload57, 0, 4294967295))
        vec80 = field5
        len82 = len(vec80)
        result81 = self.component._realloc0(caller, 0, 0, 4, len82 * 20)
        assert(isinstance(result81, int))
        for i83 in range(0, len82):
            e58 = vec80[i83]
            base59 = result81 + i83 * 20
            record60 = e58
            field61 = record60.name
            field62 = record60.protocol
            field63 = record60.auth_data
            ptr64, len65 = _encode_utf8(field61, self.component._realloc0, self.component._core_memory0, caller)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, base59, 4, len65)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, base59, 0, ptr64)
            if isinstance(field62, AuthProtocolOauth2):
                _store(ctypes.c_uint8, self.component._core_memory0, caller, base59, 8, 0)
            elif isinstance(field62, AuthProtocolJwt):
                _store(ctypes.c_uint8, self.component._core_memory0, caller, base59, 8, 1)
            elif isinstance(field62, AuthProtocolBasic):
                _store(ctypes.c_uint8, self.component._core_memory0, caller, base59, 8, 2)
            else:
                raise TypeError("invalid variant specified for AuthProtocol")
            vec76 = field63
            len78 = len(vec76)
            result77 = self.component._realloc0(caller, 0, 0, 4, len78 * 16)
            assert(isinstance(result77, int))
            for i79 in range(0, len78):
                e69 = vec76[i79]
                base70 = result77 + i79 * 16
                (tuplei,tuplei71,) = e69
                ptr72, len73 = _encode_utf8(tuplei, self.component._realloc0, self.component._core_memory0, caller)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base70, 4, len73)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base70, 0, ptr72)
                ptr74, len75 = _encode_utf8(tuplei71, self.component._realloc0, self.component._core_memory0, caller)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base70, 12, len75)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base70, 8, ptr74)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, base59, 16, len78)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, base59, 12, result77)
        _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 92, len82)
        _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 88, result81)
        if field6 is None:
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 96, 0)
        else:
            payload85 = field6
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 96, 1)
            record86 = payload85
            field87 = record86.window_limit
            field88 = record86.window_sec
            field89 = record86.query_limit
            field90 = record86.context_identifier
            field91 = record86.local_excess
            _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 100, _clamp(field87, 0, 4294967295))
            _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 104, _clamp(field88, 0, 4294967295))
            _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 108, _clamp(field89, 0, 4294967295))
            if field90 is None:
                _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 112, 0)
            else:
                payload93 = field90
                _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 112, 1)
                ptr94, len95 = _encode_utf8(payload93, self.component._realloc0, self.component._core_memory0, caller)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 120, len95)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 116, ptr94)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 124, _clamp(field91, 0, 4294967295))
        ret = self.component.lift_callee0(caller, ptr)
        assert(isinstance(ret, int))
        load = _load(ctypes.c_uint8, self.component._core_memory0, caller, ret, 0)
        expected: Result[None, Error]
        if load == 0:
            expected = Ok(None)
        elif load == 1:
            load96 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 4)
            load97 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 8)
            ptr98 = load96
            len99 = load97
            list = _decode_utf8(self.component._core_memory0, caller, ptr98, len99)
            expected = Err(list)
        else:
            raise TypeError("invalid variant discriminant for expected")
        self.component._post_return0(caller, ret)
        return expected
    def finalize_typegraph(self, caller: wasmtime.Store) -> Result[str, Error]:
        ret = self.component.lift_callee1(caller)
        assert(isinstance(ret, int))
        load = _load(ctypes.c_uint8, self.component._core_memory0, caller, ret, 0)
        expected: Result[str, Error]
        if load == 0:
            load0 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 4)
            load1 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 8)
            ptr = load0
            len2 = load1
            list = _decode_utf8(self.component._core_memory0, caller, ptr, len2)
            expected = Ok(list)
        elif load == 1:
            load3 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 4)
            load4 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 8)
            ptr5 = load3
            len6 = load4
            list7 = _decode_utf8(self.component._core_memory0, caller, ptr5, len6)
            expected = Err(list7)
        else:
            raise TypeError("invalid variant discriminant for expected")
        self.component._post_return1(caller, ret)
        return expected
    def with_injection(self, caller: wasmtime.Store, data: TypeWithInjection) -> Result[TypeId, Error]:
        record = data
        field = record.tpe
        field0 = record.injection
        ptr, len1 = _encode_utf8(field0, self.component._realloc0, self.component._core_memory0, caller)
        ret = self.component.lift_callee2(caller, _clamp(field, 0, 4294967295), ptr, len1)
        assert(isinstance(ret, int))
        load = _load(ctypes.c_uint8, self.component._core_memory0, caller, ret, 0)
        expected: Result[TypeId, Error]
        if load == 0:
            load2 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 4)
            expected = Ok(load2 & 0xffffffff)
        elif load == 1:
            load3 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 4)
            load4 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 8)
            ptr5 = load3
            len6 = load4
            list = _decode_utf8(self.component._core_memory0, caller, ptr5, len6)
            expected = Err(list)
        else:
            raise TypeError("invalid variant discriminant for expected")
        self.component._post_return0(caller, ret)
        return expected
    def proxyb(self, caller: wasmtime.Store, data: TypeProxy) -> Result[TypeId, Error]:
        record = data
        field = record.name
        field0 = record.extras
        ptr, len1 = _encode_utf8(field, self.component._realloc0, self.component._core_memory0, caller)
        vec = field0
        len8 = len(vec)
        result = self.component._realloc0(caller, 0, 0, 4, len8 * 16)
        assert(isinstance(result, int))
        for i9 in range(0, len8):
            e = vec[i9]
            base2 = result + i9 * 16
            (tuplei,tuplei3,) = e
            ptr4, len5 = _encode_utf8(tuplei, self.component._realloc0, self.component._core_memory0, caller)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, base2, 4, len5)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, base2, 0, ptr4)
            ptr6, len7 = _encode_utf8(tuplei3, self.component._realloc0, self.component._core_memory0, caller)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, base2, 12, len7)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, base2, 8, ptr6)
        ret = self.component.lift_callee3(caller, ptr, len1, result, len8)
        assert(isinstance(ret, int))
        load = _load(ctypes.c_uint8, self.component._core_memory0, caller, ret, 0)
        expected: Result[TypeId, Error]
        if load == 0:
            load10 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 4)
            expected = Ok(load10 & 0xffffffff)
        elif load == 1:
            load11 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 4)
            load12 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 8)
            ptr13 = load11
            len14 = load12
            list = _decode_utf8(self.component._core_memory0, caller, ptr13, len14)
            expected = Err(list)
        else:
            raise TypeError("invalid variant discriminant for expected")
        self.component._post_return0(caller, ret)
        return expected
    def integerb(self, caller: wasmtime.Store, data: TypeInteger, base: TypeBase) -> Result[TypeId, Error]:
        ptr = self.component._realloc0(caller, 0, 0, 4, 80)
        assert(isinstance(ptr, int))
        record = data
        field = record.min
        field0 = record.max
        field1 = record.exclusive_minimum
        field2 = record.exclusive_maximum
        field3 = record.multiple_of
        field4 = record.enumeration
        if field is None:
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 0, 0)
        else:
            payload5 = field
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 0, 1)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 4, _clamp(payload5, -2147483648, 2147483647))
        if field0 is None:
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 8, 0)
        else:
            payload7 = field0
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 8, 1)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 12, _clamp(payload7, -2147483648, 2147483647))
        if field1 is None:
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 16, 0)
        else:
            payload9 = field1
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 16, 1)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 20, _clamp(payload9, -2147483648, 2147483647))
        if field2 is None:
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 24, 0)
        else:
            payload11 = field2
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 24, 1)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 28, _clamp(payload11, -2147483648, 2147483647))
        if field3 is None:
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 32, 0)
        else:
            payload13 = field3
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 32, 1)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 36, _clamp(payload13, -2147483648, 2147483647))
        if field4 is None:
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 40, 0)
        else:
            payload15 = field4
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 40, 1)
            ptr16, len17 = _list_canon_lower(payload15, ctypes.c_int32, 4, 4, self.component._realloc0, self.component._core_memory0, caller)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 48, len17)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 44, ptr16)
        record18 = base
        field19 = record18.name
        field20 = record18.runtime_config
        field21 = record18.as_id
        if field19 is None:
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 52, 0)
        else:
            payload23 = field19
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 52, 1)
            ptr24, len25 = _encode_utf8(payload23, self.component._realloc0, self.component._core_memory0, caller)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 60, len25)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 56, ptr24)
        if field20 is None:
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 64, 0)
        else:
            payload27 = field20
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 64, 1)
            vec = payload27
            len34 = len(vec)
            result = self.component._realloc0(caller, 0, 0, 4, len34 * 16)
            assert(isinstance(result, int))
            for i35 in range(0, len34):
                e = vec[i35]
                base28 = result + i35 * 16
                (tuplei,tuplei29,) = e
                ptr30, len31 = _encode_utf8(tuplei, self.component._realloc0, self.component._core_memory0, caller)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base28, 4, len31)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base28, 0, ptr30)
                ptr32, len33 = _encode_utf8(tuplei29, self.component._realloc0, self.component._core_memory0, caller)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base28, 12, len33)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base28, 8, ptr32)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 72, len34)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 68, result)
        _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 76, int(field21))
        ret = self.component.lift_callee4(caller, ptr)
        assert(isinstance(ret, int))
        load = _load(ctypes.c_uint8, self.component._core_memory0, caller, ret, 0)
        expected: Result[TypeId, Error]
        if load == 0:
            load36 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 4)
            expected = Ok(load36 & 0xffffffff)
        elif load == 1:
            load37 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 4)
            load38 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 8)
            ptr39 = load37
            len40 = load38
            list = _decode_utf8(self.component._core_memory0, caller, ptr39, len40)
            expected = Err(list)
        else:
            raise TypeError("invalid variant discriminant for expected")
        self.component._post_return0(caller, ret)
        return expected
    def floatb(self, caller: wasmtime.Store, data: TypeFloat, base: TypeBase) -> Result[TypeId, Error]:
        ptr = self.component._realloc0(caller, 0, 0, 8, 128)
        assert(isinstance(ptr, int))
        record = data
        field = record.min
        field0 = record.max
        field1 = record.exclusive_minimum
        field2 = record.exclusive_maximum
        field3 = record.multiple_of
        field4 = record.enumeration
        if field is None:
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 0, 0)
        else:
            payload5 = field
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 0, 1)
            _store(ctypes.c_double, self.component._core_memory0, caller, ptr, 8, payload5)
        if field0 is None:
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 16, 0)
        else:
            payload7 = field0
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 16, 1)
            _store(ctypes.c_double, self.component._core_memory0, caller, ptr, 24, payload7)
        if field1 is None:
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 32, 0)
        else:
            payload9 = field1
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 32, 1)
            _store(ctypes.c_double, self.component._core_memory0, caller, ptr, 40, payload9)
        if field2 is None:
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 48, 0)
        else:
            payload11 = field2
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 48, 1)
            _store(ctypes.c_double, self.component._core_memory0, caller, ptr, 56, payload11)
        if field3 is None:
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 64, 0)
        else:
            payload13 = field3
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 64, 1)
            _store(ctypes.c_double, self.component._core_memory0, caller, ptr, 72, payload13)
        if field4 is None:
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 80, 0)
        else:
            payload15 = field4
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 80, 1)
            ptr16, len17 = _list_canon_lower(payload15, ctypes.c_double, 8, 8, self.component._realloc0, self.component._core_memory0, caller)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 88, len17)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 84, ptr16)
        record18 = base
        field19 = record18.name
        field20 = record18.runtime_config
        field21 = record18.as_id
        if field19 is None:
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 96, 0)
        else:
            payload23 = field19
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 96, 1)
            ptr24, len25 = _encode_utf8(payload23, self.component._realloc0, self.component._core_memory0, caller)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 104, len25)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 100, ptr24)
        if field20 is None:
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 108, 0)
        else:
            payload27 = field20
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 108, 1)
            vec = payload27
            len34 = len(vec)
            result = self.component._realloc0(caller, 0, 0, 4, len34 * 16)
            assert(isinstance(result, int))
            for i35 in range(0, len34):
                e = vec[i35]
                base28 = result + i35 * 16
                (tuplei,tuplei29,) = e
                ptr30, len31 = _encode_utf8(tuplei, self.component._realloc0, self.component._core_memory0, caller)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base28, 4, len31)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base28, 0, ptr30)
                ptr32, len33 = _encode_utf8(tuplei29, self.component._realloc0, self.component._core_memory0, caller)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base28, 12, len33)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base28, 8, ptr32)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 116, len34)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 112, result)
        _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 120, int(field21))
        ret = self.component.lift_callee5(caller, ptr)
        assert(isinstance(ret, int))
        load = _load(ctypes.c_uint8, self.component._core_memory0, caller, ret, 0)
        expected: Result[TypeId, Error]
        if load == 0:
            load36 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 4)
            expected = Ok(load36 & 0xffffffff)
        elif load == 1:
            load37 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 4)
            load38 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 8)
            ptr39 = load37
            len40 = load38
            list = _decode_utf8(self.component._core_memory0, caller, ptr39, len40)
            expected = Err(list)
        else:
            raise TypeError("invalid variant discriminant for expected")
        self.component._post_return0(caller, ret)
        return expected
    def booleanb(self, caller: wasmtime.Store, base: TypeBase) -> Result[TypeId, Error]:
        record = base
        field = record.name
        field0 = record.runtime_config
        field1 = record.as_id
        if field is None:
            variant = 0
            variant4 = 0
            variant5 = 0
        else:
            payload2 = field
            ptr, len3 = _encode_utf8(payload2, self.component._realloc0, self.component._core_memory0, caller)
            variant = 1
            variant4 = ptr
            variant5 = len3
        if field0 is None:
            variant16 = 0
            variant17 = 0
            variant18 = 0
        else:
            payload7 = field0
            vec = payload7
            len14 = len(vec)
            result = self.component._realloc0(caller, 0, 0, 4, len14 * 16)
            assert(isinstance(result, int))
            for i15 in range(0, len14):
                e = vec[i15]
                base8 = result + i15 * 16
                (tuplei,tuplei9,) = e
                ptr10, len11 = _encode_utf8(tuplei, self.component._realloc0, self.component._core_memory0, caller)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base8, 4, len11)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base8, 0, ptr10)
                ptr12, len13 = _encode_utf8(tuplei9, self.component._realloc0, self.component._core_memory0, caller)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base8, 12, len13)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base8, 8, ptr12)
            variant16 = 1
            variant17 = result
            variant18 = len14
        ret = self.component.lift_callee6(caller, variant, variant4, variant5, variant16, variant17, variant18, int(field1))
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
    def stringb(self, caller: wasmtime.Store, data: TypeString, base: TypeBase) -> Result[TypeId, Error]:
        ptr = self.component._realloc0(caller, 0, 0, 4, 80)
        assert(isinstance(ptr, int))
        record = data
        field = record.min
        field0 = record.max
        field1 = record.format
        field2 = record.pattern
        field3 = record.enumeration
        if field is None:
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 0, 0)
        else:
            payload4 = field
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 0, 1)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 4, _clamp(payload4, 0, 4294967295))
        if field0 is None:
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 8, 0)
        else:
            payload6 = field0
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 8, 1)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 12, _clamp(payload6, 0, 4294967295))
        if field1 is None:
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 16, 0)
        else:
            payload8 = field1
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 16, 1)
            ptr9, len10 = _encode_utf8(payload8, self.component._realloc0, self.component._core_memory0, caller)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 24, len10)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 20, ptr9)
        if field2 is None:
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 28, 0)
        else:
            payload12 = field2
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 28, 1)
            ptr13, len14 = _encode_utf8(payload12, self.component._realloc0, self.component._core_memory0, caller)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 36, len14)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 32, ptr13)
        if field3 is None:
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 40, 0)
        else:
            payload16 = field3
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 40, 1)
            vec = payload16
            len20 = len(vec)
            result = self.component._realloc0(caller, 0, 0, 4, len20 * 8)
            assert(isinstance(result, int))
            for i21 in range(0, len20):
                e = vec[i21]
                base17 = result + i21 * 8
                ptr18, len19 = _encode_utf8(e, self.component._realloc0, self.component._core_memory0, caller)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base17, 4, len19)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base17, 0, ptr18)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 48, len20)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 44, result)
        record22 = base
        field23 = record22.name
        field24 = record22.runtime_config
        field25 = record22.as_id
        if field23 is None:
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 52, 0)
        else:
            payload27 = field23
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 52, 1)
            ptr28, len29 = _encode_utf8(payload27, self.component._realloc0, self.component._core_memory0, caller)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 60, len29)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 56, ptr28)
        if field24 is None:
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 64, 0)
        else:
            payload31 = field24
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 64, 1)
            vec39 = payload31
            len41 = len(vec39)
            result40 = self.component._realloc0(caller, 0, 0, 4, len41 * 16)
            assert(isinstance(result40, int))
            for i42 in range(0, len41):
                e32 = vec39[i42]
                base33 = result40 + i42 * 16
                (tuplei,tuplei34,) = e32
                ptr35, len36 = _encode_utf8(tuplei, self.component._realloc0, self.component._core_memory0, caller)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base33, 4, len36)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base33, 0, ptr35)
                ptr37, len38 = _encode_utf8(tuplei34, self.component._realloc0, self.component._core_memory0, caller)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base33, 12, len38)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base33, 8, ptr37)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 72, len41)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 68, result40)
        _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 76, int(field25))
        ret = self.component.lift_callee7(caller, ptr)
        assert(isinstance(ret, int))
        load = _load(ctypes.c_uint8, self.component._core_memory0, caller, ret, 0)
        expected: Result[TypeId, Error]
        if load == 0:
            load43 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 4)
            expected = Ok(load43 & 0xffffffff)
        elif load == 1:
            load44 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 4)
            load45 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 8)
            ptr46 = load44
            len47 = load45
            list = _decode_utf8(self.component._core_memory0, caller, ptr46, len47)
            expected = Err(list)
        else:
            raise TypeError("invalid variant discriminant for expected")
        self.component._post_return0(caller, ret)
        return expected
    def fileb(self, caller: wasmtime.Store, data: TypeFile, base: TypeBase) -> Result[TypeId, Error]:
        record = data
        field = record.min
        field0 = record.max
        field1 = record.allow
        if field is None:
            variant = 0
            variant3 = 0
        else:
            payload2 = field
            variant = 1
            variant3 = _clamp(payload2, 0, 4294967295)
        if field0 is None:
            variant6 = 0
            variant7 = 0
        else:
            payload5 = field0
            variant6 = 1
            variant7 = _clamp(payload5, 0, 4294967295)
        if field1 is None:
            variant14 = 0
            variant15 = 0
            variant16 = 0
        else:
            payload9 = field1
            vec = payload9
            len12 = len(vec)
            result = self.component._realloc0(caller, 0, 0, 4, len12 * 8)
            assert(isinstance(result, int))
            for i13 in range(0, len12):
                e = vec[i13]
                base10 = result + i13 * 8
                ptr, len11 = _encode_utf8(e, self.component._realloc0, self.component._core_memory0, caller)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base10, 4, len11)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base10, 0, ptr)
            variant14 = 1
            variant15 = result
            variant16 = len12
        record17 = base
        field18 = record17.name
        field19 = record17.runtime_config
        field20 = record17.as_id
        if field18 is None:
            variant25 = 0
            variant26 = 0
            variant27 = 0
        else:
            payload22 = field18
            ptr23, len24 = _encode_utf8(payload22, self.component._realloc0, self.component._core_memory0, caller)
            variant25 = 1
            variant26 = ptr23
            variant27 = len24
        if field19 is None:
            variant41 = 0
            variant42 = 0
            variant43 = 0
        else:
            payload29 = field19
            vec37 = payload29
            len39 = len(vec37)
            result38 = self.component._realloc0(caller, 0, 0, 4, len39 * 16)
            assert(isinstance(result38, int))
            for i40 in range(0, len39):
                e30 = vec37[i40]
                base31 = result38 + i40 * 16
                (tuplei,tuplei32,) = e30
                ptr33, len34 = _encode_utf8(tuplei, self.component._realloc0, self.component._core_memory0, caller)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base31, 4, len34)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base31, 0, ptr33)
                ptr35, len36 = _encode_utf8(tuplei32, self.component._realloc0, self.component._core_memory0, caller)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base31, 12, len36)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base31, 8, ptr35)
            variant41 = 1
            variant42 = result38
            variant43 = len39
        ret = self.component.lift_callee8(caller, variant, variant3, variant6, variant7, variant14, variant15, variant16, variant25, variant26, variant27, variant41, variant42, variant43, int(field20))
        assert(isinstance(ret, int))
        load = _load(ctypes.c_uint8, self.component._core_memory0, caller, ret, 0)
        expected: Result[TypeId, Error]
        if load == 0:
            load44 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 4)
            expected = Ok(load44 & 0xffffffff)
        elif load == 1:
            load45 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 4)
            load46 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 8)
            ptr47 = load45
            len48 = load46
            list = _decode_utf8(self.component._core_memory0, caller, ptr47, len48)
            expected = Err(list)
        else:
            raise TypeError("invalid variant discriminant for expected")
        self.component._post_return0(caller, ret)
        return expected
    def arrayb(self, caller: wasmtime.Store, data: TypeArray, base: TypeBase) -> Result[TypeId, Error]:
        record = data
        field = record.of
        field0 = record.min
        field1 = record.max
        field2 = record.unique_items
        if field0 is None:
            variant = 0
            variant4 = 0
        else:
            payload3 = field0
            variant = 1
            variant4 = _clamp(payload3, 0, 4294967295)
        if field1 is None:
            variant7 = 0
            variant8 = 0
        else:
            payload6 = field1
            variant7 = 1
            variant8 = _clamp(payload6, 0, 4294967295)
        if field2 is None:
            variant11 = 0
            variant12 = 0
        else:
            payload10 = field2
            variant11 = 1
            variant12 = int(payload10)
        record13 = base
        field14 = record13.name
        field15 = record13.runtime_config
        field16 = record13.as_id
        if field14 is None:
            variant20 = 0
            variant21 = 0
            variant22 = 0
        else:
            payload18 = field14
            ptr, len19 = _encode_utf8(payload18, self.component._realloc0, self.component._core_memory0, caller)
            variant20 = 1
            variant21 = ptr
            variant22 = len19
        if field15 is None:
            variant33 = 0
            variant34 = 0
            variant35 = 0
        else:
            payload24 = field15
            vec = payload24
            len31 = len(vec)
            result = self.component._realloc0(caller, 0, 0, 4, len31 * 16)
            assert(isinstance(result, int))
            for i32 in range(0, len31):
                e = vec[i32]
                base25 = result + i32 * 16
                (tuplei,tuplei26,) = e
                ptr27, len28 = _encode_utf8(tuplei, self.component._realloc0, self.component._core_memory0, caller)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base25, 4, len28)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base25, 0, ptr27)
                ptr29, len30 = _encode_utf8(tuplei26, self.component._realloc0, self.component._core_memory0, caller)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base25, 12, len30)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base25, 8, ptr29)
            variant33 = 1
            variant34 = result
            variant35 = len31
        ret = self.component.lift_callee9(caller, _clamp(field, 0, 4294967295), variant, variant4, variant7, variant8, variant11, variant12, variant20, variant21, variant22, variant33, variant34, variant35, int(field16))
        assert(isinstance(ret, int))
        load = _load(ctypes.c_uint8, self.component._core_memory0, caller, ret, 0)
        expected: Result[TypeId, Error]
        if load == 0:
            load36 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 4)
            expected = Ok(load36 & 0xffffffff)
        elif load == 1:
            load37 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 4)
            load38 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 8)
            ptr39 = load37
            len40 = load38
            list = _decode_utf8(self.component._core_memory0, caller, ptr39, len40)
            expected = Err(list)
        else:
            raise TypeError("invalid variant discriminant for expected")
        self.component._post_return0(caller, ret)
        return expected
    def optionalb(self, caller: wasmtime.Store, data: TypeOptional, base: TypeBase) -> Result[TypeId, Error]:
        record = data
        field = record.of
        field0 = record.default_item
        if field0 is None:
            variant = 0
            variant3 = 0
            variant4 = 0
        else:
            payload1 = field0
            ptr, len2 = _encode_utf8(payload1, self.component._realloc0, self.component._core_memory0, caller)
            variant = 1
            variant3 = ptr
            variant4 = len2
        record5 = base
        field6 = record5.name
        field7 = record5.runtime_config
        field8 = record5.as_id
        if field6 is None:
            variant13 = 0
            variant14 = 0
            variant15 = 0
        else:
            payload10 = field6
            ptr11, len12 = _encode_utf8(payload10, self.component._realloc0, self.component._core_memory0, caller)
            variant13 = 1
            variant14 = ptr11
            variant15 = len12
        if field7 is None:
            variant26 = 0
            variant27 = 0
            variant28 = 0
        else:
            payload17 = field7
            vec = payload17
            len24 = len(vec)
            result = self.component._realloc0(caller, 0, 0, 4, len24 * 16)
            assert(isinstance(result, int))
            for i25 in range(0, len24):
                e = vec[i25]
                base18 = result + i25 * 16
                (tuplei,tuplei19,) = e
                ptr20, len21 = _encode_utf8(tuplei, self.component._realloc0, self.component._core_memory0, caller)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base18, 4, len21)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base18, 0, ptr20)
                ptr22, len23 = _encode_utf8(tuplei19, self.component._realloc0, self.component._core_memory0, caller)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base18, 12, len23)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base18, 8, ptr22)
            variant26 = 1
            variant27 = result
            variant28 = len24
        ret = self.component.lift_callee10(caller, _clamp(field, 0, 4294967295), variant, variant3, variant4, variant13, variant14, variant15, variant26, variant27, variant28, int(field8))
        assert(isinstance(ret, int))
        load = _load(ctypes.c_uint8, self.component._core_memory0, caller, ret, 0)
        expected: Result[TypeId, Error]
        if load == 0:
            load29 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 4)
            expected = Ok(load29 & 0xffffffff)
        elif load == 1:
            load30 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 4)
            load31 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 8)
            ptr32 = load30
            len33 = load31
            list = _decode_utf8(self.component._core_memory0, caller, ptr32, len33)
            expected = Err(list)
        else:
            raise TypeError("invalid variant discriminant for expected")
        self.component._post_return0(caller, ret)
        return expected
    def unionb(self, caller: wasmtime.Store, data: TypeUnion, base: TypeBase) -> Result[TypeId, Error]:
        record = data
        field = record.variants
        ptr, len0 = _list_canon_lower(field, ctypes.c_uint32, 4, 4, self.component._realloc0, self.component._core_memory0, caller)
        record1 = base
        field2 = record1.name
        field3 = record1.runtime_config
        field4 = record1.as_id
        if field2 is None:
            variant = 0
            variant8 = 0
            variant9 = 0
        else:
            payload5 = field2
            ptr6, len7 = _encode_utf8(payload5, self.component._realloc0, self.component._core_memory0, caller)
            variant = 1
            variant8 = ptr6
            variant9 = len7
        if field3 is None:
            variant20 = 0
            variant21 = 0
            variant22 = 0
        else:
            payload11 = field3
            vec = payload11
            len18 = len(vec)
            result = self.component._realloc0(caller, 0, 0, 4, len18 * 16)
            assert(isinstance(result, int))
            for i19 in range(0, len18):
                e = vec[i19]
                base12 = result + i19 * 16
                (tuplei,tuplei13,) = e
                ptr14, len15 = _encode_utf8(tuplei, self.component._realloc0, self.component._core_memory0, caller)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base12, 4, len15)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base12, 0, ptr14)
                ptr16, len17 = _encode_utf8(tuplei13, self.component._realloc0, self.component._core_memory0, caller)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base12, 12, len17)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base12, 8, ptr16)
            variant20 = 1
            variant21 = result
            variant22 = len18
        ret = self.component.lift_callee11(caller, ptr, len0, variant, variant8, variant9, variant20, variant21, variant22, int(field4))
        assert(isinstance(ret, int))
        load = _load(ctypes.c_uint8, self.component._core_memory0, caller, ret, 0)
        expected: Result[TypeId, Error]
        if load == 0:
            load23 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 4)
            expected = Ok(load23 & 0xffffffff)
        elif load == 1:
            load24 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 4)
            load25 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 8)
            ptr26 = load24
            len27 = load25
            list = _decode_utf8(self.component._core_memory0, caller, ptr26, len27)
            expected = Err(list)
        else:
            raise TypeError("invalid variant discriminant for expected")
        self.component._post_return0(caller, ret)
        return expected
    def eitherb(self, caller: wasmtime.Store, data: TypeEither, base: TypeBase) -> Result[TypeId, Error]:
        record = data
        field = record.variants
        ptr, len0 = _list_canon_lower(field, ctypes.c_uint32, 4, 4, self.component._realloc0, self.component._core_memory0, caller)
        record1 = base
        field2 = record1.name
        field3 = record1.runtime_config
        field4 = record1.as_id
        if field2 is None:
            variant = 0
            variant8 = 0
            variant9 = 0
        else:
            payload5 = field2
            ptr6, len7 = _encode_utf8(payload5, self.component._realloc0, self.component._core_memory0, caller)
            variant = 1
            variant8 = ptr6
            variant9 = len7
        if field3 is None:
            variant20 = 0
            variant21 = 0
            variant22 = 0
        else:
            payload11 = field3
            vec = payload11
            len18 = len(vec)
            result = self.component._realloc0(caller, 0, 0, 4, len18 * 16)
            assert(isinstance(result, int))
            for i19 in range(0, len18):
                e = vec[i19]
                base12 = result + i19 * 16
                (tuplei,tuplei13,) = e
                ptr14, len15 = _encode_utf8(tuplei, self.component._realloc0, self.component._core_memory0, caller)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base12, 4, len15)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base12, 0, ptr14)
                ptr16, len17 = _encode_utf8(tuplei13, self.component._realloc0, self.component._core_memory0, caller)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base12, 12, len17)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base12, 8, ptr16)
            variant20 = 1
            variant21 = result
            variant22 = len18
        ret = self.component.lift_callee12(caller, ptr, len0, variant, variant8, variant9, variant20, variant21, variant22, int(field4))
        assert(isinstance(ret, int))
        load = _load(ctypes.c_uint8, self.component._core_memory0, caller, ret, 0)
        expected: Result[TypeId, Error]
        if load == 0:
            load23 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 4)
            expected = Ok(load23 & 0xffffffff)
        elif load == 1:
            load24 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 4)
            load25 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 8)
            ptr26 = load24
            len27 = load25
            list = _decode_utf8(self.component._core_memory0, caller, ptr26, len27)
            expected = Err(list)
        else:
            raise TypeError("invalid variant discriminant for expected")
        self.component._post_return0(caller, ret)
        return expected
    def structb(self, caller: wasmtime.Store, data: TypeStruct, base: TypeBase) -> Result[TypeId, Error]:
        ptr = self.component._realloc0(caller, 0, 0, 4, 68)
        assert(isinstance(ptr, int))
        record = data
        field = record.props
        field0 = record.additional_props
        field1 = record.min
        field2 = record.max
        field3 = record.enumeration
        vec = field
        len8 = len(vec)
        result = self.component._realloc0(caller, 0, 0, 4, len8 * 12)
        assert(isinstance(result, int))
        for i9 in range(0, len8):
            e = vec[i9]
            base4 = result + i9 * 12
            (tuplei,tuplei5,) = e
            ptr6, len7 = _encode_utf8(tuplei, self.component._realloc0, self.component._core_memory0, caller)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, base4, 4, len7)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, base4, 0, ptr6)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, base4, 8, _clamp(tuplei5, 0, 4294967295))
        _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 4, len8)
        _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 0, result)
        _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 8, int(field0))
        if field1 is None:
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 12, 0)
        else:
            payload10 = field1
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 12, 1)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 16, _clamp(payload10, 0, 4294967295))
        if field2 is None:
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 20, 0)
        else:
            payload12 = field2
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 20, 1)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 24, _clamp(payload12, 0, 4294967295))
        if field3 is None:
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 28, 0)
        else:
            payload14 = field3
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 28, 1)
            vec19 = payload14
            len21 = len(vec19)
            result20 = self.component._realloc0(caller, 0, 0, 4, len21 * 8)
            assert(isinstance(result20, int))
            for i22 in range(0, len21):
                e15 = vec19[i22]
                base16 = result20 + i22 * 8
                ptr17, len18 = _encode_utf8(e15, self.component._realloc0, self.component._core_memory0, caller)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base16, 4, len18)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base16, 0, ptr17)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 36, len21)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 32, result20)
        record23 = base
        field24 = record23.name
        field25 = record23.runtime_config
        field26 = record23.as_id
        if field24 is None:
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 40, 0)
        else:
            payload28 = field24
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 40, 1)
            ptr29, len30 = _encode_utf8(payload28, self.component._realloc0, self.component._core_memory0, caller)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 48, len30)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 44, ptr29)
        if field25 is None:
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 52, 0)
        else:
            payload32 = field25
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 52, 1)
            vec41 = payload32
            len43 = len(vec41)
            result42 = self.component._realloc0(caller, 0, 0, 4, len43 * 16)
            assert(isinstance(result42, int))
            for i44 in range(0, len43):
                e33 = vec41[i44]
                base34 = result42 + i44 * 16
                (tuplei35,tuplei36,) = e33
                ptr37, len38 = _encode_utf8(tuplei35, self.component._realloc0, self.component._core_memory0, caller)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base34, 4, len38)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base34, 0, ptr37)
                ptr39, len40 = _encode_utf8(tuplei36, self.component._realloc0, self.component._core_memory0, caller)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base34, 12, len40)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base34, 8, ptr39)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 60, len43)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 56, result42)
        _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 64, int(field26))
        ret = self.component.lift_callee13(caller, ptr)
        assert(isinstance(ret, int))
        load = _load(ctypes.c_uint8, self.component._core_memory0, caller, ret, 0)
        expected: Result[TypeId, Error]
        if load == 0:
            load45 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 4)
            expected = Ok(load45 & 0xffffffff)
        elif load == 1:
            load46 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 4)
            load47 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 8)
            ptr48 = load46
            len49 = load47
            list = _decode_utf8(self.component._core_memory0, caller, ptr48, len49)
            expected = Err(list)
        else:
            raise TypeError("invalid variant discriminant for expected")
        self.component._post_return0(caller, ret)
        return expected
    def get_type_repr(self, caller: wasmtime.Store, id: TypeId) -> Result[str, Error]:
        ret = self.component.lift_callee14(caller, _clamp(id, 0, 4294967295))
        assert(isinstance(ret, int))
        load = _load(ctypes.c_uint8, self.component._core_memory0, caller, ret, 0)
        expected: Result[str, Error]
        if load == 0:
            load0 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 4)
            load1 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 8)
            ptr = load0
            len2 = load1
            list = _decode_utf8(self.component._core_memory0, caller, ptr, len2)
            expected = Ok(list)
        elif load == 1:
            load3 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 4)
            load4 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 8)
            ptr5 = load3
            len6 = load4
            list7 = _decode_utf8(self.component._core_memory0, caller, ptr5, len6)
            expected = Err(list7)
        else:
            raise TypeError("invalid variant discriminant for expected")
        self.component._post_return1(caller, ret)
        return expected
    def funcb(self, caller: wasmtime.Store, data: TypeFunc) -> Result[TypeId, Error]:
        record = data
        field = record.inp
        field0 = record.out
        field1 = record.mat
        field2 = record.rate_calls
        field3 = record.rate_weight
        if field3 is None:
            variant = 0
            variant5 = 0
        else:
            payload4 = field3
            variant = 1
            variant5 = _clamp(payload4, 0, 4294967295)
        ret = self.component.lift_callee15(caller, _clamp(field, 0, 4294967295), _clamp(field0, 0, 4294967295), _clamp(field1, 0, 4294967295), int(field2), variant, variant5)
        assert(isinstance(ret, int))
        load = _load(ctypes.c_uint8, self.component._core_memory0, caller, ret, 0)
        expected: Result[TypeId, Error]
        if load == 0:
            load6 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 4)
            expected = Ok(load6 & 0xffffffff)
        elif load == 1:
            load7 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 4)
            load8 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 8)
            ptr = load7
            len9 = load8
            list = _decode_utf8(self.component._core_memory0, caller, ptr, len9)
            expected = Err(list)
        else:
            raise TypeError("invalid variant discriminant for expected")
        self.component._post_return0(caller, ret)
        return expected
    def register_policy(self, caller: wasmtime.Store, pol: Policy) -> Result[PolicyId, Error]:
        record = pol
        field = record.name
        field0 = record.materializer
        ptr, len1 = _encode_utf8(field, self.component._realloc0, self.component._core_memory0, caller)
        ret = self.component.lift_callee16(caller, ptr, len1, _clamp(field0, 0, 4294967295))
        assert(isinstance(ret, int))
        load = _load(ctypes.c_uint8, self.component._core_memory0, caller, ret, 0)
        expected: Result[PolicyId, Error]
        if load == 0:
            load2 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 4)
            expected = Ok(load2 & 0xffffffff)
        elif load == 1:
            load3 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 4)
            load4 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 8)
            ptr5 = load3
            len6 = load4
            list = _decode_utf8(self.component._core_memory0, caller, ptr5, len6)
            expected = Err(list)
        else:
            raise TypeError("invalid variant discriminant for expected")
        self.component._post_return0(caller, ret)
        return expected
    def with_policy(self, caller: wasmtime.Store, data: TypePolicy) -> Result[TypeId, Error]:
        record = data
        field = record.tpe
        field0 = record.chain
        vec = field0
        len16 = len(vec)
        result = self.component._realloc0(caller, 0, 0, 4, len16 * 36)
        assert(isinstance(result, int))
        for i17 in range(0, len16):
            e = vec[i17]
            base1 = result + i17 * 36
            if isinstance(e, PolicySpecSimple):
                payload = e.value
                _store(ctypes.c_uint8, self.component._core_memory0, caller, base1, 0, 0)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base1, 4, _clamp(payload, 0, 4294967295))
            elif isinstance(e, PolicySpecPerEffect):
                payload2 = e.value
                _store(ctypes.c_uint8, self.component._core_memory0, caller, base1, 0, 1)
                record3 = payload2
                field4 = record3.none
                field5 = record3.create
                field6 = record3.update
                field7 = record3.delete
                if field4 is None:
                    _store(ctypes.c_uint8, self.component._core_memory0, caller, base1, 4, 0)
                else:
                    payload9 = field4
                    _store(ctypes.c_uint8, self.component._core_memory0, caller, base1, 4, 1)
                    _store(ctypes.c_uint32, self.component._core_memory0, caller, base1, 8, _clamp(payload9, 0, 4294967295))
                if field5 is None:
                    _store(ctypes.c_uint8, self.component._core_memory0, caller, base1, 12, 0)
                else:
                    payload11 = field5
                    _store(ctypes.c_uint8, self.component._core_memory0, caller, base1, 12, 1)
                    _store(ctypes.c_uint32, self.component._core_memory0, caller, base1, 16, _clamp(payload11, 0, 4294967295))
                if field6 is None:
                    _store(ctypes.c_uint8, self.component._core_memory0, caller, base1, 20, 0)
                else:
                    payload13 = field6
                    _store(ctypes.c_uint8, self.component._core_memory0, caller, base1, 20, 1)
                    _store(ctypes.c_uint32, self.component._core_memory0, caller, base1, 24, _clamp(payload13, 0, 4294967295))
                if field7 is None:
                    _store(ctypes.c_uint8, self.component._core_memory0, caller, base1, 28, 0)
                else:
                    payload15 = field7
                    _store(ctypes.c_uint8, self.component._core_memory0, caller, base1, 28, 1)
                    _store(ctypes.c_uint32, self.component._core_memory0, caller, base1, 32, _clamp(payload15, 0, 4294967295))
            else:
                raise TypeError("invalid variant specified for PolicySpec")
        ret = self.component.lift_callee17(caller, _clamp(field, 0, 4294967295), result, len16)
        assert(isinstance(ret, int))
        load = _load(ctypes.c_uint8, self.component._core_memory0, caller, ret, 0)
        expected: Result[TypeId, Error]
        if load == 0:
            load18 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 4)
            expected = Ok(load18 & 0xffffffff)
        elif load == 1:
            load19 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 4)
            load20 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 8)
            ptr = load19
            len21 = load20
            list = _decode_utf8(self.component._core_memory0, caller, ptr, len21)
            expected = Err(list)
        else:
            raise TypeError("invalid variant discriminant for expected")
        self.component._post_return0(caller, ret)
        return expected
    def register_context_policy(self, caller: wasmtime.Store, key: str, check: ContextCheck) -> Result[Tuple[PolicyId, str], Error]:
        ptr, len0 = _encode_utf8(key, self.component._realloc0, self.component._core_memory0, caller)
        if isinstance(check, ContextCheckValue):
            payload = check.value
            ptr1, len2 = _encode_utf8(payload, self.component._realloc0, self.component._core_memory0, caller)
            variant = 0
            variant6 = ptr1
            variant7 = len2
        elif isinstance(check, ContextCheckPattern):
            payload3 = check.value
            ptr4, len5 = _encode_utf8(payload3, self.component._realloc0, self.component._core_memory0, caller)
            variant = 1
            variant6 = ptr4
            variant7 = len5
        else:
            raise TypeError("invalid variant specified for ContextCheck")
        ret = self.component.lift_callee18(caller, ptr, len0, variant, variant6, variant7)
        assert(isinstance(ret, int))
        load = _load(ctypes.c_uint8, self.component._core_memory0, caller, ret, 0)
        expected: Result[Tuple[PolicyId, str], Error]
        if load == 0:
            load8 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 4)
            load9 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 8)
            load10 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 12)
            ptr11 = load9
            len12 = load10
            list = _decode_utf8(self.component._core_memory0, caller, ptr11, len12)
            expected = Ok((load8 & 0xffffffff, list,))
        elif load == 1:
            load13 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 4)
            load14 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 8)
            ptr15 = load13
            len16 = load14
            list17 = _decode_utf8(self.component._core_memory0, caller, ptr15, len16)
            expected = Err(list17)
        else:
            raise TypeError("invalid variant discriminant for expected")
        self.component._post_return2(caller, ret)
        return expected
    def rename_type(self, caller: wasmtime.Store, data: TypeRenamed) -> Result[TypeId, Error]:
        record = data
        field = record.tpe
        field0 = record.name
        ptr, len1 = _encode_utf8(field0, self.component._realloc0, self.component._core_memory0, caller)
        ret = self.component.lift_callee19(caller, _clamp(field, 0, 4294967295), ptr, len1)
        assert(isinstance(ret, int))
        load = _load(ctypes.c_uint8, self.component._core_memory0, caller, ret, 0)
        expected: Result[TypeId, Error]
        if load == 0:
            load2 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 4)
            expected = Ok(load2 & 0xffffffff)
        elif load == 1:
            load3 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 4)
            load4 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 8)
            ptr5 = load3
            len6 = load4
            list = _decode_utf8(self.component._core_memory0, caller, ptr5, len6)
            expected = Err(list)
        else:
            raise TypeError("invalid variant discriminant for expected")
        self.component._post_return0(caller, ret)
        return expected
    def expose(self, caller: wasmtime.Store, fns: List[Tuple[str, TypeId]], default_policy: Optional[List[PolicySpec]]) -> Result[None, Error]:
        vec = fns
        len3 = len(vec)
        result = self.component._realloc0(caller, 0, 0, 4, len3 * 12)
        assert(isinstance(result, int))
        for i4 in range(0, len3):
            e = vec[i4]
            base0 = result + i4 * 12
            (tuplei,tuplei1,) = e
            ptr, len2 = _encode_utf8(tuplei, self.component._realloc0, self.component._core_memory0, caller)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, base0, 4, len2)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, base0, 0, ptr)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, base0, 8, _clamp(tuplei1, 0, 4294967295))
        if default_policy is None:
            variant = 0
            variant25 = 0
            variant26 = 0
        else:
            payload5 = default_policy
            vec21 = payload5
            len23 = len(vec21)
            result22 = self.component._realloc0(caller, 0, 0, 4, len23 * 36)
            assert(isinstance(result22, int))
            for i24 in range(0, len23):
                e6 = vec21[i24]
                base7 = result22 + i24 * 36
                if isinstance(e6, PolicySpecSimple):
                    payload8 = e6.value
                    _store(ctypes.c_uint8, self.component._core_memory0, caller, base7, 0, 0)
                    _store(ctypes.c_uint32, self.component._core_memory0, caller, base7, 4, _clamp(payload8, 0, 4294967295))
                elif isinstance(e6, PolicySpecPerEffect):
                    payload9 = e6.value
                    _store(ctypes.c_uint8, self.component._core_memory0, caller, base7, 0, 1)
                    record = payload9
                    field = record.none
                    field10 = record.create
                    field11 = record.update
                    field12 = record.delete
                    if field is None:
                        _store(ctypes.c_uint8, self.component._core_memory0, caller, base7, 4, 0)
                    else:
                        payload14 = field
                        _store(ctypes.c_uint8, self.component._core_memory0, caller, base7, 4, 1)
                        _store(ctypes.c_uint32, self.component._core_memory0, caller, base7, 8, _clamp(payload14, 0, 4294967295))
                    if field10 is None:
                        _store(ctypes.c_uint8, self.component._core_memory0, caller, base7, 12, 0)
                    else:
                        payload16 = field10
                        _store(ctypes.c_uint8, self.component._core_memory0, caller, base7, 12, 1)
                        _store(ctypes.c_uint32, self.component._core_memory0, caller, base7, 16, _clamp(payload16, 0, 4294967295))
                    if field11 is None:
                        _store(ctypes.c_uint8, self.component._core_memory0, caller, base7, 20, 0)
                    else:
                        payload18 = field11
                        _store(ctypes.c_uint8, self.component._core_memory0, caller, base7, 20, 1)
                        _store(ctypes.c_uint32, self.component._core_memory0, caller, base7, 24, _clamp(payload18, 0, 4294967295))
                    if field12 is None:
                        _store(ctypes.c_uint8, self.component._core_memory0, caller, base7, 28, 0)
                    else:
                        payload20 = field12
                        _store(ctypes.c_uint8, self.component._core_memory0, caller, base7, 28, 1)
                        _store(ctypes.c_uint32, self.component._core_memory0, caller, base7, 32, _clamp(payload20, 0, 4294967295))
                else:
                    raise TypeError("invalid variant specified for PolicySpec")
            variant = 1
            variant25 = result22
            variant26 = len23
        ret = self.component.lift_callee20(caller, result, len3, variant, variant25, variant26)
        assert(isinstance(ret, int))
        load = _load(ctypes.c_uint8, self.component._core_memory0, caller, ret, 0)
        expected: Result[None, Error]
        if load == 0:
            expected = Ok(None)
        elif load == 1:
            load27 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 4)
            load28 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 8)
            ptr29 = load27
            len30 = load28
            list = _decode_utf8(self.component._core_memory0, caller, ptr29, len30)
            expected = Err(list)
        else:
            raise TypeError("invalid variant discriminant for expected")
        self.component._post_return0(caller, ret)
        return expected
