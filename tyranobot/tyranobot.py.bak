#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import json
import time
from builtins import str
from random import randint
from urllib import unquote
from slackclient import SlackClient


class SlackException(Exception):
    pass


class TyranoBot(SlackClient):

    def __init__(self, bot_data, *args, **kwargs):
        # Call SlackClient's initialization function
        SlackClient.__init__(self, bot_data['bot_token'], *args, **kwargs)

        # Store the token and id then set the socket delay
        self.token = bot_data['bot_token']
        self.bot_id = self.get_bot_id(bot_data)
        self.web_socket_delay = 1

        # Our dictionaries of replies
        self.replies = {
            'passive': [],
            'active': []
        }

    def get_bot_id(self, bot_data):
        """
        Determine's our bot's user id either through the given bot bot_data
        or by combing through the user list
        """
        if bot_data.get('bot_id') and bot_data['bot_id'] != '':
            return bot_data['bot_id']
        elif bot_data.get('bot_name'):
            user_list = self.api_call("users.list")
            if not user_list.get('ok'):
                raise SlackException('Unable to retrieve user list for bot identification')
            if user_list.get('ok'):
                # retrieve all users so we can find our bot
                for user in user_list.get('members'):
                    if 'name' in user and user.get('name') == bot_data['bot_name']:
                        if not user['deleted']:
                            return user['id']
                        else:
                            raise SlackException('Bot user {0} appears to have been deleted. Please use another bot.'.format(bot_data['bot_name']))

                # If the loop completes without finding the bot, raise an exception
                raise SlackException('Bot user {0} not found.'.format(bot_data['bot_name']))

    @property
    def web_socket_delay(self):
        return self._web_socket_delay

    @web_socket_delay.setter
    def web_socket_delay(self, value):
        self._web_socket_delay = value

    def start(self):
        # Connect to the Slack RTM
        if self.rtm_connect():
            self.listen()
        else:
            raise SlackException('Could not connect, purging bot from list')

    def listen(self):
        """
        Listen to Slack traffic
        """
        while True:
            # Parse the messages for the info SNAPBot needs
            msg, channel, active = self.parse_messages(self.rtm_read())

            if msg:
                # Determine whether to reply passively or actively
                reply = self.get_reply(msg, channel, active)

                # If we have a reply, send it
                if reply:
                    if type(reply) is dict:
                        # If the reply is a dict, try to send it as a formatted slack message
                        reply["channel"] = channel
                        try:
                            self.send_formatted_message(reply)
                        except KeyError as e:
                            raise SlackException('Slack message formatted incorrectly. Problem with key: {0}'.format(e))

                    else:
                        # Otherwise, just send the message as a normal string
                        self.api_call("chat.postMessage", channel=channel, text=unquote(reply), as_user=True)

            # Sleep for a sec
            time.sleep(self.web_socket_delay)

    def send_formatted_message(self, reply):
        """
        The SlackClient library doesn't support message attachments.
        So to get around that, we'll use the requests library to post
        more complex message types.
        """
        # Build a nicely formatted Slack message
        message = {
            'token': self.token,
            'channel': reply['channel'],
            'as_user': 'true',
            'text': reply['text'],
            'attachments': json.dumps(reply['attachments'])
        }

        # Send it
        from requests import post
        resp = post("https://slack.com/api/chat.postMessage", params=message)

    def parse_messages(self, messages):
        """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
        """
        msg = None
        channel = None
        active = False

        if messages and len(messages) > 0:
            for message in messages:
                if message and 'text' in message:
                    # Make sure TyranoBot doesn't start talking to itself. That would be crazy.
                    if 'user' in message and message['user'] == self.bot_id:
                        return msg, channel, active

                    # See if this message was addressed to someone
                    user = re.match(r"(<(@.*)>)", message['text'])
                    channel = message['channel']

                    # If SNAPBot is the intended recipient, reply actively
                    if user and user.group(2) == '@' + self.bot_id:
                        msg = message['text'].split(user.group(1))[1].strip().lower()
                        active = True

                    # If SNAPBot is not the intended recipient, reply passively
                    elif not user:
                        msg = message['text'].strip().lower()
                        active = False

        return msg, channel, active

    def get_reply(self, msg, channel, active):
        """
        Finds the correct reply for the received message
        """
        # Everything in lowercase makes regex easier
        msg = msg.lower()

        reply_type = 'passive'
        if active:
            reply_type = 'active'

        if channel:
            # Search the replies until we found one that matches
            for reply in self.replies[reply_type]:
                pattern = re.compile(reply['pattern'], re.IGNORECASE)
                if(pattern.match(msg)):
                    # If our response type is a custom function, attempt to execute it
                    # and return it's output as the response. Otherwise just return
                    # the response like normal.
                    if reply['action'] == 'random':
                        return self.get_random_reply(reply['response'])
                    if reply['action'] == 'function':
                        return self.get_function_reply(reply['response'], msg)
                    else:
                        return reply['response']

        # Return None if there was no message to reply to
        return None

    def get_random_reply(self, reply_list):
        """
        Returns a randomly selected reply from a given list
        """
        selection = randint(0, int(len(reply_list) - 1))
        return reply_list[selection]

    def get_function_reply(self, function_name, msg):
        """
        Makes sure that the intended function exists and is callable
        before returning it's output
        """
        reply_function = getattr(self, function_name, None)
        if reply_function and callable(reply_function):
            return reply_function(msg)

    def add_passive_reply(self, reply):
        """
        Add a reply to the passive reply list
        """
        if type(reply).__name__ != 'dict' or ('pattern' not in reply or 'response' not in reply):
            raise TypeError("add_passive_reply(): Takes requires a dict with `pattern`, `response`, and `action`(optional) attributes")

        # Save the reply
        new_reply = {
            'pattern': reply['pattern'],
            'response': reply['response'],
            'action': reply.get('action', 'message')
        }
        # Save the reply
        self.replies['passive'].append(new_reply)

    def add_active_reply(self, reply):
        """
        Add a reply to the acive reply list
        """
        if type(reply).__name__ != 'dict' or ('pattern' not in reply or 'response' not in reply):
            raise TypeError("add_active_reply(): Takes requires a dict with `pattern`, `response`, and `action`(optional) attributes")

        # Save the reply
        new_reply = {
            'pattern': reply['pattern'],
            'response': reply['response'],
            'action': reply.get('action', 'message')
        }
        self.replies['active'].append(new_reply)

    def add_replies(self, filepath):
        """
        Loads a set of replies from a dictionary
        """
        with open(filepath) as replies_file:
            replies = json.load(replies_file)
            for reply in replies:
                reply_type = reply.pop('type', None)
                if reply_type == 'passive':
                    self.add_passive_reply(reply)
                elif reply_type == 'active':
                    self.add_active_reply(reply)
