from apa102_pi.driver import apa102
from flask import Flask, abort, request, jsonify
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


class LEDDevice(Resource):
    NUM_LEDS = 3
    dev = apa102.APA102(num_led=NUM_LEDS)

    def get(self, led_id: int) -> dict:
        check_led_range(led_id)

        led_color = dev.get_pixel(led_id)
        return led_color

    def post(self, led_id: int) -> dict:
        check_led_range(led_id)
        color = request.form["data"]
        dev.set_pixel(
            led_id,
            color["red"],
            color["green"],
            color["blue"],
            bright_percent=color["bright_percent"],
        )

        return {"status": "ok"}


api.add_resource(LEDDevice, "/led/<int:led_id>")


# Helpers
def check_led_range(led_id: int) -> None:
    if led_id < 0 or led_id > LEDDevice.NUM_LEDS:
        abort(
            404,
            description=f"LED with id {led_id} not found. It needs to be in the range betweeb 0 and {NUM_LEDS}.",
        )


if __name__ == "__main__":
    app.run(debug=True)
