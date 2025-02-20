from pytubefix import YouTube

def download():
    res = ['144p', '240p', '360p', '480p', '720p', '1080p', '1440p', '2160p']
    fps = 60
    mime_type = 'video/mp4'
    streams = YouTube('https://www.youtube.com/watch?v=LXb3EKWsInQ').streams.filter(res=res, fps=fps,
                                                                                    mime_type=mime_type)
    for stream in streams:
        if (stream.resolution not in res):
            continue
        res.remove(stream.resolution)
        stream.download(output_path=f'./videos/')
        print(f'downloaded: {stream}')

if __name__ == "__main__":
    ys = YouTube('https://www.youtube.com/watch?v=LXb3EKWsInQ').streams
    stream = ys.get_by_itag(337)
    stream.download(output_path=f'./videos/')