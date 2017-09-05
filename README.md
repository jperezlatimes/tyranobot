TyranoBot
===================
![Python versions](https://img.shields.io/badge/python-2.7-blue.svg)

An easily customizable Slackbot built on the SlackClient python library.

Installation
------------
Install the TyranoBot module from [Pypi](https://pypi.python.org/pypi/TyranoBot)
```bash
pip install TyranoBot
```

Usage
-------
TyranoBot can be started very simply by just providing a bot_token, and bot_id:

```python
from tyranobot import TyranoBot

# Initialize the bot
MyBot = TyranoBot({
    'bot_token': 'xoxb-a-bot-token-from-slack',
    'bot_id': 'TESTING'
})

# Add a reply
MyBot.add_passive_reply({
    'pattern': 'hello',
    'response': 'hi there',
    'action': 'message'
})

# Start the bot
MyBot.start()
```

TyranoBot really shines when it's extended and customized. By adding different reply types TyranoBot can reply in different ways:
```python
import re
from random import randint
from tyranobot import TyranoBot

class MyBot(TyranoBot):

  def __init__(self, bot_data, *args, **kwargs):
      # Call TroncBot's initialization function
      TyranoBot.__init__(self, bot_data, *args, **kwargs)

      # Add a passive message reply
      self.add_passive_reply({
        'pattern': 'hello',
        'response': 'hi there',
        'action': 'message'
      })

      # Add an active random reply
      self.add_active_reply({
        "pattern": "tell\s*(me)*\s*a*\s*joke",
        "response": [
          "https://www.youtube.com/watch?v=kTcRRaXV-fg",
          "https://www.youtube.com/watch?v=Mdqv5xIsFLM",
          "Q: Where do orcas hear music? A: Orca-stras!",
          "Q: What do you call a blind dinosaur? A: Do-you-think-he-saurus"
        ],
        "action": "random"
      })

      # Add an active function reply
      self.add_active_reply(
        "type": "active",
        "pattern": "(?:R|roll\\s)*([1-9]*)(d|D)([1-9].*)",
        "response": "roll_dice",
        "action": "function"
      })

  def roll_dice(self, msg):
      """
      This is an example of a function response. When MyBot hears @MyBot Roll X dY,
      MyBot will roll X number of Y sided dice and send the result back as a Slack message.
      """
      dice = re.match(r"(?:R|roll\s)*([1-9]*)(d|D)([1-9].*)", msg)

      num_rolls = 1
      sides = dice.group(3)
      reply = ""

      # Make sure the dice has a correct number of sides
      if sides in ['4', '6', '8', '10', '20']:
          reply = ":game_die: You rolled: "
          total = 0
          # How many dice should we roll?
          if dice.group(1) and dice.group(1) != '':
              num_rolls = int(dice.group(1))

          # Roll as many dice as indicated, recording each result in reply
          this_roll = 1
          while (this_roll <= num_rolls):
              roll = randint(1, int(sides))
              total = total + roll
              reply = reply + str(roll) + ', '
              this_roll = this_roll + 1

          # Stri the last comman and add the total roll to the end o the reply
          reply = reply.strip(', ')
          reply = reply + ". Total roll: " + str(total)
      else:
          reply = "I don't have a dice like that"

      return reply

# Gather the bot data
MyBot = TyranoBot({
    'bot_token': 'xoxb-a-bot-token-from-slack',
    'bot_id': 'TESTING'
})

# Start the bot
MyBot.start()
```

Reply Objects
-------
TyranoBot responds to messages via a list of reply objects. A reply object is a dictionary with the following structure:
```python
{
  "type": "passive|active",
  "pattern": "(.*?)a regex pattern(.*?)",
  "response": "string|array|callable",
  "action": "message|random|function"
}
```

Key       | Value
--------- | -------------
`type`    | The type of reply this is. Expected values are "passive" or "active". See Reply Types below for details.
`pattern` | A regular expression string that TyranoBot should use to identify messages it should respond to. TyranoBot automatically converts incoming messages to lowercase to make regex matching simpler.
`response`| TyranoBot's response to any messages that match the `pattern`. Can be a string, list(array), or the name of a callable function depending on the value of  `action`.
`action`  | The action that TyranoBot is making to reply. Expected values are "message", "random", or "function". See Reply Actions below for more details.


Reply Types
-------
TyranoBot has two reply types:

**Passive:** Passive replies are replies TyranoBot can use to reply to any incidental chatter in whatever channel(s) it has been invited too.

**Active:** Active replies are replies that TyranoBot can use to reply to targeted @<your-bot-name> messages.


Reply Actions
-------
**Message:** A simple message reply. TyranoBot will reply to the received message with a simple string message.

**Random:** TyranoBot will reply to the received message by randomly selecting one of a list of possible replies

**Function (Advanced):** TyranoBot will reply to the received message with the output of the named function. TyranoBot will pass the received message as arguments to the named function for processing.

TyranoBot has support for Slack message attachments in it's responses. If the final `response` from a reply object is a dictionary, TyranoBot will assume that it is a [Slack message object](https://api.slack.com/docs/messages) and will send the whole dict as a POST request to the channel that TyranoBot was originally messaged from.


Adding Replies
-------
TyranoBot has 3 options for adding replies to it's repotoire.

`add_passive_reply(reply dict)`: Adds a single passive reply to TyranoBot's list. The `type` key can be omitted from the passed reply dict.

`add_active_reply(reply dict)`: Adds a single active reply to TyranoBot's list. The `type` key can be omitted from the passed reply dict.

`add_replies(reply list)`: Adds a list of replies to TyranoBot. Most useful during the initializatio process. Accepts a list(array) of reply dicts as an argument. Can even be used to load a list of replies from an external file. The the replies for the MyBot example above can be listed in a `json` file:

```json
[
    {
      "type": "passive",
      "pattern": "h[ello|i].*mybot.*",
      "response": "Hello human!",
      "action": "message"
    },
    {
      "type": "active",
      "pattern": "tell\s*(me)*\s*a*\s*joke",
      "response": [
        "https://www.youtube.com/watch?v=kTcRRaXV-fg",
        "https://www.youtube.com/watch?v=Mdqv5xIsFLM",
        "Q: Where do orcas hear music? A: Orca-stras!",
        "Q: What do you call a blind dinosaur? A: Do-you-think-he-saurus"
      ],
      "action": "random"
    },
    {
      "type": "active",
      "pattern": "(?:R|roll\\s)*([1-9]*)(d|D)([1-9].*)",
      "response": "roll_dice",
      "action": "function"
    }
]
```

And then loaded into your instance of TyranoBot at initialization:
```python
import os
import re
from random import randint
from tyranobot import TyranoBot

class MyBot(TyranoBot):

  def __init__(self, bot_data, *args, **kwargs):
      # Call TroncBot's initialization function
      TyranoBot.__init__(self, bot_data, *args, **kwargs)

      # Load list of replies from a json file
      filepath = os.path.dirname(os.path.realpath(__file__)) + "/replies.json"
      self.add_replies(filepath)

  def roll_dice(self, msg):
      """
      This is an example of a function response. When MyBot hears @MyBot Roll X dY,
      MyBot will roll X number of Y sided dice and send the result back as a Slack message.
      """
        ...
```

This can help to keep the code for your TyranoBot instance as clean as possible.
