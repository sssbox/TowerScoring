from test_leds import *

for tower in ['low_blue', 'high_red', 'center', 'low_red', 'high_blue']:
    for level in LEDs[tower]:
        for led in ['red', 'green', 'blue']:
            run_command(LEDs[tower][level][led]+'0o')
