from os import listdir, remove
import numpy as np
import pandas as pd
"""
processing.py
Developed By: Derek Johnston @ Texas Tech University

Special-purpose functions for data cleaning and pre-processing.
"""
def remove_ena_labels(filename):
	"""
	The Keysight ENA creates two extra lines of metadata at the 
	top of a measurement .CSV file. These should be removed so
	that datafiles can be imported into Pandas.
	
	Keyword Arguments:
	filename -- the file name (and path) to the .CSV to be cleaned.
	"""
	line_buffer = [] # Pull each line out of the file, and write back all but the last two.
	with open(f"{filename}.csv", "r") as fp:
		line_buffer = fp.readlines()
	with open(f"{filename}_t.csv", "w") as fp:
		for number, line in enumerate(line_buffer):
			if number >= 2:
				fp.write(line)

def process_ena_data(directory):
	"""
	For a given directory containing raw ENA data, process the data and generate
	new columns for the complex value, magnitude, and phase information.

	Keyword Arguments:
	directory -- The folder containing the datafiles.
	"""
	# Get a list of all the datafiles in the given directory.
	directories = listdir(directory)
	# Iterate through all the files in the directory.
	for file in directories:
		# Remove the .csv tag from the end of the file.
		file = file.replace(".csv", "")
		# Remove the ENA metadata lines.
		remove_ena_labels(f"{directory}\{file}")
		# Read-in the temporary file as a pandas dataframe.
		df = pd.read_csv(f"{directory}\{file}_t.csv")
		df.rename(columns={" Formatted Data": "Real", " Formatted Data.1": "Imag"}, inplace=True)
		# Get the complex number for each frequency component.
		df["Complex"] = [complex(df["Real"][idx], df["Imag"][idx]) for idx in df.index]
		# Get the magnitude and phase for each row of the dataframe.
		df["Magnitude"] = np.abs(df["Complex"].to_numpy())
		df["Phase"] 		= np.unwrap(np.angle(df["Complex"].to_numpy()))
		# Add the new processed file
		df.to_csv(f"{directory}_p\{file}.csv")
		# Remove the temporary data file.
		remove(f"{directory}\{file}_t.csv")
	
if __name__ == "__main__":
	process_ena_data("data")
