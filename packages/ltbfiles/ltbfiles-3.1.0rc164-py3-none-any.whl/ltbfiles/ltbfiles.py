"""
This module contains functions designed for reading file formats used by LTB spectrometers.

LICENSE
  Copyright (C) 2022 Dr. Sven Merk

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 3 of the License, or
  (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License along
  with this program; if not, write to the Free Software Foundation, Inc.,
  51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""
import collections
import configparser
import json
import os
from pathlib import Path
import struct
import tempfile
from typing import Union, Optional, Tuple, List
import zipfile
import numpy as np


Spectra = collections.namedtuple('Spectra', ['Y', 'x', 'o', 'head'])
SPEC_EXTENSIONS = ['.ary', '.aryx']


class UnknownTypeException(Exception):

    def __init__(self, extension: str):
        super().__init__(f"Unknown file extension '{extension}'")


class IncompatibleSpectraException(Exception):
    pass


def _load_file(filename: Union[Path,str]) -> Spectra:
    filename = Path(filename)
    ext = filename.suffix.lower()
    if ".ary" == ext:
        return read_ltb_ary(filename)
    if  ".aryx" == ext:
        return read_ltb_aryx(filename)
    raise UnknownTypeException(ext)


def load_files(filelist: Union[List[Path],List[str]], *, interpolate:bool=False) -> Spectra:
    """
    This function reads the content of multiple spectra files into a merged numpy-array.

    Syntax
    ------
        >>> Y,x,o,head = load_files(filenames)

    Inputs
    ------
        filenames : list[Path]|list[str]
            List of filenames to be loaded
    Keyword Arguments
    -----------------
        interpolate: bool
            Interpolate if wavelength axis does not match.
    Outputs
    -------
        Y: numpy-array (m x n)
            2D array containing the intensity values, where the number of
            rows (m) corresponds to the spectral pixels und the number of
            columns (n) corresponds to the number of spectra
        x: numpy-array (m x 1)
            1D array containing the wavelength values
        o: numpy-array (m x 1)
            1D array containing the spectral orders
        head: list[dict]
            A list of dictionaries containing the metadata of the spectra loaded
    """
    if not isinstance(filelist, list):
        filelist = [filelist]
    assert len(filelist) > 0, "At least one file must be passed"
    y, wl, order, h = _load_file(filelist[0])
    Y = np.full((len(y), len(filelist)), np.nan)
    Y[:,0] = y
    head = [h]
    if len(filelist) > 1:
        for i_file, file in enumerate(filelist[1:], start=1):
            y,x,o,h = _load_file(file)
            if not (np.array_equal(x, wl) and np.array_equal(o, order)):
                if not interpolate:
                    raise IncompatibleSpectraException(
                        f"Can only merge spectra with identical wavelength axis (current: '{str(file)}'")
                y = np.interp(wl, x, y)
                order = np.zeros(x.shape)
            Y[:,i_file] = y
            head.append(h)
    return Spectra(Y, wl, order, head)


def scan_for_files(folder: Union[Path,str], *, extensions=None) -> List[Path]:
    """
    Returns a list of all spectra in a given folder.

    Syntax
    ------
        >>> files = scan_for_files(folder, extensions=SPEC_EXTENSIONS)

    Inputs
    ------
        folder : Path|str
            Name of the folder to be scanned for files
    Keyword Arguments
    -----------------
        extensions : list[str]
            File extensions that should be searched for. Default = ['.ary', '.aryx']
    Outputs
    -------
        files : list[Path]
            List of spectra files found within the folder
    """
    folder = Path(folder)
    if extensions is None:
        extensions = SPEC_EXTENSIONS
    return [
        folder / file for file in folder.iterdir()
        if any(ext == file.suffix for ext in extensions)
    ]


def load_folder(folder: Union[Path,str], *, interpolate:bool=False, extensions=None) -> Optional[Spectra]:
    """
    Load all spectra to be found in a given folder

    Syntax
    ------
        >>> Spectra = load_folder(folder, extensions=SPEC_EXTENSIONS)
        >>> Y,x,o,head = load_folder(folder, extensions=SPEC_EXTENSIONS)

    Inputs
    ------
        folder : Path|str
            Name of the folder to be scanned for spectra
    Keyword Arguments
    -----------------
        interpolate: bool
            Interpolate if wavelength axis does not match.
        extensions : list[str]
            File extensions that should be searched for. Default = ['.ary', '.aryx']
    Outputs
    -------
        Spectra : namedtuple
            Spectra loaded from the folder.
            Spectra.Y is a p x n numpy array with "n" being the number of spectra and "p" the number of pixels.
            Spectra.x is the wavelength axis, a p x 1 numpy array
            Spectra.o is the spectral order information, a p x 1 numpy array
            Spectra.head is a list[dict] containing the spectra metadata. Its len is "n"
    """
    if extensions is None:
        extensions = SPEC_EXTENSIONS
    files = scan_for_files(folder, extensions=extensions)
    if len(files) > 0:
        Y, x, o, head = load_files(files, interpolate=interpolate)
        return Spectra(Y,x,o,head)
    return None


def read_ltb_ary(filename: Union[Path,str], *, sort_wl: bool=True) -> Spectra:
    """
    This function reads data from binary *.ary files for LTB spectrometers.

    Syntax
    ------
        >>> y,x,o,head = read_ltb_ary(filename, sort_wl)

    Inputs
    ------
       filename : Path|str
           Name of the *.ary file to be read. May be a relative path or full filename.
    Keyword Arguments
    -----------------
       sortWL : bool
           OPTIONAL flag, if spectra should be sorted by their wavelength after reading. default: true
    Outputs
    -------
       x : float array
           Wavelengths
       o : float array
           Spectral order of the current pixel
       y : float array
           Intensity
       head : dict
           additional file header (list)

    Caution! Due to order overlap, it may happen that two pixels have the
    same wavelength. If this causes problems in later data treatment, such
    pixels should be removed using

        >>> x, ind = numpy.unique(x, True)
        >>> o=o[ind]
        >>> y=y[ind]
    """
    x = None
    y = None
    sort_order = None
    order_info = None
    head = {'filename': filename}
    with tempfile.TemporaryDirectory(prefix='ary_') as extract_folder:
        with zipfile.ZipFile(filename) as f_zip:
            file_list = f_zip.namelist()
            f_zip.extractall(extract_folder)

        for i_file in file_list:

            if i_file.endswith('~tmp'):
                spec_file_full = os.path.join(extract_folder, i_file)
                with open(spec_file_full, 'rb') as f_spec:
                    dt = np.dtype([('int', np.float32), ('wl', np.float32)])
                    values = np.fromfile(f_spec, dtype=dt)
                if sort_wl:
                    sort_order = np.argsort(values['wl'])
                    x = values['wl'][sort_order]
                    y = values['int'][sort_order]
                else:
                    sort_order = np.arange(0, len(values['wl']))
                    x = values['wl']
                    y = values['int']

            elif i_file.endswith('~aif'):
                add_file_full = os.path.join(extract_folder, i_file)
                with open(add_file_full, 'rb') as f_aif:
                    dt = np.dtype([('indLow', np.int32),
                                   ('indHigh', np.int32),
                                   ('order', np.int16),
                                   ('lowPix', np.int16),
                                   ('highPix', np.int16),
                                   ('foo', np.int16),
                                   ('lowWave', np.float32),
                                   ('highWave', np.float32)])
                    order_info = np.fromfile(f_aif, dt)

            elif i_file.endswith('~rep'):
                rep_file_full = os.path.join(extract_folder, i_file)
                with open(rep_file_full, 'r', encoding="utf-8") as f_rep:
                    for i_line in f_rep:
                        stripped_line = str.strip(i_line)
                        if '[end of file]' == str.strip(stripped_line):
                            break
                        new_entry = stripped_line.split('=')
                        head[new_entry[0].replace(' ', '_')] = new_entry[1]

        assert x is not None and y is not None, "File is corrupted. No spectral information was found."
        scaling = str(head.get("Scaling"))
        head["Raman_excitation_wavelength"] = str(head.pop("Raman_exitation_wavelength", "0"))
        excitation_wl = float(head["Raman_excitation_wavelength"])
        if (scaling is not None) and ("Raman" in scaling) and (excitation_wl > 0):
            x = (1e7 / excitation_wl) - (1e7 / x)
            head["x_unit"] = "cm^{-1}"
            head["x_name"] = "Raman shift"
        else:
            head["x_unit"] = "nm"
            head["x_name"] = "Wavelength"
        if (sort_order is not None) and (order_info is not None):
            o = np.empty(x.size)
            o[:] = np.NAN
            for i_curr_order in order_info:
                o[i_curr_order['indLow']:i_curr_order['indHigh'] + 1] = i_curr_order['order']
            o = o[sort_order]
        else:
            o = np.ones(x.size)

    return Spectra(y, x, o, head)


def read_ltb_aryx(filename: Union[Path,str], *, sort_wl:bool=True) -> Spectra:
    """
    This function reads data from binary *.aryx files for LTB spectrometers.

    Syntax
    ------
        >>> y,x,o,head = read_ltb_aryx(filename, sort_wl)

    Inputs
    ------
       filename : Path
           Name of the *.aryx file to be read. May be a relative path or full filename.
    Keyword Arguments
    -----------------
       sortWL : bool
           OPTIONAL flag, if spectra should be sorted by their wavelength after reading. default: true
    Outputs
    -------
       x : float array
           Wavelengths
       o : float array
           Spectral order of the current pixel
       y : float array
           Intensity
       head : dict
           additional file header (list)

    Caution! Due to order overlap, it may happen that two pixels have the
    same wavelength. If this causes problems in later data treatment, such
    pixels should be removed using

        >>> x, ind = numpy.unique(x, True)
        >>> o=o[ind]
        >>> y=y[ind]
    """
    x = None
    y = None
    sort_order = None
    order_info = None
    head = {}
    with tempfile.TemporaryDirectory(prefix='aryx_') as extract_folder:
        with zipfile.ZipFile(filename) as f_zip:
            file_list = f_zip.namelist()
            f_zip.extractall(extract_folder)

        for i_file in file_list:

            if i_file.endswith('~tmp'):
                spec_file_full = os.path.join(extract_folder, i_file)
                with open(spec_file_full, 'rb') as f_spec:
                    dt = np.dtype([('int', np.float64), ('wl', np.float64)])
                    values = np.fromfile(f_spec, dtype=dt)
                if sort_wl:
                    sort_order = np.argsort(values['wl'])
                else:
                    sort_order = np.arange(0, len(values['wl']))
                x = values['wl'][sort_order]
                y = values['int'][sort_order]


            elif i_file.endswith('~aif'):
                add_file_full = os.path.join(extract_folder, i_file)
                with open(add_file_full, 'rb') as f_aif:
                    dt = np.dtype([('indLow', np.int32),
                                   ('indHigh', np.int32),
                                   ('order', np.int16),
                                   ('lowPix', np.int16),
                                   ('highPix', np.int16),
                                   ('foo', np.int16),
                                   ('lowWave', np.float64),
                                   ('highWave', np.float64)])
                    order_info = np.fromfile(f_aif, dt)

            elif i_file.endswith('~json'):
                rep_file_full = os.path.join(extract_folder, i_file)
                with open(rep_file_full, 'r', encoding="utf-8") as f_rep:
                    head = json.load(f_rep)

        assert x is not None and y is not None, "File is corrupted. No spectral information was found."
        excitation_wl = head["measure"].get("ExcitationLength")
        if excitation_wl is not None:
            x = (1e7 / float(excitation_wl)) - (1e7 / x)
            head["x_unit"] = "cm^{-1}"
            head["x_name"] = "Raman shift"
        else:
            head["x_unit"] = "nm"
            head["x_name"] = "Wavelength"
        if (sort_order is not None) and (order_info is not None):
            o = np.empty(x.size)
            o[:] = np.NAN
            for i_curr_order in order_info:
                o[i_curr_order['indLow']:i_curr_order['indHigh'] + 1] = i_curr_order['order']
            o = o[sort_order]
        else:
            o = np.ones(x.size)

    head['filename'] = filename
    return Spectra(y, x, o, head)


def _make_header_from_array(data):
    head = {'ChipWidth': int(data[0]),
            'ChipHeight': int(data[1]),
            'PixelSize': float(data[2]),
            'HorBinning': int(data[3]),
            'VerBinning': int(data[4]),
            'BottomOffset': int(data[5]),
            'LeftOffset': int(data[6]),
            'ImgHeight': int(data[7]),
            'ImgWidth': int(data[8])
            }
    return head


def read_ltb_raw(filename: Union[Path,str]) -> Tuple[np.ndarray, dict]:
    """
    This function reads *.raw image files created with LTB spectrometers.
    Input
    -----
    filename : Path|str

    Outputs
    -------
    image : np.array of image shape
    head : dict containing image properties
    """
    data = np.loadtxt(filename)
    head = _make_header_from_array(data[0:9])
    image = np.reshape(data[9:].astype(np.int32), (head['ImgHeight'], head['ImgWidth']))
    return image, head


def read_ltb_rawb(filename: Union[Path,str]) -> Tuple[np.ndarray, dict]:
    """
    This function reads *.rawb image files created with LTB spectrometers.
    Input
    -----
    filename : Path|str

    Outputs
    -------
    image : np.array of image shape
    head : dict containing image properties
    """
    struct_fmt = '=iidiiiiii'
    struct_len = struct.calcsize(struct_fmt)
    struct_unp = struct.Struct(struct_fmt).unpack_from

    with open(filename,'rb') as f_file:
        metadata = f_file.read(struct_len)
        im_stream = np.fromfile(f_file, dtype=np.int32)
        h = struct_unp(metadata)
        head = _make_header_from_array(h)
        image = np.reshape(im_stream, (head['ImgHeight'], head['ImgWidth']))
    return image, head


def read_ltb_rawx(filename: Union[Path,str]) -> Tuple[np.ndarray, dict]:
    """
    This function reads *.rawx image files created with LTB spectrometers.
    Input
    -----
    filename : Path|str

    Outputs
    -------
    image : np.array of image shape
    head : dict containing all measurement and spectrometer parameters
    """
    with tempfile.TemporaryDirectory(prefix='rawx_') as extract_folder:
        with zipfile.ZipFile(filename) as f_zip:
            file_list = f_zip.namelist()
            f_zip.extractall(extract_folder)

        image = None
        sophi_head = configparser.ConfigParser()
        aryelle_head = configparser.ConfigParser()
        for i_file in file_list:
            if i_file.endswith('rawdata'):
                img_file_full = os.path.join(extract_folder, i_file)
                image = np.loadtxt(img_file_full)
            elif i_file.lower() == 'aryelle.ini':
                aryelle_file_full = os.path.join(extract_folder, i_file)
                aryelle_head.read(aryelle_file_full)
            elif i_file.lower() == 'sophi.ini':
                sophi_file_full = os.path.join(extract_folder, i_file)
                sophi_head.read(sophi_file_full)
        width = int(aryelle_head['CCD']['width']) // int(sophi_head['Echelle 1']['vertical binning'])
        height = int(aryelle_head['CCD']['height']) // int(sophi_head['Echelle 1']['horizontal binning'])
        head = {'sophi_ini': sophi_head,
                'aryelle_ini': aryelle_head}
        assert image is not None
        image = image.reshape((height, width))

    return image, head
