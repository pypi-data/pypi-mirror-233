import subprocess
import sys
import os

def go_to_target_convert_val(dur_string, target_char, index):
    t_string = ''
    for index2, char in enumerate(dur_string[index:]):
        if char==target_char:
            break
        t_string += char

    return float(t_string), index+index2

def convert_to_seconds(dur_string):
    "Convert duration string from X:Y:Z or XhYmZs format to seconds"
    if ':' in dur_string:
        dur_list = dur_string.split(':')
        if len(dur_list) == 2:
            hours = 0
            minutes = float(dur_list[0])
            seconds = float(dur_list[1])
        else:
            hours = float(dur_list[-3])
            minutes = float(dur_list[-2])
            seconds = float(dur_list[-1])
    elif 'm' in dur_string:
        hours = 0.
        if 'h' in dur_string:
            hours, index = go_to_target_convert_val(dur_string, 'h', 0)
            minutes, index = go_to_target_convert_val(dur_string, 'm', index+1)
        else:
            minutes, index = go_to_target_convert_val(dur_string, 'm', 0)
        seconds, index = go_to_target_convert_val(dur_string, 's', index+1)

    else:
        raise ValueError(f"Passed in duration string {dur_string} must be in"
                         "the format Y:Z or X:Y:Z or YmZs or XhYmZs")

    return 3600*hours + 60*minutes + seconds

def get_video_duration(filename):
    ps = subprocess.Popen(('ffprobe', '-i', f'{filename}'), stderr=subprocess.PIPE) 

    with open('temp.txt','w') as tempfile:
        subprocess.run(('grep', 'Duration'), stdin=ps.stderr, stdout=tempfile) 

    with open('temp.txt','r') as tempfile:
        dur_string = tempfile.readline().split()[1].replace(',','')

    os.remove('temp.txt')

    return convert_to_seconds(dur_string)

def gvd():
    video_duration = get_video_duration(sys.argv[1])
    print(f"The video duration is {video_duration} seconds")

def cts():
    seconds = convert_to_seconds(sys.argv[1])
    print(f"{seconds} seconds")

if __name__ == '__main__':
    if sys.argv[1].lower() == 'file':
        duration = get_video_duration(sys.argv[2])
    elif sys.argv[1].lower() == 'dur_string':
        duration = convert_to_seconds(sys.argv[2])
    else:
        raise ValueError("Argument 1 must be either 'file' or 'dur_string'. "
                         "Argument 2 then must be either a video filename or a"
                         " correctly formatted duration string, respectively")
    print(f"Video is {duration} seconds long")
