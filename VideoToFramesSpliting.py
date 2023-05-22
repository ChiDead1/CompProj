#citations got lots of help from al

import argparse
import csv
import datetime
import os
import re
import pymongo
import subprocess
import sys
import cv2
import xlsxwriter
print("FML")

def main(input, outputarg):
    testkey = [] 
    frames = "frames"
    print("works")
    print(f"Processing video file: {input}")
    input_file = "video.mp4"
    output = "/Users/nhann/Desktop/python/Python-Scripting-Project-main/data/Project2/"
    start_frame = 0
    end_frame = 11000
    frame_rate = 1
    output_dir = os.path.join(output, 'frames')
 
    video_file = input
    cap = cv2.VideoCapture(video_file) 

    frame_number = 0
    frame_list= []
 
    frame_directory = "/Users/nhann/Desktop/python/Python-Scripting-Project-main/data/Project2/frames"
    png_files = [f for f in os.listdir(frame_directory) if f.endswith('.png')]
    frame_pattern = re.compile(r'frame(\d{4})\.png')
    #connect()
    
    frame_list = [int(frame_pattern.search(f).group(1)) for f in png_files if frame_pattern.search(f)]
    #file_numbers = set
    #xytech = []
    xytech_dict = {}
  
    max_frame_num = max(frame_list)
    print(max_frame_num)
    client = pymongo.MongoClient("mongodb://localhost:27017/")
  
    mydb = client['ProjectTwoDatabase']
    filesub = mydb["files"]
    mycollection = mydb["user_data"]
    collection2 = mydb["file_data"]
    xytechbasenumfiles =[]
    newlist = []
    filepaths = []
    filerange = []
    testing = {}
    for entry in collection2.find({}, {"Files to Fix": 1}):
        files_to_fix = entry.get("Files to Fix", [])
        
        xytechbasenumfiles.append(files_to_fix)
    
    print(f'{files_to_fix}\n')
    print("\n")

    for eachpath in xytechbasenumfiles:
        for path in eachpath:
            split_value = path.split()
            keypath = split_value[0]
            numrange = split_value[1]
            if keypath in xytech_dict:
                xytech_dict[keypath].append(numrange)
            else:
                xytech_dict[keypath] = [numrange]
    
    print("outside of test")
    print("\n")
    for key, value in xytech_dict.items():
        print(f"Key: {key}, Value: {value}")
    new_frames_hmap = {}
    for document in collection2.find():
      
        if "Files to Fix" in document:
           
            for path in document["Files to Fix"]:
                path_parts = path.split()
                if len(path_parts) == 2:
                    location, frame_range = path_parts
                    testkey.append(location)
                    if "-" not in frame_range:
                        # Case of single frame number
                        frame_num = int(frame_range)
                        if frame_num <= max_frame_num:
                            if location not in new_frames_hmap:
                                new_frames_hmap[location] = []
                            new_frames_hmap[location].append([frame_num])
                    else:
                        # Case of frame range
                        start, end = frame_range.strip('[]').split('-')
                        if int(end) <= max_frame_num and int(start) <= max(frame_list):
                            if location not in new_frames_hmap:
                                new_frames_hmap[location] = []
                            new_frames_hmap[location].append(list(range(int(start), int(end) + 1)))

    

   
    print('this is the hmap\n')

    
    for key, value in new_frames_hmap.items():
        print(f"Key: {key}, Value: {value}")
   
    for entry in mydb.collection2.find({}, {"Files to Fix": 1}):
        files_to_fix = entry.get("Files to Fix", [])
        for file in files_to_fix:
          path, *nums = file.split()
          if not nums:
            continue
          nums = nums[0].strip("[]")
          if "-" in nums:
            start, end = nums.split("-")
            start, end = int(start), int(end)
            if end <= max_frame_num:
                xytech_dict[path] = list(range(start, end + 1))
          else:
            num = int(nums)
            if num <= max_frame_num:
                xytech_dict[path] = [num]
              
    
    for doc in collection2.find():
        if "Files to Fix" in doc:
            for each in doc["Files to Fix"]:
         
                 
                 print(each)
                 path_and_numbers = each.strip().split(" ")
             
                 print("Path and numbers", path_and_numbers)
                 path = path_and_numbers[0]
                 numbers = path_and_numbers[1]
                
                 if len(path_and_numbers) >= 2:
                    path = ' '.join(path_and_numbers[:-1])

                    numbers = path_and_numbers[-1]
                       
                     
                    xytech_dict[path] = numbers

                 each = each.strip() 
                 parts = each.split(' ')  
                 if len(parts) > 1:
                      path = parts[0]
                      nums = parts[1]
                      nums = nums.strip('[]')  
                      nums = nums.replace('-', ':') 
                      nums = nums.split(':')  
                      nums = [int(num) for num in nums] 
                      num_range = list(range(nums[0], nums[-1]+1))  
              

    else:
        print("No frame_ranges field found in the document with _id:", doc["_id"])
    
    
    testdict = {}
    testval = set()
    for key, value in xytech_dict.items():
        for i in range(len(value)):
            if '-' in value[i]:
                start, end = value[i].strip('[]').split('-')
                value[i] = list(range(int(start), int(end)+1))
    
        
                testdict[key] = value
          
    testval = set()
    for key, value in xytech_dict.items():
        modified_value = []
        for item in value:
            if '-' in item:
                start, end = item.strip('[]').split('-')
                modified_value.extend(list(range(int(start), int(end) + 1)))
        if modified_value:
            testdict[key] = modified_value

    testval = set()
    for key, value in xytech_dict.items():
        modified_value = []
        for item in value:
            if '-' in item:
                start, end = item.strip('[]').split('-')
                modified_value.extend(filter(lambda x: x <= 5918, range(int(start), int(end) + 1)))
        if modified_value:
            testdict[key] = modified_value
    print("testdict")
    #print(testdict)
    for key, value in testdict.items():
        print(f"Key: {key}, Value: {value}")

   
    print("\n")
    fps = get_fps(input)
    print("\n")
    print("FPS: ",fps)
    lengthofvid = get_vid_length(input)
    print("\n")
    print("Length of video: ",lengthofvid)
    fpscheck = int(fps * lengthofvid)
    print("\n")
    print("FPSCHECK: ",fpscheck)
    testval = []
    
    for key, value in testdict.items():
        for item in value:
         if isinstance(item, list):
            for sub_item in item:
                testval.append(sub_item)
         else:
            testval.append(item)
    testval = list(set(testval))
    print("Value Check: ")
    print("\n")
    print(sorted(testval))

    
    deci_seconds = list(set([frame_number/fps for frame_number in  testval]))

    deci_seconds.sort()

    print("fucken timecode stop being a bitch")
    timecode = convert_frames_to_timecodes(testval, fps)

    print("\n")
    print("\n",sorted(timecode))
 
    
    print("\n")

    print(len(testkey))
    print(len(testval))
    print(len(timecode))

    print("\n")
   
    
    if outputarg == "csv": 
        print("CSV File output\n")
        #f = open("project.csv", "x")
        with open("project3.csv", "w", newline="") as csvfile:
            fields= ["Location", "Ranges", "Timecode", "Thumbnail"]
            thewriter = csv.DictWriter(csvfile, fieldnames=fields)
            thewriter.writeheader()

    elif args.output == "xls":
        print("XLS output")
        workbook = xlsxwriter.Workbook("project3.xlsx")
        worksheet = workbook.add_worksheet()
        worksheet.write(0, 0, "Location")
        worksheet.write(0, 1, "Ranges")
        worksheet.write(0, 2, "Timecode")
        worksheet.write(0, 3, "Thumbnail")
        worksheet.set_column(0, 200, 50)
        video_file = input
        sorted_dict = sorted(xytech_dict.items(), key=lambda x: x[0])
        
        row = 0
        for key, value in sorted_dict:
            location = key
            ranges = []

            for frame in value:
                if '-' in frame:
                    start, end = frame.strip('[]').split('-')
                    start_num = int(start)
                    end_num = int(end)
                    ranges.append(f"{start_num}-{end_num}")
                else:
                    frame_num = int(frame)
                    ranges.append(f"{frame_num}")

                worksheet.write(row, 0, location)
                for each in ranges:
                 #' '.join(ranges)
                 worksheet.write(row, 1,each)
                 row += 1
        workbook.close()
        row = 1
        for key, value in xytech_dict.items():
            location = key
            ranges = []

            for frame in value:
                if '-' in frame:
                    start, end = frame.strip('[]').split('-')
                    start_num = int(start)
                    end_num = int(end)
                    ranges.append((start_num, end_num))
                else:
                    frame_num = int(frame)
                    ranges.append((frame_num, frame_num))

            sorted_ranges = sorted(ranges, key=lambda x: x[0])
            sorted_ranges_formatted = [f"[{start}-{end}]" if start != end else f"[{start}]" for start, end in sorted_ranges]
            

            worksheet.write(row, 0, location)
            for each in sorted_ranges_formatted:
                worksheet.write(row, 1, each)
                row += 1
            
        ranges_dict = {}
        row = 1
        
        for key, value in testdict.items():
            location = key
            ranges = []

            
            sorted_frames = sorted(value)

            start_frame = sorted_frames[0]
            end_frame = sorted_frames[0]
            for frame in sorted_frames[1:]:
                if frame == end_frame + 1:
                    end_frame = frame
                else:
                    ranges.append((start_frame, end_frame))
                    start_frame = frame
                    end_frame = frame

            
            ranges.append((start_frame, end_frame))

            ranges_formatted = [f"[{start}-{end}]" if start != end else f"[{start}]" for start, end in ranges]
            ranges_dict[location] = ranges_formatted

       
        sorted_items = sorted(ranges_dict.items(), key=lambda x: (min(int(val[1:-1].split('-')[0]) for val in x[1])))

        for location, ranges in sorted_items:
            
            print(f"Key: {location}, Value: {ranges}") 
            #frame_timecodes = [timecode[frame] for start, end in ranges for frame in range(start, end + 1)]
            #print(f"Key: {location}, Value: {ranges}, Timecodes: {frame_timecodes}")
            worksheet.write(row, 0, location)
            for each in ranges:
                worksheet.set_row(row, 90)
                worksheet.write(row, 1 ,each)
                worksheet.write(row, 0, location)
                row += 1
        column = 1
        
        print("ranges")
        
        finaltimecode= []
        storestart = []
        
        for location, ranges in sorted_items:
            for range_str in ranges:
                
                start, end = map(int, range_str.strip('[]').split('-'))
                middle_number = (start + end) // 2
               
                storestart.append(middle_number)
                
                print("middle#",middle_number)
                print(start)
                print(end)
                
                start_indices = [i for i, val in enumerate(testval) if val == start]
                end_indices = [i for i, val in enumerate(testval) if val == end]
                print(f"Range {range_str}: Start Indices = {start_indices}, End Indices = {end_indices}")
                for eachl in start_indices:
                    
                    
                    for eachr in end_indices:
                        start_timecode = timecode[eachl]
                        end_timecode = timecode[eachr]
                        print(start_timecode)
                        print(end_timecode)
                        timecode_range = (f"{start_timecode}/{end_timecode}")
                        finaltimecode.append(timecode_range)
            
        
        match_number = [start_val for start_val in storestart if start in frame_list]
        print(storestart)
        
        matchingpng_files = []
        
        for every in match_number:
            matching_files = [f for f in os.listdir(frame_directory) if f.endswith(f'{str(every).zfill(4)}.png')]
            matchingpng_files.extend(matching_files)
        

        print(len(match_number))
        print("# of png")
        print(len(matchingpng_files))

        for eachlr in finaltimecode:
            worksheet.write(column, 2 ,eachlr)
            column +=1

       
        matching_numbers = [x for x in testval if x in frame_list]
        print("matchnumber")
        print(match_number)
       
        print(matchingpng_files)
        thirdrow = 1
        

        for image_file in matchingpng_files:
            image_path = "/Users/nhann/Desktop/python/Python-Scripting-Project-main/data/Project2/frames/" + image_file
            worksheet.insert_image(thirdrow, 3, image_path,{'x_scale': 0.1, 'y_scale': 0.1,'width': 30, 'height': 30})
            thirdrow+=1

        
        workbook.close()
  
