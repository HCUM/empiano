# EMPiano: A System to Enable Expressive Pitch Control on the Piano Keyboard.

This repository contains a system that, in combination with the correct hard- and softwares, offers sound modulation via muscular activity, captured by an electromyography device.

In short: the system is trained to recognize a performed finger gesture and adds a pitch vibrato to the sound output.

![](./pics/figures_teaser_new.png)

##  Requirements

- **Electrodes** plus **Amplifier** to capture the muscle activity.  
We used the LiveAmp EEG recorder from "Brain Products" (https://www.brainproducts.com/productdetails.php?id=63), to which eight plus one ground and one reference active surface electrodes were connected.  
The recording software is only available on Windows for us.
- **Lab Streaming Layer (LSL) framework** (https://github.com/sccn/labstreaminglayer)  
We used BrainVision RDA Connector to tap the BrainVision data.
- **Music software**, which is able to receive and play back MIDI.  
For example Waveform 11 (https://www.tracktion.com/products/waveform-free), together with the Piano-One instrument (https://neovst.com/piano-one/)
- **Electric-Piano** 
 We used a MIDI-to-USB cable to play the sound through the music software.
- We additionally used **Speakers**, for the purpose of providing a better sound

## Installation

All required packages can be found and installed using the Pipfile.  
The source code itself can be found in the folder "src".

## Setup

### Electrode Setup
The electrodes were placed in two rings around the upper right forearm. Each of the rings counted five electrodes and had to include either ground or reference electrode.
![](./pics/figures_electrode_ring.jpg)

### Hardware Setup
![](./pics/fullSetup.png)

## Steps to Running the System
1. Attach the electrodes to the piano player
2. Run the program that comes with the electrodes
3. Impedance check of the electrodes
4. Start LSL stream
5. Start this python program
6. Connect this program to the LSL stream in the local network
7. Open music program (check MIDI inputs)
8. Perform Calibration
9. Ready to go!


## Additional Information
- Our system requires the data-samples sent through the LSL stream to have the following format:  
([channel 1, channel 2, ...], timestamp)
- For sending the sound-modulation MIDI messages to the music software, a virtual MIDI cable is required:
    - On **Windows**: Sometimes have an inbuilt **virtual MIDI cable** available,  
    otherwise: use **loopMIDI** to create one yourself (http://www.tobias-erichsen.de/software/loopmidi.html).
    - On **MacOS**: usually there is an inbuilt virtual MIDI cable available: IAC driver
    - Most of the times the library mido itself can be used to create a virtual MIDI cable, but it does not work when using Windows MultiMedia API.  
    To open an outport check the corresponding box in the Settings. 
    - The name of your virtual MIDI cable can be changed in the Settings



## Citing "Hit the Thumb Jack!"

Below are the BibTex entries to cite Hit the Thumb Jack!

```
@inproceedings{10.1145/3357236.3395500,
author = {Karolus, Jakob and Kilian, Annika and Kosch, Thomas and Schmidt, Albrecht and Wozniak, Pawe\l{} W.},
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
