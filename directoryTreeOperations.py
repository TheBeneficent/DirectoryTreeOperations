import os
import pathlib
import platform
import re
import shutil
import tkinter as tk
from tkinter import filedialog
from tkinter import scrolledtext

def fileTree(p, file_types='', dst_drive='',dirtree=True, filetree=True, inc_base=True, dst_files_type=''):
    if platform.system() == "Windows":
        path_type = 'windows'
        if dst_drive:
            dst_drive=pathlib.PureWindowsPath(dst_drive)
    elif platform.system() == "Linux":
        path_type = 'linux'
        if dst_drive:
            dst_drive=pathlib.PurePosixPath(dst_drive)
    else:
        raise RuntimeError("Unknown platform")
    path_len = len(p)
    base_dir=os.path.basename(p)
    
    i = 0
    j=0
    file_tree = []
    rel_file_tree = []
    dst_file_tree = []
    file_with_ext = []
    file_dir_with_ext=[]
    dir_tree = []
    file_dir=[]
    rel_file_dir=[]
    rel_dir_tree = []
    dst_dir_tree = []
    dst_file_with_ext=[]
    dst_dir_with_ext=[]
    dst_file_with_dst_ext=[]
    dir_with_ext = []
    str_file_tree = ''
    str_dir_tree=''
    file_with_ext_str = ''
    dst_file_with_ext_str=''
    src_size=0
    src_with_ext_size=0
    if dst_files_type and not dst_files_type.startswith('.'):
        dst_files_type = '.' + dst_files_type
    if file_types:
        file_types = list(map(str, file_types.replace(' ','').split(',')))
    for path, subdirs, files in os.walk(p):
        if dirtree:
            for name in subdirs:
                if path_type == 'windows':
                    if inc_base:
                        dir_tree.append(str(os.path.join(base_dir, pathlib.PureWindowsPath(path, name))))
                        rel_dir_tree.append(str(os.path.join(base_dir, pathlib.PureWindowsPath(dir_tree[j][path_len+1:]))))
                    else:
                        dir_tree.append(str( pathlib.PureWindowsPath(path, name)))
                        rel_dir_tree.append(str(pathlib.PureWindowsPath(dir_tree[j][path_len+1:])))
                else:
                    if inc_base:
                        dir_tree.append(str(os.path.join(base_dir, pathlib.PurePosixPath(path, name))))
                        rel_dir_tree.append(str(os.path.join(base_dir, pathlib.PurePosixPath(dir_tree[j][path_len+1:]))))
                    else:
                        dir_tree.append(str(pathlib.PurePosixPath(path, name)))
                        rel_dir_tree.append(str(pathlib.PurePosixPath(dir_tree[j][path_len+1:])))
                
                if dst_drive:
                    dst_dir_tree.append( str(os.path.join(dst_drive,rel_dir_tree[j])) )

                str_dir_tree += str(j+1)+') '+str(rel_dir_tree[j])+'\n'
                j += 1
        if filetree:
            for name in files:
                if path_type == 'windows':
                    file_tree.append(str(pathlib.PureWindowsPath(path, name)))
                    file_dir.append(str(pathlib.PureWindowsPath(path)))
                    if inc_base:
                        rel_file_tree.append(str(os.path.join(base_dir,pathlib.PureWindowsPath(file_tree[i][path_len+1:]))))
                        rel_file_dir.append(str(os.path.join(base_dir,pathlib.PureWindowsPath(file_dir[i][path_len+1:]))))
                    else:
                        rel_file_tree.append(str(pathlib.PureWindowsPath(file_tree[i][path_len+1:])))
                        rel_file_dir.append(str(pathlib.PureWindowsPath(file_dir[i][path_len+1:])))
                        
                elif path_type == 'linux':
                    file_tree.append(str(pathlib.PurePosixPath(path, name)))
                    file_dir.append(str(pathlib.PurePosixPath(path)))
                    if inc_base:
                        rel_file_tree.append(str(os.path.join(base_dir,pathlib.PurePosixPath(file_tree[i][path_len+1:]))))
                        rel_file_dir.append(str(os.path.join(base_dir,pathlib.PurePosixPath(file_dir[i][path_len+1:]))))
                    else:
                        rel_file_tree.append(str(pathlib.PurePosixPath(file_tree[i][path_len+1:])))
                        rel_file_dir.append(str(pathlib.PurePosixPath(file_dir[i][path_len+1:])))
                    
                if dst_drive:
                    dst_file_tree.append(str(os.path.join(dst_drive,rel_file_tree[i])) )
                    
                if file_types:
                    for extindex in range(0,len(file_types)):
                        if not file_types[extindex].startswith('.'):
                            file_types[extindex] = '.'+file_types[extindex]
                        if file_tree[i].lower().endswith(file_types[extindex]):
                            file_with_ext.append(file_tree[i])
                            file_dir_with_ext.append(file_dir[i])
                            src_with_ext_size += os.path.getsize(file_tree[i])
                            dst_file_with_ext.append(dst_file_tree[i])
                            if(dst_files_type):
                                dst_file_with_dst_ext.append(dst_file_tree[i][:dst_file_tree[i].rfind('.')]+dst_files_type)
                            dst_dir_with_ext.append(dst_file_tree[i].rpartition(os.sep)[0])
                            
                src_size += os.path.getsize(file_tree[i])
                str_file_tree += str(i+1)+') '+str(rel_file_tree[i])+'\n'
                i += 1
        
    l=len(file_with_ext)
    m=0
    while m<l:
        file_with_ext_str += str(m+1) + ') '+str(file_with_ext[m])+'\n'
        m+=1
    n=0
    while n<l:
        dst_file_with_ext_str += str(n+1) + ') '+str(dst_file_with_ext[n])+'\n'
        n+=1
    
    return {"file_count": i,"dir_count":j, "file_with_ext_count":len(file_with_ext), "file_dir_with_ext_count":len(file_dir_with_ext), "file_tree": file_tree, "rel_file_tree": rel_file_tree, "rel_file_tree_str": str_file_tree, "dst_file_tree": dst_file_tree, "file_with_ext": file_with_ext, "file_dir_with_ext":file_dir_with_ext, "file_with_ext_str": file_with_ext_str, "dst_file_with_ext":dst_file_with_ext, "dst_file_with_ext_str":dst_file_with_ext_str, "dst_file_with_dst_ext":dst_file_with_dst_ext, "dst_dir_with_ext":dst_dir_with_ext, "file_dir":file_dir, "rel_file_dir":rel_file_dir, "dir_tree":dir_tree,"rel_dir_tree":rel_dir_tree,"rel_dir_tree_str":str_dir_tree, "dst_dir_tree":dst_dir_tree, "src_size":src_size,"src_with_ext_size":src_with_ext_size}

