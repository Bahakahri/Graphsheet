from tkinter import *
from tkinter.ttk import *
from pandas import *
import PyQt5
import re
import sys
from IPython.display import display
from matplotlib import pyplot
import seaborn as sns
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pandas.api.types import is_numeric_dtype
import matplotlib.ticker as mticker
from PIL import Image,ImageTk
from tkinter import filedialog



#this function will make the number of columns wanted to the user appear so he can fill it with the names of its columns
def getInput():
    global Le,Ll,elabe
    Le = list()
    Ll = list()
    nc=int(Entry.get(colentry))


    for i in range(1,nc+1) :
        labelC=Label(window2,text=str(i))
        entryC=Entry(window2)
        Ll.append(labelC)
        Le.append(entryC)
        labelC.grid(column=i,row=0)
        entryC.grid(column=i,row=1)

    bcreate = Button(window2, text="Create excel", command=dbCreate)
    bcreate.grid(column=0, row=6)

#delete entries if needed
def delete_entry():
    for i in Ll:
     i.destroy()
    for i in Le:
     i.destroy()

def dbCreate():

    L=list()
    for i in Le:
      e=i.get()
      L.append(e)
    df=DataFrame(columns=L)
    try:
        with filedialog.asksaveasfile(mode='w', defaultextension=".xlsx") as file:
            df.to_excel(file.name,index = False)
            window2.destroy()
    except AttributeError:
        print("The user cancelled save")

def add(df):
    global DF,t1
    Lbd=list()
    DF=DataFrame()
    for e in Le2:
        Lbd.append(Entry.get(e))
    DF=DataFrame([Lbd],columns=[Le3])
    df.loc[len(df)] = Lbd
    df.to_excel(filename,index=False)
    xscrollbar = Scrollbar(window3, orient=HORIZONTAL)
    xscrollbar.grid(row=12, column=3, columnspan=3, sticky=N + S + E + W)
    t1 = Text(window3, wrap=NONE, xscrollcommand=xscrollbar.set, height=10, width=40)
    t1.grid(row=11, column=3, columnspan=3)
    ScrollBar = Scrollbar(window3, command=t1.yview, orient="vertical")
    ScrollBar.grid(row=11, column=6, rowspan=2, sticky="ns")
    t1.configure(yscrollcommand=ScrollBar.set)
    xscrollbar.config(command=t1.xview)
    ScrollBar.config(command=t1.yview)
    sys.stdout = PrintToT1()
    display(df.to_string())

def delete(df,n):
    global t1
    df.drop(df.index[n],inplace=True)
    df.reset_index(drop=True,inplace=True)
    df.to_excel(filename, index=False)
    xscrollbar = Scrollbar(window3, orient=HORIZONTAL)
    xscrollbar.grid(row=12, column=3, columnspan=3, sticky=N + S + E + W)
    t1 = Text(window3, wrap=NONE, xscrollcommand=xscrollbar.set, height=10, width=40)
    t1.grid(row=11, column=3, columnspan=3)
    ScrollBar = Scrollbar(window3, command=t1.yview, orient="vertical")
    ScrollBar.grid(row=11, column=6, rowspan=2, sticky="ns")
    t1.configure(yscrollcommand=ScrollBar.set)
    xscrollbar.config(command=t1.xview)
    ScrollBar.config(command=t1.yview)
    sys.stdout = PrintToT1()
    display(df.to_string())


def selected_item(l):
    for i in l.curselection():
        return l.get(i)


