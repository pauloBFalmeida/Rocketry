import csv
import pyautogui

# On 'Export data' field 'Comments', must be checked on:
	# Include field description
	# Include flight events

headers_line_in_csv = 0 	# Include simulation description: Off
# headers_line_in_csv = 6 	# Include simulation description: On

csv_filename  = 'saida.csv'


# 83 a 87 de 1 em 1
launch_angle = [i for i in range(83,88,1)]
# 0 a 90 de 10 em 10,
#	100 a 150 de 25 em 25
wind_speed   = [i*10 for i in range(0,10, 1)] + [i for i in range(100,151, 25)]
# 0 a 270 de 90 a 90
wind_angle   = [i for i in range(0,271, 90)]

# return vector
# 		[altitude       (m),
# 		 position East  (m),
# 		 position North (m),
# 		 Stability]
def get_important_collumns(collumn):
	return [
		collumn[col_altitude],
		collumn[col_posEast],
		collumn[col_posNorth],
		collumn[col_stability]
	]

# return vector
# 		[(LAUNCHROD , get_important_collumns),
# 		 (BURNOUT  , get_important_collumns),
# 		 (APOGEE   , get_important_collumns),
# 		 (GROUNDHIT, get_important_collumns)]
def extract(rows):
	# === Get headers positions on collumns ===
	headers = rows[headers_line_in_csv -1]

	global col_altitude
	global col_posEast
	global col_posNorth
	global col_stability

	col_altitude = 0
	col_posEast  = 1
	col_posNorth = 2
	col_stability = 1

	for i in range(len(headers)):
		header = headers[i]
		if 'Altitude' in header:
			col_altitude = i
		if 'Position East' in header:
			col_posEast  = i
		if 'Position North' in header:
			col_posNorth = i
		if 'Stability' in header:
			col_stability = i

	# === Find info in csv ===
	vector_out = [None for _ in range(4)]

	for i in range(len(rows)-1):
		row = rows[i]
		# get the collumns in the next row (where the values are)
		collumns = rows[i+1]

		# LAUNCHROD
		if '# Event LAUNCHROD occurred' in row[0]:
			vector_out[0] = get_important_collumns(collumns)

		# BURNOUT
		if '# Event BURNOUT occurred' in row[0]:
			vector_out[1] = get_important_collumns(collumns)

		# APOGEE
		if '# Event APOGEE occurred' in row[0]:
			vector_out[2] = get_important_collumns(collumns)

		# SIMULATION_END same as GROUND_HIT (but it comes after)
		if '# Event SIMULATION_END occurred' in row[0]:
			vector_out[3] = get_important_collumns(collumns)

	return vector_out

def to_3_digits_str(number):
	out = ""
	if number < 10:
			out += "0"
	if number < 100:
		out += "0"
	out += str(number)
	return  out

headers_names = [ 	"Launch Pad",
				 	"Burnout",
					"Apogee",
					"Ground Hit"
				]

atributes_names = [	'Altitude',
					'Position East',
					'Position North',
					'Stability'
				  ]

def get_info_from_vector_out(vector_out):
	info = []

	# Launch Pad Stability
	info.append( (	headers_names[0],
					atributes_names[3],
					vector_out[0][3]	)
				)

	# Burnout Altitude
	info.append( (	headers_names[1],
					atributes_names[0],
					vector_out[1][0]	)
				)
	# Burnout Stability
	info.append( (	headers_names[1],
					atributes_names[3],
					vector_out[1][3]	)
				)

	# Apogee Altitude
	info.append( (	headers_names[2],
					atributes_names[0],
					vector_out[2][0]	)
				)

	# Ground Hit Position East
	info.append( (	headers_names[3],
					atributes_names[1],
					vector_out[3][1]	)
				)
	# Ground Hit Position North
	info.append( (	headers_names[3],
					atributes_names[2],
					vector_out[3][2]	)
				)

	return info

def start_text_file(filename):
	total_data = [	[],
					[],
					[],
					[]  ]

	text_out = "Laun_Ang  Wind_Spe Wind_Ang\n"
	for h in headers_names:
		text_out += h + '\t' + str(['Altitude', 'Position East', 'Position North', 'Stability']) + '\n'
	text_out += '\n'

	# append to file
	with open('saidas.txt', 'a') as f:
		f.write(text_out)

def output_text_file(simulation_numbers, vector_out, text_filename):
	text_out = ""
	# data that we want
	# LAUNCHROD			[0]
		# Stability 		[3]
	text_out += 'LAUNCHROD Stability: '+ str(vector_out[0][3]) +'\n'

	# BURNOUT			[1]
		# Altitude 			[0]
		# Stability 		[3]
	text_out += 'BURNOUT   Altitude : '+ str(vector_out[1][0]) +'\n'
	text_out += 'BURNOUT   Stability: '+ str(vector_out[1][3]) +'\n'

	# APOGEE			[2]
		# Altitude 			[0]
	text_out += 'APOGEE    Altitude : '+ str(vector_out[2][0]) +'\n'

	# GROUND_HIT		[3]
		# position East 	[1]
		# position North 	[2]
	text_out += 'GROUND   Pos East  : '+ str(vector_out[3][1]) +'\n'
	text_out += 'GROUND   Pos North : '+ str(vector_out[3][2]) +'\n'

	text_out += '\n'

	# append to text file
	with open(text_filename, 'a') as f:
		f.write(text_out)



