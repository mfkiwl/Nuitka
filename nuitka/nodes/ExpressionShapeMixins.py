#     Copyright 2021, Kay Hayen, mailto:kay.hayen@gmail.com
#
#     Part of "Nuitka", an optimizing Python compiler that is compatible and
#     integrates with CPython, but also works on its own.
#
#     Licensed under the Apache License, Version 2.0 (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.
#
"""Mixins for expressions that have specific shapes.

Providing derived implementation, such that e.g. for a given shape, shortcuts
are automatically implemented.
"""

from abc import abstractmethod

from nuitka.Constants import (
    the_empty_bytearray,
    the_empty_dict,
    the_empty_frozenset,
    the_empty_list,
    the_empty_set,
    the_empty_tuple,
)

from .shapes.BuiltinTypeShapes import (
    tshape_bool,
    tshape_bytearray,
    tshape_bytes,
    tshape_dict,
    tshape_frozenset,
    tshape_list,
    tshape_set,
    tshape_str,
    tshape_str_or_unicode,
    tshape_tuple,
    tshape_unicode,
)


class ExpressionSpecificExactMixinBase(object):
    """Mixin that provides all shapes exactly false overloads.

    This is to be used as a base class for specific shape mixins,
    such that they automatically provide false for all other exact
    shape checks except the one they care about.
    """

    __slots__ = ()

    @staticmethod
    def hasShapeBoolExact():
        return False

    @staticmethod
    def hasShapeDictionaryExact():
        return False

    @staticmethod
    def hasShapeListExact():
        return False

    @staticmethod
    def hasShapeSetExact():
        return False

    @staticmethod
    def hasShapeFrozesetExact():
        return False

    @staticmethod
    def hasShapeTupleExact():
        return False

    @staticmethod
    def hasShapeStrExact():
        return False

    @staticmethod
    def hasShapeUnicodeExact():
        return False

    @staticmethod
    def hasShapeStrOrUnicodeExact():
        return False

    @staticmethod
    def hasShapeBytesExact():
        return False

    @staticmethod
    def hasShapeBytearrayExact():
        return False

    @staticmethod
    def hasShapeTrustedAttributes():
        return True

    @abstractmethod
    def isKnownToHaveAttribute(self, attribute_name):
        return True

    @abstractmethod
    def getKnownAttributeValue(self, attribute_name):
        """Can be used as isKnownToHaveAttribute is True"""

    def mayRaiseExceptionAttributeLookup(self, exception_type, attribute_name):
        # TODO: The exception_type is not checked, pylint: disable=unused-argument
        return not self.isKnownToHaveAttribute(attribute_name)

    @staticmethod
    def mayRaiseExceptionBool(exception_type):
        # We cannot raise anything, pylint: disable=unused-argument
        return False

    @staticmethod
    def mayHaveSideEffectsBool():
        return False


class ExpressionDictShapeExactMixin(ExpressionSpecificExactMixinBase):
    """Mixin for nodes with exact dictionary shape."""

    __slots__ = ()

    @staticmethod
    def getTypeShape():
        return tshape_dict

    @staticmethod
    def hasShapeDictionaryExact():
        return True

    @staticmethod
    def isKnownToHaveAttribute(attribute_name):
        return hasattr(the_empty_dict, attribute_name)

    @staticmethod
    def getKnownAttributeValue(attribute_name):
        return getattr(the_empty_dict, attribute_name)

    @staticmethod
    def isKnownToBeHashable():
        return False

    def extractUnhashableNodeType(self):
        from .ConstantRefNodes import makeConstantRefNode

        return makeConstantRefNode(constant=dict, source_ref=self.source_ref)


class ExpressionListShapeExactMixin(ExpressionSpecificExactMixinBase):
    """Mixin for nodes with exact list shape."""

    __slots__ = ()

    @staticmethod
    def getTypeShape():
        return tshape_list

    @staticmethod
    def hasShapeListExact():
        return True

    @staticmethod
    def isKnownToHaveAttribute(attribute_name):
        return hasattr(the_empty_list, attribute_name)

    @staticmethod
    def getKnownAttributeValue(attribute_name):
        return getattr(the_empty_list, attribute_name)

    @staticmethod
    def isKnownToBeHashable():
        return False

    def extractUnhashableNodeType(self):
        from .ConstantRefNodes import makeConstantRefNode

        return makeConstantRefNode(constant=list, source_ref=self.source_ref)


class ExpressionFrozensetShapeExactMixin(ExpressionSpecificExactMixinBase):
    """Mixin for nodes with exact frozenset shape."""

    __slots__ = ()

    @staticmethod
    def getTypeShape():
        return tshape_frozenset

    @staticmethod
    def hasShapeListExact():
        return True

    @staticmethod
    def isKnownToHaveAttribute(attribute_name):
        return hasattr(the_empty_frozenset, attribute_name)

    @staticmethod
    def getKnownAttributeValue(attribute_name):
        return getattr(the_empty_frozenset, attribute_name)

    @staticmethod
    def isKnownToBeHashable():
        return True