def getplot(df,x,y):
    figure1 = pyplot.Figure(figsize=(7, 3), dpi=100)
    ax1 = figure1.add_subplot(211)
    p1 = FigureCanvasTkAgg(figure1, window4)
    p1.get_tk_widget().grid(row=5, column=0,columnspan=3,rowspan=2)
    if x==y:
        if is_numeric_dtype(df[str(y)])==True :
          df1 = df[[str(y)]]
          df1.plot(kind='hist', legend=True, ax=ax1,bins=5,title=str(y)+' histogram')
        else :
          df[str(y)].value_counts().plot(kind='bar',legend=True, ax=ax1,title=str(y)+' barplot');
    elif x==None :
        if is_numeric_dtype(df[str(y)])==True :
          df1 = df[[str(y)]]
          df1.plot(kind='hist', legend=True, ax=ax1,bins=5,title=str(y)+' histogram')
        else :
          df[str(y)].value_counts().plot(kind='bar',legend=True, ax=ax1,title=str(y)+' barplot');
    elif y==None :
        if is_numeric_dtype(df[str(x)])==True :
          df1 = df[[str(x)]]
          df1.plot(kind='hist', legend=True, ax=ax1,bins=5,title=str(x)+' histogram')
        else :
          df[str(x)].value_counts().plot(kind='bar',legend=True, ax=ax1,title=str(x)+' barplot');
    else:
        if is_numeric_dtype(df[str(x)])==True and is_numeric_dtype(df[str(y)])==True :
            ax1.scatter(df[str(x)], df[str(y)], color='blue',s=10)
            ax1.set_xlabel(str(x))
            ax1.set_ylabel(str(y))
            ax1.title.set_text(str(x)+"/"+str(y)+" scatterplot")
        elif is_numeric_dtype(df[str(x)])==True and is_numeric_dtype(df[str(y)])==False:
            ax=sns.barplot(df[str(y)],df[str(x)],ax=ax1)
            ax.set_xticklabels(ax.get_xticklabels(), rotation=90, ha="right",fontsize=7)
            ax.set_title(str(x)+"/"+str(y)+" Barplot")
        elif is_numeric_dtype(df[str(y)])==True and is_numeric_dtype(df[str(x)])==False:
            ax = sns.barplot(df[str(x)], df[str(y)], ax=ax1)
            ax.set_xticklabels(ax.get_xticklabels(), rotation=90, ha="right", fontsize=7)
            ax.set_title(str(x)+"/"+str(y)+" Barplot")
        else:
            label_format = '{:,.0f}'
            df1 = df[[str(x),str(y)]]
            az= sns.histplot(df1,x=str(x), hue=str(y),multiple='stack', palette='tab20c', shrink=0.8,ax=ax1)
            az.set_xticklabels(az.get_xticklabels(), rotation=40, ha="right", fontsize=7)
            az.set_title(str(x)+"/"+str(y)+" Stacked Barchart")

def stat(df):
    global t2,window4
    i=1
    set_option('display.max_rows', 500)
    set_option('display.max_columns', 500)
    set_option('display.width', 1000)
    window4=Toplevel()
    window4.geometry("700x1000")
    window4.rowconfigure(6, weight=4)
    xscrollbar = Scrollbar(window4, orient=HORIZONTAL)
    xscrollbar.grid(row=1, column=0,columnspan=2, sticky=N + S + E + W)
    t2 = Text(window4, wrap=NONE, xscrollcommand=xscrollbar.set, height=10, width=40)
    t2.grid(row=0, column=0,columnspan=2)
    ScrollBar = Scrollbar(window4, command=t2.yview, orient="vertical")
    ScrollBar.grid(row=0, column=2, sticky="ns")
    t2.configure(yscrollcommand=ScrollBar.set)
    xscrollbar.config(command=t2.xview)
    ScrollBar.config(command=t2.yview)
    sys.stdout = PrintToT2()
    DF=df.describe()
    DF2=df.mode()
    DF2=DF2.head(1)
    DF2.set_index(Series(['mode']),inplace=True)
    display(DF)
    display(DF2)
    xaxis = Label(window4, text="x-axis")
    yaxis = Label(window4, text="y-axis")
    xlistbox = Listbox(window4,exportselection=0,selectmode=MULTIPLE)
    ylistbox = Listbox(window4,exportselection=0,selectmode=MULTIPLE)
    for col_name1 in df.columns:
        xlistbox.insert(i,str(col_name1))
        ylistbox.insert(i,str(col_name1))
        i=i+1
    xaxis.grid(column=0,row=2)
    yaxis.grid(column=1, row=2)
    xlistbox.grid(column=0, row=3)
    ylistbox.grid(column=1, row=3)
    pb = Button(window4, text="Run")
    pb.bind("<Button-1>", lambda event: getplot(df=df,x=selected_item(xlistbox),y=selected_item(ylistbox)))
    pb.grid(column=0, row=4,columnspan=2)

class PrintToT2(object):
    def write(self, s):
        t2.insert(END, s)

class PrintToT1(object):
    def write(self, s):
        t1.insert(END, s)

