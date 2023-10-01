import enum


class EnumByName(enum.Enum):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        names = [m.name for m in cls]
        if isinstance(v, cls):
            if v not in cls:
                raise ValueError("not a valid Enum member")
        elif isinstance(v, str):
            if v not in names:
                raise ValueError("no Enum member with that name")
        else:
            raise TypeError("not an Enum")
        return v

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema["enum"] = [m.name for m in cls]
