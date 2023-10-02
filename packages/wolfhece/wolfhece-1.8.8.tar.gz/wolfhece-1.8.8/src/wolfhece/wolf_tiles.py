
import glob
from os.path import join, exists
from os import remove
from osgeo import gdal
import logging

from .PyTranslate import _
from .wolf_array import WolfArray, WolfArrayMB
from .PyVertexvectors import zone,Zones,vector


class Tiles(Zones):

    def __init__(self, filename='', ox: float = 0, oy: float = 0, tx: float = 0, ty: float = 0, parent=None, is2D=True, idx: str = '', plotted: bool = True, mapviewer=None, need_for_wx: bool = False, linked_data_dir=None) -> None:
        super().__init__(filename, ox, oy, tx, ty, parent, is2D, idx, plotted, mapviewer, need_for_wx)

        self.linked_data_dir  = linked_data_dir
        self.linked_data_dir_comp = linked_data_dir

        self.loaded_tiles = []

    def set_comp_dir(self, comp_dir:str):

        if (comp_dir is not None):
            if len(comp_dir.strip())>0:
                self.linked_data_dir_comp = comp_dir.strip()

    def get_array(self, boundvector:vector = None, forceupdate = True):

        retarray=None
        bbox = boundvector.get_bounds()
        boundname = boundvector.myname
        comp = None
        src = None

        if self.linked_data_dir == self.linked_data_dir_comp:
            # pas de comparaison car répertoire source et comp identique

            file = glob.glob(join(self.linked_data_dir,'*{}*.tif').format(boundname))

            if len(file)>0:
                if not file[0] in self.loaded_tiles or forceupdate:
                    retarray = WolfArray(fname=file[0], mapviewer=self.mapviewer, idx=boundname, plotted=True)

                    #if abs(float(retarray.dx*retarray.nbx) - (bbox[1][0]-bbox[0][0])) > 1e-2:
                    #    return None
                    if retarray.array.shape != (int(abs(bbox[1][0]-bbox[0][0])/retarray.dx), int(abs(bbox[1][1]-bbox[0][1])/retarray.dy)):
                        return None

                    self.loaded_tiles.append(file[0])
            else:
                file = glob.glob(join(self.linked_data_dir,'*.tif'))
                if len(file)>0:
                    if '-' in file[0]:
                        logging.info(_('No file with {}'.format(boundname)))
                        return None

                    newname = file[0] + '-' + str(int(bbox[0][0])) + '_' + str(int(bbox[1][1])) + '.tif'

                    gdal.Translate(newname, file[0], projWin = [bbox[0][0], bbox[1][1], bbox[1][0], bbox[0][1]])
                    retarray = WolfArray(fname=newname, mapviewer=self.mapviewer, idx=boundname, plotted=True)
                    retarray.count()
                else:
                    return None
            assert(isinstance(retarray, WolfArray)), 'Bad type'
        else:
            # comparaison car répertoire source et comp différents

            file1 = glob.glob(join(self.linked_data_dir,'*{}*.tif').format(boundname))
            file2 = glob.glob(join(self.linked_data_dir_comp,'*{}*.tif').format(boundname))

            if len(file1)>0:
                src = WolfArray(fname = file1[0], mapviewer = self.mapviewer, idx = file1[0])
            else:
                file1 = glob.glob(join(self.linked_data_dir,'*.tif'))
                if len(file1)>0:
                    if '-' in file1[0]:
                        logging.info(_('No file with {}'.format(boundname)))
                        return None

                    newname = file1[0] + '-' + str(int(bbox[0][0])) + '_' + str(int(bbox[1][1])) + '.tif'
                    gdal.Translate(newname, file1[0], projWin = [bbox[0][0], bbox[1][1], bbox[1][0], bbox[0][1]])
                    src = WolfArray(fname = newname, mapviewer = self, idx = file1[0])

            if len(file2)>0:
                comp = WolfArray(fname = file2[0], mapviewer = self.mapviewer, idx = file2[0])
            else:
                file2 = glob.glob(join(self.linked_data_dir_comp,'*.tif'))
                if len(file2)>0:
                    newname = file2[0] + '-' + str(int(bbox[0][0])) + '_' + str(int(bbox[1][1])) + '.tif'
                    gdal.Translate(newname, file2[0], projWin = [bbox[0][0], bbox[1][1], bbox[1][0], bbox[0][1]])
                    comp = WolfArray(fname = newname, mapviewer = self, idx = file2[0])

            if comp is None or src is None:
                logging.info(_('At least one file is missing --  Nothing to do ! -- Retry or Debug !'))
                return None

            if comp.dx != src.dx:
                comp.rebin(src.dx/comp.dx)

            if src.array.shape != (int(abs(bbox[1][0]-bbox[0][0])/src.dx), int(abs(bbox[1][1]-bbox[0][1])/src.dy)):
                return None

            if comp.array.shape == src.array.shape:
                retarray = comp-src
                retarray.count()
                assert(isinstance(retarray, WolfArray)), 'Bad type'
            else:
                logging.info(_('Bad shape for {}'.format(boundname)))
                try:
                    if exists(newname):
                        remove(newname)
                except:
                    pass
                retarray = None

        return retarray