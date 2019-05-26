
import audio_processing
import board
import time
import neopixel
import sys
import os

# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
pixel_pin = board.D18

# The number of NeoPixels
num_pixels = 121

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=1, auto_write=False,
                           pixel_order=ORDER)


def main():

    a = audio_processing.AudioProcessor(40)
    fps = audio_processing.FPS(30)
    while True:
        try:
            group = 0
            data = a.update()
            #a.print_bars()
            for index in range(len(data)):
                value = a.mapping(0, 20, 0, 255, data[index]['max_volume'])
                value_f = a.mapping(0, 20, 0, 255, data[index]['floating_max'])
                #for i in range(group, group + 11):
                #    pixels[i] = (0,int(value_f),int(value_f))
                
                mod = a.mapping(0, 120, 0, 1, index)
         
                pixels[int(a.mapping(0, 120, 120, 0, (index * 3) + 1))] = (int(value_f * mod), int(value), int(value_f))
                pixels[int(a.mapping(0, 120, 120, 0, index * 3))] = (int(value_f * mod), int(value), int(value_f))
                pixels[int(a.mapping(0, 120, 120, 0, (index * 3) - 1))] = (int(value_f * mod), int(value), int(value_f))
                # pixels[index] = (int(0), int(value_f), int(0))
                if index < 15:
                    print(index, data[index]['max_volume'],"\t",index * 2, data[index * 2]['max_volume'])
            pixels.show()
            fps.maintain()
            os.system('clear')
        except KeyboardInterrupt: 
            pixels.deinit()


if __name__ == "__main__":
    main()
