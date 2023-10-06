# -*- coding: utf-8 -*-
# Copyright (C) Duncan Macleod (2014-2020)
#
# This file is part of GWpy.
#
# GWpy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# GWpy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with GWpy.  If not, see <http://www.gnu.org/licenses/>.

"""GWF I/O utilities for LALFrame.

This module provides the LALFrame implementation of the functions
that make up the `gwpy.io.gwf` module API.
"""

from enum import IntEnum

import lalframe

from ...utils.enum import NumpyTypeEnum


# -- type mapping -------------------------------------------------------------

class FrVectType(IntEnum, NumpyTypeEnum):
    INT8 = lalframe.FRAMEU_FR_VECT_C
    INT16 = lalframe.FRAMEU_FR_VECT_2S
    INT32 = lalframe.FRAMEU_FR_VECT_4S
    INT64 = lalframe.FRAMEU_FR_VECT_8S
    FLOAT32 = lalframe.FRAMEU_FR_VECT_4R
    FLOAT64 = lalframe.FRAMEU_FR_VECT_8R
    COMPLEX64 = lalframe.FRAMEU_FR_VECT_8C
    COMPLEX128 = lalframe.FRAMEU_FR_VECT_16C
    BYTES = lalframe.FRAMEU_FR_VECT_STRING
    UINT8 = lalframe.FRAMEU_FR_VECT_1U
    UINT16 = lalframe.FRAMEU_FR_VECT_2U
    UINT32 = lalframe.FRAMEU_FR_VECT_4U
    UINT64 = lalframe.FRAMEU_FR_VECT_8U


def _lalframe_proctype(type_):
    return getattr(lalframe, f"FRAMEU_FR_PROC_TYPE_{type_.upper()}")


class FrProcDataType(IntEnum):
    UNKNOWN = _lalframe_proctype("UNKNOWN")
    TIME_SERIES = _lalframe_proctype("TIME_SERIES")
    FREQUENCY_SERIES = _lalframe_proctype("FREQUENCY_SERIES")
    OTHER_1D_SERIES_DATA = _lalframe_proctype("OTHER_1D_SERIES_DATA")
    TIME_FREQUENCY = _lalframe_proctype("TIME_FREQUENCY")
    WAVELETS = _lalframe_proctype("WAVELETS")
    MULTI_DIMENSIONAL = _lalframe_proctype("MULTI_DIMENSIONAL")


def _lalframe_proc_subtype(type_):
    return getattr(lalframe, f"FRAMEU_FR_PROC_SUB_TYPE_{type_.upper()}")


class FrProcDataSubType(IntEnum):
    UNKNOWN = _lalframe_proc_subtype("UNKNOWN")
    DFT = _lalframe_proc_subtype("DFT")
    AMPLITUDE_SPECTRAL_DENSITY = _lalframe_proc_subtype("AMPLITUDE_SPECTRAL_DENSITY")
    POWER_SPECTRAL_DENSITY = _lalframe_proc_subtype("POWER_SPECTRAL_DENSITY")
    CROSS_SPECTRAL_DENSITY = _lalframe_proc_subtype("CROSS_SPECTRAL_DENSITY")
    COHERENCE = _lalframe_proc_subtype("COHERENCE")
    TRANSFER_FUNCTION = _lalframe_proc_subtype("TRANSFER_FUNCTION")


def _iter_channels(framefile):
    if not isinstance(framefile, lalframe.FrameUFrFile):
        framefile = lalframe.FrameUFrFileOpen(framefile, "r")
    toc = lalframe.FrameUFrTOCRead(framefile)
    for type_ in ('sim', 'proc', 'adc'):
        nchan = getattr(lalframe, f"FrameUFrTOCQuery{type_.title()}N")(toc)
        get_name = getattr(lalframe, f"FrameUFrTOCQuery{type_.title()}Name")
        for i in range(nchan):
            yield get_name(toc, i), type_
