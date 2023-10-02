import os
import glob
from osgeo import osr, gdal

def convert_asc2tif(wdir:str, fout:str='out.tif', onlyonefile=True):
    """
    Conversion de tous les fichiers .ASC dans un répertoire en un fichier .tif unique (onlyonefile==True)
    ou
    Conversion de tous les fichiers .ASC dans un répertoire en autant de fichier .tif (ajout pur et simple de l'extension .tif au nom de fichier)
    """
    curdir = os.getcwd()
    os.chdir(wdir)

    if onlyonefile:
        gdal.BuildVRT(os.path.join(wdir,fout+'.vrt') , glob.glob(os.path.join(wdir,'*.asc')))
        gdal.Translate(fout, fout+'.vrt')
    else:
        ascfiles = glob.glob(os.path.join(wdir,'*.asc'))
        for curfile in ascfiles:
            gdal.Translate(curfile+'.tif', curfile)

    os.chdir(curdir)

if __name__=='__main__':
    # convert_asc2tif(r'D:\OneDrive\OneDrive - Universite de Liege\Crues\2021-07 Vesdre\CSC - Convention - ARNE\Data\2023\MNT_50cm', onlyonefile=False)
    # convert_asc2tif(r'D:\OneDrive\OneDrive - Universite de Liege\Crues\2021-07 Vesdre\CSC - Convention - ARNE\Data\2023\MNS_50cm', onlyonefile=False)
    # convert_asc2tif(r'D:\OneDrive\OneDrive - Universite de Liege\Crues\2021-07 Vesdre\CSC - Convention - ARNE\Data\2023\MNC_50cm', onlyonefile=False)
    convert_asc2tif(r'D:\OneDrive\OneDrive - Universite de Liege\Crues\2021-07 Vesdre\CSC - Convention - ARNE\Data\2023\v2_reprise\MNT_Bati+Muret', onlyonefile=False)