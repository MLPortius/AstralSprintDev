#%% IMPORTAR LIBRERIAS
import os
import tqdm
import shutil
import argparse


#%% CONFIGURAR SCRIPT

parser = argparse.ArgumentParser()
parser.add_argument("--path", "-p", type=str, required=True)
parser.add_argument("--animid", "-a", type=str, required=True)
parser.add_argument("--extension", "-e", type=str, default='.png', required=True)
args = parser.parse_args()

route = args.path
animid = args.animid
extension = args.extension


#%% DEFINIR FUNCIONES AUXILIARES

def fix_len(x, lm):
    xl = len(str(x))
    if xl < lm:
        y = '0' * (lm - xl) + str(x)
    else:
        y = str(x)
    return y


#%% DEFINIR FUNCIONES MODULO PRINCIPAL

def change_workdir():
    startfolder = os.getcwd()

    basename = 'AstralSprint'
    basefolder = startfolder.split(basename)[0] + basename

    print('Cambiando direccion desde:', startfolder, 'a', basefolder)
    os.chdir(basefolder)

    print('\nDireccion actual: ', os.getcwd())


def define_infolder(route):
    
    infolder = route

    if infolder[-1] != '/':
        infolder = infolder + '/'

    if not os.path.exists(infolder):
        print('Error: Folder does not exist ...', infolder)
        return 'error'
    
    else:
        return infolder
    

def define_outfolder(infolder):

    outfolder = infolder + 'del/'

    if not os.path.exists(outfolder):
        os.mkdir(outfolder)
    else:
        files = os.listdir(outfolder)
        for x in files:
            os.remove(outfolder + x)

    return outfolder

def read_input_files(infol, oufol, ext, anid):

    files = os.listdir(infol)
    files = [x for x in files if x.endswith(ext)]
    files = [x for x in files if not x.startswith(anid)]

    print('Loaded files:', len(files))

    nums = [int(x.split(ext)[0]) for x in files]
    nmax = str(max(nums))
    lmax = len(nmax)

    nums = [str(x) for x in nums]
    nums_fix = [fix_len(x, lm = lmax) for x in nums]

    files_original = [x + ext for x in nums]
    files_fixed = [x + ext for x in nums_fix]

    files_anim = [anid + '_' + x for x in files_fixed]

    infiles = [infol + x for x in files_original]
    outfiles = [infol + x for x in files_anim]
    delfiles = [oufol + x for x in files_original]

    print('Original:', infiles[0])
    print('Fixed:', outfiles[0])
    print('Delete:', delfiles[0])

    return infiles, outfiles, delfiles

def backup_files(inlist, dellist):
    for i in tqdm.tqdm(range(len(inlist))):
        origen = inlist[i]
        destino = dellist[i]
        shutil.copyfile(origen, destino)

def change_names(inlist, outlist):
    for i in tqdm.tqdm(range(len(inlist))):
        origen = inlist[i]
        destino = outlist[i]
        os.rename(origen, destino)

#%% DEFINIR MODULO PRINCIPAL

def __main__(r, a, e):
    
    print('\n\nCHANGING WORKDIR...','\n')
    change_workdir()

    print('\n\nDEFINING INFOLDER...','\n')
    infolder = define_infolder(r)
    if infolder == 'error':
        exit()

    print('\n\nDEFINING OUTFOLDER...','\n')
    outfolder = define_outfolder(infolder)

    print('\n\nREADING INPUT FILES...','\n')
    inpfi, outfi, delfi = read_input_files(infol = infolder, oufol = outfolder, ext = e, anid = a)

    print('\n\nBACKING UP INPUT FILES...','\n')
    backup_files(inlist = inpfi, dellist = delfi)

    print('\n\nCHANGING NAMES...','\n')
    change_names(inlist = inpfi, outlist = outfi)

#%% EJECUTAR MODULO PRINCIPAL

if __name__ == "__main__":
    __main__(r=route, a=animid, e=extension)