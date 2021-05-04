#!/usr/bin/env python
# -*- encoding=utf8 -*-
import requests

from log import logger
from messenger import Channel

DEFAULT_TITLE = 'Hello!'
DEFAULT_CONTENT = 'Here is the content!'


class Messenger:
    """消息推送类"""

    def __init__(self, title=DEFAULT_TITLE, content=DEFAULT_CONTENT, **kwargs):
        self.title = title
        self.content = content
        self.headers = {'Content-Type': 'application/json'}
        self.channel = kwargs.get('channel')

    def send(self, **kwargs):
        raise NotImplementedError

    @property
    def predefined_data_for_sending(self):
        result = dict()
        return result

    @property
    def build_data_for_sending(self):
        result = dict()
        result.update(self.predefined_data_for_sending)
        content = self.content_to_send
        result.update(content)
        return result

    @property
    def content_to_send(self):
        result = dict()
        return result


class EnterpriseWeChatMessenger(Messenger):
    """企业微信应用推送"""

    def __init__(self, corpid, secret, agentid, **kwargs):

        super(EnterpriseWeChatMessenger, self).__init__(channel=Channel.ENTERPRISE_WE_CHAT_APP, **kwargs)

        self.corpid = corpid
        self.secret = secret
        self.agentid = agentid
        self.touser = kwargs.get('touser', '@all')
        self.toparty = kwargs.get('toparty', '')

    def __str__(self):
        return f'[corpid: {self.corpid}, secret: {self.secret}, agentid: {self.agentid} ' \
               f'touser: {self.touser}, toparty: {self.toparty}]'

    def send(self, title=DEFAULT_TITLE, content=DEFAULT_CONTENT, **kwargs):
        self.title = title
        self.content = content
        self._send_message_to_enterprise_we_chat_app()

    def _send_message_to_enterprise_we_chat_app(self):
        access_token = self.enterprise_we_chat_access_token
        hook_url = f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}"
        json_data = self.build_data_for_sending
        logger.info(f'json_data: {json_data}')
        resp = requests.post(url=hook_url, json=json_data, headers=self.headers)
        logger.info(f'resp_text: {resp.text}')

    @property
    def enterprise_we_chat_access_token(self):
        corp_id = self.corpid
        secret = self.secret
        access_token = requests.get(url=f'https://qyapi.weixin.qq.com/cgi-bin/gettoken?'
                                        f'corpid={corp_id}&corpsecret={secret}').json()['access_token']
        return access_token

    @property
    def predefined_data_for_sending(self):
        predefined_data = {
            "touser": self.touser,
            "toparty": self.toparty,
            "agentid": self.agentid,
            "msgtype": 'text'
        }
        return predefined_data

    @property
    def content_to_send(self):
        result = dict()
        result["text"] = {"content": "{}\n\n{}".format(self.title, self.content)}
        return result


class MessengerFactory:

    MessengerMap = {
        Channel.ENTERPRISE_WE_CHAT_APP.value: EnterpriseWeChatMessenger
    }

    @classmethod
    def _get_messenger(cls, channel_name, **kwargs):
        if channel_name not in cls.MessengerMap:
            return
        return cls.MessengerMap[channel_name](**kwargs)

    @classmethod
    def get_messenger(cls, channel_name, **kwargs):
        messenger = cls._get_messenger(channel_name, **kwargs)
        return messenger


if __name__ == '__main__':
    pass
