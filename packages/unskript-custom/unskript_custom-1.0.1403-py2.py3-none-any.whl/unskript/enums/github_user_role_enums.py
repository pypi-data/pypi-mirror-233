from unskript.enums.enum_by_name import EnumByName
import enum

@enum.unique
class GithubUserRole(str, EnumByName):
    admin = "admin", 
    direct_member = "direct_member", 
    billing_manager = "billing_manager"