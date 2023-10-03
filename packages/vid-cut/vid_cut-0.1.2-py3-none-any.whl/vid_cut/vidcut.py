"""
Usage:
    vidcut (--in=<in_file>) (--out=<out_file>) [--maintain|--subtractive] (--start=<start_t> --end=<end_t>)...
"""
from docopt import docopt
from vid_cut.get_video_duration import get_video_duration, convert_to_seconds
from vid_cut.build_ffmpeg import build_ffmpeg_cmd

arguments = docopt(__doc__, version='Video cut 0.1.0')

def is_int(val):
    try:
        new_val = int(val)
        return True
    except:
        return False

def enforce_mode(arguments):
    """Enforce that the script is being run in a specific mode (maintain or
    subtractive). If neither is specified, set it to maintain."""
    if not arguments['--maintain'] and not arguments['--subtractive']:
        arguments['--maintain'] = True

def convert_times_to_seconds(arguments):
    """Convert all times to seconds, but also, add a dictionary to 'arguments',
    that specifies the list index of 'start' or 'end' if they were ever
    specified, so that the downstream function call can construct the correct
    ffmpeg command."""
    if 'start_end_index' not in arguments.keys():
        arguments['start_end_index'] = {}

    for index, start_t in enumerate(arguments['--start']):
        if start_t == 'start':
            arguments['--start'][index] = 0.
            arguments['start_end_index']['start'] = index
        if arguments['--end'][index] == 'end':
            arguments['--end'][index] = get_video_duration(arguments['--in'])
            arguments['start_end_index']['end'] = index

        if not is_int(start_t) and start_t != 'start':
            arguments['--start'][index] = convert_to_seconds(start_t)
        if not is_int(arguments['--end'][index]) and arguments['--end'][index] != 'end':
            arguments['--end'][index] = convert_to_seconds(arguments['--end'][index])

def sort_time_points(arguments):
    convert_times_to_seconds(arguments)
    arguments['--start'] = [int(i) for i in arguments['--start']]
    arguments['--end'] = [int(i) for i in arguments['--end']]
    arguments['--start'].sort()
    arguments['--end'].sort()

def check_non_overlap(argments):
    "Confirm that none of the time windows are overlapping"
    for index, start_t in enumerate(arguments['--start'][1:]):
        if start_t < arguments['--end'][index]:
            raise ValueError("Time windows must not be overlapping.\n"
                f"{arguments}")

def check_start_end_order(arguments):
    "Confirm that all start/end pairs are in the correct sequential order"
    for index, start_t in enumerate(arguments['--start']):
        if start_t > arguments['--end'][index]:
            raise ValueError("Start times can never be greater than end "
                f"times\n{arguments}")

def check_in_bounds(arguments):
    "Confirm that none of the times are beyond the video duration"
    duration = get_video_duration(arguments['--in'])
    for index, start_t in enumerate(arguments['--start']):
        if start_t > duration or arguments['--end'][index] > duration:
            raise ValueError("Times must not exceed video duration")

def check_format(arguments):
    check_non_overlap(arguments)
    check_start_end_order(arguments)
    check_in_bounds(arguments)

def run():
    enforce_mode(arguments)
    convert_times_to_seconds(arguments)
    sort_time_points(arguments)
    check_format(arguments)

    build_ffmpeg_cmd(arguments)

    print(arguments)

if __name__ == '__main__':
    run()

"""
python vidcut.py --in=test_vid_in.mp4 --out=out.mp4 --start=60 --end=80 --start=10 --end=20 --end=55 --start=44

Returns the following dictionary for arguments:

{'--end': [20, 55, 80],
 '--in': 'test_vid_in.mp4',
 '--maintain': True,
 '--out': 'out.mp4',
 '--start': [10, 44, 60],
 '--subtractive': False}


https://superuser.com/questions/681885/how-can-i-remove-multiple-segments-from-a-video-using-ffmpeg
# For my test, I want to remove seconds 28-50 from my test video

Example ffmpeg cmd:
ffmpeg -i utv.ts -filter_complex \
"[0:v]trim=duration=30[av];[0:a]atrim=duration=30[aa];\
 [0:v]trim=start=40:end=50,setpts=PTS-STARTPTS[bv];\
 [0:a]atrim=start=40:end=50,asetpts=PTS-STARTPTS[ba];\
 [av][bv]concat[cv];[aa][ba]concat=v=0:a=1[ca];\
 [0:v]trim=start=80,setpts=PTS-STARTPTS[dv];\
 [0:a]atrim=start=80,asetpts=PTS-STARTPTS[da];\
 [cv][dv]concat[outv];[ca][da]concat=v=0:a=1[outa]" -map [outv] -map [outa] out.ts
"""
