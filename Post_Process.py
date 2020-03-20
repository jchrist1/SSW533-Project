import os 
import csv 
import numpy as np
import matplotlib.pyplot as plt

pmccabeData = []
# Helper function to parse the lizard file
def process_lizard_file(fileName):
	print (fileName)

# Helper function to parse the pmccabe file
def process_pmccabe_file(fileName):
	data = []
	with open(os.path.join('commit_output_files',fileName)) as pmccabeFile:
		for line in pmccabeFile:
			data.append(dict(zip(['Mod_MC', 'MC', 'Statements', 'FOF', 'LIF', 'FN', 'FUNCT'], line.split())))

	#print (data)
	mc_array = np.array([int(x['MC']) for x in data])
	statements_array = np.array([int(x['Statements']) for x in data])
	LIF_array = np.array([int(x['LIF']) for x in data])

	return [np.mean(mc_array), np.amax(mc_array), np.true_divide(mc_array, LIF_array)[np.argmax(mc_array)]]

def plot_pmccabe_file(fileName):
	data = []
	with open(os.path.join('commit_output_files',fileName)) as pmccabeFile:
		for line in pmccabeFile:
			data.append(dict(zip(['Mod_MC', 'MC', 'Statements', 'FOF', 'LIF', 'FN', 'FUNCT'], line.split())))

	#print (data)
	mc_array = np.array([int(x['MC']) for x in data])
	statements_array = np.array([int(x['Statements']) for x in data])
	LIF_array = np.array([int(x['LIF']) for x in data])

	x_axis = np.linspace(0, len(mc_array), len(mc_array))
	plt.plot(x_axis, mc_array, 'o')
	plt.plot(x_axis, statements_array, 'o')
	plt.plot(x_axis, LIF_array, 'o')
	plt.plot(x_axis, np.true_divide(mc_array, LIF_array), 'o')
	plt.show()


lizardFiles = []
pmccabeFiles = []
# Loop through the file names and call the helper functions 
for file in os.listdir('commit_output_files'):
	if 'lizard' in file:
		lizardFiles.append(file)
	elif 'pmccabe' in file:
		pmccabeFiles.append(file)
	else:
		print ("File name " + file + " not recognized")
lizardFiles.sort(key=lambda file: int(file.split('_')[1].split('.')[0]))
pmccabeFiles.sort(key=lambda file: int(file.split('_')[1].split('.')[0]))

for file in pmccabeFiles:
	pmccabeData.append(process_pmccabe_file(file))

plot_pmccabe_file(pmccabeFiles[0])
plot_pmccabe_file(pmccabeFiles[-1])