#!/usr/bin/env python

import asyncio
import websockets
import json
import logging
import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))


def on_publish(client, userdata, mid):
    print("mid: "+str(mid))


def on_message(client, userdata, message):
    msg = message.payload.decode("utf-8")
    print('received message: {}'.format(msg))


def parse_json(input_json):
    json_content = json.loads(input_json)
    current_event = json_content["event"]
    if current_event == "noteCut" or current_event == "noteFullyCut":
        event_note_cut(json_content["noteCut"])
    elif current_event == "bombCut":
        event_bomb_cut()
    elif current_event == "beatmapEvent":
        event_beat_map(json_content["beatmapEvent"])
    else:
        print("other event: " + current_event)


def event_note_cut(note_cut_object):
    print("Note Cut")
    event_note_cut_parse(note_cut_object)


def event_note_cut_parse(note_cut_object):
    saber_type = note_cut_object["saberType"]
    note_type = note_cut_object["noteType"]
    light_value = 0
    if note_type == "NoteA":
        light_value = 7
    elif note_type == "NoteB":
        light_value = 3

    if saber_type == "SaberA":
        trigger_saber_a(light_value)
    elif saber_type == "SaberB":
        trigger_saber_b(light_value)


def trigger_saber_a(light_value):
    print("saber a: " + str(light_value))
    mqtt_publish_saber("saber/a", light_value)


def trigger_saber_b(light_value):
    print("saber b: " + str(light_value))
    mqtt_publish_saber("saber/b", light_value)


def mqtt_publish_saber(saber_type, light_value):
    publish_path = 'beatsaber/' + str(saber_type)
    client.publish(publish_path, light_value, qos=0, retain=True)


def event_bomb_cut():
    print("Bomb Cut")


def event_beat_map(event_object):
    # print("Beatmap")
    event_beat_map_parse(event_object)


def event_beat_map_parse(beatmap_event_object):
    type = beatmap_event_object["type"]
    value = beatmap_event_object["value"]
    if 0 < type < 5:
        if type == 0:
            trigger_light_small(value)
        elif type == 1:
            trigger_light_big(value)
        elif type == 2:
            trigger_light_left(value)
        elif type == 3:
            trigger_light_right(value)
        elif type == 4:
            trigger_light_center(value)


def mqtt_publish_light(light_type, light_value):
    publish_path = 'beatsaber/light/' + str(light_type)
    client.publish(publish_path, light_value, qos=0, retain=True)


def trigger_light_small(value):
    mqtt_publish_light(str('small'), str(value))
    print("light small " + str(value))


def trigger_light_big(value):
    mqtt_publish_light(str('big'), str(value))
    print("light big " + str(value))


def trigger_light_center(value):
    mqtt_publish_light(str('center'), str(value))
    print("light center " + str(value))


def trigger_light_left(value):
    mqtt_publish_light(str('left'), str(value))
    print("light left " + str(value))


def trigger_light_right(value):
    mqtt_publish_light(str('right'), str(value))
    print("light right " + str(value))


async def loop_websocket():
    async with websockets.connect('ws://localhost:6557/socket') as websocket:
        while True:
            result = await websocket.recv()
            # print(f"< {result}")
            parse_json(result)


if __name__ == '__main__':
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("10.42.0.244", 1883, 60)

    client.loop_start()

    asyncio.get_event_loop().run_until_complete(loop_websocket())
