ZERO_STR = """
 ## 
#  #
#  #
#  #
 ##
"""

ONE_STR = """
  #
 ##
  #
  #
 ###
"""

TWO_STR = """
###
   #
 ##
#
####
"""

THREE_STR = """
###
   #
 ##
   #
###
"""

FOUR_STR = """
  #
 #
#  #
####
   #
"""

FIVE_STR = """
####
#
####
   #
###
"""

SIX_STR = """
 ###
#
####
#  #
 ##
"""

SEVEN_STR = """
####
   #
  #
 #
 #
"""

EIGHT_STR = """
 ## 
#  #
 ##
#  #
 ##
"""

NINE_STR = """
####
#  #
 ###
   #
###
"""

def str_to_grid(s):
  grid = []
  for line in s.split('\n'):  
    if not line:
      continue
    row = [3 if ch == '#' else 0 for ch in line ]
    while (len(row) < 4):
      row.append(0)
    assert(len(row) == 4)
    grid.append(row)
  assert(len(grid) == 5)
  return grid

digit_grids = [
  str_to_grid(ZERO_STR),
  str_to_grid(ONE_STR),
  str_to_grid(TWO_STR),
  str_to_grid(THREE_STR),
  str_to_grid(FOUR_STR),
  str_to_grid(FIVE_STR),
  str_to_grid(SIX_STR),
  str_to_grid(SEVEN_STR),
  str_to_grid(EIGHT_STR),
  str_to_grid(NINE_STR),
]


    
