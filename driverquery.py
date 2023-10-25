import csv
from subprocess import Popen, PIPE
import locale


command = 'driverquery /fo csv'
output_file = 'driverquery.csv'
encoding = locale.getencoding()

with open(output_file, "w", newline='', encoding=encoding) as file:
    with Popen(command,  stdout=PIPE, stderr=PIPE) as p:
          output, errors = p.communicate()

    file.write(output.decode(encoding=encoding, errors='ignore'))

with open('driverquery.csv', newline='', encoding=encoding) as csvfile:
    driverquery = csv.reader(csvfile, delimiter=',')
    driverquery_fs = [driver[0] for driver in driverquery if driver[2].strip() == 'File System']
    print(driverquery_fs)
