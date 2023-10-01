import typing

import pydantic

# Python 3.8/3.9 compatible import of TypeGuard
try:
    from typing import TypeGuard
except ImportError:
    try:
        from typing_extensions import TypeGuard
    except ImportError:
        pass

T = typing.TypeVar("T")


class NotSetType(pydantic.BaseModel):
    """
    A sentinel value for fields (e.g. kwargs) that are not set, useful when 'None' is a meaningful value.

    It extends pydantic.BaseModel so that it integrates nicely with pydantic's schema generation/json serialization.
    """

    @staticmethod
    def openapi_schema_modifier(
        schema: dict[str, typing.Any], model: typing.Any
    ) -> None:
        """
        Replace NotSetType with null in anyOf lists.

        To use in pydantic.BaseModel, add the following to your model:
        >>> class Config:
        ...     schema_extra = NotSetType.openapi_schema_modifier


        See https://docs.pydantic.dev/1.10/usage/schema/#schema-customization
        """
        for prop in schema.get("properties", {}).values():
            if "anyOf" in prop:
                any_of = prop.pop("anyOf")

                without_notset = []
                for sub_prop in any_of:
                    if isinstance(sub_prop, dict) and "NotSetType" in sub_prop.get(
                        "$ref", ""
                    ):
                        if "default" in prop and prop["default"] == {}:
                            del prop["default"]
                        without_notset.append({"type": "null"})
                    else:
                        without_notset.append(sub_prop)

                if without_notset:
                    if len(without_notset) == 1:
                        prop.update(without_notset[0])
                    else:
                        prop["anyOf"] = without_notset

    def __bool__(self) -> bool:
        return False


def is_not_set(value: typing.Any) -> TypeGuard[NotSetType]:
    return isinstance(value, NotSetType)


def is_set(value: typing.Union[T, NotSetType]) -> TypeGuard[T]:
    return not isinstance(value, NotSetType)


def value_or_not_set(value: typing.Optional[T]) -> typing.Union[T, NotSetType]:
    if value is None:
        return NotSet
    else:
        return value


def value_or_default_if_unset(value: typing.Union[T, NotSetType], default: T) -> T:
    if isinstance(value, NotSetType):
        return default
    else:
        return value


NotSet = NotSetType()
