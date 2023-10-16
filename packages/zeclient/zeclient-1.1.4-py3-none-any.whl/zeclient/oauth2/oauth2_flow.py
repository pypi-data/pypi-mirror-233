import enum


# Using enum class create enumerations
class OAuth2Flow(enum.Enum):
    AuthorizationCodeGrantType = 1
    ResourceOwnerPasswordCredentialsGrantType = 2
