import numpy as np
import numpy.ma as ma
from os import path
from pathlib import Path

from .PyTranslate import _
from .wolf_array import WolfArray
from .wolfresults_2D import Wolfresults_2D, views_2D, getkeyblock
from .CpGrid import CpGrid
from .PyPalette import wolfpalette
from .gpu.results_store import ResultsStore

class wolfres2DGPU(Wolfresults_2D):

    def __init__(self, fname:str, eps=0., idx: str = '', plotted: bool = True, mapviewer=None):

        super().__init__(fname = str(Path(fname).parent / "simul"), eps=eps, idx=idx, plotted=plotted, mapviewer=mapviewer, gpu_loader=True)

        # MERGE Inheriting is a bad idea in general because it allows
        # classes to look inside others, and induces hard
        # coupling. It's better to connect with instances and use
        # their functions so that the provider can better enforce what
        # is available to class's users.

        self._result_store = ResultsStore(sim_path = Path(fname), mode='r')

    def get_nbresults(self):
        return self._result_store.nb_results

    def read_oneresult(self,which:int=-1):
        """
        Lecture d'un pas de sauvegarde

        which: result number to read; 0-based; -1 == last one
        """
        which = self._result_store.nb_results-1 if which==-1 else which
        #print(f"which = {which}")
        _, _, _, _, wd_np, qx_np, qy_np = self._result_store.get_result(which+1)

        # self.myblocks[getkeyblock(0)].waterdepth.array.data = wd_np.astype(np.float32)
        # self.myblocks[getkeyblock(0)].qx.array.data = qx_np.astype(np.float32)
        # self.myblocks[getkeyblock(0)].qy.array.data = qy_np.astype(np.float32)

        curblock = self.myblocks[getkeyblock(1,False)]
        if self.epsilon > 0.:
            curblock.waterdepth.array=ma.masked_less_equal(wd_np.astype(np.float32).T,self.epsilon)
        else:
            curblock.waterdepth.array=ma.masked_equal(wd_np.astype(np.float32).T,0.)

        curblock.qx.array=ma.masked_where(curblock.waterdepth.array.mask,qx_np.astype(np.float32).T)
        curblock.qy.array=ma.masked_where(curblock.waterdepth.array.mask,qy_np.astype(np.float32).T)

        curblock.waterdepth.count()
        curblock.qx.count()
        curblock.qy.count()

        if self.epsilon > 0.:
            curblock.waterdepth.set_nullvalue_in_mask()
            curblock.qx.set_nullvalue_in_mask()
            curblock.qy.set_nullvalue_in_mask()

        self.current_result = which
        self.loaded=True

    def _update_result_view(self):
        which = self.current_result

        nb = self._result_store.nb_results

        self.read_oneresult(which)
        self.set_currentview()

        self.current_result = which
        self.loaded=True

    def read_next(self):
        """
        Lecture du pas suivant
        """
        if self.current_result < self._result_store.nb_results-1:
            self.current_result+=1

        self._update_result_view()

    def read_previous(self):
        """
        Lecture du pas suivant
        """
        if self.current_result > 0:
            self.current_result -= 1

        self._update_result_view()
