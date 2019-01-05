# BeatSaberMqttProxy
This is a simple websocket to mqtt proxy for Beat Saber that uses the [Beat Saber HTTP Status plugin](https://github.com/opl-/beatsaber-http-status).

## Dependencies
* Python ≥ 3.6 (because of Websockets)
* [WebSockets - WebSocket implementation in Python 3](https://github.com/aaugustin/websockets)
* [Eclipse Paho™ MQTT Python Client](https://github.com/eclipse/paho.mqtt.python)
* [Beat Saber HTTP Status plugin](https://github.com/opl-/beatsaber-http-status)

## Manual
* Clone / Download the Repo
  * ```git clone https://github.com/Elektrospy/BeatSaberMqttProxy.git```
* Install requirement python packages
  * ```pip3 install -r requirements.txt```
* Make sure that Beat Saber is running.
* Start the Proxy Script
  * ```python3 ./BeatSaberMqttProxy.py```

## Mqtt Messages
Currently the Proxy does only publish the following (lighting) events:
* Topics:
  * beatsaber/light/small
  * beatsaber/light/big
  * beatsaber/light/center
  * beatsaber/light/left
  * beatsaber/light/right
  * beatsaber/saber/a
  * beatsaber/saber/b
* Payload:
  * Based on the events values from the Steam Community Modding Guide:
    * [Beat Saber Modding Guide](https://steamcommunity.com/sharedfiles/filedetails/?id=1377190061)
  * 0: Off
  * 1-2: blue
  * 3: blue + fade out
  * 4: unused?
  * 5-6: red
  * 7: red _ fade out

## Credits
**[opl-](https://github.com/opl)** for the [Beat Saber HTTP Status plugin](https://github.com/opl-/beatsaber-http-status), on which this proxy is based.
