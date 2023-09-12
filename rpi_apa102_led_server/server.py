from typing import Annotated

from fastapi import FastAPI, HTTPException, Path
from apa102_pi.driver import apa102
from pydantic import BaseModel, Field

NUM_LEDS = 3

app = FastAPI()

dev = apa102.APA102(num_led=NUM_LEDS)


class Color(BaseModel):
    red: int = Field(default=None, title="red part of rgb", ge=0, le=255)
    green: int = Field(default=None, title="green part of rgb", ge=0, le=255)
    blue: int = Field(default=None, title="blue part of rgb", ge=0, le=255)
    bright_percent: float = Field(
        default=None, title="brightness in percent", ge=0, le=100
    )


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/led/{led_id}")
async def get_led_color(led_id: Annotated[int, Path(title="ID of the led")]) -> dict:
    check_led_range(led_id)

    led_color = dev.get_pixel(led_id)
    return led_color


@app.post("/led/{led_id}")
async def set_led_color(
    led_id: Annotated[int, Path(title="ID of the led")],
    color: Annotated[Color, Body(embed=True)],
) -> dict:
    check_led_range(led_id)

    dev.set_pixel(
        led_id, color.red, color.green, color.blue, bright_percent=color.bright_percent
    )

    return {"status": "ok"}


# Helpers
def check_led_range(led_id: int) -> None:
    if led_id < 0 or led_id > NUM_LEDS:
        raise HTTPException(
            status_code=404,
            detail=f"LED with id {led_id} not found. It needs to be in the range betweeb 0 and {NUM_LEDS}.",
        )
