from unskript.enums.enum_by_name import EnumByName
import enum


@enum.unique
class Method(str, EnumByName):
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    PATCH = 'PATCH'
    DELETE = 'DELETE'
