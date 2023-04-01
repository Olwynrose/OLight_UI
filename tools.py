import random

def rgb2hex(r,g,b):
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)

def hex2rgb(color):
  rgb = []
  for i in (1, 3, 5):
    decimal = int(color[i:i+2], 16)
    rgb.append(decimal)
  return tuple(rgb)

def randomRGBColor():
    return rgb2hex(random.randint(0,255),random.randint(0,255),random.randint(0,255))

def darkenColor(color, att):
   r,g,b = hex2rgb(color)
   newColor = rgb2hex(round(att*r), round(att*g),round(att*b))
   return newColor
