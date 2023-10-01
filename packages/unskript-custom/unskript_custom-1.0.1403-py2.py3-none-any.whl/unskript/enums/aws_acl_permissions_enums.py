from unskript.enums.enum_by_name import EnumByName
import enum

@enum.unique
class BucketACLPermissions(str, EnumByName):
    READ = "READ"
    WRITE = "WRITE"
    READ_ACP = "READ_ACP"
    WRITE_ACP = "WRITE_ACP"
    FULL_CONTROL = "FULL_CONTROL"