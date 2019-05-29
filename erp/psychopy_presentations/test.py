import numpy as np
from pandas import DataFrame
from psychopy import visual, core, event
from time import time, strftime, gmtime
from optparse import OptionParser
from pylsl import StreamInfo, StreamOutlet

def present(duration=10):

    # create
    info = StreamInfo('Markers', 'Markers', 1, 0, 'int32', 'myuidw43536')

    # next make an outlet
    outlet = StreamOutlet(info)

    markernames = [1, 2]

    start = time()

    n_trials = 5
    iti = .5
    soa = 0.3
    jitter = 0.2
    record_duration = np.float32(duration)

    # Setup log
    position = np.random.binomial(1, 0.15, n_trials)

    trials = DataFrame(dict(position=position,
                            timestamp=np.zeros(n_trials)))

    # graphics
    mywin = visual.Window([1366, 768], units="deg",
                          fullscr=True)
    go = visual.ImageStim(win=mywin, image='go.png', mask=None, pos=(0.5, 0.5),size=0.5)
    no_go = visual.ImageStim(win=mywin, image='./no_go.png', mask=None, pos=(0.0, 0.0),size=0.2)
    go.draw()
    mywin.close()

present()
