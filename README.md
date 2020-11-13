# EMPiano: A System to Enable Expressive Pitch Control on the Piano Keyboard.

This repository contains a system that, in combination with the correct hard- and software, offers sound modulation via muscular activity, captured by an electromyography device.

In short: the system is trained to recognize a performed finger gesture (wiggle motion of the thumb) and adds a pitch vibrato to the sound output.

[![System teaser|600x](./pics/figures_teaser_video.png)](http://www.jakob-karolus.de/publications/disfp6537-karolus20.mp4)

##  Requirements

- **Electrodes** plus **Amplifier** to capture the muscle activity.  
We used the LiveAmp EEG recorder from "Brain Products" (https://www.brainproducts.com/productdetails.php?id=63), to which eight plus one ground and one reference active surface electrodes were connected.  
The recording software is only available on Windows for us.  
Another electrode set we tested was the **EMBody toolkit** (https://github.com/HCUM/embody). We used it with two channels.
- **Lab Streaming Layer (LSL) framework** (https://github.com/sccn/labstreaminglayer)  
The RDA Connector can be used to tap the BrainVision data. 
- **Music software**, which is able to receive and play back MIDI.  
For example Waveform 11 (https://www.tracktion.com/products/waveform-free), together with the Piano-One instrument (https://neovst.com/piano-one/)
- **Electric-Piano** 
 We used a MIDI-to-USB cable to play the sound through the music software.
- We additionally used **Speakers**, for the purpose of providing a better sound

## Installation

The easiest way to run this project, is to install pipenv on your computer, for example by executing '''pip3 install pipenv'''. 
Now clone this project and open it in your terminal. With the command '''pipenv install''' all the requirements stated in the Pipfile are installed.
And ready to go!

In case you do not want to use the pipenv, you will need to install the following libraries:
   - numpy
   - matplotlib
   - scikit-learn
   - pylsl
   - scipy
   - mido
   - wxpython
   - pypubsub


## Setup

### Electrode Setup
The electrodes were placed in two rings around the upper right forearm. Each of the rings counted five electrodes and had to include either ground or reference electrode.  
When using the EMBody toolkit, we attached the reference electrode close to the elbow and the two channels on opposite sides of the upper forearm.

<p align="center">
    <img src="./pics/figures_electrode_ring.jpg" alt="electrode_ring" width="500"/>
</p>


### Hardware Setup
<p align="center">
    <img src="./pics/fullSetup.png" alt="electrode_ring" width="500"/>
</p>


## Steps to Running the System
1. Attach the electrodes to the piano player
2. Start the [LSL-Stream](#LSL-Stream)
3. Start this python program
4. This program will find all available LSL-streams, from these you can choose one to connect to.
5. Prepare music software
6. Perform the calibration
7. Ready to go!

## Calibration
Our system offers two different types of calibration.
1. **Video Calibration**:
You are expected to play the shown song in the speed of the blue marker. Whenever this marker hits a note marked in red, you are expected to perform a back-and-forth wiggle motion, using the thumb, for as long as this red note is playing.  
It is possible to reset and restart the video calibration, in case of a mistake.
2. **Custom Calibration**:
You are free to calibrate yourself, by playing whatever and tracking your performance of the back-and-forth wiggle motion by the thumb using the "Mod:on" and "Mod:off" button. With starting the wiggle motion press "Mod:on" and with ending it press "Mod:off" (it is the same button that changes the label after being pressed).  
Here it is also possible to reset and restart the custom calibration, in case of a mistake.

<p align="center"> 
    <img src="./pics/wiggle_motion.gif" width="600" /> 
</p>

## Best Practices
- 10 electrodes (including Ref und Gnd) around the upper forearm
- Best when using a medical EMG-/EEG-device
- The **finger motion** that works best for our system is a back-and-forth wiggle motion of the **thumb** (cf. gif). Feel free to try a sideways wiggle motion or other fingers as well, but know that these might not work as well.
- Use a sampling rate of at least 250Hz


## Additional Information
### LSL-Stream
- Our system requires the data-samples, sent through the LSL-stream, to be formatted as followed:  
([channel 1, channel 2, ...], timestamp)

### MIDI
- For sending the sound-modulation MIDI messages to the music software, a virtual MIDI cable is required:
    - On **Windows**: Sometimes an inbuilt **virtual MIDI cable** is available,  
    otherwise: use **loopMIDI** to create one yourself (http://www.tobias-erichsen.de/software/loopmidi.html).
    - On **MacOS**: Usually there is an inbuilt virtual MIDI cable available: IAC driver
    - Most of the times the library mido itself can be used to create a virtual MIDI cable, but it does not work when using Windows MultiMedia API.  
    To open an output check the corresponding box in the Settings. 
    - The name of your virtual MIDI cable can be changed in the Settings




## Citing "Hit the Thumb Jack!"

Below are the BibTex entries to cite Hit the Thumb Jack!

```
@inproceedings{10.1145/3357236.3395500,
author = {Karolus, Jakob and Kilian, Annika and Kosch, Thomas and Schmidt, Albrecht and Wo\'{z}niak, Pawe\l W.},
title = {Hit the Thumb Jack! Using Electromyography to Augment the Piano Keyboard},
year = {2020},
isbn = {9781450369749},
publisher = {Association for Computing Machinery},
address = {New York, NY, USA},
url = {https://doi.org/10.1145/3357236.3395500},
doi = {10.1145/3357236.3395500},
booktitle = {Proceedings of the 2020 ACM on Designing Interactive Systems Conference},
pages = {429–440},
numpages = {12},
keywords = {creative support tool, motor tasks, electromyography, seamless integration, expressive piano play},
location = {Eindhoven, Netherlands},
series = {DIS ’20}
}
```

```
@misc{karolus:hitthethumb,
  author = {Karolus, Jakob and Kilian, Annika and Kosch, Thomas and Schmidt, Albrecht and Wo\'{z}niak, Pawe\l W.},
  title = {Hit the Thumb Jack!},
  year = {2020},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/HCUM/empiano}}
}
```
