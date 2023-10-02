from enum import Enum, auto, unique


@unique
class EnvVarName(Enum):
    """
    Environment Variables that are used by this project.
    """

    def _generate_next_value_(name, start, count, last_values):
        return name

    # TODO: Documentation
    LOG_LEVEL = auto()
    LOCATION = auto()
    REGION = auto()
    TIMEZONE = auto()
    LATITUDE = auto()
    LONGITUDE = auto()

    # The key needed to access the AirNow API
    AIRNOW_API_KEY = auto()

    TWITTER_CONSUMER_KEY = auto()
    TWITTER_CONSUMER_SECRET = auto()
    TWITTER_ACCESS_TOKEN = auto()
    TWITTER_ACCESS_TOKEN_SECRET = auto()
    TWITTER_BEARER_TOKEN = auto()
    TWITTER_HASHTAG = auto()
