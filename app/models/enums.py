from enum import Enum


class Role(Enum):
    ADMIN = 0
    USER = 1


class OAuthProvider(Enum):
    PASSWORD = "password"
    GITHUB = "github"
