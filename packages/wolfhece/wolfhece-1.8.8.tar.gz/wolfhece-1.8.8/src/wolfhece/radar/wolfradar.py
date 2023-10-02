import wradlib
from datetime import datetime as date
from os import path
from osgeo import gdal
from drawing_obj import Element_To_Draw


class L08L72:

    def __init__(self) -> None:
        pass

    def L08_2_72(x:float, y:float):
        pass

    def L72_2_08(x:float, y:float):
        pass



class RadarIRM(Element_To_Draw):
    def __init__(self, idx: str = '', plotted: bool = True, mapviewer=None, need_for_wx: bool = False) -> None:
        super().__init__(idx, plotted, mapviewer, need_for_wx)
        pass


    def convert2rain(self, coord1, coord2, dateBegin:date, dateEnd:date):
        # extract all the points in all the .hdf files and their values -> check whether to crop during this process of after

        # create polygons out of the given points

        # project the Lambert 2008 in Lambert 1972 coordinates -> let the possibility to crop either points or polygons

        # save the polygons in .shp shapefile

        # Create a folder with the time serie for each polygone

        pass


    # def plot(self):
    #     pass

    def _shapefile(fileName:str):
        pass

    
