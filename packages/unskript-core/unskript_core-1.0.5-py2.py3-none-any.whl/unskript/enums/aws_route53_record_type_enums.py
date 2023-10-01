from unskript.enums.enum_by_name import EnumByName
import enum

@enum.unique
class Route53RecordType(str, EnumByName):
    A = "A"
    AAAA = "AAAA"
    CAA = "CAA"
    CNAME = "CNAME"
    DS = "DS"
    MX = "MX"
    NAPTR = "NAPTR"
    NS = "NS"
    PTR = "PTR"
    SOA = "SOA"
    SPF = "SPF"
    SRV = "SRV"
    TXT = "TXT"