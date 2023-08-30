import os, csv
import spider_configs as sconfig

def check_if_file_empty():
	filenames = [
		sconfig.CARS_CSV_PATH, 
		sconfig.DETAILED_CARS_CSV_PATH, 
		sconfig.DATETIME_EXEC_PATH]
	for file in filenames:
		fullpath_file = sconfig.DATA_PATH+file

		# creates the file if it don't exists
		if not os.path.exists(fullpath_file):
			with open(fullpath_file, "w") as f:
				pass


			return True

		else:
			continue

	return False


def to_csv(list_to_write:list, filename:str):
	"""Writes the contents of a list to a CSV file.
	Args:
	list_to_write: The list of data to write to the CSV file.
	filename: The name of the CSV file to create.
	"""
	filename = sconfig.DATA_PATH + filename
	# Create the CSV file if it doesn't exist.
	if not os.path.exists(filename):
		with open(filename, "w") as f:
			pass

	# Write the contents of the list to the CSV file.
	with open(filename,"w", newline="", encoding="UTF-8") as file:
		writer=csv.writer(file)
		for line in list_to_write:
			writer.writerow([line])

def to_csv_next_column(
      csv_file:str, 
      list_to_write:list, 
      title:str, 
      clear_repeats=False):
	"""open an already existent csv file and put a list_to_write
   in the next column with the new column title recieved by the function caller"""
	import pandas as pd

	csv_file = sconfig.DATA_PATH + csv_file

	# Carregue o arquivo CSV existente
	df = pd.read_csv(csv_file)

	# print(f"Lista recebida: {list_to_write}")

	if clear_repeats:
		lista_nova = list(set(list_to_write))
		#  list_to_write = lista_nova
		# print(f"Duplicated Values: {list_to_write}")

	df[title] = list_to_write

	# Save updated data back in the csv file
	df.to_csv(csv_file, index=False)

   