def get_fps(video_path):
    cmd = ['ffprobe', '-v', 'error', '-select_streams', 'v', '-of', 
           'default=noprint_wrappers=1:nokey=1', '-show_entries', 
           'stream=r_frame_rate', video_path]
    output = subprocess.check_output(cmd).decode('utf-8').strip()
    if '/' in output:  # Frame rate might be a ratio, so we compute it
        num, den = output.split('/')
        return float(num) / float(den)
    else:
        return float(output)

def get_vid_length(input):
    video = input
    command = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", video]
    x = float(subprocess.check_output(command))
    return x


def convert_frames_to_timecodes(frames, fps):
    timecodes = []
    for frame in frames:
        total_seconds = frame / fps
        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)
        seconds = int(total_seconds % 60)
        deci_seconds = round((total_seconds - int(total_seconds)) * fps)
        timecodes.append(f"{hours:02d}:{minutes:02d}:{seconds:02d}:{deci_seconds:02d}")
    return timecodes


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='OpenCV video processing')
    parser.add_argument('-p', "--process", help='full path to input video that will be processed')
    parser.add_argument("--output", choices=["csv", "xls"])
    args = parser.parse_args()

    if args.process is None:
    # or args.output is None:
        sys.exit("Please provide path to input and output video files! See --help")

    main(args.process, args.output)