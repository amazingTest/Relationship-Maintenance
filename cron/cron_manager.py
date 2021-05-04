from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
import json
from collections import defaultdict
from messenger.custom_messenger import MessengerFactory
from cron.cron_mission import CronMission
from pytz import timezone
from log import logger


class BaseManagerAdaptor:

    def __init__(self, **kwargs):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def start_all(self):
        raise NotImplementedError


with open('config/cron.json') as file:
    cron_config = json.load(file)

with open('config/messenger.json') as file:
    messenger_config = json.load(file)


class CronManagerAdaptor(BaseManagerAdaptor):

    def __init__(self, **kwargs):
        super(CronManagerAdaptor, self).__init__(**kwargs)
        self.cron_scheduler = BlockingScheduler(timezone=timezone('Asia/Shanghai'))
        self.messengers = defaultdict(list)
        self.cron_missions = defaultdict(list)

    def _load_cron_config(self):
        for cron_info in cron_config:
            cron_method = cron_info['mission']['name']
            cron_payload = cron_info['mission']['payload']
            cron_expression = cron_info['cron']
            cron_messenger = cron_info['messenger']
            cron_messenger_instances = self.__get_all_messenger_instances(cron_messenger)
            self.__load_cron_missions(cron_messenger_instances, cron_method, cron_expression, **cron_payload)

    def __load_cron_missions(self, cron_messenger_instances, cron_method, cron_expression, **cron_payload):
        for messenger_instance in cron_messenger_instances:
            cron_mission = CronMission(messenger_instance, cron_method, cron_expression, **cron_payload)
            self.cron_missions[cron_method].append(cron_mission)

    def __get_all_messenger_instances(self, cron_messenger):
        messenger_instances = self.messengers.get(cron_messenger)
        if not messenger_instances:
            raise BaseException(f'cron_messenger: [{cron_messenger}] not found in messenger.json!')
        return messenger_instances

    def _load_messenger_config(self):
        for messenger_info in messenger_config:
            channel = messenger_info['channel']
            payload = messenger_info['payload']
            messenger_instance = MessengerFactory.get_messenger(channel, **payload)
            self.messengers[channel].append(messenger_instance)

    def _load_all_config(self):
        self._load_messenger_config()
        self._load_cron_config()

    def __enter__(self):
        self._load_all_config()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return

    def _add_cron_jobs(self, cron_missions):
        for cron_mission in cron_missions:
            cron_trigger = CronTrigger.from_crontab(cron_mission.cron_expression)
            self.cron_scheduler.add_job(func=cron_mission.start,
                                        trigger=cron_trigger,
                                        coalesce=True,
                                        replace_existing=True)
            logger.info(f'cron_mission: {cron_mission} successfully added')

    def start_all(self):
        for mission_name, cron_missions in self.cron_missions.items():
            self._add_cron_jobs(cron_missions)
        self.cron_scheduler.start()


if __name__ == '__main__':
    pass

