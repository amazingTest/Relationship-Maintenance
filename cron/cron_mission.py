from info_robot.info_bot import InfoFactory
from log import logger


class CronMission:

    def __init__(self, messenger, info_bot_name, cron_expression, **kwargs):
        self.messenger = messenger
        self.info_bot_name = info_bot_name
        self.cron_expression = cron_expression
        self.kwargs = kwargs

    def __str__(self):
        return f'[info_bot_name: {self.info_bot_name}, kwargs: {self.kwargs} ' \
               f'cron_expression: {self.cron_expression}, messenger: {self.messenger}]'

    def start(self):
        info = InfoFactory.get_info(self.info_bot_name, **self.kwargs)
        info_title = info.get('title', '')
        info_content = info.get('content', '')
        self.messenger.send(title=info_title, content=info_content)


if __name__ == '__main__':
    pass

