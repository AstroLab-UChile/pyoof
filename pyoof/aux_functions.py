#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from scipy.constants import c as light_speed
from astropy.io import fits

__all__ = [
    'extract_data_effelsberg', 'str2LaTeX',
    ]


def extract_data_effelsberg(pathfits):
    """
    Extracts the necessary data for the pyoof package. Change in the future to
    a more general and not only speficif to Effelsberg data.
    """

    # Opening fits file with astropy
    hdulist = fits.open(pathfits)

    # Observation frequency
    freq = hdulist[0].header['FREQ']  # Hz
    wavel = light_speed / freq

    # Mean elevation
    meanel = hdulist[0].header['MEANEL']  # Degrees

    # name of the fit file to fit
    name = os.path.split(pathfits)[1][:-5]

    beam_data = [hdulist[i].data['fnu'] for i in range(1, 4)][::-1]
    u_data = [hdulist[i].data['DX'] for i in range(1, 4)][::-1]
    v_data = [hdulist[i].data['DY'] for i in range(1, 4)][::-1]
    d_z_m = [hdulist[i].header['DZ'] for i in range(1, 4)][::-1]

    # Permuting the position to provide same as main_functions
    beam_data.insert(1, beam_data.pop(2))
    u_data.insert(1, u_data.pop(2))
    v_data.insert(1, v_data.pop(2))
    d_z_m.insert(1, d_z_m.pop(2))

    # path or directory where the fits file is located
    pthto = os.path.split(pathfits)[0]

    data_info = [name, pthto, freq, wavel, d_z_m, meanel]
    data_obs = [beam_data, u_data, v_data]

    return data_info, data_obs


def str2LaTeX(python_string):
    """
    Function that solves the underscore problem in a python string to LaTeX
    it changes it from _ -> \_ symbol.

    Parameters
    ----------
    python_string : str
        String that needs to be changed.

    Returns
    -------
    LaTeX_string : str
        Sring with the new underscore symbol.
    """

    string_list = list(python_string)

    for idx, string in enumerate(string_list):
        if string_list[idx] == '_':
            string_list[idx] = '\_'

    LaTeX_string = ''.join(string_list)

    return LaTeX_string