#this class will represent the excel file opened with all the variables needed to manupilate it
class Efile:
    def __init__(self,filename):
        self.filename=filename
        self.df=read_excel(self.filename)

    def readwrite(self):
        global Le2,DF,Le3
        style.configure('W.TButton', font=('calibri', 10, 'bold'), borderwidth='2')
        style.map('W.TButton', foreground=[('active', '!disabled', 'red')], background=[('active', 'black')])
        style.configure('W.TLabel', font=('Helvetica', 8))
        Lbd=list()
        Le2 = list()
        Le3=list()
        i=0
        DF=DataFrame()
        style.configure('W.TLabel', font=('Helvetica', 8))
        for col_name in self.df.columns:
            Le3.append(col_name)
            labelC = Label(window3, text=str(col_name),style='W.TLabel' )
            entryC = Entry(window3)
            Le2.append(entryC)
            labelC.grid(column=i, row=0,padx=8)
            entryC.grid(column=i, row=1,padx=8)
            i=i+1
        delb=Button(window3, text="Delete",style='W.TButton')
        delb.grid(column=0, row=4)
        labeld = Label(window3, text="Delete row number: ",style='W.TLabel')
        entryd = Entry(window3)
        labeld.grid(column=0, row=2)
        entryd.grid(column=0, row=3)
        delb.bind("<Button-1>", lambda event: delete(df=self.df,n=int(Entry.get(entryd))))
        rwb = Button(window3, text="Add")
        rwb.bind("<Button-1>", lambda event: add(df=self.df))
        rwb.grid(column=i, row=1)


#this function will enable the creation of a file
def createFile():
    global colentry,window2
    style.configure('left.TButton', font=('calibri', 10, 'bold'), borderwidth='2')
    style.map('left.TButton', foreground=[('active', '!disabled', 'green')], background=[('active', 'black')])
    style.configure('W.TButton', font=('calibri', 10, 'bold'),borderwidth='2')
    style.map('W.TButton', foreground=[('active', '!disabled', 'red')], background=[('active', 'black')])
    style.configure('TLabel', font=('Helvetica', 10))
    window2=Toplevel()
    window2.geometry("800x200")
    window2.rowconfigure(0, weight=2)
    window2.rowconfigure(1, weight=2)
    window2.rowconfigure(2, weight=1)
    window2.rowconfigure(3, weight=1)
    collabel=Label(window2,text="Please choose the number of columns",style='TLabel')
    collabel.grid(column=0,row=0,)
    colentry=Entry(window2)
    colentry.grid(column=0,row=1)
    colbutton=Button(window2,text="Run",style = 'left.TButton',command=getInput)
    colbutton.grid(column=0,row=2)
    colbutton = Button(window2, text="Clear",style = 'W.TButton',command=delete_entry)
    colbutton.grid(column=0, row=3)
    window2.mainloop()





#this function will enable file browsing in a window and creating an instance of eFile
def browseFiles():
    global window3,filename,t1
    filename = filedialog.askopenfilename(initialdir="/",title="Select a File",filetypes=[("Excel files", "*.xlsx")])
    f=Efile(filename)
    window3=Toplevel()
    window3.geometry("1000x300")
    f.readwrite()
    xscrollbar = Scrollbar(window3, orient=HORIZONTAL)
    t1 = Text(window3, wrap=NONE,xscrollcommand=xscrollbar.set,height=10, width=40)
    ScrollBar = Scrollbar(window3, command=t1.yview, orient="vertical")
    t1.configure(yscrollcommand=ScrollBar.set)
    xscrollbar.config(command=t1.xview)
    ScrollBar.config(command=t1.yview)
    sys.stdout = PrintToT1()
    display(f.df.to_string())
    statb=Button(window3,text="Statistics")
    statb.bind("<Button-1>", lambda event: stat(f.df))
    xscrollbar.grid(row=12, column=3, columnspan=3, sticky=N + S + E + W)
    t1.grid(row=11, column=3, columnspan=3)
    ScrollBar.grid(row=11, column=6, rowspan=2, sticky="ns")
    statb.grid(column=4,row=4)
    window3.mainloop()




window=Tk()
window.title("Graphsheet")
window.geometry("350x400")
window.rowconfigure(0,weight=2)
window.rowconfigure(1,weight=1)
window.rowconfigure(2,weight=1)
image = Image.open('C:/Users/21699/Downloads/1111.jpg' )
image.thumbnail((350,600),Image.ANTIALIAS)
photo= ImageTk.PhotoImage(image)
label_image= Label(image=photo)
label_image.grid(columnspan=2,row=0)
style = Style()
style.configure('TButton', font =('calibri', 10, 'bold'),borderwidth = '2')
style.map('TButton', foreground = [('active', '!disabled', 'green')],background = [('active', 'black')])
button=Button(window,text="Choose excel file",command=browseFiles,style = 'TButton')
button2=Button(window,text="Create excel file",command=createFile,style = 'TButton')
button.grid(column=0, row=1)
button2.grid(column=1,row=1)
cl=Label(window,text="Created by Baha Kahri")
cl.grid(columnspan=2,row=2)

window.mainloop()
