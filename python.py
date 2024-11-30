import time
import serial
import tkinter
import tkinter.messagebox
import re
#from PIL import Image, ImageTk

ser=serial.Serial("COM7", 115200,timeout=2)

flag = True
        
def setFlag(value):
    global flag 
    flag = True
    
def print_selection2(value): 
    global flag
    msg = ser.readline().decode()
    print('msg format ={}'.format(msg))
    msg_data=re.split(',|:',msg)
    LabelA.config(text=f"Speed : {msg_data[3]} cm/s")
    LabelA.update_idletasks()
    Tkwindow.update()
    if("distance"in str(msg_data[0])) and len(msg_data) == 4:
            #將拉桿位置顯示出來
            if float(msg_data[1]) < 10:
                tkinter.messagebox.showwarning(title='距離',message='距離過近')
            elif float(msg_data[1]) == 0:
                if flag:
                    tkinter.messagebox.showerror(title='距離',message='危險')
                    distance = msg_data[1].replace(r"\r\n", '')
                    flag = False
                    LabelA.config(text="Error!!")
                    LabelA.update_idletasks()
                    print("上傳完成")
                
    Tkwindow.update()
    Tkwindow.after(10000,print_selection2(1))
    
def SerialWrite(command):
    ser.write(command)
    rv=ser.readline()
    
    print(rv.decode("utf-8"))
    data=rv.decode("utf-8")
    print(data)
    time.sleep(1)
    ser.flushInput()


def SendCmdC():
    Ardiuno_cmd='c'
    cmd=Ardiuno_cmd.encode("utf-8")
    SerialWrite(cmd)
    condition=True
    while(condition):
        rv1=ser.readline()
        data=rv1.decode("utf-8")
        print(data)
        LabelA.config(text=data)
        LabelA.update_idletasks()
        Tkwindow.update()
        if(condition==False):
            break
        
def Send_turnOff():
    Ardiuno_cmd='turnOff'
    cmd=Ardiuno_cmd.encode("utf-8")
    SerialWrite(cmd)
    condition=False
    
    LabelA.config(text="Send the command 'turnOff' to Ardiuno")
    LabelA.update_idletasks()
    Tkwindow.update()

def Serial_Connect():
    print("Connecting to Ardiuno.....")
    LabelA.config(text="No detect key")
    LabelA.update_idletasks()
    Tkwindow.update()
    time.sleep(1)
    Str_Message=rv.decode("utf-8")
    while Str_Message[0:6] != "locked": 
        for i in range(1,10):
            rv=ser.readline()
            print("Loading....")
            
            LabelA.config(text="Loading....")
            LabelA.update_idletasks()
            Tkwindow.update()
            
            print(rv.decode("utf-8"))
            ser.flushInput()
            time.sleep(1)
            Str_Message=rv.decode("utf-8")
            
            if Str_Message[0:6]=='unlocked':
                print("Unlock the car.")
                LabelA.config(text="Unlock the car.") 
                buttonStart.config(state="disabled")
                LabelA.update_idletasks()
                Tkwindow.update()
                break
        
def Exit():
    Isexit = tkinter.messagebox.askokcancel(title='askquestion',message='是否要熄火?')
    if Isexit:
        print("Exit...")
        LabelA.config(text="Exit...")
        LabelA.update_idletasks()
        Tkwindow.update()
        time.sleep(1)
        chr_num=27
        cmd=(chr(chr_num).encode('utf-8'))
        SerialWrite(cmd)
        ser.close()
        Tkwindow.destroy()
    

    
Tkwindow=tkinter.Tk()
Tkwindow.title("車輛儀表板")
Tkwindow.minsize(600,400)
Tkwindow.configure(background='#000000')

LabelA=tkinter.Label(Tkwindow,bg='#9F35FF',fg='white',text="Press '發動' button to start",font=("Helvetica",15,'bold'),width=30,height=10,justify=tkinter.LEFT)
LabelA.pack(side=tkinter.TOP)
buttonStart=tkinter.Button(Tkwindow,anchor=tkinter.S,text="發動",width=10,height=1,command=Serial_Connect)
buttonStart.pack(side=tkinter.RIGHT)
buttonEnd=tkinter.Button(Tkwindow,anchor=tkinter.S,text="熄火",width=10,height=1,command=Exit)
buttonEnd.pack(side=tkinter.LEFT)

var=tkinter.IntVar()
var2=tkinter.IntVar()
var3=tkinter.IntVar()

msg=ser.readline().decode()
print('serial_msg: ',msg)
msg_data=re.split(',|:',msg)
time.sleep(1)
   
Tkwindow.after(10000,print_selection2(1))

Tkwindow.mainloop()
