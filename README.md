# EMPiano: A System to Enable Expressive Pitch Control on the Piano Keyboard.

This repository contains a system that, in combination with the correct hard- and softwares, offers sound modulation via muscular activity, captured by an electromyography device.

In short: the system is trained to recognize a performed finger gesture and adds a pitch vibrato to the sound output.

![system sketch](./figures_teaser_new.png)

##  Requirements

- **Electrodes** and an **Amplifier** to capture the muscle activity. We used the LiveAmp EEG recorder from "Brain Products" (https://www.brainproducts.com/productdetails.php?id=63), to which eight plus one ground and one reference active surface electrodes were connected. An additional Windows pc was needed, because the amplifier program didn't work for MacOS.
- **Lab Streaming Layer (LSL) framework** (https://github.com/sccn/labstreaminglayer)
- Currently **MacBook**, because we make use of the inbuilt MIDI cable (IAC driver); used as the controlling PC
- **Music software**, which is able to receive and play back MIDI. We used the free trial version of Ableton Live 10 (https://www.ableton.com/de/trial/)
- **Electric-Piano**; We used a MIDI-to-USB cable to play the sound through Ableton
- We additionally used **speakers**, for the purpose of providing a better sound

## Installation

All required packages can be found and installed using the Pipfile.  
The source code itself can be found in the folder "src".

## Setup

### Electrode Setup
The electrodes were placed in two rings around the upper right forearm. Each of the rings counted five electrodes and had to include either ground or reference electrode.
![system sketch](./figures_electrode_ring.jpg)

### Hardware Setup
![system sketch](./fullSetup.png)

## Steps to Running the System

## Citing Hit the Thumb Jack!

Below are the BibTex entries to cite Hit the Thumb Jack!