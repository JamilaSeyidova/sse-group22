#!/bin/bash
# -------------------------------------------------------------------
# This script uses ffmpeg to encode a raw video file to an H.264/265 encoded video in an MP4 container.
#
# Original command:
# ffmpeg -i input_raw_video.yuv -c:v libx264 -preset slow -crf 22 encoded_video.mp4
#
# Explanation of each parameter:
#
# - -i input_raw_video.yuv
#     Specifies the input file. Replace "input_raw_video.yuv" with your source video file.
#
# - -c:v libx264
#     Selects the video codec to use. "libx264" "libx265".
#
# - -preset slow
#     Controls the encoding speed versus compression efficiency.
#     Available options include (from fastest/lowest compression to slowest/highest compression):
#         ultrafast, superfast, veryfast, faster, fast, medium, slow, slower, veryslow, placebo.
#     A slower preset (like "slow") will usually produce better compression at the cost of speed.
#
# - -crf 22
#     The Constant Rate Factor (CRF) determines quality and file size.
#     Lower values mean higher quality (and larger file sizes), while higher values lower quality.
#     Common CRF values for H.264 range from 18 (nearly lossless) to 28. Adjust as needed.
#
# - encoded_video.mp4
#     The output file name along with its container format.
#     Changing the extension (e.g., .mkv, .mov) will change the container type.
#
# Additional useful options you might consider:
#
# - -b:v <bitrate>
#     Instead of CRF, you could set a target bitrate (e.g., "-b:v 1M" for 1 megabit per second)
#     if you need a specific file size or bandwidth requirement.
#
# - -vf "scale=1280:720"
#     Applies a video filter. Here, it scales the video to 1280x720 resolution.
#     You can replace or add filters depending on your needs (e.g., cropping, deinterlacing).
#
# - -c:a aac -b:a 128k
#     If the input has audio, these options set the audio codec (AAC) and bitrate (128 kbps).
#
# - -movflags +faststart
#     Optimizes the MP4 file for streaming by moving some metadata to the beginning of the file.
#
# Example modified command with extra options:
# ffmpeg -i input_video.mp4 -c:v libx264 -preset slow -crf 22 -vf "scale=1280:720" -c:a aac -b:a 128k -movflags +faststart output_video.mp4
#
# Adjust the parameters above based on your desired quality, speed, resolution, and file size.
# -------------------------------------------------------------------

# Here is the basic encoding command:
ffmpeg -i input_raw_video.yuv -c:v libx264 -preset slow -crf 22 encoded_video.mp4

echo "Starting encoding process..."
ffmpeg -i test.mp4 -c:v libx264 -preset slow -crf 22 encoded_video.mp4
echo "Encoding completed."

# Decoding (Playback) phase: Play the encoded video directly (decoding on the fly)
# Note: The decoding process generetes frames on the fly, so either you save the frames, 
# or you have to add another encoding phase to generate a video so to make it more realistic
# the script plays the video in a new window while the encoded video is being decoded.
# Note: This command will play the video in a new window. Close the window to continue.
echo "Starting video playback..."
ffplay encoded_video.mp4
