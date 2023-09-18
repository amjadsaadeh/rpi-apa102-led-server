# rpi-apa102-led-server

This project is a simple server to control the leds of the [ReSpeaker 2-Mics Pi HAT](https://wiki.seeedstudio.com/ReSpeaker_2_Mics_Pi_HAT/) via a REST API.
It's basically a wrapper around the [apa102-pi package](https://github.com/tinue/apa102-pi/tree/main/apa102_pi) and is inspired by the [example script](https://github.com/respeaker/mic_hat/blob/master/interfaces/pixels.py) provided by ReSpeaker.

# installation

The only system dependencies are python 3.11 or later and [poetry](https://python-poetry.org/).
Typically I use [pyenv](https://github.com/pyenv/pyenv) to enable this on my raspberry pi zero.
The rest is done with the following lines:

```bash
$ git clone https://github.com/amjadsaadeh/rpi-apa102-led-server.git
$ cd rpi-apa102-led-server
$ poetry install
```

# run

After the installation the server can be started with gunicorn:

```bash
$ poetry run gunicorn -w 4 -b 0.0.0.0 'rpi_apa102_led_server.server:app'
```

# usage

The server exposes an `/led` endpoint for the `get` and `post` method.

## `get` method

Running a `get` request on `/led/<led_id>` returns the current state of the given led.

```bash
$ curl <server name>:8000/led/<led_id>
{"red": 0, "green": 0, "blue": 0, "brightness": 0, "bright_percent": 0.0}
```

## `post` method

Setting a LED color is done via the `post` method on `/led/<led_id>`

```bash
$ curl -H "Content-Type: application/json" -d '{"red": "50", "green": "50", "blue": "100", "bright_percent": "50"}' -X POST <server name>:8000/led/<led_id>
{"status": "ok"}
```

