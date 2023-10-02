import os
import glob
from osgeo import osr, gdal
import logging

def create_vrt(wdir:str, fout:str='out.vrt', format:str='tif'):
    """
    Agglomération de tous les fichiers .tif dans un layer virtuel .vrt
    """
    curdir = os.getcwd()
    os.chdir(wdir)

    if not fout.endswith('.vrt'):
        fout+='.vrt'

    gdal.BuildVRT(os.path.join(wdir,fout) , glob.glob(os.path.join(wdir,'*.'+format)))

    os.chdir(curdir)

def crop_vrt(fn:str, crop:list, fout:str=None):
    """
    Crop vrt file

    Args:
        fn (str): '.vrt' file to crop
        crop (list): Bounds [[xmin, xmax], [ymin,ymax]] aka [[xLL, xUR], [yLL,yUR]]
        fout (str, optional): '.tif' file out. Defaults to None --> fn+'_crop.tif'
    """
    if os.path.exists(fn):

        if not fn.endswith('.vrt'):
            logging.warning('Bad file -- not .vrt extension !')
            return

        [xmin, xmax], [ymin, ymax] = crop

        if fout is None:
            fout = fn +'_crop.tif'

        if not fout.endswith('.tif'):
            fout+='.tif'

        gdal.Translate(fout, fn, projWin=[xmin, ymax, xmax, ymin])

    else:
        logging.warning('The file does not exist !')


if __name__=='__main__':
    #create_vrt(r'D:\OneDrive\OneDrive - Universite de Liege\Crues\2021-07 Vesdre\CSC - Convention - ARNE\Data\2023\GeoTif\encours\MNT_Bati+Muret_50cm', fout='AllData_MNT_BatiMuret.vrt')
    crop_vrt(r'D:\OneDrive\OneDrive - Universite de Liege\Crues\2021-07 Vesdre\CSC - Convention - ARNE\Data\2023\GeoTif\encours\MNT_Bati+Muret_50cm\AllData_MNT_BatiMuret.vrt', [[251000,254000],[135500,140000]])