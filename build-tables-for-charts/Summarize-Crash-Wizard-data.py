
import csv
import collections
import sys

csvfile = open(sys.argv[1])
input_data = csv.reader(csvfile, delimiter=',', quotechar='"')
#input_data = csv.reader(csvfile, delimiter='\t', quotechar='"')
headers = next(input_data)
headers.append('COLLISION')
out_data = open('data.csv', 'w')
output_data = csv.writer(out_data)
output_data.writerow(headers)
for row in input_data:
    output_data.writerow(row+[1])


out_data.close()

fields = ["COLLISION", "KILLED", "INJURED"]
for field in fields:
    reader = csv.DictReader(open('data.csv'))
    bymonth = collections.defaultdict(int)
    for row in reader:
        if row['COLLISION DATE'][1] == "/":
            date = "0"+row['COLLISION DATE'][0]
        else:
            date = row['COLLISION DATE'][0:2]
        bymonth[date] += int(row[field])

    orderedmonth = sorted(bymonth.items())
    writer = csv.writer(open(field + '.csv', 'w'))
    writer.writerow(["MONTH", field])
    for x, y in orderedmonth:
        writer.writerow([x, y])