class ExpressionSetShapeExactMixin(ExpressionSpecificExactMixinBase):
    """Mixin for nodes with exact set shape."""

    __slots__ = ()

    @staticmethod
    def getTypeShape():
        return tshape_set

    @staticmethod
    def hasShapeSetExact():
        return True

    @staticmethod
    def isKnownToHaveAttribute(attribute_name):
        return hasattr(the_empty_set, attribute_name)

    @staticmethod
    def getKnownAttributeValue(attribute_name):
        return getattr(the_empty_set, attribute_name)

    @staticmethod
    def isKnownToBeHashable():
        return False

    def extractUnhashableNodeType(self):
        from .ConstantRefNodes import makeConstantRefNode

        return makeConstantRefNode(constant=set, source_ref=self.source_ref)


class ExpressionTupleShapeExactMixin(ExpressionSpecificExactMixinBase):
    """Mixin for nodes with exact tuple shape."""

    __slots__ = ()

    @staticmethod
    def getTypeShape():
        return tshape_tuple

    @staticmethod
    def hasShapeSetExact():
        return True

    @staticmethod
    def isKnownToHaveAttribute(attribute_name):
        return hasattr(the_empty_tuple, attribute_name)

    @staticmethod
    def getKnownAttributeValue(attribute_name):
        return getattr(the_empty_tuple, attribute_name)

    @staticmethod
    def isKnownToBeHashable():
        return None


class ExpressionBoolShapeExactMixin(ExpressionSpecificExactMixinBase):
    """Mixin for nodes with exact bool shape."""

    __slots__ = ()

    @staticmethod
    def getTypeShape():
        return tshape_bool

    @staticmethod
    def hasShapeBoolExact():
        return True

    @staticmethod
    def isKnownToHaveAttribute(attribute_name):
        return hasattr(False, attribute_name)

    @staticmethod
    def getKnownAttributeValue(attribute_name):
        return getattr(False, attribute_name)

    @staticmethod
    def isKnownToBeHashable():
        return True


class ExpressionStrExactMixin(ExpressionSpecificExactMixinBase):
    """Mixin for nodes with exact str shape."""

    __slots__ = ()

    @staticmethod
    def getTypeShape():
        return tshape_str

    @staticmethod
    def hasShapeStrExact():
        return True

    @staticmethod
    def hasShapeStrOrUnicodeExact():
        return True

    @staticmethod
    def isKnownToHaveAttribute(attribute_name):
        return hasattr("", attribute_name)

    @staticmethod
    def getKnownAttributeValue(attribute_name):
        return getattr("", attribute_name)

    @staticmethod
    def isKnownToBeHashable():
        return True


class ExpressionBytesShapeExactMixin(ExpressionSpecificExactMixinBase):
    """Mixin for nodes with exact bytes shape."""

    __slots__ = ()

    @staticmethod
    def getTypeShape():
        return tshape_bytes

    @staticmethod
    def hasShapeBytesExact():
        return True

    @staticmethod
    def isKnownToHaveAttribute(attribute_name):
        return hasattr(b"", attribute_name)

    @staticmethod
    def getKnownAttributeValue(attribute_name):
        return getattr(b"", attribute_name)

    @staticmethod
    def isKnownToBeHashable():
        return True


class ExpressionBytearrayShapeExactMixin(ExpressionSpecificExactMixinBase):
    """Mixin for nodes with exact bytearray shape."""

    __slots__ = ()

    @staticmethod
    def getTypeShape():
        return tshape_bytearray

    @staticmethod
    def hasShapeBytearrayExact():
        return True

    @staticmethod
    def isKnownToHaveAttribute(attribute_name):
        return hasattr(the_empty_bytearray, attribute_name)

    @staticmethod
    def getKnownAttributeValue(attribute_name):
        return getattr(the_empty_bytearray, attribute_name)

    @staticmethod
    def isKnownToBeHashable():
        return False

    def extractUnhashableNodeType(self):
        from .ConstantRefNodes import makeConstantRefNode

        return makeConstantRefNode(constant=bytearray, source_ref=self.source_ref)


class ExpressionUnicodeShapeExactMixin(ExpressionSpecificExactMixinBase):
    """Mixin for nodes with exact unicode shape."""

    __slots__ = ()

    @staticmethod
    def getTypeShape():
        return tshape_unicode

    @staticmethod
    def hasShapeUnicodeExact():
        return True

    @staticmethod
    def hasShapeStrOrUnicodeExact():
        return True

    @staticmethod
    def isKnownToHaveAttribute(attribute_name):
        return hasattr(u"", attribute_name)

    @staticmethod
    def getKnownAttributeValue(attribute_name):
        return getattr(u"", attribute_name)

    @staticmethod
    def isKnownToBeHashable():
        return True


if str is not bytes:
    ExpressionStrOrUnicodeExactMixin = ExpressionStrExactMixin
else:

    class ExpressionStrOrUnicodeExactMixin(ExpressionSpecificExactMixinBase):
        """Mixin for nodes with str_or_unicode shape."""

        __slots__ = ()

        @staticmethod
        def getTypeShape():
            return tshape_str_or_unicode

        @staticmethod
        def hasShapeStrOrUnicodeExact():
            return True

        @staticmethod
        def isKnownToHaveAttribute(attribute_name):
            return hasattr(u"", attribute_name) and hasattr("", attribute_name)

        @staticmethod
        def getKnownAttributeValue(attribute_name):
            return getattr("", attribute_name)

        @staticmethod
        def isKnownToBeHashable():
            return True
