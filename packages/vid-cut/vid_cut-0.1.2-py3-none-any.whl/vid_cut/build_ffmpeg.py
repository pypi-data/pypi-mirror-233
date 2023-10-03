import os

def build_fragment_labels():
    "Build labels for video and audio fragments"
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    labels = [letter for letter in alphabet]

    for letter in alphabet:
        labels.extend([letter+letter2 for letter2 in alphabet])

    return labels

def build_ffmpeg_cmd(arguments):
    # If arguments['start_end_index']['start'] or ['end'] exist, then the user has specified that
    # They want the start and end of the video somewhere.
    start = arguments['--start']
    end = arguments['--end']
    labels = build_fragment_labels()
    cmd = f'ffmpeg -i {arguments["--in"]} -filter_complex "'

    t_index = 0
    index = 0

    for times in zip(start, end):
        start_t = times[0]
        end_t = times[1]

        # Start at the beginning of the video (do not specify begin time, just duration for this segment)
        if index == 0 and 'start' in arguments['start_end_index']:
            cmd += f"[0:v]trim=duration={end_t}[{labels[index]}v];"
            cmd += f"[0:a]atrim=duration={end_t}[{labels[index]}a];"
        # Go to the end of the video (do not specify end time, just start time for this segment
        elif t_index == len(start)-1 and 'end' in arguments['start_end_index']:
            cmd += f"[0:v]trim=start={start_t},setpts=PTS-STARTPTS[{labels[index]}v];"
            cmd += f"[0:a]atrim=start={start_t},asetpts=PTS-STARTPTS[{labels[index]}a];"
        # Regular segment with start and end time specified
        else:
            cmd += f"[0:v]trim=start={start_t}:end={end_t},setpts=PTS-STARTPTS[{labels[index]}v];"
            cmd += f"[0:a]atrim=start={start_t}:end={end_t},asetpts=PTS-STARTPTS[{labels[index]}a];"

        # Concatenate fragments
        if index > 0:
            index += 1
            cmd += f"[{labels[index-2]}v][{labels[index-1]}v]concat[{labels[index]}v];"
            cmd += f"[{labels[index-2]}a][{labels[index-1]}a]concat=v=0:a=1[{labels[index]}a];"

        index += 1
        t_index += 1

    # Final touch
    cmd = cmd[:-1] # Remove trailing semicolon
    cmd += f'" -map [{labels[index-1]}v] -map [{labels[index-1]}a] {arguments["--out"]}'

    os.system(cmd)

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