def deletefile(X):
    for i in X:
        s=''
        if os.path.exists(i):
            try:
                os.remove(i)
            except Exception as e:
                s += 'Error deleting "'+i+'":' + str(e)+'\n'
            

def makedir(X):
    s=''
    for dir in X:
        if not os.path.exists(dir):
            try:
                os.makedirs(dir)
            except Exception as e:
                s += 'Error creating "'+dir+'":' + str(e)+'\n'
    return s
def rec_copy(srclist,destlist,dst_dir_tree):
    l=len(srclist)
    if len(destlist) != l:
        return False
    
    message=''
    message += makedir(dst_dir_tree)

    if message:
        return 'Error creating destination directories!\n'+message
    copy_msg=''
    for i in range(0,l):
        try:
            copy_msg = shutil.copy2(srclist[i],destlist[i])
            message += str(i+1)+ ') Successfully copied ' + copy_msg + '\n'
        except:
            message += str(i+1)+ ') Error copying '+copy_msg+'\n'
    return message
def rec_move(srclist,destlist,dst_dir_tree):
    message=''
    message=rec_copy(srclist,destlist,dst_dir_tree)
    deletefile(srclist)
    return message

global folder
global dst_folder
global file_extensions
global source_dir
global results
global dir_check_state
global operate_state
folder=''
dst_folder=''
source_dir=''
results=''
dir_check_state=False
operate_state=''
win_w = 800
win_h = 650
y = 20
h = 25
t0=15
t1=25
t2=25
t=30
h2=int(win_h*5/12)
x1=int(win_w/12)
x2=int(win_w*6.5/12)
w=int(win_w*4.5/12)
w2=2*w
w_btn=60

