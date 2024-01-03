import os
import time
import tqdm
import rpa as r
import argparse

import pyautogui as gui

print('Configurando entorno ...')
pythondir = os.getcwd()
rpadir = pythondir + "\\rpa\\"
savedir = rpadir + 'results\\pixel_sprite_saver\\'

print('Configurando script ...')

parser = argparse.ArgumentParser()
parser.add_argument("--nframes", "-nf", type=int, required=True)
parser.add_argument("--scale", "-s", type=int, choices=[16, 8, 4, 3, 2, 1], required=True)
args = parser.parse_args()

scale = args.scale
nframes = args.nframes
frames = [str(i+1) for i in range(nframes)]

screen_width, screen_height = gui.size()
midpoint = (int(screen_width / 2), int(screen_height / 2))

first_frame_point = (120, 55)
frame_delta_x = 62

xpoints = {16:(1110, 660), 8:(1040, 660), 4:(972, 660), 3:(905, 660), 2:(838, 660)}

typepoints = {'png':(838, 730), 'gif':(905, 730)}

namepoint = (838, 800)
savepoint = (838, 870)
dirpoint = (1600, 55)

print('Trabajando con una pantalla de:', screen_width, 'x', screen_height)

print('Inicializando RPA ...')
os.chdir(rpadir)
r.init(visual_automation=True, chrome_browser = False)
os.chdir(pythondir)

print('Ejecutando RPA ...')
point = midpoint
r.hover(point[0], point[1])

print('Buscando pixel studio ...')
r.keyboard('[win]')
r.wait(0.5)
r.keyboard('pixel[space]studio')
r.wait(1)
r.keyboard('[enter]')
r.wait(8)

print('Posicionando mouse ...')

for i in range(nframes):
  
    f = frames[i]

    point = first_frame_point
    r.click(point[0] + frame_delta_x * i, point[1])

    r.keyboard('[ctrl]s')

    # asignar escala
    if scale != 1:
        point = xpoints[scale]
        r.click(point[0], point[1])

    # asignar tipo png
    point = typepoints['png']
    r.click(point[0], point[1])
    
    # asignar nombre
    point = namepoint
    r.click(point[0], point[1])
    r.keyboard(f + '[enter]')

    # guardar frame
    point = savepoint
    r.click(point[0], point[1])

    # cambiar directorio
    if i == 0:
        r.keyboard('[tab]' * 6 + '[enter]')
        r.keyboard(savedir + '[enter]')
        r.keyboard('[tab]' * 8 + '[enter]')
    else:
        r.keyboard('[enter]')                       

    r.wait(0.5)

# # guardar gif
# point = first_frame_point
# r.click(point[0], point[1])

# r.keyboard('[ctrl]s')

# point = typepoints['gif']
# r.click(point[0], point[1])

# point = namepoint
# r.click(point[0], point[1])
# r.keyboard('anim_x' + str(scale) + '[enter]')

# point = savepoint
# r.click(point[0], point[1])

# r.keyboard('[enter]')


r.close()


