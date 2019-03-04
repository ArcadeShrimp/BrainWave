
from multiprocessing import Process
import time

class Tracker:
    """
    Tracks PsychoPy Calibration and MuseLsL Data
    """

    currentMode = None
    currentStage = None

    # Whether or not we are ready to record
    readyToRecord = True

    # Keep track of whether something is already recording
    isRecording = False

    # to hold the process that will do the recording
    recordingProcess = None

    # to hold the eeg data
    eeg_data = {'relax1' : list(), "relax2": list(), "relax3": list(), "focus1": list(), "focus2": list(), "focus3": list()}
    mydata = list()
    def __init__(self):#, inlet):
        """
        Initialize with inlet.
        :param inlet:
        """
        pass

    def _start_recording(self, arr):
        """ Write smooth band power to the df

        :return:
        """
        # Initialize museLSL

        # While loop for recording 
        while(self.readyToRecord) :
            print("recording: " + self.currentMode + " " + str(self.currentStage))
            time.sleep(1)
        
        pass

    def start_stage(self, mode=None, stage=0):
        """
            Start relax stage and record data.

        :return:
        """

        if (self.recordingProcess == None or ~self.recordingProcess.is_alive()) : 
            self.isRecording = True

            self.recordingProcess = Process(target=self._start_recording, args=(self.eeg_data[mode + str(stage)],))

            self.currentMode = mode
            self.currentStage = stage

            self.recordingProcess.start()
        else :
            print("Unable to start process because already running")


        pass

    def end_stage(self, mode=None, stage=0):
        self.recordingProcess.terminate()
        self.currentMode = None
        self.currentStage = None

        pass

