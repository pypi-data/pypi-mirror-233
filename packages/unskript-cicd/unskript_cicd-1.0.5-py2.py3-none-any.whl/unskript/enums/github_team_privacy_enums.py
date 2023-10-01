from unskript.enums.enum_by_name import EnumByName
import enum

@enum.unique
class GithubTeamPrivacy(str, EnumByName):
    closed = "closed"
    secret = "secret"