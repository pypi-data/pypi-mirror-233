__version__ = "0.0.5"

from .decs import (
    set_attr, set_default, set_fallback, set_fbmem, 
    set_method, set_dtype, set_repr
)

from .meta import (
    DataTypedEnumMeta, FallbackEnumMeta, TypedEnumMeta
)

from .enum import (
    TypedFallbackMixin, BaseTypedEnum, OperatorEnum, LiteralEnum,
    LitStrEnum, LitIntEnum, Litum, Strum, Intum
)

__all__ = [
    'set_attr', 'set_default', 'set_fallback', 'set_fbmem',
    'set_method', 'set_dtype', 'set_repr',

    'DataTypedEnumMeta', 'FallbackEnumMeta', 'TypedEnumMeta',

    'TypedFallbackMixin', 'BaseTypedEnum', 'OperatorEnum', 'LiteralEnum',
    'LitStrEnum', 'LitIntEnum', 
    'Litum', 'Strum', 'Intum', 
]