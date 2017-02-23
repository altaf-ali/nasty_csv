import csv
import os
from itertools import chain

def columize(fname):
	with open(fname, 'rU') as csvfile:
		reader = csv.reader(csvfile, delimiter=',', dialect=csv.excel_tab)
		
		# # # Skip preamble
		for _ in xrange(6):
			reader.next()

		#Print header
		header = reader.next()
		print(header)

		for row in reader:
			print(row)
			return

		#Return header and list of lists

		#We need to know the structure of internal structure to make header
		first_data_row = reader.next()

		new_headers = []
		for header, cell in zip(header, first_data_row):
			
			if '[' in cell:
				# We're in a list
				for i, list_element in enumerate(cell.split(' ')):
					new_headers += [(header + '_' + str(i)).replace('[', '').replace(']', '')]
			else:
				new_headers += [header.replace('[', '').replace(']', '')]

		new_rows = []
		for data in chain([first_data_row], reader):
			new_row = []
			for cell in data:
				if '[' in cell:
					# we have a list
					for list_element in cell.split(' '):
						new_row += [list_element.replace('[', '').replace(']', '')]
				else:
					new_row += [cell]
			new_rows.append(new_row)
		return new_headers, new_rows

# [[9, 6, 4, True, [ 1 2 3 ]], ...]
# [[9, 64, True, 1, 2, 3], [4, 64, True, ...], ...]

def write_csv(new_headers, new_rows, filename):
	with open(filename, 'wb') as csvfile:
	    csvwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
	    csvwriter.writerow(new_headers)
	    for row in new_rows:
			csvwriter.writerow(row)

PREAMBLE = '/Users/miranda/Google Drive/RemainingCsvs/H2_H_PC/'
MAPPING = {
 			#PREAMBLE +'mergedAug21/merged_IHS10.csv': PREAMBLE + 'mergedAug21/merged_IHS_ST_FAM10.csv',
 			#PREAMBLE +'merged/merged_Illegal_VAL.csv': PREAMBLE + 'merged/merged_Illegal_VAL_output.csv',

			}

def run():
	for candidate in os.listdir(PREAMBLE):
		if 'csv' in candidate:
			new_headers, new_rows = columize(PREAMBLE +'H2_HOFF_PUNIF/merged_H2_HOFF_PUNIF.csv')
			write_csv(new_headers, new_rows, PREAMBLE + 'H2_HOFF_PUNIF/merged_H2_HOFF_PUNIF_output.csv')
			#new_headers, new_rows = columize(PREAMBLE +'mergedAug21/merged_IHS_ST_FAM.csv')
			#write_csv(new_headers, new_rows, PREAMBLE + 'mergedAug21/TEST2.csv')

if __name__ == '__main__':
 	run()