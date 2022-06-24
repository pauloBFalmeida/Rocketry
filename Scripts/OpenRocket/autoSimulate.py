# How to run:
#	for configuring the mouse positions: 
#		python autoSimulate.py config
#	
#	for running the auto clicker from start:
#		python autoSimulate.py
#
#	for running the auto clicker for simulations after a file (non included):
#		python autoSimulate.py 086_125_090

import pyautogui, configparser
import sys
from time import sleep, time

config_filename = 'autoSim.ini'

sp_move 		= 0.1
sp_after_move 	= 0.05
sp_new_sim		= 0.3
sp_after_click	= 0.05
sp_after_enter	= 0.05
sp_delete		= 0.05
sp_write		= 0.05
sp_save_file	= 0.6
sp_next_iter	= 0.1
sp_simulate		= 1.2
sp_export		= 0.9

# time in seconds to wait with the cursor over the box
time_to_set_param = 3

# 83 a 87 de 1 em 1
launch_angle = [i for i in range(83,88,1)]
# 0 a 90 de 10 em 10,
#	100 a 150 de 25 em 25
wind_speed   = [i*10 for i in range(0,10, 1)] + [i for i in range(100,151, 25)]
# 0 a 270 de 90 a 90
wind_angle   = [i for i in range(0,271, 90)]


params_tags = [
		'pos_x_new_sim',
		'pos_y_new_sim',
		'pos_x_wing_speed',
		'pos_y_wing_speed',
		'pos_x_wing_direction',
		'pos_y_wing_direction',
		'pos_x_unclick',
		'pos_y_unclick',
		'pos_x_launch_angle',
		'pos_y_launch_angle',
		'pos_x_launch_direction',
		'pos_y_launch_direction',
		'pos_x_simulate',
		'pos_y_simulate',
		'pos_x_export_data',
		'pos_y_export_data',
		'pos_x_export',
		'pos_y_export',
		'pos_x_filename_box',
		'pos_y_filename_box',
		'pos_x_ok',
		'pos_y_ok'
		]

