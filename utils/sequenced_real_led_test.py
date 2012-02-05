import time
from field_leds import *

for tower in ['low_blue', 'high_red', 'center', 'low_red', 'high_blue']:
    print '\nTower:', tower
    for level in TOWERS[tower]:
        print '\t Level:', level
        for color in ['red', 'green', 'blue']:
            set_light_output(tower, level, color)
            time.sleep(0.3)
        set_light_output(tower, level, 'off')
