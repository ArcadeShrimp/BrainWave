
from psychopy import visual, core

win = visual.Window(fullscr=True)
msg = visual.ImageStim(win, image="go.png")

msg.draw()
win.flip()
core.wait(1)
win.close()
