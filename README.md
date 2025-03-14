# sse-group22

## Running the experiments

### 1. Setup EnergiBridge
All the required files are in the `energibridge` folder. See the [EnergiBridge](https://github.com/tdurieux/EnergiBridge) GitHub page for more information. Run the following commands in an elevated (Admin) command line:
#### Windows
```shell
#Create:
sc create rapl type=kernel binPath="<absolute_path_to_energibridge_folder\LibreHardwareMonitor.sys"

#Start:
sc start rapl
```

### 2. Install FFMPEG
Install [FFMPEG](https://ffmpeg.org/).
```shell
#windows
winget install ffmpeg
```

### 3. Configure Video
Put the video you want to run the experiments with inside `videos>Original`.
This can, for example, be a 4K mp4 video which gets converted to other formats and resolutions for the experiments.
Here you can find the video that was used for the experiments: [4k.mp4](https://drive.google.com/drive/folders/1szMRa1EiEV6eTaOxet7m-NW5r2Phh-6_?usp=sharing.)

### 4. Install dependencies
Install all the required dependencies by running `pip install -r requirements.txt`.

### 5. Convert the input video
Each experiment requires an input video of a specific format and resolutions.
Running `converter` will automatically create al the necessary videos.

### 6. Run the experiments
The experiments can be run by running `main`. Before doing so, make sure you are in an elevated (Admin) environment. The output of all experiments will be written to the `results` folder.

The following settings were used during the execution of the experiment:
- Computer connected to wall outlet and the battery was fully charged
- Airplane modus enabled
- All other programs and processes closed (`main` was run through the command line)
- No external devices were connected
- The screen was turned off