from django.conf import settings
import subprocess

LEDs = {
    'low_blue': {
        'level_1': {
            'red'  : '5d',
            'green': '3d',
            'blue' : '4d',
        },
    },
    'high_red': {
        'level_1': {
            'red'  : '1b',
            'green': '3b',
            'blue' : '2b',
        },
        'level_2': {
            'red'  : '4b',
            'green': '6b',
            'blue' : '5b',
        },
    },
    'center': {
        'level_1': {
            'red'  : '1c',
            'green': '1e',
            'blue' : '0c',
        },
        'level_2': {
            'red'  : '6e',
            'green': '0b',
            'blue' : '7e',
        },
    },
    'low_red': {
        'level_1': {
            'red'  : '7c',
            'green': '5c',
            'blue' : '6c',
        },
    },
    'high_blue': {
        'level_1': {
            'red'  : '7f',
            'green': '5f',
            'blue' : '6f',
        },
        'level_2': {
            'red'  : '4f',
            'green': '2f',
            'blue' : '3f',
        },
    },
}

def turn_off_tl(tl):
    command = ''
    for color in LEDs[tl.tower.name]['level_'+str(tl.level)]:
        command += LEDs[tl.tower.name]['level_'+str(tl.level)][color] + '0o '
    return command

def turn_on_color(tl):
    return LEDs[tl.tower.name]['level_'+str(tl.level)][tl.state] + '1o '

def turn_off_color(tl):
    return LEDs[tl.tower.name]['level_'+str(tl.level)][tl.state] + '0o '

# Txtzyme
# http://dorkbotpdx.org/blog/wardcunningham/shell_programming_with_txtzyme
# https://github.com/WardCunningham/Txtzyme
def run_command(command):
    subprocess.Popen(['echo "'+command+'" >/dev/ttyACM0'], stdout=subprocess.PIPE, shell=True)

def update_test_led(tl):
    if settings.DEBUG_LEDS == False:
        return
    command = ''
    if tl.state == 'off':
        command += turn_off_tl(tl)
    elif tl.state == 'purple':
        tl.state = 'green'
        command += turn_off_color(tl)
        tl.state = 'red'
        command += turn_on_color(tl)
        tl.state = 'blue'
        command += turn_on_color(tl)
    else:
        command += turn_off_tl(tl)
        command += turn_on_color(tl)
    if command:
        run_command(command)
