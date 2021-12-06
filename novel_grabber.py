
from tkinter import *
from tkinter.ttk import *
import requests                 #pip install requests 
from threading import Thread
import webbrowser
import time
from bs4 import BeautifulSoup as bs
import os
import urllib.request

        


#--------------------------------------
#       CLASSES
#--------------------------------------


class timer(Thread):
    
    "counts the total time of operatoin"
    exit_thread = False
    t1 = 0
    
    def __init__(self,t1):
        self.t1= t1
        Thread.__init__(self)

    def run(self):
        while(not self.exit_thread):
            time.sleep(1) #updates every second
            runtime.set(str(int(time.time()-self.t1))+ ' s')
            continue
        #StatusCode.set('closing timer ..')
      
    def kill(self):
        self.exit_thread = True

    


class download(Thread):
    
    "counts the total time of operatoin"
    exit_thread = False
    download_begin_flag = False
    
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        while(not self.exit_thread):
            if self.download_begin_flag:
                soup = get_chapter()
                if soup:
                    try:
                        nxt = next_chapter(soup)
                        url.set(nxt)
                    except:
                        StatusCode.set('download complete..')
                        self.download_begin_flag = False
                        
                else:
                    self.download_begin_flag = False
                

    def kill(self):
        self.exit_thread = True

    

class function_runner(Thread):
    "runs functions you define based on button click, in a seperate thread ie in parallel"
    check_requests_flag = False
    check_urllib_flag = False
    open_checkfile_flag = False
    requests_module_working_flag = False
    urllib_module_working_flag = False
    exit_thread = False

    
    
    def __init__(self):
        Thread.__init__(self)

    def run(self):

        while(not self.exit_thread):

            if self.check_requests_flag :
                try:
                    check_requests()
                except:
                    StatusCode.set('connection failed..')
                    parallel.requests_module_working_flag = False
                    
                self.check_requests_flag = False

            if self.check_urllib_flag :
                try:
                    check_urllib()
                except:
                    StatusCode.set('connection failed..')
                    parallel.urllib_module_working_flag = False
                self.check_urllib_flag = False

                
            if self.open_checkfile_flag :
                open_check_file()
                self.open_checkfile_flag = False

        #StatusCode.set('closing function runner..')

    def kill(self):
        self.exit_thread = True




#------------------------------------------------------
#       FUNCTIONS
#------------------------------------------------------

def check_requests():
    
    "download html data and make a checkfile"
    
    
    #parallel.check_accessibility_companion()
    #StatusCode.set("fetching data..")
    
    StatusCode.set("fetching..")
    print("fetching ..")

    t1 = time.time()
    r = requests.get(url.get(),headers=headers)
    t2 = time.time()
    
    print(r.status_code)

    if r.status_code == 200:
        parallel.requests_module_working_flag = True
    else:
        parallel.requests_module_working_flag = False
        
    

    StatusCode.set("status code : " + str(r.status_code)+' || time taken :'+' %.2f'%(t2-t1)+' s')

    f= open("checkfile.html",'w',encoding = 'utf-8')
    soup = bs(r.content,'html.parser')
    f.write(soup.prettify())
    f.close()
    
    
def check_requests_flagsetter():
    parallel.check_requests_flag = True


def check_urllib():
    
    print("fetching..")
    StatusCode.set("fetching..")

    t1 = time.time()    
    request = urllib.request.Request(url.get(), headers=headers)
    t2 = time.time()
    
    r = urllib.request.urlopen(request)
    code = r.getcode()
    r = r.read()

    if code == 200:
        parallel.urllib_module_working_flag = True
    
    else:
        parallel.urllib_module_working_flag = False
        

    print(code)
    
    content = r.decode('utf-8')
    soup = bs(content,'html.parser')
    
    
    StatusCode.set("status code : " + str(code)+' || time taken :'+' %.2f'%(t2-t1)+' s')



    f= open("checkfile.html",'w',encoding = 'utf-8')
    f.write(soup.prettify())
    f.close()
    
   
 

def check_urllib_flagsetter():
    parallel.check_urllib_flag = True



def get_chapter():


    if parallel.requests_module_working_flag == True :
        StatusCode.set("using requests module..")

        print("fetching..")
        StatusCode.set("fetching..")
        
        t1 = time.time()
        r = requests.get(url.get(),headers=headers)
        t2 = time.time()
    
        print(r.status_code)
        f= open("novel.html",'a+',encoding = 'utf-8')
        soup = bs(r.content,'html.parser')
        f.write(soup.prettify())
        f.close()

        StatusCode.set("status code : " + str(r.status_code)+' || time taken :'+' %.2f'%(t2-t1)+' s')

        return soup
        
        
        
    elif parallel.urllib_module_working_flag == True :

        StatusCode.set("using urllib module..")

        print("fetching..")
        StatusCode.set("fetching..")
        
        t1 = time.time()    
        request = urllib.request.Request(url.get(), headers=headers)
        t2 = time.time()
    
        r = urllib.request.urlopen(request)
        code = r.getcode()
        r = r.read()

        print(code)
    
        content = r.decode('utf-8')
        soup = bs(content,'html.parser')
    
    
        f= open("novel.html",'a+',encoding = 'utf-8')
        f.write(soup.prettify())
        f.close()

        StatusCode.set("status code : " + str(code)+' || time taken :'+' %.2f'%(t2-t1)+' s')

        return soup


        

    else:
        StatusCode.set("All available modules are unable to fetch..")

        return None
    
    
    

