
from tkinter import *
from psutil import disk_partitions,disk_usage,virtual_memory,cpu_percent
from tabulate import tabulate 


#definition of GUI window
window=Tk()
window.geometry("900x600")
window.title("CPU - RAM - DISK USAGE")

# create a menu
menubar = Menu(window)
window.config(menu=menubar)
file_menu = Menu(menubar, tearoff=0)
# add a menu item to the menu

menubar.add_cascade(
    label="File",
    menu=file_menu
)




file_menu.add_command(
    label='Exit',
    command=window.destroy
)



# function to display CPU info
def show_cpu_info():
    cpu_use=cpu_percent(interval=1)
    cpu_label.config(text='{} %'.format(cpu_use))
    cpu_label.after(200,show_cpu_info)

# Function to convert bytes to GB
def converter(byte):
    one_gigabyte=1073741824 #bytes
    giga=byte/one_gigabyte
    giga='{0:.1f}'.format(giga)
    return giga

# function to display RAM info 
def show_ram_info():
    ram_usage=virtual_memory()
    ram_usage=dict(ram_usage._asdict())
    for key in ram_usage:
        if key!='percent':
            ram_usage[key]=converter(ram_usage[key])
              
    ram_label.config(text='{} GB/{} GB({}%)'.format(ram_usage["used"],ram_usage["total"],ram_usage["percent"]))
    ram_label.after(200,show_ram_info)


data=disk_partitions(all=False)

# function for device name
def details(device_name):
    for i in data: 
        if i.device==device_name:
            return i

# function for disk partions 
def get_device_names():
    return [i.device for i in data] #return c

# function to show disk info
def disk_info(device_name):
        disk_info={}
        try:
            usage=disk_usage(device_name)
            disk_info['Device']=device_name
            disk_info['Total']=f"{converter(usage.used+usage.free)} GB"
            disk_info['Used']=f"{converter(usage.used)} GB"
            disk_info['Free']=f"{converter(usage.free)} GB"
            disk_info['Percent']=f"{usage.percent} %"
        except PermissionError:
            pass
        except FileNotFoundError:
            pass
        info=details(device_name)
        disk_info.update({"Device":info.device})
        disk_info["Mount Point"]=info.mountpoint
        disk_info["FS type"]=info.fstype
        disk_info["Opts"]=info.opts
        return disk_info    

# function to return info of all partions
def all_disk_info(): 
    return_all=[]
    for i in get_device_names():
        return_all.append(disk_info(i))
    return return_all

def save_table():
    info=infoTabulated
    file=open("Disk info.txt", "a+")
    file.write(infoTabulated)
    file.close()


    
def write_file():
    file = open("save_comment.txt", "a+")
    file.write(commentsbox.get("1.0", END) + "\n" + "\n")
    file.close()
    commentsbox.delete("1.0", END)

#title of program 
title_program=Label(window, text ='PC Performance Manager', font="arial 35", fg="#14747F")
title_program.place(x=110, y=20)

#CPU title
cpu_title_label=Label(window, text='CPU Usage: ', font="arial 16", fg="#FA5124")
cpu_title_label.place(x=20, y=155)

#label to show cpu percent 
cpu_label=Label(window, bg='#071C1E', fg='#FA5124', font="arial 16", width=20)
cpu_label.place(x=230, y=150)


# RAM title 
ram_title_label=Label(window, text='RAM usage: ', fg='#FA5124', font="arial 16", width=20)
ram_title_label.place(x=20,y=255) 
# label to show RAM 
ram_label=Label(window,bg='#071C1E', fg='#FA5124', font="arial 16", width=20)
ram_label.place(x=230,y=250)

# Disk title
disk_title_label=Label(window, text='Disk usage: ', font="arial 16", fg='#FA5124')
disk_title_label.place(x=350,y=360)
#Text area for disk info
textArea=Text(window,bg="#071C1E", fg="yellow", width=85, height=6, padx=10, font=("consolas",14))
textArea.place(x=15,y=410)



# textbox for comments
commentsbox = Text(window, height=10, width=30)
commentsbox.place(x=550,y=120)


#save button
button =  Button(text='Save', height=2, width=10, padx=5, command=write_file)
button.place(x=620,y=300)

file_menu.add_command(
    label='Export disk info to txt', 
    command=save_table 
    )


if __name__ =='__main__':
    show_cpu_info()
    show_ram_info()
    info=all_disk_info()
    _list=[i.values() for i in info]
    infoTabulated=tabulate(_list,headers=info[0].keys(),tablefmt="simple",missingval="-")
    textArea.insert(END,infoTabulated)
    print(infoTabulated)
    window.mainloop()
