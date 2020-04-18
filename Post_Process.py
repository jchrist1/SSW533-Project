import os 
import csv 
import numpy as np
import matplotlib.pyplot as plt

# Helper function to parse the lizard file
def process_lizard_file(fileName):
	data = []
	with open(os.path.join('commit_output_files',fileName)) as lizardFile:
		for line in lizardFile:
			data.append(dict(zip(['NLOC','CCN','TOKEN','PARAM', 'Length'],line.split(',')[:5])))
		
		mc_array = np.array([int(x['CCN']) for x in data])
		LIF_array = np.array([int(x['Length']) for x in data])
		if mc_array.size > 1:
			return [np.mean(mc_array), np.amax(mc_array), np.true_divide(mc_array, LIF_array)[np.argmax(mc_array)]]

# Helper function to parse the pmccabe file
def process_pmccabe_file(fileName):
	data = []
	with open(os.path.join('commit_output_files',fileName)) as pmccabeFile:
		for line in pmccabeFile:
			data.append(dict(zip(['Mod_MC', 'MC', 'Statements', 'FOF', 'LIF', 'FN', 'FUNCT'], line.split())))

	#print (data)
	mc_array = np.array([int(x['MC']) for x in data])
	LIF_array = np.array([int(x['LIF']) for x in data])
	if mc_array.size > 1:
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
lizardData = []
pmccabeData = []
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
for file in lizardFiles:
	lizardData.append(process_lizard_file(file))

#print (pmccabeData)
for dataSet in [(pmccabeData, 'PMccabe'), (lizardData, 'Lizard')]:
	#Seperate the returns into seperate arrays
	mean_complexity = []
	max_complexity = []
	max_complexity_lif = []

	for record in dataSet[0]:
		if record is not None:
			mean_complexity.append(record[0])
			max_complexity.append(record[1])
			max_complexity_lif.append(record[2])

	x_axis = np.linspace(0, len(mean_complexity), len(mean_complexity))
	plt.figure(figsize=(12,4))
	plt.subplot(131)
	plt.plot(x_axis, mean_complexity, 'o')
	plt.ylabel('Average Complexity')
	plt.subplot(132)
	plt.plot(x_axis, max_complexity, 'r^')
	plt.ylabel('Max Complexity')
	plt.subplot(133)
	plt.plot(x_axis, max_complexity_lif, 'bs')
	plt.ylabel('Max Complexity/ lines in file')
	plt.suptitle('Complexity Introduced throughout the Project\n'+ dataSet[1] + ' Complexity Tool output')
	plt.show()