# BrainWave
A python project which uses a Muse 2016 to make a servo-powered hand wave by using theta power as a biomarker
for 'focus'.


## Process chain
Users wear Muse and neural signal is sent to Windows PC through [Muselsl](https://github.com/alexandrebarachant/muse-lsl) and 
[BlueMuse](https://github.com/kowalej/BlueMuse/tree/master/Dist). Muselsl supports time series visualization using
`muselsl view`. To start calibration with system, run Wave.ipynb. This will initiate a PsychoPy calibration screen which
directs users to relax and focus. This trains our system to understand the users current specific theta power threshold which
determines 'focused' vs 'non-focused' states.


## PsychoPy_Code
- BrainWave.py contains the most up-to-date code for the PsychoPy calibration portion. 
To run, make sure you have PsychoPy dependencies installed https://www.psychopy.org/installation.html
Workflow: 
  1) Introduction *click*
  2) Instructions *click*
  3) Loop (3 times, each with a random landscape and Waldo image) <br>
      3a) Relax cue 1s <br>
      3b) Relax 10s w/ Landscape image <br>
      3c) Focus cue 1s <br>
      3d) Focus 7s w/ Where's Waldo image <br>
  
  
