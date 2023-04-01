from tkinter import *
import colorSelector



# Window setting
mainWin = Tk()
mainWin.geometry("1080x720")

mainWin.title("OLight")
mainWin.resizable(width=False, height=False)


# Hexagonal color selector
cs = colorSelector.hexagonColorSelector(mainWin, 300, 5)
cs.pack()



mainloop()