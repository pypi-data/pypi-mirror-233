from unskript.enums.enum_by_name import EnumByName
import enum

@enum.unique
class AccessKeyStatus(str, EnumByName):
    Active = "Active"
    Inactive = "Inactive"