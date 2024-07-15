# -*- coding: utf-8 -*-
"""
Created on Mon Jul 15 17:40:20 2024

@author: Nanoelectronics.ad
"""

#%%% Initialize Setup

#%%%% Connect VISA
import os
import time
import numpy as np
import qcodes as qc
import scipy.signal as scp
import matplotlib.pyplot as plt
from qcodes import load_by_run_spec, ScaledParameter, Parameter
from qcodes import Station, initialise_or_create_database_at, \
    load_or_create_experiment, Measurement
# from qcodes.tests.instrument_mocks import DummyInstrument, \
#    DummyInstrumentWithMeasurement
from qcodes.utils.dataset.doNd import do0d,do1d,do2d
from qcodes.dataset.plotting import plot_dataset, plot_by_id
qc.config.plotting['default_color_map']='Blues_r'

qc.logger.start_all_logging()
station = Station()
def add_or_replace_component(component):
    if component.name in station.components:
        station.remove_component(component.name)
        station.add_component(component)
        print("Component replaced!")

    else:
        station.add_component(component)
        print("Success!")
        
#%%%% Set up PyVisa
import pyvisa
rm = pyvisa.ResourceManager()
instruments = rm.list_resources()
print("Connected instruments:", instruments)

#%%%% Connect to IVVI
import qcodes.instrument_drivers.FastDuck as IVVI
dac=IVVI.FastDuck('IVVI', 'COM3', dac_step=50.0, dac_delay=0.100)
# import os
# os.environ['VI_PYTHON_VISA_LIBRARY'] = 'C:\\Windows\\System32\\visa32.dll'
dac.get_all()
dac.print_readable_snapshot()


#%%%% Connect to multimeters
from qcodes.instrument_drivers.Keysight.Keysight_34465A_submodules import Keysight_34465A

dmm_left = Keysight_34465A('DMM_left', address='TCPIP0::K-000000-00000::inst0::INSTR')
dmm_left.reset()

dmm_right = Keysight_34465A('DMM_right', address='TCPIP0::10.21.64.178::inst0::INSTR')
dmm_right.reset()

#%%%% Connect to SR830 Lock in amplifier
from qcodes.instrument_drivers.stanford_research import SR860
sr_left = SR860('lockin_left', 'TCPIP0::192.168.88.251')
station.add_component(sr_left)
# sr_right = SR830('lockin_right', 'GPIB0::2::INSTR')
# station.add_component(sr_right)