from enum import Enum


class ExternalInfoBotName(str, Enum):
    WHETHER_FORECAST = 'whether_forecast'
    LOTTERY = 'lottery'


class ExternalInfoBotUrls(dict, Enum):
    pass


class InternalInfoBotName(str, Enum):
    LOVER_GREETING = 'lover_greeting'
