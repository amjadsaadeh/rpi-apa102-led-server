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
    check_led_range(led_id)
    
    led_color = dev.get_pixel(led_id)
    return led_color

@app.post("/led/{led_id}")
async def set_led_color(led_id: int):
    check_led_range(led_id)
    # TODO SET COLOR
    led_color = dev.get_pixel(led_id)
    return led_color
    
# Helpers
def check_led_range(led_id: int) -> None:
    if led_id < 0 or led_id > NUM_LEDS:
        raise HTTPException(status_code=404, detail=f'LED with id {led_id} not found. It needs to be in the range betweeb 0 and {NUM_LEDS}.')
   