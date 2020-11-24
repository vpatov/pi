import enum

# if raspberry pi can stream 4k through hdmi.... up to two 4k hdmi streams...
# we can make a smart TV out of it??

class Action(enum):
  TELL_JOKE = 1
  PLAY_RIFF = 2
  SAY_WEATHER = 3
  SAY_UPTIME = 4
  PLAY_YOUTUBE = 5
  ORDER_MYRTLE_THAI = 6
  SAY_TEMPERATURE_IN_ROOM = 7
  
## TODO 
"""
1) Probably subdivide actions into further categories i.e. SAY <ARG>, PLAY YOUTUBE <CATEGORY>
2) Write code in receiver server that uses a rolling code and converts a group of RF codes into a remote code
"""


REMOTE_CODE_ACTION_MAP = {
  122: Action.TELL_JOKE,
  776: Action.PLAY_RIFF
}

class Action:
  def __init__(self):
    pass

  def execute_action(self, remote_code):
    pass