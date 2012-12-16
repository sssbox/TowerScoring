import time
from test_leds import *

for tower in ['low_blue', 'high_red', 'center', 'low_red', 'high_blue']:
    print '\nTower:', tower
    for level in LEDs[tower]:
        print '\t Level:', level
        for led in ['red', 'green', 'blue']:
            run_command(LEDs[tower][level][led]+'1o')
            time.sleep(0.3)
            run_command(LEDs[tower][level][led]+'0o')
