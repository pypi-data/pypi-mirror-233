"""EXAMPLE 7 - Simple GUI

This example shows the DDS functionality with 20 carriers
with a GUI that can use the different DDS features
"""

import sys
import spcm
from PyQt5.QtWidgets import QApplication, QMainWindow, QCheckBox, QDoubleSpinBox
from PyQt5 import uic

def exec_click():
	global ui, card
	print()
	enable = False
	freq_time_div = ui.frequencyTimeDivider.value()
	ampl_time_div = ui.amplitudeTimeDivider.value()

	connection = 0b00000
	conn_ch1 = ui.buttonGroup_01.checkedButton().text()
	conn_ch2 = ui.buttonGroup_02.checkedButton().text()
	conn_ch3 = ui.buttonGroup_03.checkedButton().text()
	print(conn_ch1)
	print(conn_ch2)
	print(conn_ch3)
	if not conn_ch1 == "Channel 0":
		connection |= spcm.SPCM_DDS_CONN_CORE8_11_TO_CH1
	else:
		connection &= ~spcm.SPCM_DDS_CONN_CORE8_11_TO_CH1
	if not conn_ch2 == "Channel 0":
		connection |= spcm.SPCM_DDS_CONN_CORE12_15_TO_CH2
	else:
		connection &= ~spcm.SPCM_DDS_CONN_CORE12_15_TO_CH2
	if not conn_ch3 == "Channel 0":
		connection |= spcm.SPCM_DDS_CONN_CORE16_19_TO_CH3
	else:
		connection &= ~spcm.SPCM_DDS_CONN_CORE16_19_TO_CH3

	ampl_time_div = ui.amplitudeTimeDivider.value()
	mod_ampl = ui.modulationAmplitude_0.isChecked()
	if mod_ampl:
		connection |= spcm.SPCM_DDS_CONN_CORE1_TO_CORE0_AM
	else:
		connection &= ~spcm.SPCM_DDS_CONN_CORE1_TO_CORE0_AM

	mod_freq = ui.modulationFrequency_0.isChecked()
	if mod_freq:
		connection |= spcm.SPCM_DDS_CONN_CORE2_TO_CORE0_FM
	else:
		connection &= ~spcm.SPCM_DDS_CONN_CORE2_TO_CORE0_FM
	print("connection: {:b}".format(connection))

	if card:
		card.freq_ramp_stepsize(freq_time_div)
		card.amp_ramp_stepsize(ampl_time_div)
		card.connections(connection)

	for carrier in range(23):
		enable = ui.findChild(QCheckBox, "enable_{}".format(carrier)).isChecked()
		freq_MHz = ui.findChild(QDoubleSpinBox, "frequency_{}".format(carrier)).value()
		ampl = 0
		if enable:
			ampl = ui.findChild(QDoubleSpinBox, "amplitude_{}".format(carrier)).value()
		phas_deg = ui.findChild(QDoubleSpinBox, "phase_{}".format(carrier)).value()
		freq_slope_MHz_s = ui.findChild(QDoubleSpinBox, "frequencySlope_{}".format(carrier)).value()

		if enable:
			print("Frequency {}: {} MHz".format(carrier, freq_MHz))
			print("Amplitude {}: {}".format(carrier, ampl))
			print("Phase {}: {} deg".format(carrier, phas_deg))
			print("Frequency slope {}: {} MHz/s".format(carrier, freq_slope_MHz_s))
		
		if card:
			card.amp(carrier, ampl)
			card.freq(carrier, freq_MHz * pow(10, 6))
			card.phase(carrier, phas_deg)
			card.frequency_slope(carrier, freq_slope_MHz_s * pow(10,6))
	
	for carrier in [0, 20, 21, 22]:
		ampl_slope_1_s = ui.findChild(QDoubleSpinBox, "amplitudeSlope_{}".format(carrier)).value()
		if enable:
			print("Amplitude slope {}: {} MHz/s".format(carrier, ampl_slope_1_s))
		
		if card:
			card.amplitude_slope(carrier, ampl_slope_1_s)

	if card:
		card.exec_now()
		card.write_to_card()


class gui_window(QMainWindow):
    def __init__(self):
        super(gui_window, self).__init__()
        uic.loadUi("examples/example_7_gui.ui",self)

with spcm.DDS('/dev/spcm0') as card:
	if card:
		print("Driver version: {major}.{minor}.{build}".format(**card.drv_version()))
		## Setup the card
		num_channels = 2
		card.set(spcm.SPC_CHENABLE, (0x1 << num_channels) - 1) # enable all channels
		for channel_index in range(num_channels):
			card.out_enable(channel_index, True)
			card.out_amp(channel_index, 1000)
		card.write_to_card()

		## Setup DDS
		card.dds_reset()

		## Start the card
		card.start()

	## Start the test
	app = QApplication(sys.argv)

	ui = gui_window()
	ui.pushButton.clicked.connect(exec_click)
	ui.show()

	try:
		sys.exit(app.exec_())
	except:
		print("Exiting")