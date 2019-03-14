###############
### Imports ###
###############

# Allow Python 2 to run this code. 
from __future__ import absolute_import, division

# psychopy imports
from psychopy import locale_setup, sound, gui, visual, core, data, event, logging, clock
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)

import random as rd

# numpy imports
import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle

import os  # handy system and path functions
import sys  # to get file system encoding

sys.path.append('../')

import command

# constants
RELAX = 'relax'
FOCUS = 'focus'

relax_images = ["landscape1.jpg", "landscape2.jpg", "landscape3.jpg"]
rd.shuffle(relax_images)
waldo_images = ["waldo1.png", "waldo2.png", "waldo3.png"]
rd.shuffle(waldo_images)

# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)


def run_psychopy(cmd: command.Tracker):

    #################
    ### Start Box ###
    #################
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
        savePickle=True, saveWideText=True,
        dataFileName=filename)
    # save a log file for detail verbose info
    logFile = logging.LogFile(filename+'.log', level=logging.EXP)
    logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

    ### ESC flag ###
    endExpNow = False  # flag for 'escape' or other condition => quit the exp

    ####################
    ### Window Setup ###
    ####################
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



    #############################
    ### Initialize components ###
    #############################

    # Initialize components for Routine "intro"
    introduction = visual.TextStim(win=win, name='introduction',
        text='BrainWave\n\nCalibration Phase\n\nClick to advance. ',
        font='Arial',
        pos=(0, 0), height=0.1, wrapWidth=None, ori=0,
        color='white', colorSpace='rgb', opacity=1,
        languageStyle='LTR',
        depth=0.0)
    mouse = event.Mouse(win=win)
    x, y = [None, None]

    # Initialize components for Routine "instr"
    instructions = visual.TextStim(win=win, name='instructions',
        text='There will be 3 rounds of stimuli. \n\n1) Relax when you see pretty landscapes.\n\n2) Focus when you need to find Waldo. \n\n\n\nClick to get started.',
        font='Arial',
        pos=(0, 0), height=0.05, wrapWidth=None, ori=0,
        color='white', colorSpace='rgb', opacity=1,
        languageStyle='LTR',
        depth=0.0)
    mouse2 = event.Mouse(win=win)
    x, y = [None, None]

    # Initialize components for Routine "relax_cue"
    cue = visual.TextStim(win=win, name='cue',
        text='~~~Relax~~~',
        font='Arial',
        pos=(0, 0), height=0.1, wrapWidth=None, ori=0,
        color='white', colorSpace='rgb', opacity=1,
        languageStyle='LTR',
        depth=0.0)

    # Initialize components for Routine "relax"
    relaxing_image = visual.ImageStim(
        win=win, name='relaxing_image',
        image='sin', mask=None,
        ori=0, pos=(0, 0), size=(1.7, 1),
        color=[1,1,1], colorSpace='rgb', opacity=1,
        flipHoriz=False, flipVert=False,
        texRes=128, interpolate=True, depth=0.0)

    # Initialize components for Routine "focus_cue"
    whereswaldo = visual.ImageStim(
        win=win, name='whereswaldo',
        image='wheres-waldo.jpg', mask=None,
        ori=0, pos=(0, 0), size=(0.7, 0.5),
        color=[1,1,1], colorSpace='rgb', opacity=1,
        flipHoriz=False, flipVert=False,
        texRes=128, interpolate=True, depth=0.0)

    # Initialize components for Routine "focus"
    focus_image = visual.ImageStim(
        win=win, name='focus_image',
        image='sin', mask=None,
        ori=0, pos=(0, 0), size=(1.7, 1),
        color=[1,1,1], colorSpace='rgb', opacity=1,
        flipHoriz=False, flipVert=False,
        texRes=128, interpolate=True, depth=0.0)


    # Create some handy timers
    globalClock = core.Clock()  # to track the time since experiment started
    routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine

    ################
    ### Routines ###
    ################

    ############################
    ############################
    ### INTRODUCTION ROUTINE ###
    ############################
    ############################

    # ------Prepare to start Routine "intro"-------

    introComponents = [introduction, mouse]
    for thisComponent in introComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED

    continueRoutine = True

    # -------Start Routine "intro"-------
    while continueRoutine:

        # *introduction* updates
        if introduction.status == NOT_STARTED:
            introduction.status = STARTED
            introduction.setAutoDraw(True)

        # Start mouse if not started
        if mouse.status == NOT_STARTED:
            # keep track of start time/frame for later
            mouse.status = STARTED
            prevButtonState = mouse.getPressed()  # if button is down already this ISN'T a new click

        # Check if mouse pressed
        if mouse.status == STARTED:  # only update if started and not finished!
            buttons = mouse.getPressed()
            if buttons != prevButtonState:  # button state changed?
                prevButtonState = buttons
                if sum(buttons) > 0:  # state changed to a new click
                    # abort routine on response
                    continueRoutine = False

        # Check for ESC quit
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()

        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()

    # -------Ending Routine "intro"-------
    for thisComponent in introComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)

    routineTimer.reset()

    ###########################
    ###########################
    ### INSTRUCTION ROUTINE ###
    ###########################
    ###########################

    # ------Prepare to start Routine "instr"-------

    instrComponents = [instructions, mouse2]
    for thisComponent in instrComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED

    continueRoutine = True

    # -------Start Routine "instr"-------
    while continueRoutine:

        # *introduction* updates
        if instructions.status == NOT_STARTED:
            instructions.status = STARTED
            instructions.setAutoDraw(True)

        # Start mouse if not started
        if mouse2.status == NOT_STARTED:
            # keep track of start time/frame for later
            mouse2.status = STARTED
            prevButtonState = mouse2.getPressed()  # if button is down already this ISN'T a new click

        # Check if mouse pressed
        if mouse2.status == STARTED:  # only update if started and not finished!
            buttons = mouse2.getPressed()
            if buttons != prevButtonState:  # button state changed?
                prevButtonState = buttons
                if sum(buttons) > 0:  # state changed to a new click
                    # abort routine on response
                    continueRoutine = False

        # Check for ESC quit
        if endExpNow or event.getKeys(keyList=["escape"]):
            win.close()
            core.quit()

        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()

    # -------Ending Routine "intro"-------
    for thisComponent in instrComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)

    routineTimer.reset()


    #####################
    #####################
    ### TRIAL SET UP  ###
    #####################
    #####################

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

    trialCounter = 0
    for thisTrial in trials:
        trialCounter += 1
        currentLoop = trials
        # abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
        if thisTrial != None:
            for paramName in thisTrial:
                exec('{} = thisTrial[paramName]'.format(paramName))


        #########################
        #########################
        ### RELAX CUE ROUTINE ###
        #########################
        #########################

        # ------Prepare to start Routine "relax_cue"-------

        relax_cueComponents = [cue]
        for thisComponent in relax_cueComponents:
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED

        routineTimer.add(1.000000)
        continueRoutine = True
        # -------Start Routine "relax_cue"-------
        while continueRoutine and routineTimer.getTime() > 0:

            if cue.status == NOT_STARTED:
                cue.status = STARTED
                cue.setAutoDraw(True)

            # check for quit (typically the Esc key)
            if endExpNow or event.getKeys(keyList=["escape"]):
                core.quit()

            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()

        # -------Ending Routine "relax_cue"-------
        for thisComponent in relax_cueComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)


        #####################
        #####################
        ### RELAX ROUTINE ###
        #####################
        #####################

        # ------Prepare to start Routine "relax"-------

        relaxing_image.setImage(relax_images[trialCounter])

        relaxComponents = [relaxing_image]
        for thisComponent in relaxComponents:
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED


        cmd.start_stage(mode=RELAX, stage=trialCounter)
        routineTimer.add(10.000000)
        continueRoutine = True
        # -------Start Routine "relax"-------
        while continueRoutine and routineTimer.getTime() > 0:
            if relaxing_image.status == NOT_STARTED:
                relaxing_image.status = STARTED
                relaxing_image.setAutoDraw(True)

            # check for quit (typically the Esc key)
            if endExpNow or event.getKeys(keyList=["escape"]):
                cmd.end_stage(mode=RELAX, stage=trialCounter)
                win.close()
                core.quit()

            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()

        cmd.end_stage(mode=RELAX, stage=trialCounter)
        
        # -------Ending Routine "relax"-------
        for thisComponent in relaxComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)

        #########################
        #########################
        ### FOCUS CUE ROUTINE ###
        #########################
        #########################

        # ------Prepare to start Routine "focus_cue"-------

        focus_cueComponents = [whereswaldo]
        for thisComponent in focus_cueComponents:
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED

        routineTimer.add(1.000000)
        continueRoutine = True
        # -------Start Routine "focus_cue"-------
        while continueRoutine and routineTimer.getTime() > 0:

            if whereswaldo.status == NOT_STARTED:
                whereswaldo.status = STARTED
                whereswaldo.setAutoDraw(True)

            # check for quit (typically the Esc key)
            if endExpNow or event.getKeys(keyList=["escape"]):
                win.close()
                core.quit()
                

            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()

        # -------Ending Routine "focus_cue"-------
        for thisComponent in focus_cueComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)

        #####################
        #####################
        ### FOCUS ROUTINE ###
        #####################
        #####################

        # ------Prepare to start Routine "focus"-------

        focus_image.setImage(waldo_images[trialCounter])

        focusComponents = [focus_image]
        for thisComponent in focusComponents:
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED

        cmd.start_stage(mode=FOCUS, stage=trialCounter)
        routineTimer.add(7.000000)
        continueRoutine = True
        # -------Start Routine "focus"-------
        while continueRoutine and routineTimer.getTime() > 0:
            if focus_image.status == NOT_STARTED:
                focus_image.status = STARTED
                focus_image.setAutoDraw(True)

            # check for quit (typically the Esc key)
            if endExpNow or event.getKeys(keyList=["escape"]):
                cmd.end_stage(mode=RELAX, stage=trialCounter)
                win.close()
                core.quit()

            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()

        cmd.end_stage(mode=FOCUS, stage=trialCounter)
        
        # -------Ending Routine "focus"-------
        for thisComponent in focusComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)

    logging.flush()
    # make sure everything is closed down
    thisExp.abort()  # or data files will save again on exit
    win.close()
    core.quit()