win = tk.Tk()
win.title("Mostanad File Copier 0.3 \u00A9 github.com/TheBeneficent")
win.geometry(str(win_w)+"x"+str(win_h))
dir_label = tk.Label(text="Enter the source directory")
path_dir_input = tk.Entry()
dst_label=tk.Label(text="Enter destination directory")
dst_dir_input=tk.Entry()
ext_label = tk.Label(text="Enter file formats separated by comma, e.g. jpg, txt, png")
ext_text_input = tk.Entry()
tree_label=tk.Label(text="Directory Tree")
tree_scroll_view = scrolledtext.ScrolledText(win, wrap=tk.WORD)
filtered_label=tk.Label(text="Filtered Tree")
filtered_scroll_view = scrolledtext.ScrolledText(win, wrap=tk.WORD)
src_label=tk.Label(text="Source")
src_scroll_view = scrolledtext.ScrolledText(win, wrap=tk.WORD)
dst_label=tk.Label(text="Destination")
dst_scroll_view = scrolledtext.ScrolledText(win, wrap=tk.WORD)
oper_state_scroll_view=scrolledtext.ScrolledText(win,wrap=tk.WORD)
oper_state_label=tk.Label(text="Operation Status")

def humanReadableFileSize(size_in_bytes,prec=6):
    if size_in_bytes>=1024**4:
        return "{:.6f}".format(size_in_bytes/(1024**4))+' TB'
    elif size_in_bytes>=1024**3:
        return "{:.6f}".format(size_in_bytes/(1024**3))+' GB'
    elif size_in_bytes>=1024**2:
        return "{:.6f}".format(size_in_bytes/(1024**2))+' MB'
    elif size_in_bytes>=1024:
        return "{:.6f}".format(size_in_bytes/(1024))+' KB'
    else:
        return "{:.6f}".format(size_in_bytes)+' Bytes'

def browsetrig():
    global folder
    global dst_folder
    global file_extensions
    global source_dir
    global results
    global dir_check_state
    operate_state=''
    oper_state_scroll_view.delete('1.0', tk.END)
    folder = filedialog.askdirectory()
    path_dir_input.delete('0', tk.END)
    path_dir_input.insert('0', folder)
    folder = path_dir_input.get()
    if folder:
        operate_state='Source set!\n'
    oper_state_scroll_view.insert(tk.INSERT, operate_state)
    # results = fileTree(folder,dest_drive=dst_folder)
    # tree_scroll_view.delete('1.0', tk.END)
    # tree_scroll_view.insert(tk.INSERT, 'Directories:\n'+results["rel_dir_tree_str"]+'\nFiles:\n'+results["rel_file_tree_str"])
def dstbrowsetrig():
    global folder
    global dst_folder
    global file_extensions
    global source_dir
    global results
    global dir_check_state
    operate_state=''
    oper_state_scroll_view.insert(tk.INSERT, operate_state)
    dst_folder=filedialog.askdirectory()
    dst_dir_input.delete('0', tk.END)
    dst_dir_input.insert('0', dst_folder)
    dst_folder=dst_dir_input.get()
    if folder and dst_folder:
        operate_state='Destinatin set!\n'
        results = fileTree(folder,dst_drive=dst_folder)
        tree_scroll_view.delete('1.0', tk.END)
        src_size=humanReadableFileSize(results['src_size'])
        tree_scroll_view.insert(tk.INSERT, 'Total number of directories: '+str(results['dir_count'])+'\nTotal number of files: '+str(results['file_count'])+'\nTotal size: '+str(src_size)+'\n' + 'Directories:\n'+results["rel_dir_tree_str"]+'\n\n----------\n\nFiles:\n'+results["rel_file_tree_str"])
    oper_state_scroll_view.insert(tk.INSERT, operate_state)

def filtertrig():
    global folder
    global dst_folder
    global file_extensions
    global source_dir
    global results
    global dir_check_state
    operate_state=''
    oper_state_scroll_view.delete('1.0', tk.END)
    folder = path_dir_input.get()
    dst_folder=dst_dir_input.get()
    file_extensions=ext_text_input.get()
    results=fileTree(folder,file_types=file_extensions,dst_drive=dst_folder)
    src_with_ext_size=humanReadableFileSize(results['src_with_ext_size'])
    filtered_scroll_view.delete('1.0', tk.END)
    filtered_scroll_view.insert(tk.INSERT,'Total number of directories: '+str(results['file_dir_with_ext_count'])+'\nTotal number of files: '+str(results['file_with_ext_count'])+'\nTotal size: '+src_with_ext_size+'\n' + 'Destination files would be like:\n'+results['dst_file_with_ext_str'])
    oper_state_scroll_view.insert(tk.INSERT, operate_state)

    
