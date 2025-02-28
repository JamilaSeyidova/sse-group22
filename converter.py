import os
import subprocess
from pathlib import Path
video_path = Path('./videos/Original/4k.mp4')
#video_path = Path('sse-group22/Original/4k.mp4')
output_folder = Path('./videos/converted/')
codecs = ['H.264', 'H.265']
resolutions = [2160]#[2160, 1080, 720, 480]

def convert_videos():
    for codec in codecs:
        for res in resolutions:
            decode(res, codec, video_path, output_folder)


def decode(res: int, codec: str, video: Path, output: Path):
    os.makedirs(output, exist_ok=True)
    output = output / f'{res}p_{codec}.mp4'
    if output.exists():
        return

    if codec == 'H.264':
        cv = 'libx264'
    elif codec == 'H.265':
        cv = 'libx265'
    else:
        raise ValueError(f'Unknown codec: {codec}')

    if res == 2160:
        r = '2560:1440'
    elif res == 1080:
        r = '1920:1080'
    elif res == 720:
        r = '1280:720'
    elif res == 480:
        r = '854:480'
    else:
        raise ValueError(f'Unknown resolution: {res}')

    decoder_command = [
        'ffmpeg',
        '-i', str(video.absolute()),
        '-c:v', cv,
        '-preset', 'medium',
        '-crf', '23',
        '-vf', f'scale={r}',
        str(output.absolute()),
    ]
    subprocess.Popen(decoder_command, shell=True).wait()


if __name__ == "__main__":
    convert_videos()