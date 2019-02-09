import sys
import alexandra
import click
import pychromecast
from flask_ask import Ask, statement, question, session
from flask import Flask, render_template

app = Flask(__name__)
ask = Ask(app, '/')
cast = None
device_name = None

@ask.launch
def server():
    global cast
    global device_name

    print('>> trying to connect to {}'.format(device_name))

    device_name = device_name    
    #cast = pychromecast.get_chromecasts(friendly_name=device)
    cast = pychromecast.get_chromecasts()[0]
    if cast is None:
        return statement("Couldn't find device '{}'".format(device_name))


@ask.intent('Reconnect')
def reconnect():
    global cast

    #cast = pychromecast.get_chromecast(friendly_name=device_name)
    cast = pychromecast.get_chromecasts()
    if cast is None:
        return statement(
            'Failed to connect to Chromecast named %s.' % device_name)

    return statement('Reconnected device.')


@ask.intent('SkipMedia')
def skip_media():
    mc = cast.media_controller

    if not mc.status.supports_skip_forward:
        return statement("Skipping not supported")

    mc.skip()
    return statement("") # Should do the job quietly here


@ask.intent('PlayMedia')
def play_media(slots, session):
    mc = cast.media_controller

    if mc.status.player_is_playing:
        return statement("Already playing")

    mc.play()
    return statement("") # Talking after the media starts is dumb


@ask.intent('PauseMedia')
def pause_media():
    mc = cast.media_controller

    if not mc.status.player_is_playing:
        return statement("Already paused")

    mc.pause()
    return statement("") # When it pauses, you will know.


@ask.intent('Reboot')
def reboot():
    cast.reboot()
    return statement("") # Unless you are blinded by too much TV


if __name__ == '__main__':
    server()