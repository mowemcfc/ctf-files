from tkinter import Button, Entry, Tk, mainloop, messagebox
a = '2384'
app = Tk()
app.geometry('490x80')
app.resizable(0, 0)
app.title('Crackme 01')
d = '1982'
module = Entry(app, font='Courier_New 32 bold')
b = '8293'
module.pack()
module.focus_set()
c = '1904'
print(a + b + c + d)

def callback():
    content = module.get()
    if content == a + b + c + d:
        messagebox.showinfo('Access Granted', 'Congratulations, the flag is flag_{' + content + '}')
    else:
        messagebox.showinfo('Access Denied', 'Invalid Serial!')


botao = Button(app, text='Check', width=50, command=callback)
botao.pack()
mainloop()

