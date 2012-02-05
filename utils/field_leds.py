import serial

TOWERS = {
    'low_blue': { 'level_1': 0x10, },
    'high_red': { 'level_1': 0x20, 'level_2': 0x30, },
    'center': { 'level_1': 0x40, 'level_2': 0x50, },
    'low_red': { 'level_1': 0x60, },
    'high_blue': { 'level_1': 0x70, 'level_2': 0x80, },
}
COLORS = {
    'red': 0x08, 'green': 0x04, 'blue': 0x02, 'yellow': 0x0C,
    'cyan': 0x06, 'purple': 0x0A, 'white': 0x0E, 'off': 0x00
}

def set_light_output(tower, level, color):
    if tower not in TOWERS or level not in TOWERS[tower] or color not in COLORS:
        return
    output_char = chr(TOWERS[tower][level] | COLORS[color])
    ser = serial.Serial('/dev/ttyACM0', 2400)
    ser.write(output_char)
    ser.close()

def update_real_leds(tl):
    if not settings.REAL_LEDS:
        return
    set_light_output(tl.tower.name, 'level_' + str(tl.level), tl.state)
