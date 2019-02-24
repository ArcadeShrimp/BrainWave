#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v3.0.5),
    on Sat Feb 23 15:56:46 2019
If you publish work using this script please cite the PsychoPy publications:
    Peirce, JW (2007) PsychoPy - Psychophysics software in Python.
        Journal of Neuroscience Methods, 162(1-2), 8-13.
    Peirce, JW (2009) Generating stimuli for neuroscience using PsychoPy.
        Frontiers in Neuroinformatics, 2:10. doi: 10.3389/neuro.11.010.2008
"""

from __future__ import absolute_import, division
from psychopy import locale_setup, sound, gui, visual, core, data, event, logging, clock
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)
import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle
import os  # handy system and path functions
import sys  # to get file system encoding


# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)

# Store info about the experiment session
psychopyVersion = '3.0.5'
expName = 'BrainWave'  # from the Builder filename that created this script
expInfo = {'participant': '', 'session': '001'}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False:
    core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName
expInfo['psychopyVersion'] = psychopyVersion

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + u'data/%s_%s_%s' % (expInfo['participant'], expName, expInfo['date'])

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    originPath='/Users/glchau/Desktop/UCSD/brainwave/BrainWave_lastrun.py',
    savePickle=True, saveWideText=True,
    dataFileName=filename)
# save a log file for detail verbose info
logFile = logging.LogFile(filename+'.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

endExpNow = False  # flag for 'escape' or other condition => quit the exp

# Start Code - component code to be run before the window creation

# Setup the Window
win = visual.Window(
    size=(1024, 768), fullscr=True, screen=0,
    allowGUI=False, allowStencil=True,
    monitor='testMonitor', color=[0,0,0], colorSpace='rgb',
    blendMode='avg', useFBO=True,
    units='height')
# store frame rate of monitor if we can measure it
expInfo['frameRate'] = win.getActualFrameRate()
if expInfo['frameRate'] != None:
    frameDur = 1.0 / round(expInfo['frameRate'])
else:
    frameDur = 1.0 / 60.0  # could not measure, so guess

# Initialize components for Routine "intro"
introClock = core.Clock()
introduction = visual.TextStim(win=win, name='introduction',
    text='BrainWave\n\nCalibration Phase\n\nClick to advance. ',
    font='Arial',
    pos=(0, 0), height=0.1, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=0.0);
mouse = event.Mouse(win=win)
x, y = [None, None]
mouse.mouseClock = core.Clock()

# Initialize components for Routine "instr"
instrClock = core.Clock()
instructions = visual.TextStim(win=win, name='instructions',
    text='There will be 3 rounds of stimuli. \n\n1) Relax when you see pretty landscapes.\n\n2) Focus when you need to find Waldo. \n\n\n\nClick to get started.',
    font='Arial',
    pos=(0, 0), height=0.05, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=0.0);
mouse2 = event.Mouse(win=win)
x, y = [None, None]
mouse2.mouseClock = core.Clock()

# Initialize components for Routine "relax_cue"
relax_cueClock = core.Clock()
cue = visual.TextStim(win=win, name='cue',
    text='~~~Relax~~~',
    font='Arial',
    pos=(0, 0), height=0.1, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=0.0);

# Initialize components for Routine "relax"
relaxClock = core.Clock()
relaxing_image = visual.ImageStim(
    win=win, name='relaxing_image',
    image='sin', mask=None,
    ori=0, pos=(0, 0), size=(2, 1),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=0.0)

# Initialize components for Routine "focus_cue"
focus_cueClock = core.Clock()
whereswaldo = visual.ImageStim(
    win=win, name='whereswaldo',
    image='wheres-waldo.jpg', mask=None,
    ori=0, pos=(0, 0), size=(0.7, 0.5),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=0.0)

# Initialize components for Routine "focus"
focusClock = core.Clock()
focus_image = visual.ImageStim(
    win=win, name='focus_image',
    image='sin', mask=None,
    ori=0, pos=(0, 0), size=(2, 1),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=0.0)
mouse_2 = event.Mouse(win=win)
x, y = [None, None]
mouse_2.mouseClock = core.Clock()
aperture = visual.Aperture(
    win=win, name='aperture',
    units='norm', size=0.3, pos=[0,0])
aperture.disable()  # disable until its actually used

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine 

# ------Prepare to start Routine "intro"-------
t = 0
introClock.reset()  # clock
frameN = -1
continueRoutine = True
# update component parameters for each repeat
# setup some python lists for storing info about the mouse
gotValidClick = False  # until a click is received
# keep track of which components have finished
introComponents = [introduction, mouse]
for thisComponent in introComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

# -------Start Routine "intro"-------
while continueRoutine:
    # get current time
    t = introClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *introduction* updates
    if t >= 0.0 and introduction.status == NOT_STARTED:
        # keep track of start time/frame for later
        introduction.tStart = t
        introduction.frameNStart = frameN  # exact frame index
        introduction.setAutoDraw(True)
    # *mouse* updates
    if t >= 0.0 and mouse.status == NOT_STARTED:
        # keep track of start time/frame for later
        mouse.tStart = t
        mouse.frameNStart = frameN  # exact frame index
        mouse.status = STARTED
        mouse.mouseClock.reset()
        prevButtonState = mouse.getPressed()  # if button is down already this ISN'T a new click
    if mouse.status == STARTED:  # only update if started and not finished!
        buttons = mouse.getPressed()
        if buttons != prevButtonState:  # button state changed?
            prevButtonState = buttons
            if sum(buttons) > 0:  # state changed to a new click
                # abort routine on response
                continueRoutine = False
    
    # check for quit (typically the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in introComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "intro"-------
for thisComponent in introComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# store data for thisExp (ExperimentHandler)
x, y = mouse.getPos()
buttons = mouse.getPressed()
thisExp.addData('mouse.x', x)
thisExp.addData('mouse.y', y)
thisExp.addData('mouse.leftButton', buttons[0])
thisExp.addData('mouse.midButton', buttons[1])
thisExp.addData('mouse.rightButton', buttons[2])
thisExp.nextEntry()
# the Routine "intro" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# ------Prepare to start Routine "instr"-------
t = 0
instrClock.reset()  # clock
frameN = -1
continueRoutine = True
# update component parameters for each repeat
# setup some python lists for storing info about the mouse2
gotValidClick = False  # until a click is received
# keep track of which components have finished
instrComponents = [instructions, mouse2]
for thisComponent in instrComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

# -------Start Routine "instr"-------
while continueRoutine:
    # get current time
    t = instrClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *instructions* updates
    if t >= 0.0 and instructions.status == NOT_STARTED:
        # keep track of start time/frame for later
        instructions.tStart = t
        instructions.frameNStart = frameN  # exact frame index
        instructions.setAutoDraw(True)
    # *mouse2* updates
    if t >= 0.0 and mouse2.status == NOT_STARTED:
        # keep track of start time/frame for later
        mouse2.tStart = t
        mouse2.frameNStart = frameN  # exact frame index
        mouse2.status = STARTED
        mouse2.mouseClock.reset()
        prevButtonState = mouse2.getPressed()  # if button is down already this ISN'T a new click
    if mouse2.status == STARTED:  # only update if started and not finished!
        buttons = mouse2.getPressed()
        if buttons != prevButtonState:  # button state changed?
            prevButtonState = buttons
            if sum(buttons) > 0:  # state changed to a new click
                # abort routine on response
                continueRoutine = False
    
    # check for quit (typically the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in instrComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "instr"-------
for thisComponent in instrComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# store data for thisExp (ExperimentHandler)
x, y = mouse2.getPos()
buttons = mouse2.getPressed()
thisExp.addData('mouse2.x', x)
thisExp.addData('mouse2.y', y)
thisExp.addData('mouse2.leftButton', buttons[0])
thisExp.addData('mouse2.midButton', buttons[1])
thisExp.addData('mouse2.rightButton', buttons[2])
thisExp.nextEntry()
# the Routine "instr" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# set up handler to look after randomisation of conditions etc
trials = data.TrialHandler(nReps=1, method='random', 
    extraInfo=expInfo, originPath=-1,
    trialList=data.importConditions('images.xlsx'),
    seed=None, name='trials')
thisExp.addLoop(trials)  # add the loop to the experiment
thisTrial = trials.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
if thisTrial != None:
    for paramName in thisTrial:
        exec('{} = thisTrial[paramName]'.format(paramName))

for thisTrial in trials:
    currentLoop = trials
    # abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
    if thisTrial != None:
        for paramName in thisTrial:
            exec('{} = thisTrial[paramName]'.format(paramName))
    
    # ------Prepare to start Routine "relax_cue"-------
    t = 0
    relax_cueClock.reset()  # clock
    frameN = -1
    continueRoutine = True
    routineTimer.add(1.000000)
    # update component parameters for each repeat
    # keep track of which components have finished
    relax_cueComponents = [cue]
    for thisComponent in relax_cueComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    # -------Start Routine "relax_cue"-------
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = relax_cueClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *cue* updates
        if t >= 0.0 and cue.status == NOT_STARTED:
            # keep track of start time/frame for later
            cue.tStart = t
            cue.frameNStart = frameN  # exact frame index
            cue.setAutoDraw(True)
        frameRemains = 0.0 + 1.0- win.monitorFramePeriod * 0.75  # most of one frame period left
        if cue.status == STARTED and t >= frameRemains:
            cue.setAutoDraw(False)
        
        # check for quit (typically the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in relax_cueComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "relax_cue"-------
    for thisComponent in relax_cueComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    
    # ------Prepare to start Routine "relax"-------
    t = 0
    relaxClock.reset()  # clock
    frameN = -1
    continueRoutine = True
    routineTimer.add(10.000000)
    # update component parameters for each repeat
    relaxing_image.setImage(relaxing_images)
    # keep track of which components have finished
    relaxComponents = [relaxing_image]
    for thisComponent in relaxComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    # -------Start Routine "relax"-------
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = relaxClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *relaxing_image* updates
        if t >= 0.0 and relaxing_image.status == NOT_STARTED:
            # keep track of start time/frame for later
            relaxing_image.tStart = t
            relaxing_image.frameNStart = frameN  # exact frame index
            relaxing_image.setAutoDraw(True)
        frameRemains = 0.0 + 10- win.monitorFramePeriod * 0.75  # most of one frame period left
        if relaxing_image.status == STARTED and t >= frameRemains:
            relaxing_image.setAutoDraw(False)
        
        # check for quit (typically the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in relaxComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "relax"-------
    for thisComponent in relaxComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    
    # ------Prepare to start Routine "focus_cue"-------
    t = 0
    focus_cueClock.reset()  # clock
    frameN = -1
    continueRoutine = True
    routineTimer.add(1.000000)
    # update component parameters for each repeat
    # keep track of which components have finished
    focus_cueComponents = [whereswaldo]
    for thisComponent in focus_cueComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    # -------Start Routine "focus_cue"-------
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = focus_cueClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *whereswaldo* updates
        if t >= 0.0 and whereswaldo.status == NOT_STARTED:
            # keep track of start time/frame for later
            whereswaldo.tStart = t
            whereswaldo.frameNStart = frameN  # exact frame index
            whereswaldo.setAutoDraw(True)
        frameRemains = 0.0 + 1.0- win.monitorFramePeriod * 0.75  # most of one frame period left
        if whereswaldo.status == STARTED and t >= frameRemains:
            whereswaldo.setAutoDraw(False)
        
        # check for quit (typically the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in focus_cueComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "focus_cue"-------
    for thisComponent in focus_cueComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    
    # ------Prepare to start Routine "focus"-------
    t = 0
    focusClock.reset()  # clock
    frameN = -1
    continueRoutine = True
    routineTimer.add(10.000000)
    # update component parameters for each repeat
    focus_image.setImage(focus_images)
    # setup some python lists for storing info about the mouse_2
    mouse_2.x = []
    mouse_2.y = []
    mouse_2.leftButton = []
    mouse_2.midButton = []
    mouse_2.rightButton = []
    mouse_2.time = []
    gotValidClick = False  # until a click is received
    # keep track of which components have finished
    focusComponents = [focus_image, mouse_2, aperture]
    for thisComponent in focusComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    # -------Start Routine "focus"-------
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = focusClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *focus_image* updates
        if t >= 0.0 and focus_image.status == NOT_STARTED:
            # keep track of start time/frame for later
            focus_image.tStart = t
            focus_image.frameNStart = frameN  # exact frame index
            focus_image.setAutoDraw(True)
        frameRemains = 0.0 + 10- win.monitorFramePeriod * 0.75  # most of one frame period left
        if focus_image.status == STARTED and t >= frameRemains:
            focus_image.setAutoDraw(False)
        # *mouse_2* updates
        if t >= 0.0 and mouse_2.status == NOT_STARTED:
            # keep track of start time/frame for later
            mouse_2.tStart = t
            mouse_2.frameNStart = frameN  # exact frame index
            mouse_2.status = STARTED
            mouse_2.mouseClock.reset()
            prevButtonState = mouse_2.getPressed()  # if button is down already this ISN'T a new click
        frameRemains = 0.0 + 10- win.monitorFramePeriod * 0.75  # most of one frame period left
        if mouse_2.status == STARTED and t >= frameRemains:
            mouse_2.status = FINISHED
        if mouse_2.status == STARTED:  # only update if started and not finished!
            x, y = mouse_2.getPos()
            mouse_2.x.append(x)
            mouse_2.y.append(y)
            buttons = mouse_2.getPressed()
            mouse_2.leftButton.append(buttons[0])
            mouse_2.midButton.append(buttons[1])
            mouse_2.rightButton.append(buttons[2])
            mouse_2.time.append(mouse_2.mouseClock.getTime())
        
        # *aperture* updates
        if t >= 0 and aperture.status == NOT_STARTED:
            # keep track of start time/frame for later
            aperture.tStart = t
            aperture.frameNStart = frameN  # exact frame index
            aperture.enabled = True
        frameRemains = 0 + 10- win.monitorFramePeriod * 0.75  # most of one frame period left
        if aperture.status == STARTED and t >= frameRemains:
            aperture.enabled = False
        if aperture.status == STARTED:  # only update if being  drawn
            aperture.setPos([mouse_2.getPos()[0],mouse_2.getPos()[1]], log=False)
        
        # check for quit (typically the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in focusComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "focus"-------
    for thisComponent in focusComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store data for trials (TrialHandler)
    trials.addData('mouse_2.x', mouse_2.x)
    trials.addData('mouse_2.y', mouse_2.y)
    trials.addData('mouse_2.leftButton', mouse_2.leftButton)
    trials.addData('mouse_2.midButton', mouse_2.midButton)
    trials.addData('mouse_2.rightButton', mouse_2.rightButton)
    trials.addData('mouse_2.time', mouse_2.time)
    aperture.enabled = False  # just in case it was left enabled
    thisExp.nextEntry()
    
# completed 1 repeats of 'trials'

# these shouldn't be strictly necessary (should auto-save)
thisExp.saveAsWideText(filename+'.csv')
thisExp.saveAsPickle(filename)
logging.flush()
# make sure everything is closed down
thisExp.abort()  # or data files will save again on exit
win.close()
core.quit()
