import os
import csv

def ensure_csv_file_exists(file_path, headers):
    """ Ensure that the specified CSV file exists with the given headers. """
    if not os.path.exists(file_path):
        with open(file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(headers)
