from field_leds import *

for tower in ['low_blue', 'high_red', 'center', 'low_red', 'high_blue']:
    for level in TOWERS[tower]:
        set_light_output(tower, level, 'off')
