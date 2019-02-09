import time
import board


class TestNeopixel:
    @staticmethod
    def name():
        return 'Test Neopixel LED'

    def run(self):
        # For Trinket M0, Gemma M0, ItsyBitsy M0 Express and ItsyBitsy M4 Express
        # import adafruit_dotstar
        # led = adafruit_dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 1)
        # For Feather M0 Express, Metro M0 Express, Metro M4 Express and Circuit Playground Express
        import neopixel
        led = neopixel.NeoPixel(board.NEOPIXEL, 1)

        def wheel(pos):
            # Input a value 0 to 255 to get a color value.
            # The colours are a transition r - g - b - back to r.
            if pos < 0 or pos > 255:
                return 0, 0, 0
            if pos < 85:
                return int(255 - pos * 3), int(pos * 3), 0
            if pos < 170:
                pos -= 85
                return 0, int(255 - pos * 3), int(pos * 3)
            pos -= 170
            return int(pos * 3), 0, int(255 - (pos * 3))

        led.brightness = 0.3

        for i in range(0, 255):
            led.fill(wheel(i % 256)) # run from 0 to 255
            time.sleep(0.1)


class TestDigitalPort:
    @staticmethod
    def name():
        return 'Test digital I/O ports'

    def run(self):
        import digitalio
        leds = [
            digitalio.DigitalInOut(board.A0),
            digitalio.DigitalInOut(board.A1),
            digitalio.DigitalInOut(board.A2),
            digitalio.DigitalInOut(board.A3),
            digitalio.DigitalInOut(board.A4),
            digitalio.DigitalInOut(board.A5),
            digitalio.DigitalInOut(board.D2),
            digitalio.DigitalInOut(board.D5),
            digitalio.DigitalInOut(board.D6),
            digitalio.DigitalInOut(board.D9),
            digitalio.DigitalInOut(board.D10),
            digitalio.DigitalInOut(board.D11),
            digitalio.DigitalInOut(board.D12),
            digitalio.DigitalInOut(board.D13),
            digitalio.DigitalInOut(board.SCK),
            digitalio.DigitalInOut(board.MOSI),
            digitalio.DigitalInOut(board.MISO),
            digitalio.DigitalInOut(board.RX),
            digitalio.DigitalInOut(board.TX),
            digitalio.DigitalInOut(board.SDA),
            digitalio.DigitalInOut(board.SCL),
            digitalio.DigitalInOut(board.SWITCH),
            digitalio.DigitalInOut(board.RED_LED),
            digitalio.DigitalInOut(board.BLUE_LED),
            ]

        for i in range(0, len(leds)):
            leds[i].direction = digitalio.Direction.OUTPUT
        for i in range(0, len(leds)):
            leds[i].value = False

        for i in range(0, len(leds)):
            leds[i].value = True
            time.sleep(0.2)

        for i in range(0, len(leds)):
            leds[i].value = False
        for i in range(0, len(leds)):
            leds[i].direction = digitalio.Direction.INPUT


class TestI2C:
    @staticmethod
    def name():
        return 'Test I2C bus'

    def run(self):
        import busio

        i2c = busio.I2C(board.SCL, board.SDA)
        while not i2c.try_lock():
             pass
        print('scanning in I2C bus...')
        try:
            addrs = [hex(x) for x in i2c.scan()]
        finally:
            i2c.unlock()
        print(addrs)

#
#  main
#
tests = [
    TestNeopixel,
    TestDigitalPort,
    TestI2C,
]
cmd = None
while cmd is None:
    try:
        print()
        print('Select:')
        for i in range(0, len(tests)):
            print('  %d. %s' % (i, tests[i].name()))
        print('  %d. exit' % len(tests))
        cmd = int(input('Please type a number: '))
        if cmd < 0 or len(tests) < cmd:
            cmd = None
    except Exception as ex:
        pass

if cmd < len(tests):
    print('Run %s...' % tests[cmd].name())
    tests[cmd]().run()