def get_path_to_checkfile():
    
    path_to_file = os.getcwd()
    path_to_file='file:///'+path_to_file.replace('\\','/')+'/'
    return(path_to_file)



def killer():
    "kills everything"
    downloader.kill()
    print("killed download thread")
    tmr.kill()
    #tmr.join()
    print('Killed Timer thread')
    parallel.kill()
    #parallel.join()
    print('Killed function_runner thread')
    time.sleep(1) #to prevent an error : RuntimeError: main thread is not in main loop
    root.destroy()
    print("Killed TK window")


def next_chapter(soup):
    StatusCode.set("finding the next chapter url..")
    prefix = url_prefix.get()
    lst = soup.findAll('a', attrs = {attribute_name.get():attribute_value.get()})
    #print(lst)
    no = int(element_no.get())
    if lst != [] :
        temp = lst[no]
        print(prefix+temp['href'])
        #url.set(prefix+temp['href'])
        return prefix+temp['href']
   



def open_check_file():

    StatusCode.set("opening checkfile..")
    #time.sleep(1)
    "opens the checkfile to check if the data was received properly"
    print("opening check file...")
    path = get_path_to_checkfile()
    path += 'checkfile.html'
    brwsr = webbrowser.get()
    brwsr.open(path)
    print("checkfile is open")
    StatusCode.set("checkfile is open in broswer..")




def open_checkfile_flagsetter():
    parallel.open_checkfile_flag = True



    
def download_begin_flagsetter():
    downloader.download_begin_flag = True

def temp():
    downloader.exit_thread = True


#------------------------------------------------------------------
#               MAIN
#------------------------------------------------------------------


if __name__ =='__main__':

    temp_url = '..enter the url of the first chapter here..'
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'}
    
    root  = Tk()
    root.title("NOVEL GRABBER (1.0)")

    #the entry box values
    url = StringVar()
    url.set(temp_url)
    StatusCode =StringVar()
    runtime = StringVar()
    url_prefix = StringVar()
    attribute_name = StringVar()
    attribute_value = StringVar()
    element_no  = StringVar()
    

    #preset values
    url_prefix.set('https://novelfull.com')
    attribute_name.set('id')
    attribute_value.set('next_chap')
    element_no.set(0)
    
    #managing threads
    parallel = function_runner()
    downloader = download()
    tmr = timer(int(time.time()))
    downloader.start()
    parallel.start()
    tmr.start()
    
    #creating the menu
    run_time_label           = Label(root,text = '-RunTime-')
    run_time_label.grid(row = 0, column = 0, sticky = W, pady = 2)
    run_time                 = Entry(root,   width = 10, textvariable = runtime)
    run_time.grid(row = 0, column = 2, sticky = W, pady = 2)
    url_entry_label          = Label(root, text = '-Target Url-')
    url_entry_label.grid(row = 1, column = 0, sticky = W, pady = 2)
    url_entry               = Entry(root,   width = 60, textvariable = url)
    url_entry.grid(row = 1, column = 2, sticky = W, pady = 2)
    status_entry_label      = Label(root,   text = '-Status-')
    status_entry_label.grid(row = 2, column = 0, sticky = W, pady = 2)
    status_entry            = Entry(root,   width = 60, textvariable = StatusCode)
    status_entry.grid(row = 2, column = 2, sticky = W, pady = 2)
    url_prefix_entry_label  = Label(root,   text = '-Url Prefix Entry-')
    url_prefix_entry_label.grid(row = 3, column = 0, sticky = W, pady = 2)
    url_prefix_entry        = Entry(root,   width = 60, textvariable = url_prefix)
    url_prefix_entry.grid(row = 3, column = 2, sticky = W, pady = 2)
    attribute_label         = Label(root,   text = '-Attribute-')
    attribute_label.grid(row = 4, column = 0, sticky = W, pady = 2)
    attribute               = Entry(root,   width = 60, textvariable = attribute_name)
    attribute.grid(row = 4, column = 2, sticky = W, pady = 2)
    attribute_entry_label  = Label(root,   text = '-Attribute Value-')
    attribute_entry_label.grid(row = 5, column = 0, sticky = W, pady = 2)
    attribute_entry        = Entry(root,   width = 60, textvariable = attribute_value)
    attribute_entry.grid(row = 5, column = 2, sticky = W, pady = 2)
    element_number_label    = Label(root,   text = '-Element Number-')
    element_number_label.grid(row = 6, column = 0, sticky = W, pady = 2)
    element_number          = Entry(root,   width = 60, textvariable = element_no)
    element_number.grid(row = 6, column = 2, sticky = W, pady = 2)
    
    requests_btn                 = Button(root, width = 20,  text = 'check requests', command = check_requests_flagsetter)
    requests_btn.grid(row = 7, column = 0, sticky = W, pady = 2)
    urllib_btn                 = Button(root, width = 20,  text = 'check urllib', command = check_urllib_flagsetter)
    urllib_btn.grid(row = 7, column = 1, sticky = W, pady = 2)
    open_check_file_button  = Button(root, width = 20 , text = 'open checkfile', command = open_checkfile_flagsetter)
    open_check_file_button.grid(row = 7, column = 2, sticky = W, pady = 2)
    dwnload_button            = Button(root, width = 20 , text = 'download begin'          , command = download_begin_flagsetter)
    dwnload_button.grid(row = 8, column = 0, sticky = W, pady = 2)
    
    
    close_button            = Button(root, width = 20 , text = 'close'          , command = killer)
    close_button.grid(row = 8, column = 2, sticky = W, pady = 2)


    
    
    root.mainloop()
    
