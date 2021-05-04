from info_robot import ExternalInfoBotName, ExternalInfoBotUrls, InternalInfoBotName
import copy
import requests
import json
import random
from datetime import datetime
from log import logger

with open('config/builtin_sentences.json') as file:
    internal_sentences = json.load(file)


class BaseInfoBot:

    def __init__(self, **kwargs):
        self.bot_name = kwargs.get('bot_name')
        self.info = dict({'title': '', 'content': ''})

    def get_set_info(self, **kwargs) -> dict:
        result = dict()
        self.info.update(result)
        return self.info


class InternalInfoBot(BaseInfoBot):
    def __init__(self, **kwargs):
        super(InternalInfoBot, self).__init__(**kwargs)


class LoverGreetingBot(InternalInfoBot):

    def __init__(self, **kwargs):
        super(LoverGreetingBot, self).__init__(**kwargs)
        self.internal_sentences_map = internal_sentences.get(InternalInfoBotName.LOVER_GREETING, {})
        self.begin_date = kwargs.get('begin_date')

    def get_set_info(self, **kwargs) -> dict:
        result = dict()
        result['title'] = kwargs.get('title', '')
        greeting_type = kwargs.get('greeting_type', 'normal')
        if self.together_days:
            result['title'] += ' ' if result['title'] else result['title']
            result['title'] += f'今天我们在一起 {self.together_days} 天了～'
        result['content'] = kwargs.get('content', '')
        if not result['content']:
            sentences = self.internal_sentences_map.get(greeting_type, [])
            sentence = random.choice(sentences)
            result['content'] = sentence
        self.info.update(result)
        return self.info

    @property
    def together_days(self):
        if not self.begin_date:
            return
        begin_datetime = datetime.strptime(self.begin_date, '%Y-%m-%d')
        now_datetime = datetime.now()
        together_days = (now_datetime - begin_datetime).days
        return together_days


class ExternalInfoBot(BaseInfoBot):
    def __init__(self, **kwargs):
        super(ExternalInfoBot, self).__init__(**kwargs)
        self.session = requests.Session()


class WeatherForecastBot(ExternalInfoBot):

    def __init__(self, **kwargs):
        super(WeatherForecastBot, self).__init__(bot_name=ExternalInfoBotName.WHETHER_FORECAST, **kwargs)

    def get_set_info(self, **kwargs) -> dict:
        result = dict()
        self.info.update(result)
        return self.info


class LotteryBot(ExternalInfoBot):

    def __init__(self, **kwargs):
        super(LotteryBot, self).__init__(bot_name=ExternalInfoBotName.LOTTERY, **kwargs)

    def get_set_info(self, **kwargs) -> dict:
        result = dict()
        self.info.update(result)
        return self.info


class InfoFactory:

    ExternalInfoBotMap = {
        ExternalInfoBotName.WHETHER_FORECAST.value: WeatherForecastBot,
        ExternalInfoBotName.LOTTERY.value: LotteryBot
    }

    InternalInfoBotMap = {
        InternalInfoBotName.LOVER_GREETING.value: LoverGreetingBot
    }

    @classmethod
    def get_info_bot_map(cls):
        external_info_bot_map = copy.deepcopy(cls.ExternalInfoBotMap)
        internal_info_bot_map = copy.deepcopy(cls.InternalInfoBotMap)
        total_info_bot_map = {**external_info_bot_map, **internal_info_bot_map}
        return total_info_bot_map
    
    @classmethod
    def __get_info_bot(cls, bot_name, **kwargs):
        info_bot_map = cls.get_info_bot_map()
        if bot_name not in info_bot_map:
            return
        return info_bot_map[bot_name](**kwargs)

    @classmethod
    def _get_info_bot(cls, bot_name, **kwargs):
        info_bot = cls.__get_info_bot(bot_name, **kwargs)
        return info_bot

    @classmethod
    def get_info(cls, bot_name, **kwargs):
        info_bot = cls._get_info_bot(bot_name, **kwargs)
        info = info_bot.get_set_info(**kwargs)
        return info


if __name__ == '__main__':
    pass
