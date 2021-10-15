from tkinter import *


class Window:
    def __init__(self, player):
        self._player = player
        self._root = Tk("GymRadio")
        self._root.geometry('400x250')

        self._lbl = Label(self._root, text="Привет")
        self._lbl.grid(column=1, row=0)

        self.btn_p = Button(self._root, text="Prev", command=self.prev)
        self.btn_pp = Button(self._root, text="Play/Pause", command=self.pp)
        self.btn_n = Button(self._root, text="Next", command=self.next)
        self.btn_p.grid(column=0, row=1)
        self.btn_pp.grid(column=1, row=1)
        self.btn_n.grid(column=2, row=1)

        self._root.title("GymRadio")

    def start(self):
        self._root.mainloop()

    def pp(self):
        if self._player.is_now_playing():
            self._player.pause()
        else:
            self._player.play()

    def next(self):
        self._lbl.configure(text=self._player.next())

    def prev(self):
        self._lbl.configure(text=self._player.prev())
