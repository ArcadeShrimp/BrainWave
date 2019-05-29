import numpy as np
from pandas import DataFrame
from psychopy import visual, core, event
from time import time, strftime, gmtime
from optparse import OptionParser
from pylsl import StreamInfo, StreamOutlet
import os


def present(duration=120):
    
    # setup streams
    info = StreamInfo('Markers', 'Markers', 1, 0, 'int32', 'moving_hand_present')
    outlet = StreamOutlet(info)
    
    start = time()
    record_duration = np.float32(duration)
    
    # define presentation variables
    num_trials = 200
    go_time = 5
    stop_time = 1
    wait_times = np.random.normal(2, 0.5, num_trials)
    
    # Ensure that relative paths start from the same directory as this script
    _thisDir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(_thisDir)
    
    # create graphic objects
    window = visual.Window(fullscr = True)
    go_image = visual.ImageStim(win = window, image = './go.png')
    stop_image = visual.ImageStim(win = window, image = './stop.jpg')
    
    for wait_time in wait_times:
        core.wait(wait_time)

        # display the go image
        go_image.draw()
        timestamp = time()
        outlet.push_sample([1], timestamp)
        window.flip()
        core.wait(go_time)
        
        # display the stop image
        stop_image.draw()
        window.flip()
        core.wait(stop_time)
       
        # display a blank screen
        window.flip()
        
        # checks if the presentation duration is up
        if len(event.getKeys()) > 0 or (time() - start) > record_duration:
            break
        event.clearEvents()
        
    # cleanup -- close window after the presentation
    window.close()
    

def main():
    parser = OptionParser()

    parser.add_option("-d", "--duration",
                      dest="duration", type='int', default=120,
                      help="duration of the recording in seconds.")

    (options, args) = parser.parse_args()
    present(options.duration)


if __name__ == '__main__':
    main()
