#!/usr/bin/env python

import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

import logging
logging.basicConfig(level = logging.INFO)
logger = logging.getLogger(__name__)

class SlackConnector():
    """Summary
    https://github.com/slackapi/python-slack-sdk

    import slackconnector
    sc = slackconnector.SlackConnector('name')
    sc.notify('Hello world.')
    """
    def __init__(self, name = None):
        self.sc, self.slack_user_id = None, None
        self.name = name if name else 'SlackConnector'
        if 'SLACK_BOT_TOKEN' in os.environ and 'SLACK_USER_ID' in os.environ:
            self.sc = WebClient(token=os.environ.get('SLACK_BOT_TOKEN'))
            self.slack_user_id = os.environ.get('SLACK_USER_ID')
            if self.sc.rtm_connect():
                logger.info('Connected to Slack.')
            else:
                raise Exception('Slack token found but connection failed.')
        else:
            logger.info('SLACK_BOT_TOKEN and SLACK_USER_ID not failed. Connection failed.')
    
    def notify(self, msg):
        try:
            m = self.sc.chat_postMessage(channel=self.slack_user_id, text = msg, username=self.name) 
            # , as_user = False 
            assert m["message"]["text"] == msg
        except SlackApiError as e:
            assert e.response["ok"] is False
            assert e.response["error"]
            logger.info(f"Got an error: {e.response['error']}")