def output_csv_file(all_data, csv_filename):
	all_launch_angles_data = [[] for _ in range(88)]
	all_launch_angles_temp = [[] for _ in range(88)]

	for data in all_data:
		la = data[0][0]
		all_launch_angles_temp[la].append(data)

	for angle_temp in all_launch_angles_temp:
		if len(angle_temp) > 1:
			# la from the first item
			la = angle_temp[0][0][0]
			#
			wind_angle_data = [[] for _ in range(4)]
			for data in angle_temp:
				wa = data[0][2]
				angle =  wa//90	# 0,1,2,3 from 0,90,180,270
				wind_angle_data[angle].append(data)
			#
			all_launch_angles_data[la] = wind_angle_data

	# all_launch_angles[la] = [wind_angles[0..3 from 0,90,180,270] ]

	with open(csv_filename, 'w', encoding='utf-8') as file:
		writer = csv.writer(file)

		for wa in wind_angle:
			# Launch Angle Row
			launch_angle_row = []
			for la in launch_angle:
				# launch_angle_row += ['Angulo de lancamento:', str(la), '', '', '', '', '', '']
				launch_angle_row += ['Angulo de lancamento:', str(la), '', '', '']
				launch_angle_row += ['\t']	# space


			writer.writerow(launch_angle_row)

			# Atributes row
			atributes_row = []
			for _ in launch_angle:
				atributes_row += ['Angulo do vento', 'Velocidade do vento']
				# atributes_row += ['', 'Burnout altitude (m)', '', '', 'Ground Posicao Leste (m)', 'Ground Posicao Norte (m)', '']
				atributes_row += ['Burnout altitude (m)', 'Ground Posicao Leste (m)', 'Ground Posicao Norte (m)']
				atributes_row += ['\t']	# space

			writer.writerow(atributes_row)

			# Wind speeds rows
			for ws in wind_speed:
				row = []
				for i in range(len(launch_angle)):
					# string of ws in float
					mod = ws %10
					ws_str = str((ws - mod) // 10)
					if mod != 0:
						ws_str += ',' + str(mod)

					# first row receives wing angle in first collumn
					if ws == 0:
						row += [str(wa)]
					else:
						row += ['']
					#
					row += [ws_str]

					# info for this la, ws, wa
					info = None
					for data in all_launch_angles_data[la][wa//90]:
						ws_data = data[0][1]
						if ws == ws_data:
							info = data[1]

					# info = [
					# 		0 ( Launch Pad, 	Stability, 		value )
					# 		1 ( Burnout, 	  	Altitude,		value )
					# 		2 ( Burnout, 		Stability, 		value )
					# 		3 ( Apogee, 		Altitude,		value )
					# 		4 ( Ground Hit, 	Position East,	value )
					# 		5 ( Ground Hit,		Position North, value )
					#         ]

					info_Burnout_Altitude = str(info[1][2]).replace('.',',')
					info_Ground_Pos_Leste = str(info[4][2]).replace('.',',')
					info_Ground_Pos_Norte = str(info[5][2]).replace('.',',')

					row += [	info_Burnout_Altitude,
								info_Ground_Pos_Leste,
								info_Ground_Pos_Norte
							]

					# space
					row += ['\t']
				writer.writerow(row)
			writer.writerow([])



if __name__ == "__main__":
	# creates new text file
	with open(text_filename, 'w') as f:
		f.write("")
	start_text_file(text_filename)

	all_data = []

	for la in launch_angle:
		for ws in wind_speed:
			for wa in wind_angle:
				# generate file name 'CSVs/la_ws_wa.csv'
				filename = 'CSVs/'
				filename += to_3_digits_str(la)
				filename += "_"+ to_3_digits_str(ws)
				filename += "_"+ to_3_digits_str(wa)
				filename += ".csv"

				# read file
				rows = []
				print(filename)
				with open(filename, 'r', encoding="utf-8") as file:
					csvreader = csv.reader(file)
					for row in csvreader:
						rows.append(row)

				# extract info from file
				vector_out = extract(rows)
				# print(vector_out)

				simulation_numbers = to_3_digits_str(la)+"_"+ to_3_digits_str(ws)+"_"+ to_3_digits_str(wa)

				# # write in txt 'text_filename'
				# output_text_file(simulation_numbers, vector_out, text_filename)


				# Write to csv
				all_data.append( ( (la, ws, wa),
									get_info_from_vector_out(vector_out))
								)


	output_csv_file(all_data, csv_filename)