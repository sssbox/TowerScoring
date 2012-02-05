import subprocess
from django.conf import settings
media_location = settings.STATIC_ROOT + 'sfx/'
SOUNDS = {
    'start': 'start.wav',
    'abort': 'start.wav',
    'reset': 'start.wav',
    'end': 'start.wav',
}

def play_sound(sound):
    if sound not in SOUNDS:
        print 'Unknown sound'
        return
    subprocess.Popen(['/usr/bin/mplayer '+media_location+SOUNDS[sound]], \
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
