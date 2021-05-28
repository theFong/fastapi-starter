import typing
import shortuuid
import pydantic.networks
from pydantic.validators import str_validator

T = typing.TypeVar("T", bound="PrefixId")


class PrefixId(str):
    prefix = ""

    @classmethod
    def __modify_schema__(cls, field_schema: typing.Dict[str, typing.Any]) -> None:
        field_schema.update(type="string", format="id")

    @classmethod
    def __get_validators__(cls) -> "pydantic.networks.CallableGenerator":

        yield str_validator
        yield cls.validate

    @classmethod
    def validate(cls, value: typing.Union[str]) -> str:
        if not value.startswith(cls.prefix):
            raise ValueError(
                f"invalid id: {value} -- {cls.__name__} must start with prefix '{cls.prefix}''"
            )
        return value

    @classmethod
    def make(cls: typing.Type[T]) -> T:
        return cls(make_named_uuid(cls.prefix))

    def __eq__(self, o: "PrefixId") -> bool:
        return super().__eq__(o)

    def __ne__(self, o: "PrefixId") -> bool:
        return super().__eq__(o)

    def __hash__(self) -> int:
        return super().__hash__()


def make_named_uuid(name: str):
    suuid = str(shortuuid.uuid())
    return f"{name[:10]}_{suuid}"  # max 36
