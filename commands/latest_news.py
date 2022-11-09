import tkinter as tk

main_window = tk.Tk()
main_window.after(5000, main_window.destroy)
main_window.title("News")
main_window.attributes('-fullscreen', True)
canv = tk.Canvas(main_window)
canv.place(x=0, y=0, relwidth=1, relheight=1)
tex = tk.Label(canv, text="Hello wold", justify="center")
tex.place()
tex.pack()
main_window.mainloop()