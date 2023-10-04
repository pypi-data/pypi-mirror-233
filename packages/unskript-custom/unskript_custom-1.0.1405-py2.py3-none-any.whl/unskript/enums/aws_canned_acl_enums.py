from unskript.enums.enum_by_name import EnumByName
import enum

@enum.unique
class CannedACLPermissions(str, EnumByName):
    Private = "private"
    PublicRead = "public-read"
    PublicReadWrite = "public-read-write"
    AuthenticatedRead = "authenticated-read"