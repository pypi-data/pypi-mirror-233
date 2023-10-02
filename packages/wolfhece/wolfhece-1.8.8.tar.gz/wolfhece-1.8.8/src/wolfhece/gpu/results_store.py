import io
import os
import csv
import zipfile
from pathlib import Path
from typing import Union

import pandas as pd
import numpy as np
from tifffile import imwrite, imread

def array_to_bytes(x: np.ndarray) -> bytes:
    np_bytes = io.BytesIO()
    np.save(np_bytes, x, allow_pickle=True)
    return np_bytes.getvalue()

def bytes_to_array(b: bytes) -> np.ndarray:
    np_bytes = io.BytesIO(b)
    return np.load(np_bytes, allow_pickle=True)

class ResultsStore:
    # We thought abut HDF5 but it seems a tad too complex four our needs.

    def __init__(self, sim_path: Path, mode:str = "a"):
        """
        * `sim_path` must include the beacon file name like `d:\alpha\bravo\simul`
        * `mode` is `r` read, `w` (over)write or `a` append.
        """

        self._dir = None
        self._zip = None
        self._mode = mode
        self._sim_times = []

        if sim_path.suffix == ".zip":
            self._path = sim_path
        else:
            self._dir = sim_path

        if mode in ('r','a'):
            self._init_filesystem_for_reading(mode)
            self._number_of_results = int(self._read(f"nb_results.txt"))

            #csvfile = self._zip.open(f"sim_times.csv")
            s = self._read(f"sim_times.csv").decode()

            csv_reader = csv.reader(io.StringIO(s))
            next(csv_reader) # Skip header

            for line in csv_reader:#,lineterminator="\n"):
                l = list(map(float,line))
                l[4] = int(l[4]) # step num
                self._sim_times.append(l)
            # self._sim_times = list(map(float, self._zip.read(f"sim_times.csv").decode().split("\n")))

        elif mode == 'w':
            self._init_filesystem_for_writing()
            self._number_of_results = 0
        else:
            raise Exception(f"Unrecognized mode : {mode}")

    @property
    def nb_results(self):
        return self._number_of_results

    @property
    def path(self) -> Path:
        return self._path

    def _update_track_files(self):
        self._writestr(f"nb_results.txt", str(self._number_of_results))

        # FIXME suboptimal (should append instead of re-writing)
        f = io.StringIO()
        csv_writer = csv.writer(f)
        csv_writer.writerow(["t","last_delta_t","dryup_niter","dryup_niter_rk","step_num"])
        csv_writer.writerows(self._sim_times)
        self._writestr("sim_times.csv", f.getvalue())

    def close(self):
        if self._dir is None:
            self._zip.close()
            self._zip = None
        else:
            pass

    def __del__(self):
        # Important for write operations (see zipfile documentation)
        self.close()
        if self._zip is not None:
            self._zip.close()


    # def append_results_multi(self, arrays: dict, values: dict):
    #     assert self._mode in ('w','a')
    #     n = f"{self._number_of_results+1:07}"

    #     assert "t" in values and "dt" in values, "You must be backward compatible"
    #     assert "h" in arrays and "qx" in arrays and "qy" in arrays, "You must be backward compatible"

    #     v = []
    #     for k, value in values.items():
    #         v.append(v)
    #     self._sim_times.append( v )

    #     for k, array in arrays.items():
    #         self._write_numpy(f"{k}_{n}", array)

    #     self._number_of_results += 1

    #     # Do this lastly because ttracking files are here to interpret the
    #     # content of the results.
    #     self._update_track_files()

    def append_result(self, step_num: int, sim_time: float, dt: float, niter: int, niter_rk: int, h:np.ndarray, qx:np.ndarray, qy:np.ndarray,
                      dbg1:np.ndarray, dbg2:np.ndarray):
        assert self._mode in ('w','a')

        # FIXME int(step_num) dirty fix. Somehow I get step num which are float
        # down here.

        self._sim_times.append( (sim_time,dt,niter,niter_rk,int(step_num)) )
        n = f"{self._number_of_results+1:07}"
        self._write_numpy(f"h_{n}", h)
        self._write_numpy(f"qx_{n}", qx)
        self._write_numpy(f"qy_{n}", qy)

        if dbg1 is not None:
            # FIXME Remove that, put in in named results.
            self._write_numpy(f"dbg1_{n}", dbg1)
        if dbg2 is not None:
            self._write_numpy(f"dbg2_{n}", dbg2)
        self._number_of_results += 1

        # Do this lastly because ttracking files are here to interpret the
        # content of the results.
        self._update_track_files()

    def additional_result(self, name, data:np.ndarray):
        n = f"{self._number_of_results:07}"
        self._write_numpy(f"{name}_{n}", data)

    def get_last_result_index(self) -> int:
        assert self._number_of_results >= 1, "This file has no results ?"
        return self.nb_results

    def get_last_result(self, ndx=0) -> tuple[float,float,int,np.ndarray,np.ndarray,np.ndarray]:
        """ returns [t,dt,n_iter_dry_up_euler, n_iter_dry_up_rk, h,qx,qy]
        """
        assert ndx <= 0, "-0 == last, -1=one before last, -2=..."
        assert self._mode in ["r","a"], "Only makes sense in read or update modes"
        # -1 to go fro one based to zero based
        return self.get_result(self.get_last_result_index() + ndx)


    def get_result(self, ndx: int) -> tuple[float,float,int,np.ndarray,np.ndarray,np.ndarray]:
        """ returns [t,dt,n_iter_dry_up_euler, n_iter_dry_up_rk, h,qx,qy]
        """
        assert ndx >= 1, "We're one based"
        assert ndx <= self.nb_results, f"You're past the last result: ndx={ndx} > {self.nb_results}"
        assert self._mode in ["r","a"], "Only makes sense in read or update modes"

        n = f"{ndx:07}"

        # Built this way so that one can look at results
        # without preventing write operations
        arrays = list(self._sim_times[ndx-1])[0:4] # [0:4] for backward compatibility
        #print(f"get_res {ndx} / {self.nb_results} / mode={self._mode}")
        for name in ("h","qx","qy"):
            arrays.append(self._read_numpy(f"{name}_{n}"))

        return tuple(arrays)



    def get_result2(self, ndx: int) -> tuple[float,float,int,np.ndarray,np.ndarray,np.ndarray,np.ndarray,np.ndarray]:
        """ returns [t,h,qx,qy,dbg1,dbg2]
        """
        assert ndx >= 1, "We're one based"
        assert self._mode == "r", f"Calling get_result2 only makes sense in read mode." \
            "Current mode is {self._mode}"

        n = f"{ndx:07}"

        # Built this way so that one can look at results
        # without preventing write operations
        try:
            with zipfile.ZipFile(self._path, mode="r") as zip:
                arrays = list(self._sim_times[ndx-1])
                for name in ("h","qx","qy","dbg1","dbg2"):
                    arrays.append(self._read_numpy(f"{name}_{n}"))
        except Exception as ex:
            raise Exception(f"Unable to load result '{n}' from {self._path}")

        return tuple(arrays)

    def get_last_named_result(self, name: Union[str,list[str]], delta_ndx:int = 0) -> Union[np.ndarray, list[np.ndarray]]:
        return self.get_named_result(name, self.get_last_result_index() + delta_ndx)

    def get_named_result(self, name: Union[str,list[str]], ndx:int) -> Union[np.ndarray, list[np.ndarray]]:
        """ Looks for result by names.
        """
        assert ndx >= 1, "We're one based"
        assert ndx <= self.nb_results, f"Your index is too far away, max is: {self.nb_results}"
        assert self._mode in ["a","r"], "Only makes sense in read or update mode"

        if type(name) == str:
            if name == "t":
                return self._sim_times[ndx-1][0]
            elif name in ("last_delta_t", "dt"):
                return self._sim_times[ndx-1][1]
            elif name == "dryup_niter":
                return self._sim_times[ndx-1][2]
            elif name == "dryup_niter_rk":
                return self._sim_times[ndx-1][3]
            elif name == "step_num":
                return self._sim_times[ndx-1][4]
            elif name in  ("h","qx","qy","alpha","debug1"):
                n = f"{ndx:07}" # FIXME We should be one based in our files too :-)

                # Built this way so that one can look at results
                # without preventing write operations
                try:
                    return self._read_numpy(f"{name}_{n}")
                except Exception as ex:
                    raise Exception(f"Unable to load result named '{name}_{n}' (data comes from {self._source_path()})")
            else:
                raise Exception(f"I don't know any values by the name of '{name}'")
        else:
            return [self.get_named_result(n,ndx) for n in name]


    def _init_filesystem_for_reading(self, mode):
        if self._dir is None:
            assert self._path.exists(), f"The file {self._path} doesn't exists"
            assert self._path.is_file(), f"The path {self._path} is not a file"
            self._zip = zipfile.ZipFile(self._path, mode=mode)
        else:
            assert self._dir.exists(), f"The directory {self._dir} doesn't exist"
            assert self._dir.is_dir(), f"The directory {self._dir} is not a directory"

    def _init_filesystem_for_writing(self):
        if self._dir is None:
            if self._path.exists():
                assert self._path.is_file()
                self._path.unlink()
            self._zip = zipfile.ZipFile(self._path, mode="x") # x=exclusive create
        else:
            if self._dir.exists():
                assert self._dir.is_dir(), f"If you want to write to {self._dir.is_dir()} \
                    then it must be a directory (it's not)"
                for f in os.listdir(self._dir):
                    os.remove(self._dir / f)
            else:
                os.makedirs(self._dir)

    def _writestr(self, fname, s):
        if self._dir is None:
            assert type(s) == str
            self._zip.writestr(fname, s)
        else:
            with open(self._dir / fname,"wb") as fout:
                if type(s) == bytes:
                    fout.write(s)
                elif type(s) == str:
                    fout.write(s.encode("utf-8"))
                else:
                    raise Exception(f"Unrecognized data type {type(s)}")

    def _write_numpy(self, fname, a):
        if self._dir is None:
            assert type(a) == np.ndarray, f"Got {type(a)} ?"
            self._zip.writestr(fname, array_to_bytes(a))
        else:
            # np.save((self._dir / fname).with_suffix(".npy"), a)
            imwrite(
                (self._dir / fname).with_suffix(".tiff"),
                np.flipud(a),
                compression='zlib',
                compressionargs={'level': 8} )


    def _read(self, fname):
        if self._dir is None:
            with zipfile.ZipFile(self._path, mode="r") as zip:
                with zip.open(fname, mode="r") as fin:
                    return fin.read()
        else:
            with open(self._dir / fname, "rb") as fin:
                return fin.read()

    def _read_numpy(self, fname):
        if self._dir is None:
            with zipfile.ZipFile(self._path, mode="r") as zip:
                with zip.open(fname, mode="r") as fin:
                    return bytes_to_array( fin.read())
        else:
            i = np.flipud(imread( (self._dir / fname).with_suffix(".tiff")))
            #print(f"reading {(self._dir / fname).with_suffix('.tiff')} -> {i.shape} {i.dtype}")
            return i
            # return np.load((self._dir / fname).with_suffix(".npy"))

    def _source_path(self):
        # For error rerporting and such. Not for looking for data.
        if self._dir is not None:
            return self._dir
        else:
            return self._path
