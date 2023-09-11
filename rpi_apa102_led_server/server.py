from fastapi import FastAPI, HTTPException
from apa102_pi.driver import apa102

NUM_LEDS = 3

app = FastAPI()

dev = apa102.APA102(num_led=NUM_LEDS)

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/led/{led_id}")
async def get_led_color(led_id: int):
    if led_id < 0 or led_id > NUM_LEDS:
        raise HTTPException(status_code=404, detail=f'LED with id {led_id} not found. It needs to be in the range betweeb 0 and {NUM_LEDS}.')

    led_color = dev.get_pixel(led_id)
    return 
    