def copytrig():
    global folder
    global dst_folder
    global file_extensions
    global source_dir
    global results
    global dir_check_state
    global operate_state
    operate_state=''
    oper_state_scroll_view.delete('1.0', tk.END)
    folder = path_dir_input.get()
    dst_folder=dst_dir_input.get()
    file_extensions=ext_text_input.get()
    if not results:
        results = fileTree(folder,dst_drive=dst_folder,file_types=file_extensions)
    if results["file_with_ext"]:

        res=rec_copy(results["file_with_ext"],results["dst_file_with_ext"],results["dst_dir_with_ext"])
        if res:
            operate_state=res
        else:
            operate_state="Copied successfully!"
    else:
        res=rec_copy(results["file_tree"],results["dst_file_tree"],results["dst_dir_tree"])
        if res:
            operate_state=res
        else:
            operate_state="Copied successfully!"
    oper_state_scroll_view.insert(tk.INSERT, operate_state)
def movetrig():
    global folder
    global dst_folder
    global file_extensions
    global source_dir
    global results
    global dir_check_state
    global operate_state
    operate_state=''
    oper_state_scroll_view.delete('1.0', tk.END)
    folder = path_dir_input.get()
    dst_folder=dst_dir_input.get()
    file_extensions=ext_text_input.get()
    if not results:
        results = fileTree(folder,dst_drive=dst_folder,file_types=file_extensions)
    if results["file_with_ext"]:

        res=rec_copy(results["file_with_ext"],results["dst_file_with_ext"],results["dst_dir_with_ext"])
        res2= deletefile(results["file_with_ext"])
        if res and res2:
            res += res+res2
        elif res2:
            res += res2
        elif res:
            res +=res
            operate_state=res
        else:
            operate_state="Moved successfully!"
    else:
        res=rec_copy(results["file_tree"],results["dst_file_tree"],results["dst_dir_tree"])
        res2= deletefile(results["file_tree"])
        if res:
            operate_state=res
        else:
            operate_state="Copied successfully!"
    oper_state_scroll_view.insert(tk.INSERT, operate_state)
def checktrig():
    global folder
    global dst_folder
    global file_extensions
    global source_dir
    global results
    global dir_check_state
    dir_check_state = not dir_check_state
def mkdirtrig():
    global folder
    global dst_folder
    global file_extensions
    global source_dir
    global results
    global dir_check_state
    operate_state=''
    oper_state_scroll_view.delete('1.0', tk.END)
    folder = path_dir_input.get()
    dst_folder=dst_dir_input.get()
    file_extensions=ext_text_input.get()
    if not results:
        results = fileTree(folder,dst_drive=dst_folder)
    operate_state=makedir(results["dst_dir_tree"])
    if not operate_state.replace(' ',''):
        operate_state='Paths made successfully!\n'
    oper_state_scroll_view.insert(tk.INSERT, operate_state)
    
browse_btn = tk.Button(text="Browse", command=browsetrig)
dest_browse_btn=tk.Button(text="Browse",command=dstbrowsetrig)
filter_btn=tk.Button(text="Filter",command=filtertrig)
dir_check=tk.Checkbutton(win,text="Create directories only",anchor='w',command=checktrig)
copy_btn=tk.Button(text="Copy",command=copytrig)
move_btn=tk.Button(text="Move",command=movetrig)
mkdir_btn=tk.Button(text="Create Folders",command=mkdirtrig)

dir_label.place(x=x1, y=y, width=w2, height=h)
y += t1
path_dir_input.place(x=x1, y=y, width=w2, height=h)
browse_btn.place(x=x1+w2, y=y, width=w_btn, height=h)
y+=t2
dst_label.place(x=x1,y=y,width=w2,height=h)
y += t1
dst_dir_input.place(x=x1,y=y,width=w2,height=h)
dest_browse_btn.place(x=x1+w2,y=y,width=w_btn,height=h)
y += t2
ext_label.place(x=x1, y=y, width=w2, height=h)
y += t1
ext_text_input.place(x=x1, y=y, width=w2, height=h)
y += t2
tree_label.place(x=x1,y=y,width=w,height=h)
filtered_label.place(x=x2,y=y,width=w,height=h)
y += t1
tree_scroll_view.place(x=x1, y=y,width=w, height=h2)
filtered_scroll_view.place(x=x2,y=y,width=w,height=h2)
y +=10+h2
copy_btn.place(x=x1,y=y,width=w_btn,height=h)
move_btn.place(x=x2-2*x1,y=y,width=w_btn,height=h)
mkdir_btn.place(x=x2,y=y,width=w_btn*2,height=h)
filter_btn.place(x=3*x1+x2,y=y,width=w_btn,height=h)
y += t2
oper_state_label.place(x=x1,y=y,width=w2,height=h)
y+=t2
oper_state_scroll_view.place(x=x1,y=y,width=w2+w_btn,height=3*h)

win.mainloop()