def read_config():
	try :
		config = configparser.ConfigParser()
		config.read(config_filename)

		positions = []
		for i in range(len(params_tags)//2):
			p1 = int(config['POSITIONS'][params_tags[i*2   ]])
			p2 = int(config['POSITIONS'][params_tags[i*2 +1]])
			positions.append( (p1,p2) )
		return positions
	except:
		print("Not able to open " + config_filename + " as configuration file")

def config_positions():
	params_names = [
		"New Simulation",
		"Average wing speed",
		"Wing direction",
		"unclick check box",
		"launch angle",
		"launch direction",
		"Simulate & Plot",
		"Export data tab",
		"Export button",
		"file name text box",
		"ok button"
		]

	params = [None for _ in range(len(params_tags))]

	print("Position your cursor over the indicated box and dont move for "+str(time_to_set_param)+" seconds")
	for i in range(len(params_names)):
		print(str(params_names[i]) + " for "+ str(time_to_set_param) +" seconds")
		# wait time_to_set_param time
		old_x, old_y = -1, -1
		sleep_step = 0.1
		counter = 0
		while counter <  time_to_set_param / sleep_step:
			x, y = pyautogui.position()
			if x == old_x and y == old_y:
				counter += 1
			else:
				counter = 0
			#
			old_x = x
			old_y = y
			#
			sleep(sleep_step)
		#
		params[i*2]    = old_x
		params[i*2 +1] = old_y
		print("saved %s position as (%d,%d)" % (params_names[i], old_x, old_y) )

	# save in config file
	config = configparser.ConfigParser()
	config['POSITIONS'] = {}
	for i in range(len(params_tags)):
		config['POSITIONS'][params_tags[i]] = str(params[i])
	# save config file in disk
	with open(config_filename, 'w') as configfile:
		config.write(configfile)


def to_3_digits_str(number):
	out = ""
	if number < 10:
			out += "0"
	if number < 100:
		out += "0"
	out += str(number)
	return  out

def generate_filename(la, ws, wa):
	# generate file name 'la_ws_wa.csv'
	filename  = ''
	filename += to_3_digits_str(la)
	filename += "_"+ to_3_digits_str(ws)
	filename += "_"+ to_3_digits_str(wa)
	filename += ".csv"
	return filename

def generate_all_filenames_after(start_filename):
	filenames = []

	# if comes with a name, else do them all
	if start_filename:
		to_do = False
		la = int(start_filename[0:3])
		ws = int(start_filename[4:4+3])
		wa = int(start_filename[8:8+3])
	else:
		to_do = True

	#
	for la in launch_angle:
		for ws in wind_speed:
			for wa in wind_angle:
				filename = generate_filename(la, ws, wa)
				if to_do:
					filenames.append(filename)
				if filename == start_filename:
					to_do = True
	return filenames

def get_data_from_name(filename):
	all_filenames = generate_all_filenames_after(filename)
	for name in all_filenames:
		la = int(name[0:3])
		ws = int(name[4:4+3])
		wa = int(name[8:8+3])

		la_str = str(90 - la)

		mod = ws % 10
		ws_str = str(int((ws-mod)/10))
		if mod != 0:
			ws_str += '.'+str(mod)

		wa_str = str(wa)

		print(name)
		# print('\t',la_str,'\t',ws_str,'\t',wa_str)
		print(str(int(100 * all_filenames.index(name) / len(all_filenames))), '%')

		run_autoclick(la_str, ws_str, wa_str, name)

def run_autoclick(la_str, ws_str, wa_str, filename):
	global positions
	# new Simulation
	pyautogui.moveTo(positions[0][0], positions[0][1], sp_move)
	sleep(sp_after_move)
	pyautogui.click()
	sleep(sp_new_sim)

	# Wind Speed
	pyautogui.moveTo(positions[1][0], positions[1][1], sp_move)
	sleep(sp_after_move)
	pyautogui.click()
	sleep(sp_after_click)
	for _ in range(4):
		pyautogui.press('delete')
		sleep(sp_delete)
		pyautogui.press('backspace')
		sleep(sp_delete)
	pyautogui.write(ws_str, interval=sp_write)
	sleep(sp_after_move)
	pyautogui.press('enter')
	sleep(sp_after_enter)

	# Wind direction
	pyautogui.moveTo(positions[2][0], positions[2][1], sp_move)
	sleep(sp_after_move)
	pyautogui.click()
	sleep(sp_after_click)
	for _ in range(4):
		pyautogui.press('delete')
		sleep(sp_delete)
		pyautogui.press('backspace')
		sleep(sp_delete)
	pyautogui.write(str(wa_str), interval=sp_write)
	sleep(sp_after_click)
	pyautogui.press('enter')
	sleep(sp_after_enter)

	# unclick box
	pyautogui.moveTo(positions[3][0], positions[3][1], sp_move)
	sleep(sp_after_move)
	pyautogui.click()
	sleep(sp_after_click)

	# launch angle
	pyautogui.moveTo(positions[4][0], positions[4][1], sp_move)
	sleep(sp_after_move)
	pyautogui.click()
	sleep(sp_after_click)
	for _ in range(4):
		pyautogui.press('delete')
		sleep(sp_delete)
		pyautogui.press('backspace')
		sleep(sp_delete)
	pyautogui.write(la_str, interval=sp_write)
	sleep(sp_after_enter)
	pyautogui.press('enter')
	sleep(sp_after_enter)

	# launch direction
	pyautogui.moveTo(positions[5][0], positions[5][1], sp_move)
	sleep(sp_after_move)
	pyautogui.click()
	sleep(sp_after_click)
	for _ in range(3):
		pyautogui.press('delete')
		sleep(sp_delete)
		pyautogui.press('backspace')
		sleep(sp_delete)
	pyautogui.write(str(0), interval=sp_write)
	sleep(sp_after_enter)
	pyautogui.press('enter')
	sleep(sp_after_enter)

	# simulate
	pyautogui.moveTo(positions[6][0], positions[6][1], sp_move)
	sleep(sp_after_move)
	pyautogui.click()
	sleep(sp_simulate)

	# export data
	pyautogui.moveTo(positions[7][0], positions[7][1], sp_move)
	sleep(sp_after_move)
	pyautogui.click()
	sleep(sp_after_click)

	# export
	pyautogui.moveTo(positions[8][0], positions[8][1], sp_move)
	sleep(sp_after_move)
	pyautogui.click()
	sleep(sp_export)

	# filename Box
	pyautogui.moveTo(positions[9][0], positions[9][1], sp_move)
	sleep(sp_after_move)
	pyautogui.click()
	sleep(sp_after_click)
	pyautogui.write(filename, interval=sp_write)
	pyautogui.press('enter')
	sleep(sp_after_enter)

	# ok
	pyautogui.moveTo(positions[10][0], positions[10][1], sp_move)
	sleep(sp_after_move)
	pyautogui.click()
	sleep(sp_save_file)

	# # close
	# pyautogui.moveTo(x,y, sp_move)
	# sleep(sp_after_move)
	# pyautogui.click()
	# sleep(sp_after_click)

	sleep(sp_next_iter)


if __name__ == "__main__":
	print("Put a filename to run for the next ones, or dont put anything to do them all")
	argv = None
	try:
		argv = sys.argv[1]
	except:
		pass

	if argv and "config" in argv:
		config_positions()
	else:
		global positions
		positions = read_config()
		print("running ", len(generate_all_filenames_after(argv)), " simulations")
		get_data_from_name(argv)
