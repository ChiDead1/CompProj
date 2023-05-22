#citations: got help from a classmate Alie
import argparse
import csv
import sys
import pymongo
import datetime as dt




def convert_to_string(localfiles):
    file_str = ""
    for file in localfiles:
        file_str += file
    return file_str
parser = argparse.ArgumentParser(description='Description of your program')
parser.add_argument('--baselight', metavar='filename', type=str, nargs='+',
                    help='Baselight/Flames text file(s) to process')
parser.add_argument('--xytech', metavar='filename', type=str, nargs=1,
                    help='Xytech file input')
parser.add_argument('--verbose', action='store_true',
                    help='turn on verbose console output')
parser.add_argument('--output', type=str, help='Output format: csv or db')


args = parser.parse_args()


if args.baselight is None:
    print("Error: No Baselight/Flames text file(s) provided.")
    sys.exit(1)


localFiles = args.baselight


if args.xytech is None:
    print("Error: No Xytech file input provided.")
    sys.exit(1)


client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client['ProjectTwoDatabase']


# Create the collections
user_data_collection = db['user_data']
file_data_collection = db['file_data']
xytechFile = args.xytech[0]


# Loop through each file in the local_files list
for file_name in localFiles:
    # Parse the file name to extract the machine, user, and date
    parts = file_name.replace('.txt', '').split('_')
    machine = parts[0]
    user = parts[1]
    date = parts[2]


    # Insert the user data into the user_data collection
    user_data_collection.insert_one({'user': user, 'machine': machine, 'file_user': parts[1], 'date': date, 'submitted_date': dt.datetime.utcnow()})


    #file_data_collection.insert_one({'file_user': user, 'date': date, 'location': xytechFile,  'frame_ranges': []})




if args.verbose:
    print("Processing Baselight/Flames files:")






# Open baselight files


it = ""
setRange = []
localFilesPath = []
locNum = []
fileNum = []
dataNumFile = []
fileDict = {}
data = {}


for fileName in localFiles:
    try:
        f = open(fileName, "r")
        for x in f:
            y = it.join(x)
            t = y.replace("/images1/","")
            w = t.split()
            pathnum = x.strip().split(" ")[1:]
            fileNum.append(pathnum)


            localFilesPath.append(t)
            locNum += pathnum
            path = x.strip().split(" ")[0]
            path_parts = path.split("/")
            filt_name = "/".join(path_parts[2:])
            localFile = filt_name.split('.')[0]
            localFiles.append(localFile)


            key = localFile
            parts = x.strip().split(" ")
            path1 = parts[0].replace("/images1/" ,"")


            numbers =  [int(x) for x in parts[1:]if x.isdigit() and x != "<null>" and x != "<err>"]


            ranges = sum((list(t) for t in zip(numbers, numbers[1:]) if t[0]+1 != t[1]), [])
            iranges = iter(numbers[0:1] + ranges + numbers[-1:])
            plzrange = ( ', '.join([str(n) + '-' + str(next(iranges)) for n in iranges]))


            setRange.append(plzrange)
            if key not in data:
             data[key] = numbers


            else:
                data[key].extend(numbers)
    except FileNotFoundError:
        print(" file :", fileName)


a = localFiles
print(a)




exclude = []
lineNumber = 8
produce =[]
f2 = xytechFile
file = open(f2, "r")
producers = []
locations = []
notes = []
other_lines = []


for line in file:
    if line.startswith("Producer"):
        producer = line.replace("Producer:", "").strip()
        producers.append(producer)
       
    elif line.startswith("Operator"):
        operator = line.replace("Operator:", "").strip()
        producers.append(operator)
       
    elif line.startswith("Job"):
        job = line.replace("Job:", "").strip()
        producers.append(job)
       
    elif line.startswith("/ddnsata"):
        location = line.strip()
        locations.append(location)
        values = location.split(" ")
       
    elif line.startswith("Notes"):
        note = line.replace("Notes:", "").strip()
        notes.append(note)
       
    else:
        other_lines.append(line.strip())


final_dict = {}
final_path = []
dict_files = {}




# locations of data
for location in locations:
    for key in data:
        if location.endswith(key):
            final_key = location
            final_value = data[key]
           
            if final_key not in final_dict:
                final_dict[final_key] = final_value
            else:
                final_dict[final_key].extend(final_value)


print("Dictionary")
for ele in final_dict:
    print(f"{ele} {final_dict[ele]}")


# Split  ranges of number and string list
string_list = []
number_list = []
for key, value in final_dict.items():
    value_ranges = []
    start = end = value[0]
    for i in range(1, len(value)):
        if value[i] == start + 1:
            start = value[i]
        else:
            value_ranges.append((end, start))
            start = end = value[i]
    value_ranges.append((start, end))
    for vr in value_ranges:
        if vr[0] == vr[1]:
            number_list.append(str(vr[0]))
        else:
            number_list.append(f"{vr[0]}-{vr[1]}")
        string_list.append(key)


k = 0
while k < len(string_list):
    print(string_list[k], number_list[k])
    k += 1


# make CSV file
if args.output == 'csv':
    with open("Project1.csv", "w", newline="") as csvfile:
        fields = ["Producer: ", "Operator: ", "Job: ", "Notes: "]
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writeheader()
       
        filename = ["File"]
        write = csv.writer(csvfile)
        split_dr = ["directory", "ranges"]
        last_write = csv.DictWriter(csvfile, fieldnames=split_dr)
        j = 0
        for combined in string_list:
            last_write.writerow({"directory": string_list[j], "ranges": number_list[j]})
            j += 1
        print("Output saved to Project1.csv")


file_path = 'Project1.csv'


import csv


# Open the CSV file and read its contents
with open(file_path, newline='') as csvfile:
    csv_reader = csv.reader(csvfile)
    header = next(csv_reader)  # Skip the header row
    frame_ranges = []
    for row in csv_reader:
        # Check that the row has at least 1 value before accessing index 1
        if len(row) >= 1:
            # Check that the row has at least 2 values before accessing index 1 and 2
            if len(row) >= 2:
                # Extract the start and end frames from each row
                # If the frames are in columns 1 and 2, respectively
                if '-' in row[1]:
                    start_frame, end_frame = row[1].split('-')
                    start_frame = int(start_frame)
                    end_frame = int(end_frame)
                else:
                    start_frame = int(row[1])
                    end_frame = int(row[1])


                # Check that the row has at least 3 values before accessing index 2
                if len(row) >= 3:
                    frame_info = f"{row[0]}:{row[1]}-{row[2]}"
                else:
                    frame_info = f"{row[0]}:{row[1]}"
                   
                frame_ranges.append(frame_info)
            else:
                # Handle rows with only 1 value
                frame_ranges.append(f"{row[0]}")
        else:
            continue


    # Insert the data into MongoDB
    file_data_collection.insert_one({
        'file_user': user,
        'date': date,
        'location': xytechFile,
        'frame_ranges': frame_ranges
    })











