from apa102_pi.driver import apa102
from flask import Flask, abort, request, jsonify
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)


class LEDDevice(Resource):
    NUM_LEDS = 3
    dev = apa102.APA102(num_led=NUM_LEDS, global_brightness=31)

    def get(self, led_id: int) -> dict:
        check_led_range(led_id)

        led_color = self.dev.get_pixel(led_id)
        return led_color

    def post(self, led_id: int) -> dict:
        check_led_range(led_id)
        parser = reqparse.RequestParser()
        parser.add_argument("red", type=int, required=True, help="red cannot be blank")
        parser.add_argument(
            "blue", type=int, required=True, help="blue cannot be blank"
        )
        parser.add_argument(
            "green", type=int, required=True, help="green cannot be blank"
        )
        parser.add_argument(
            "bright_percent",
            type=float,
            required=True,
            help="bright_percent cannot be blank",
        )
        color = parser.parse_args()
        self.dev.set_pixel(
            led_id,
            color["red"],
            color["green"],
            color["blue"],
            bright_percent=color["bright_percent"],
        )
        self.dev.show()
        return {"status": "ok"}

    def delete(self, led_id: int) -> dict:
        self.dev.set_pixel(led_id, 0, 0, 0, bright_percent=0)
        self.dev.show()
        return {"status": "ok"}


api.add_resource(LEDDevice, "/led/<int:led_id>")


# Helpers
def check_led_range(led_id: int) -> None:
    if led_id < 0 or led_id >= LEDDevice.NUM_LEDS:
        abort(
            404,
            description=f"LED with id {led_id} not found. It needs to be in the range betweeb 0 and {LEDDevice.NUM_LEDS}.",
        )


if __name__ == "__main__":
    app.run(debug=True)
