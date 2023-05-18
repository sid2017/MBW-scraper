import csv
import re

def overwrite_with_pattern(csv_file, regex_pattern):
    output_rows = []
    with open(csv_file, 'r', encoding='utf-8-sig') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) > 0:
                first_cell = row[0]
                regex_result = re.search(regex_pattern, first_cell)
                if regex_result:
                    row[0] = regex_result.group()
            output_rows.append(row)

    with open(csv_file, 'w', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file)
        writer.writerows(output_rows)

# Usage example
csv_file = 'melanchton.csv'
regex_pattern = r'MBW <span>[a\d]*'
overwrite_with_pattern(csv_file, regex_pattern)
print("Regular expression pattern overwritten successfully in the first column of the CSV file.")
