from cProfile import label
from enum import auto
from os import stat
from tkinter import *
from tkinter import messagebox
import sqlite3
import threading
from tkinter import Entry, ttk
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from time import sleep
from PIL import ImageTk, Image
import datetime
import schedule
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from time import strftime
from tkcalendar import DateEntry , Calendar

#create db

con = sqlite3.connect('irctcid.db')
cur = con.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS irctcid(userid text, password text)''')
cur.execute('''CREATE TABLE IF NOT EXISTS key(key text)''')
cur.execute('''CREATE TABLE IF NOT EXISTS paytm_upi(upiid text)''')
'''        
cur.execute("INSERT INTO key VALUES (:key)", {
                                            'key': 'Demo',

                            })
'''
cur.execute('''CREATE TABLE IF NOT EXISTS Form(
                            tfrom text, 
                            tto text,
                            date text,
                            class text,
                            quota text,
                            train text,
                            p1name text,
                            p1age text,
                            p1gender text,
                            p2name text,
                            p2age text,
                            p2gender text,
                            p3name text,
                            p3age text,
                            p3gender text,
                            p4name text,
                            p4age text,
                            p4gender text,
                            mobile text,
                            formname text
                            
                        )
                    ''')

con.commit()

#main window
def home_page():
    home_tk = Tk()
    home_tk.maxsize(width=250 ,  height=30)
    home_tk.minsize(width=250 ,  height=30)
    home_tk.title('Home Page')
    Button(home_tk, text='IRCTC ID', command=irctc_id).place(x=0, y=0)
    Button(home_tk, text='FORM', command=open_form).place(x=60, y=0)
    Button(home_tk, text='BANK', command=bank).place(x=108, y=0)
    Button(home_tk, text='NEW FORM', command=form).place(x=158, y=0)

    home_tk.mainloop()
#open form
def open_form():
    global my_w
    global imageLabel
    global imageLabel,lab1,lbl1,lab2,om22,om11,om1,log_btn
    now = datetime.datetime.now().time()
    engine = sqlite3.connect('irctcid.db')
    query="SELECT formname as class FROM Form"
                    
    my_data=engine.execute(query) # SQLAlchem engine result
    my_list = [r for r, in my_data] # create a  list 

    engine1 = sqlite3.connect('irctcid.db')
    query="SELECT userid as class FROM irctcid"
                    
    my_data1=engine.execute(query) # SQLAlchem engine result
    my_list1 = [r for r, in my_data1] # create a  list 

    engine2 = sqlite3.connect('irctcid.db')
    query="SELECT upiid as class FROM paytm_upi"

    my_data2 = engine2.execute(query)
    my_list2 = [r for r, in my_data2]

    my_w = Toplevel()
    my_w.maxsize(width=250 ,  height=200)
    my_w.minsize(width=250 ,  height=200)
    my_w.title('Form')  # Adding a title
    global options2
    global options1
    global options3
    lab1 = Label(my_w, text='Form',font = ('calibri', 10, 'bold'))
    lab1.place(x=25, y=0,)
    lbl1 = Label(my_w, text='Bank',font = ('calibri', 10, 'bold'))
    lbl1.place(x=110, y=0)
    lab2 = Label(my_w, text='ID',font = ('calibri', 10, 'bold'))
    lab2.place(x=195, y=0)
    lbl = Label(my_w, font = ('calibri', 15, 'bold'))
    lbl.place(x=10, y=170,)  

    def time():
        string = strftime('%I:%M:%S %p')
        lbl.config(text = string)
        lbl.after(1000, time)
    time()

    options3 = StringVar(my_w)
    options3.set(my_list2[0]) # default value
    om22 =OptionMenu(my_w, options3, *my_list2)
    om22.place(x=85, y=20,width=80)
    options2 = StringVar(my_w)
    options2.set(my_list[0]) # default value
    om1 =OptionMenu(my_w, options2, *my_list)
    om1.place(x=5, y=20,width=80)
    options1 = StringVar(my_w)
    options1.set(my_list1[0]) # default value
    om11 =OptionMenu(my_w, options1, *my_list1)
    om11.place(x=165, y=20,width=80)

    imageLabel = Label(my_w)
    imageLabel.place(x=1, y=10)
    
    log_btn = Button(my_w, text='LOGIN',width=5,font = ('calibri', 12, 'bold'), command=threading.Thread(target=fetch_form).start)
    log_btn.place(x=190, y=160)
    
    my_w.mainloop()
#starts booking
def fetch_form():
    form_name = options2.get()
    form_id = options1.get()
    global p_count
    global status
    lab1.destroy()
    lab2.destroy()
    lbl1.destroy()
    om1.destroy()
    om11.destroy()
    om22.destroy()
    status = Label(my_w, text='Connecting to IRCTC',font=("bold", 10),fg='Red', bg='Yellow')
    status.place(x=5, y=100)
    global driver,pfrom,pto,date,tclass,quota,train,p1name,p1age,p1gender,p2name,p2age,p2gender,p3name,p3age,p3gender,p4name,p4age,p4gender,mobile

    engine = sqlite3.connect('irctcid.db')
    query='SELECT * from irctcid where userid="%s"'

    engine1 = sqlite3.connect('irctcid.db')
    query1='SELECT * from Form where formname="%s"'

                    
    my_data=engine.execute(query%(form_id))
    my_data1=engine1.execute(query1%(form_name))
    result = my_data.fetchall()
    result1 = my_data1.fetchall()
    for row in result:
        log_id =row[0]
        log_password =row[1]

    for row1 in result1:
        pfrom = row1[0]
        pto = row1[1]
        date  = row1[2]
        tclass  = row1[3]
        quota  = row1[4]
        train  = row1[5]
        p1name  = row1[6]
        p1age  = row1[7]
        p1gender  = row1[8]
        p2name  = row1[9]
        p2age  = row1[10]
        p2gender  = row1[11]
        p3name  = row1[12]
        p3age  = row1[13]
        p3gender  = row1[14]
        p4name  = row1[15]
        p4age  = row1[16]
        p4gender  = row1[17]
        mobile  = row1[18]
        form_name1 = row1[19]
        #print(form_name1,log_id,log_password,pfrom,pto,date,tclass,quota,train,p1name,p1age,p1gender,p2name,p2age,p2gender,p3name,p3age,p3gender,p4name,p4age,p4gender,mobile,address,pincode)
        p_res = p1name+' '+p2name+' '+p3name+' '+p4name
        res = len(p_res.split())
        p_count = str(res)

        #PATH = "chromedriver.exe"
        #driver = webdriver.Chrome(PATH)
        #user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"
        caps = DesiredCapabilities().CHROME
        caps['pageLoadStrategy']='eager'
        

        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"

        options = webdriver.ChromeOptions()
        options.headless = True
        options.add_argument(f'user-agent={user_agent}')
        options.add_argument("--window-size=1920,1080")
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--allow-running-insecure-content')
        options.add_argument("--disable-extensions")
        options.add_argument("--proxy-server='direct://'")
        options.add_argument("--proxy-bypass-list=*")
        options.add_argument("--start-maximized")
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')

        driver = webdriver.Chrome(options=options, desired_capabilities=caps)
        driver.maximize_window()
        driver.get("https://www.irctc.co.in/nget/train-search")

        wait = WebDriverWait(driver,30)
        wait.until(EC.presence_of_element_located((By.XPATH,'/html/body/app-root/app-home/div[1]/app-header/p-dialog[2]/div/div/div[2]/div/form/div[2]/button')))
        driver.find_element_by_xpath("/html/body/app-root/app-home/div[1]/app-header/p-dialog[2]/div/div/div[2]/div/form/div[2]/button").click()
        #driver.find_element_by_xpath("/html/body/app-root/app-home/div[1]/app-header/div[1]/div[2]/a/i").click()
        driver.find_element_by_xpath("/html/body/app-root/app-home/div[1]/app-header/div[2]/div[2]/div[1]/a[1]").click()
        driver.find_element_by_xpath("/html/body/app-root/app-home/div[3]/app-login/p-dialog[1]/div/div/div[2]/div[2]/div/div[2]/div[2]/div[2]/form/div[1]/input").send_keys(log_id)
        sleep(0.5)
        driver.find_element_by_xpath('/html/body/app-root/app-home/div[3]/app-login/p-dialog[1]/div/div/div[2]/div[2]/div/div[2]/div[2]/div[2]/form/div[2]/input').send_keys(log_password)
        status.configure(text='Waiting for CAPTCHA')
        wait = WebDriverWait(driver,30)
        wait.until(EC.presence_of_element_located((By.XPATH,'/html/body/app-root/app-home/div[3]/app-login/p-dialog[1]/div/div/div[2]/div[2]/div/div[2]/div[2]/div[2]')))
        take_ss()
#takes captcha screenshoot
def take_ss():
        sleep(3)
        global peakstat
        tat_cap = driver.find_elements_by_xpath('//*[@id="login_header_disable"]/div/div/div[2]/div[2]/div/div[2]/div[2]/div[2]/form/div[3]/div/app-captcha/div/div/div/div/span[1]/img')
        peakstat =(len(tat_cap))

        if peakstat == 0:

            with open('captcha.png', 'wb') as file:
        #identify image to be captured
                    
                        l = driver.find_element_by_xpath('/html/body/app-root/app-home/div[3]/app-login/p-dialog[1]/div/div/div[2]/div[2]/div/div[2]/div[2]/div[2]')
        #write file
                        file.write(l.screenshot_as_png)
                        threading.Thread(target=ir_form).start()
        else:
            with open('captcha.png', 'wb') as file:
        #identify image to be captured
                    
                        l = driver.find_element_by_xpath('//*[@id="login_header_disable"]/div/div/div[2]/div[2]/div/div[2]/div[2]/div[2]/form/div[3]/div/app-captcha/div/div/div/div/span[1]/img')
        #write file
                        file.write(l.screenshot_as_png)
                        threading.Thread(target=ir_form).start()
#captcha entry box
def ir_form():
    global cap_ir
    global e
    if peakstat==0:

            im = Image.open('captcha.png')
            #left, upper, right, lowe
            cropped = im.crop((50,350,400,400))
            image = ImageTk.PhotoImage(cropped)
            imageLabel.configure(image = image)
            imageLabel.image = image
            t1 = threading.Thread(target=save).start
            log_btn.configure(text='SUBMIT',command=t1, width=6)
            status.configure(text='Please Enter Captcha')
            e = Entry(my_w,font=9)
            e.place(x=20, y=130)
    else:
            lab1.destroy()
            lab2.destroy()
            lbl1.destroy()
            om1.destroy()
            om11.destroy()
            om22.destroy()
            im = Image.open('captcha.png')
            #left, upper, right, lowe
            resize = im.resize((220,60), Image.ANTIALIAS)
            image = ImageTk.PhotoImage(resize)
            imageLabel.configure(image = image)
            imageLabel.image = image
            log_btn.configure(text='SUBMIT',command=threading.Thread(target=save).start, width=6)
            status.configure(text='Please Enter Captcha')
            e = Entry(my_w,font=9)
            e.place(x=20, y=130)
#logs in IRCTC
def save():
        textCap = e.get()
        global actions
        #check for time
        now = datetime.datetime.now().time()
        s_time = datetime.time(9,40)
        e_time = datetime.time(10,20)
        ss_time = datetime.time(10,40)
        se_time = datetime.time(11,20)

        if now >= s_time and now<=e_time:
            
            driver.find_element_by_xpath('//*[@id="captcha"]').send_keys(textCap)
        else:
                if now >=ss_time and now<=se_time:
                    driver.find_element_by_xpath('//*[@id="captcha"]').send_keys(textCap)
                else:
                    #driver.find_element_by_xpath('//*[@id="captcha"]').send_keys(textCap)
                    driver.find_element_by_xpath('/html/body/app-root/app-home/div[3]/app-login/p-dialog[1]/div/div/div[2]/div[2]/div/div[2]/div[2]/div[2]/form/div[3]/div/app-nlp-captcha/div/div[2]/div/div[3]/div[1]/input').send_keys(textCap)
        #login click
        
        driver.find_element_by_xpath('/html/body/app-root/app-home/div[3]/app-login/p-dialog[1]/div/div/div[2]/div[2]/div/div[2]/div[2]/div[2]/form/span/button').click()
        log_sucess()
#enter journey details
def log_sucess():   
        e.place_forget()
        imageLabel.place_forget()
        #search page
        wait = WebDriverWait(driver,30)
        wait.until(EC.presence_of_element_located((By.XPATH,'/html/body/app-root/app-home/div[3]/div/app-main-page/div/div/div[1]/div[2]/div[1]/app-jp-input/div/form/div[2]/div[1]/div[1]/p-autocomplete/span/input')))
        status.configure(text='Success...')
        status.place(x=5, y=10)
        status.configure(text='Entering Journey Details')
        driver.find_element(by=By.XPATH, value='//*[@id="origin"]/span/input').send_keys(pfrom)
        sleep(0.1)
        wait = WebDriverWait(driver,30)
        wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="p-highlighted-option"]'))).click()
    
        driver.find_element(by=By.XPATH, value='//*[@id="destination"]/span/input').send_keys(pto)
        sleep(0.1)
        wait = WebDriverWait(driver,30)
        wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="p-highlighted-option"]'))).click()
    
        driver.find_element(by=By.XPATH, value='//*[@id="journeyQuota"]/div/div[3]').click()
        if quota == "GENERAL":
            driver.find_element(By.XPATH,'//*[@id="journeyQuota"]/div/div[4]/div/ul/p-dropdownitem[1]').click()
        if quota == "TATKAL":
            driver.find_element(By.XPATH,'//*[@id="journeyQuota"]/div/div[4]/div/ul/p-dropdownitem[5]').click()
        if quota =="PREMIUM TATKAL":
            driver.find_element(By.XPATH,'//*[@id="journeyQuota"]/div/div[4]/div/ul/p-dropdownitem[6]').click()

        date_ui = driver.find_element(By.XPATH,'//*[@id="jDate"]/span/input')
        date_ui.send_keys(date)
        date_ui.clear()
        date_ui.send_keys(date)
        date_ui.send_keys(Keys.ENTER)
        
        wait = WebDriverWait(driver,30)
        wait.until(EC.presence_of_element_located((By.XPATH,'/html/body/app-root/app-home/div[3]/div/app-train-list/div[4]/div/div[5]/div/div[1]/app-train-avl-enq/div[1]/div[5]/div/table/tr/td[2]/div/div[2]')))
        #train list page
        status.configure(text='Searching Train')
        train_name = driver.find_element_by_xpath('//*[@id="divMain"]/div/app-train-list/div[4]/div/div[5]/div[%s]/div[1]/app-train-avl-enq/div[1]/div[1]/div[1]/strong'%train).text
        Label(my_w, text=train_name,font = ('calibri', 10, 'bold'),bg='Yellow').place(x=5, y=60)
        
        if tclass == 'Second Sitting (2S)':
            wait = WebDriverWait(driver,90)
            wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="divMain"]/div/app-train-list/div[4]/div/div[5]/div[%s]/div[1]/app-train-avl-enq/div[1]/div[5]/div/table/tr/td[1]/div/div[2]'%train)))
            driver.find_element_by_xpath('//*[@id="divMain"]/div/app-train-list/div[4]/div/div[5]/div[%s]/div[1]/app-train-avl-enq/div[1]/div[5]/div/table/tr/td[1]/div/div[2]'%train).click()
            check()
        if tclass == 'Sleeper (SL)':
            wait = WebDriverWait(driver,90)
            wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="divMain"]/div/app-train-list/div[4]/div/div[5]/div[%s]/div[1]/app-train-avl-enq/div[1]/div[5]/div/table/tr/td[2]/div/div[2]'%train)))
            driver.find_element_by_xpath('//*[@id="divMain"]/div/app-train-list/div[4]/div/div[5]/div[%s]/div[1]/app-train-avl-enq/div[1]/div[5]/div/table/tr/td[2]/div/div[2]'%train).click()
            check()
        if tclass == 'AC 3 Tier (3A)':
            wait = WebDriverWait(driver,90)
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="divMain"]/div/app-train-list/div[4]/div/div[5]/div[%s]/div[1]/app-train-avl-enq/div[1]/div[5]/div/table/tr/td[3]/div/div[2]'%train))).click()
            check()
        if tclass == 'AC 2 Tier (2A)':
            wait = WebDriverWait(driver,90)
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="divMain"]/div/app-train-list/div[4]/div/div[5]/div[%s]/div[1]/app-train-avl-enq/div[1]/div[5]/div/table/tr/td[4]/div/div[2]'%train))).click()
            check()
#check for availablity
def check():
        global book_btn
        status.configure(text='Checking...')
        wait = WebDriverWait(driver,90)
        wait.until(EC.presence_of_element_located((By.XPATH,'/html/body/app-root/app-home/div[3]/div/app-train-list/div[4]/div/div[5]/div/div[1]/app-train-avl-enq/div[1]/div[7]/div[1]/div[3]/table/tr/td[2]/div/div[2]/strong')))
        avl_seats = driver.find_element_by_xpath('/html/body/app-root/app-home/div[3]/div/app-train-list/div[4]/div/div[5]/div/div[1]/app-train-avl-enq/div[1]/div[7]/div[1]/div[3]/table/tr/td[2]/div/div[2]/strong').text
        Label(my_w, text=tclass,font = ('calibri', 10, 'bold'),bg='Yellow').place(x=135, y=60)
        Label(my_w, text=avl_seats,font = ('calibri', 10, 'bold'),bg='Yellow').place(x=5, y=90)
        driver.find_element_by_xpath('/html/body/app-root/app-home/div[3]/div/app-train-list/div[4]/div/div[5]/div/div[1]/app-train-avl-enq/div[1]/div[7]/div[1]/div[3]/table/tr/td[2]/div/div[2]').click()
    
        countele = driver.find_elements_by_xpath('//*[@id="divMain"]/div/app-train-list/div[4]/div/div[5]/div/div[1]/app-train-avl-enq/div[2]/div/span/span[1]/*[@class="btnDefault train_Search ng-star-inserted"]')
        bstatus = (len(countele))
        if bstatus ==0:
            click_available()
            if tclass == 'Sleeper (SL)':
                    status.configure(text='Availablity at 10:59:45')
                    schedule.every().day.at("10:59:45").do(shedule_book)
                    while True:
                        schedule.run_pending()
                        sleep(1)
            #if tclass == 'AC 3 Tier (3A)'or'AC 2 Tier (2A)':
            else:
                status.configure(text='Availablity at 9:59:55')
                schedule.every().day.at("09:59:55").do(shedule_book)
                while True:
                    schedule.run_pending()
                    sleep(1)
        else:
            status.configure(text='BOOK NOW Available')
            book_btn = Button(my_w, text='BOOK NOW',width=12,font = ('calibri', 12, 'bold'), command=threading.Thread(target=press_book).start(), fg='White', bg='orange')
            book_btn.place(x=135, y=90)
            click_available()
#refresh 
def check_avaiable():
    
        if tclass == 'Second Sitting (2S)':
            wait = WebDriverWait(driver,90)
            wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="divMain"]/div/app-train-list/div[4]/div/div[5]/div[%s]/div[1]/app-train-avl-enq/div[1]/div[7]/div[1]/p-tabmenu/div/ul/li[1]'%train)))
            driver.find_element_by_xpath('//*[@id="divMain"]/div/app-train-list/div[4]/div/div[5]/div[%s]/div[1]/app-train-avl-enq/div[1]/div[7]/div[1]/p-tabmenu/div/ul/li[1]'%train).click()
        
        if tclass == 'Sleeper (SL)':
            wait = WebDriverWait(driver,90)
            wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="divMain"]/div/app-train-list/div[4]/div/div[5]/div[%s]/div[1]/app-train-avl-enq/div[1]/div[7]/div[1]/p-tabmenu/div/ul/li[2]'%train)))
            driver.find_element_by_xpath('//*[@id="divMain"]/div/app-train-list/div[4]/div/div[5]/div[%s]/div[1]/app-train-avl-enq/div[1]/div[7]/div[1]/p-tabmenu/div/ul/li[2]'%train).click()
        if tclass == 'AC 3 Tier (3A)':
            wait = WebDriverWait(driver,90)
            wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="divMain"]/div/app-train-list/div[4]/div/div[5]/div[%s]/div[1]/app-train-avl-enq/div[1]/div[7]/div[1]/p-tabmenu/div/ul/li[3]'%train)))
            driver.find_element_by_xpath('//*[@id="divMain"]/div/app-train-list/div[4]/div/div[5]/div[%s]/div[1]/app-train-avl-enq/div[1]/div[7]/div[1]/p-tabmenu/div/ul/li[3]'%train).click()
        if tclass == 'AC 2 Tier (2A)':
            wait = WebDriverWait(driver,90)
            wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="divMain"]/div/app-train-list/div[4]/div/div[5]/div[%s]/div[1]/app-train-avl-enq/div[1]/div[7]/div[1]/p-tabmenu/div/ul/li[4]'%train)))
            driver.find_element_by_xpath('//*[@id="divMain"]/div/app-train-list/div[4]/div/div[5]/div[%s]/div[1]/app-train-avl-enq/div[1]/div[7]/div[1]/p-tabmenu/div/ul/li[4]'%train).click()

        wait = WebDriverWait(driver,90)
        wait.until(EC.invisibility_of_element((By.XPATH,'/html/body/app-root/app-home/div[1]/app-header/div[4]/div[2]')))
        driver.find_element_by_xpath('/html/body/app-root/app-home/div[3]/div/app-train-list/div[4]/div/div[5]/div/div[1]/app-train-avl-enq/div[1]/div[7]/div[1]/div[3]/table/tr/td[2]/div/div[2]').click()
        status.configure(text='Refreshed')
        check()
#schedule for book now button
def shedule_book():
            auto_check_avaiable()
#refresh automatically
def auto_check_avaiable():
        status.configure(text='Auto Booking Activated')
        
        status.configure(text='Auto Booking Activated - Checking...')
        if tclass == 'Second Sitting (2S)':
            wait = WebDriverWait(driver,900)
            wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="divMain"]/div/app-train-list/div[4]/div/div[5]/div[%s]/div[1]/app-train-avl-enq/div[1]/div[7]/div[1]/p-tabmenu/div/ul/li[1]'%train)))
            driver.find_element_by_xpath('//*[@id="divMain"]/div/app-train-list/div[4]/div/div[5]/div[%s]/div[1]/app-train-avl-enq/div[1]/div[7]/div[1]/p-tabmenu/div/ul/li[1]'%train).click()
        
        if tclass == 'Sleeper (SL)':
            wait = WebDriverWait(driver,900)
            wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="divMain"]/div/app-train-list/div[4]/div/div[5]/div[%s]/div[1]/app-train-avl-enq/div[1]/div[7]/div[1]/p-tabmenu/div/ul/li[2]'%train)))
            driver.find_element_by_xpath('//*[@id="divMain"]/div/app-train-list/div[4]/div/div[5]/div[%s]/div[1]/app-train-avl-enq/div[1]/div[7]/div[1]/p-tabmenu/div/ul/li[2]'%train).click()
        if tclass == 'AC 3 Tier (3A)':
            wait = WebDriverWait(driver,900)
            wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="divMain"]/div/app-train-list/div[4]/div/div[5]/div[%s]/div[1]/app-train-avl-enq/div[1]/div[7]/div[1]/p-tabmenu/div/ul/li[3]'%train)))
            driver.find_element_by_xpath('//*[@id="divMain"]/div/app-train-list/div[4]/div/div[5]/div[%s]/div[1]/app-train-avl-enq/div[1]/div[7]/div[1]/p-tabmenu/div/ul/li[3]'%train).click()
        if tclass == 'AC 2 Tier (2A)':
            wait = WebDriverWait(driver,900)
            wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="divMain"]/div/app-train-list/div[4]/div/div[5]/div[%s]/div[1]/app-train-avl-enq/div[1]/div[7]/div[1]/p-tabmenu/div/ul/li[4]'%train)))
            driver.find_element_by_xpath('//*[@id="divMain"]/div/app-train-list/div[4]/div/div[5]/div[%s]/div[1]/app-train-avl-enq/div[1]/div[7]/div[1]/p-tabmenu/div/ul/li[4]'%train).click()

        wait = WebDriverWait(driver,900)
        wait.until(EC.invisibility_of_element((By.XPATH,'/html/body/app-root/app-home/div[1]/app-header/div[4]/div[2]')))
        driver.find_element_by_xpath('/html/body/app-root/app-home/div[3]/div/app-train-list/div[4]/div/div[5]/div/div[1]/app-train-avl-enq/div[1]/div[7]/div[1]/div[3]/table/tr/td[2]/div/div[2]').click()

        auto_check()
#check for availablity automatically
def auto_check():
        global book_btn
        
        status.configure(text='Checking...')
        wait = WebDriverWait(driver,900)
        wait.until(EC.presence_of_element_located((By.XPATH,'/html/body/app-root/app-home/div[3]/div/app-train-list/div[4]/div/div[5]/div/div[1]/app-train-avl-enq/div[1]/div[7]/div[1]/div[3]/table/tr/td[2]/div/div[2]/strong')))
        avl_seats = driver.find_element_by_xpath('/html/body/app-root/app-home/div[3]/div/app-train-list/div[4]/div/div[5]/div/div[1]/app-train-avl-enq/div[1]/div[7]/div[1]/div[3]/table/tr/td[2]/div/div[2]/strong').text
        Label(my_w, text=avl_seats,font = ('calibri', 10, 'bold'),bg='Yellow').place(x=5, y=90)
        driver.find_element_by_xpath('/html/body/app-root/app-home/div[3]/div/app-train-list/div[4]/div/div[5]/div/div[1]/app-train-avl-enq/div[1]/div[7]/div[1]/div[3]/table/tr/td[2]/div/div[2]').click()
    
        countele = driver.find_elements_by_xpath('//*[@id="divMain"]/div/app-train-list/div[4]/div/div[5]/div/div[1]/app-train-avl-enq/div[2]/div/span/span[1]/*[@class="btnDefault train_Search ng-star-inserted"]')
        bstatus = (len(countele))
        if bstatus ==0:
            status.configure(text='Sleep...')
            sleep(10)
            auto_check_avaiable()
            
        else:
            book_btn = Button(my_w, text='BOOK NOW',width=12,font = ('calibri', 12, 'bold'), command=threading.Thread(target=press_book).start(), fg='White', bg='orange')
            book_btn.place(x=135, y=90)     
#manually buttons
def click_available():
        log_btn.destroy() 
        global auto_avl_btn
        global avl_btn
        avl_btn = Button(my_w, text='Check Available',width=12,font = ('calibri', 10, 'bold'), command=threading.Thread(target=check_avaiable).start, bg='blue', fg='white')
        avl_btn.place(x=145, y=130)
        auto_avl_btn = Button(my_w, text='Auto Book',width=8,font = ('calibri', 10, 'bold'), command=threading.Thread(target=auto_check_avaiable).start, bg='purple', fg='white')
        auto_avl_btn.place(x=175, y=165)
#click book and enters passanger details
def press_book():
        
        status.configure(text='Entering Passanger')
        driver.find_element_by_xpath('//*[@id="divMain"]/div/app-train-list/div[4]/div/div[5]/div[%s]/div[1]/app-train-avl-enq/div[2]/div/span/span/button[1]'%train).click()
        avl_btn.destroy()
        auto_avl_btn.place_forget()
        book_btn.place_forget()
        wait = WebDriverWait(driver,30)
        wait.until(EC.presence_of_element_located((By.XPATH,'/html/body/app-root/app-home/div[3]/div/app-train-list/div[4]/div/div[5]/div/div[1]/app-train-avl-enq/div[1]/div[7]/div[1]/div[3]/table/tr/td[2]/div/div[2]/strong')))
        actions = ActionChains(driver)
        actions.send_keys(Keys.ENTER)
        actions.perform()
        wait = WebDriverWait(driver,90)
        wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="psgn-form"]/form/div/div[1]/div[16]/div/button[2]')))
        sleep(0.5)

        if p_count =='1':

            driver.find_element_by_xpath('//*[@id="ui-panel-12-content"]/div/div[1]/div[2]/div/app-passenger/div/div[1]/span/div[1]/p-autocomplete/span/input').click()
            actions.send_keys(p1name)
            actions.perform()
            driver.find_element_by_xpath('//*[@id="ui-panel-12-content"]/div/div[1]/div[2]/div/app-passenger/div/div[1]/span/div[2]/input').click()
            actions.send_keys(p1age)
            actions.perform()
            driver.find_element_by_xpath('//*[@id="ui-panel-12-content"]/div/div[1]/div[2]/div/app-passenger/div/div[1]/span/div[3]/select').click()
            if p1gender == 'MALE':
                driver.find_element_by_xpath('//*[@id="ui-panel-12-content"]/div/div[1]/div[2]/div/app-passenger/div/div[1]/span/div[3]/select/option[2]').click()

            if p1gender == 'FEMALE':
                driver.find_element_by_xpath('//*[@id="ui-panel-12-content"]/div/div[1]/div[2]/div/app-passenger/div/div[1]/span/div[3]/select/option[3]').click()
            
        if p_count =='2':
            
            driver.find_element_by_xpath('/html/body/app-root/app-home/div[3]/div/app-passenger-input/div[5]/form/div/div[1]/div[4]/p-panel/div/div[2]/div/div[2]/div[1]/a/span').click()
            driver.find_element_by_xpath('//*[@id="ui-panel-12-content"]/div/div[1]/div[2]/div/app-passenger/div/div[1]/span/div[1]/p-autocomplete/span/input').click()
            actions.send_keys(p1name)
            actions.perform()
            driver.find_element_by_xpath('//*[@id="ui-panel-12-content"]/div/div[1]/div[2]/div/app-passenger/div/div[1]/span/div[2]/input').click()
            actions.send_keys(p1age)
            actions.perform()
            driver.find_element_by_xpath('//*[@id="ui-panel-12-content"]/div/div[1]/div[2]/div/app-passenger/div/div[1]/span/div[3]/select').click()
            if p1gender == 'MALE':
                driver.find_element_by_xpath('//*[@id="ui-panel-12-content"]/div/div[1]/div[2]/div/app-passenger/div/div[1]/span/div[3]/select/option[2]').click()

            if p1gender == 'FEMALE':
                driver.find_element_by_xpath('//*[@id="ui-panel-12-content"]/div/div[1]/div[2]/div/app-passenger/div/div[1]/span/div[3]/select/option[3]').click()

            driver.find_element_by_xpath('//*[@id="ui-panel-12-content"]/div/div[2]/div[2]/div/app-passenger/div/div[1]/span/div[1]/p-autocomplete/span/input').click()
            actions.send_keys(p2name)
            actions.perform()
            driver.find_element_by_xpath('//*[@id="ui-panel-12-content"]/div/div[2]/div[2]/div/app-passenger/div/div[1]/span/div[2]/input').click()
            actions.send_keys(p2age)
            actions.perform()
            driver.find_element_by_xpath('//*[@id="ui-panel-12-content"]/div/div[2]/div[2]/div/app-passenger/div/div[1]/span/div[3]/select').click()
            if p2gender == 'MALE':
                driver.find_element_by_xpath('//*[@id="ui-panel-12-content"]/div/div[2]/div[2]/div/app-passenger/div/div[1]/span/div[3]/select/option[2]').click()

            if p2gender == 'FEMALE':
                driver.find_element_by_xpath('//*[@id="ui-panel-12-content"]/div/div[2]/div[2]/div/app-passenger/div/div[1]/span/div[3]/select/option[3]').click()

        if p_count =='3':

            driver.find_element_by_xpath('/html/body/app-root/app-home/div[3]/div/app-passenger-input/div[5]/form/div/div[1]/div[4]/p-panel/div/div[2]/div/div[2]/div[1]/a/span').click()
            sleep(0.2)
            actions.send_keys(Keys.ENTER)
            actions.perform()
            driver.find_element_by_xpath('//*[@id="ui-panel-12-content"]/div/div[1]/div[2]/div/app-passenger/div/div[1]/span/div[1]/p-autocomplete/span/input').click()
            actions.send_keys(p1name)
            actions.perform()
            driver.find_element_by_xpath('//*[@id="ui-panel-12-content"]/div/div[1]/div[2]/div/app-passenger/div/div[1]/span/div[2]/input').click()
            actions.send_keys(p1age)
            actions.perform()
            driver.find_element_by_xpath('//*[@id="ui-panel-12-content"]/div/div[1]/div[2]/div/app-passenger/div/div[1]/span/div[3]/select').click()
            if p1gender == 'MALE':
                driver.find_element_by_xpath('//*[@id="ui-panel-12-content"]/div/div[1]/div[2]/div/app-passenger/div/div[1]/span/div[3]/select/option[2]').click()

            if p1gender == 'FEMALE':
                driver.find_element_by_xpath('//*[@id="ui-panel-12-content"]/div/div[1]/div[2]/div/app-passenger/div/div[1]/span/div[3]/select/option[3]').click()

            driver.find_element_by_xpath('//*[@id="ui-panel-12-content"]/div/div[2]/div[2]/div/app-passenger/div/div[1]/span/div[1]/p-autocomplete/span/input').click()
            actions.send_keys(p2name)
            actions.perform()
            driver.find_element_by_xpath('//*[@id="ui-panel-12-content"]/div/div[2]/div[2]/div/app-passenger/div/div[1]/span/div[2]/input').click()
            actions.send_keys(p2age)
            actions.perform()
            driver.find_element_by_xpath('//*[@id="ui-panel-12-content"]/div/div[2]/div[2]/div/app-passenger/div/div[1]/span/div[3]/select').click()
            if p2gender == 'MALE':
                driver.find_element_by_xpath('//*[@id="ui-panel-12-content"]/div/div[2]/div[2]/div/app-passenger/div/div[1]/span/div[3]/select/option[2]').click()

            if p2gender == 'FEMALE':
                driver.find_element_by_xpath('//*[@id="ui-panel-12-content"]/div/div[2]/div[2]/div/app-passenger/div/div[1]/span/div[3]/select/option[3]').click()
            
            driver.find_element_by_xpath('//*[@id="ui-panel-12-content"]/div/div[3]/div[2]/div/app-passenger/div/div[1]/span/div[1]/p-autocomplete/span/input').click()
            actions.send_keys(p3name)
            actions.perform()
            driver.find_element_by_xpath('//*[@id="ui-panel-12-content"]/div/div[3]/div[2]/div/app-passenger/div/div[1]/span/div[2]/input').click()
            actions.send_keys(p3age)
            actions.perform()
            driver.find_element_by_xpath('//*[@id="ui-panel-12-content"]/div/div[3]/div[2]/div/app-passenger/div/div[1]/span/div[3]/select').click()
            if p2gender == 'MALE':
                driver.find_element_by_xpath('//*[@id="ui-panel-12-content"]/div/div[3]/div[2]/div/app-passenger/div/div[1]/span/div[3]/select/option[2]').click()

            if p2gender == 'FEMALE':
                driver.find_element_by_xpath('//*[@id="ui-panel-12-content"]/div/div[3]/div[2]/div/app-passenger/div/div[1]/span/div[3]/select/option[3]').click()

        if p_count =='4':

            driver.find_element_by_xpath('/html/body/app-root/app-home/div[3]/div/app-passenger-input/div[5]/form/div/div[1]/div[4]/p-panel/div/div[2]/div/div[2]/div[1]/a/span').click()
            sleep(0.2)
            actions.send_keys(Keys.ENTER)
            actions.perform()
            sleep(0.2)
            actions.send_keys(Keys.ENTER)
            actions.perform()
            driver.find_element_by_xpath('//*[@id="ui-panel-12-content"]/div/div[1]/div[2]/div/app-passenger/div/div[1]/span/div[1]/p-autocomplete/span/input').click()
            actions.send_keys(p1name)
            actions.perform()
            driver.find_element_by_xpath('//*[@id="ui-panel-12-content"]/div/div[1]/div[2]/div/app-passenger/div/div[1]/span/div[2]/input').click()
            actions.send_keys(p1age)
            actions.perform()
            driver.find_element_by_xpath('//*[@id="ui-panel-12-content"]/div/div[1]/div[2]/div/app-passenger/div/div[1]/span/div[3]/select').click()
            if p1gender == 'MALE':
                driver.find_element_by_xpath('//*[@id="ui-panel-12-content"]/div/div[1]/div[2]/div/app-passenger/div/div[1]/span/div[3]/select/option[2]').click()

            if p1gender == 'FEMALE':
                driver.find_element_by_xpath('//*[@id="ui-panel-12-content"]/div/div[1]/div[2]/div/app-passenger/div/div[1]/span/div[3]/select/option[3]').click()

            driver.find_element_by_xpath('//*[@id="ui-panel-12-content"]/div/div[2]/div[2]/div/app-passenger/div/div[1]/span/div[1]/p-autocomplete/span/input').click()
            actions.send_keys(p2name)
            actions.perform()
            driver.find_element_by_xpath('//*[@id="ui-panel-12-content"]/div/div[2]/div[2]/div/app-passenger/div/div[1]/span/div[2]/input').click()
            actions.send_keys(p2age)
            actions.perform()
            driver.find_element_by_xpath('//*[@id="ui-panel-12-content"]/div/div[2]/div[2]/div/app-passenger/div/div[1]/span/div[3]/select').click()
            if p2gender == 'MALE':
                driver.find_element_by_xpath('//*[@id="ui-panel-12-content"]/div/div[2]/div[2]/div/app-passenger/div/div[1]/span/div[3]/select/option[2]').click()

            if p2gender == 'FEMALE':
                driver.find_element_by_xpath('//*[@id="ui-panel-12-content"]/div/div[2]/div[2]/div/app-passenger/div/div[1]/span/div[3]/select/option[3]').click()
            
            driver.find_element_by_xpath('//*[@id="ui-panel-12-content"]/div/div[3]/div[2]/div/app-passenger/div/div[1]/span/div[1]/p-autocomplete/span/input').click()
            actions.send_keys(p3name)
            actions.perform()
            driver.find_element_by_xpath('//*[@id="ui-panel-12-content"]/div/div[3]/div[2]/div/app-passenger/div/div[1]/span/div[2]/input').click()
            actions.send_keys(p3age)
            actions.perform()
            driver.find_element_by_xpath('//*[@id="ui-panel-12-content"]/div/div[3]/div[2]/div/app-passenger/div/div[1]/span/div[3]/select').click()
            if p3gender == 'MALE':
                driver.find_element_by_xpath('//*[@id="ui-panel-12-content"]/div/div[3]/div[2]/div/app-passenger/div/div[1]/span/div[3]/select/option[2]').click()

            if p3gender == 'FEMALE':
                driver.find_element_by_xpath('//*[@id="ui-panel-12-content"]/div/div[3]/div[2]/div/app-passenger/div/div[1]/span/div[3]/select/option[3]').click()

            driver.find_element_by_xpath('//*[@id="ui-panel-12-content"]/div/div[4]/div[2]/div/app-passenger/div/div[1]/span/div[1]/p-autocomplete/span/input').click()
            actions.send_keys(p4name)
            actions.perform()
            driver.find_element_by_xpath('//*[@id="ui-panel-12-content"]/div/div[4]/div[2]/div/app-passenger/div/div[1]/span/div[2]/input').click()
            actions.send_keys(p4age)
            actions.perform()
            driver.find_element_by_xpath('//*[@id="ui-panel-12-content"]/div/div[4]/div[2]/div/app-passenger/div/div[1]/span/div[3]/select').click()
            if p4gender == 'MALE':
                driver.find_element_by_xpath('//*[@id="ui-panel-12-content"]/div/div[4]/div[2]/div/app-passenger/div/div[1]/span/div[3]/select/option[2]').click()

            if p4gender == 'FEMALE':
                driver.find_element_by_xpath('//*[@id="ui-panel-12-content"]/div/div[4]/div[2]/div/app-passenger/div/div[1]/span/div[3]/select/option[3]').click()
        
        driver.find_element_by_xpath('//*[@id="mobileNumber"]').send_keys(mobile)
        driver.find_element_by_xpath('//*[@id="aaa1"]').send_keys('Pune')
        driver.find_element_by_xpath('//*[@id="aaa4"]').send_keys('411016')
        driver.find_element_by_xpath('//*[@id="address-postOffice"]').click()
        wait = WebDriverWait(driver,500)
        wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="address-postOffice"]/option[4]'))).click()
        driver.find_element_by_xpath('//*[@id="2"]').click()
        driver.find_element_by_xpath('//*[@id="psgn-form"]/form/div/div[1]/div[16]/div/button[2]').click()
        status.configure(text='Waiting for Booking Captcha')
        wait = WebDriverWait(driver,500)
        wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="review"]/div[1]/form/div[3]/div/button[2]')))
        fin_stat = driver.find_element_by_xpath('/html/body/app-root/app-home/div[3]/div/app-review-booking/div[4]/div/div[1]/div[1]/app-train-header/div[1]/div[3]/div[2]/span[1]').text
        Label(my_w, text=fin_stat,font = ('calibri', 12, 'bold'),bg='Yellow').place(x=5, y=100)
        actions.send_keys(Keys.PAGE_DOWN)
        actions.perform()
        sleep(0.5)
        b_tat_cap = driver.find_elements_by_xpath('//*[@id="nlpImgContainer"]')
        global b_peakstat
        b_peakstat =(len(b_tat_cap))
        print(b_peakstat)
        if b_peakstat==1:
            wait = WebDriverWait(driver,30)
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="nlpImgContainer"]')))
        else:
            wait = WebDriverWait(driver,30)
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="review"]/div[1]/div[1]/app-train-header/div[1]')))
        b_take_ss()
#take booking captcha screenshoot
def b_take_ss():
        with open('b_captcha.png', 'wb') as file:
        #identify image to be captured


                if b_peakstat==1:
                    l = driver.find_element_by_xpath('//*[@id="nlpImgContainer"]')
                    file.write(l.screenshot_as_png)
                else:
                    l = driver.find_element_by_xpath('//*[@id="review"]/div[1]/form/div[1]/div/div/app-captcha/div/div/div/div/span[1]/img')
                    file.write(l.screenshot_as_png)
        #write file
        ir_form_book()
#booking captcha entry
def ir_form_book():
    global b_cap_entry
    global b_imageLabel


    if b_peakstat==1:
            b_imageLabel = Label(my_w)
            b_imageLabel.place(x=1, y=10)
            im = Image.open('b_captcha.png')
            #left, upper, right, lowe
            cropped = im.crop((0,250,250,280))
            image = ImageTk.PhotoImage(cropped)
            b_imageLabel.configure(image = image)
            b_imageLabel.image = image
            auto_avl_btn.configure(text='SUBMIT',command=threading.Thread(target=payment_call).start, width=6)
            auto_avl_btn.place(x=175, y=165)
            status.configure(text='Enter Booking Captcha')
            b_cap_entry = Entry(my_w,font=9)
            b_cap_entry.place(x=20, y=130)
    else:
            b_imageLabel = Label(my_w)
            b_imageLabel.place(x=1, y=10)
            im = Image.open('b_captcha.png')
            #left, upper, right, lowe
            resize = im.resize((220,60), Image.ANTIALIAS)
            image = ImageTk.PhotoImage(resize)
            b_imageLabel.configure(image = image)
            b_imageLabel.image = image
            auto_avl_btn.configure(text='SUBMIT',command=threading.Thread(target=payment_call).start, width=6)
            auto_avl_btn.place(x=175, y=165)
            status.configure(text='Enter Booking Captcha')
            b_cap_entry = Entry(my_w,font=9)
            b_cap_entry.place(x=20, y=130)
#sends booking captcha and validate
def payment_call():
    b_cap = b_cap_entry.get()
    b_cap_entry.destroy()
    b_imageLabel.destroy()
    auto_avl_btn.place_forget()
    now = datetime.datetime.now().time()
    s_time = datetime.time(9,40)
    e_time = datetime.time(10,20)
    ss_time = datetime.time(10,40)
    se_time = datetime.time(11,20)

    if now >= s_time and now<=e_time:
            driver.find_element_by_xpath('//*[@id="captcha"]').send_keys(b_cap)
    else:
        if now >=ss_time and now<=se_time:
             driver.find_element_by_xpath('//*[@id="captcha"]').send_keys(b_cap)
        else:
            driver.find_element_by_xpath('/html/body/app-root/app-home/div[3]/div/app-review-booking/div[4]/div/div[1]/form/div[1]/div/div/app-nlp-captcha/div/div[2]/div/div[3]/div[1]/input').send_keys(b_cap)

    wait = WebDriverWait(driver,30)
    wait.until(EC.presence_of_element_located((By.XPATH,'/html/body/app-root/app-home/div[3]/div/app-review-booking/div[4]/div/div[1]/form/div[3]/div/button[2]')))
    driver.find_element_by_xpath('/html/body/app-root/app-home/div[3]/div/app-review-booking/div[4]/div/div[1]/form/div[3]/div/button[2]').click()
    wait = WebDriverWait(driver,90)
    wait.until(EC.invisibility_of_element((By.XPATH,'/html/body/app-root/app-home/div[1]/app-header/div[4]/div[2]')))
    sleep(1)
    log_stat =driver.find_elements_by_xpath('//*[@id="divMain"]/div/app-review-booking/p-toast/div/p-toastitem/div/div/div/div[2]')
    if (len(log_stat))==1:
            
            text_log = driver.find_element_by_xpath('//*[@id="divMain"]/div/app-review-booking/p-toast/div/p-toastitem/div/div/div/div[2]').text
            status.configure(text=text_log)
            if text_log == 'Invalid Captcha':
                                        b_take_ss()
            if text_log=='Please Enter Valid Captcha':
                                        b_take_ss()
            else:
                status.configure(text=text_log)
    else:
            status.configure(text='Success...')
            b_log_sucess()
#fills bank details and confirm booking
def b_log_sucess():
    status.configure(text='Filling Bank Details')
    wait = WebDriverWait(driver,30)
    wait.until(EC.presence_of_element_located((By.XPATH,'/html/body/app-root/app-home/div[3]/div/app-payment-options/div[4]/div[2]/div[1]/div[1]/app-payment/div[1]/div/form/div[1]/span/div[1]')))
    sleep(0.2)
    driver.find_element_by_xpath('/html/body/app-root/app-home/div[3]/div/app-payment-options/div[4]/div[2]/div[1]/div[1]/app-payment/div[1]/div/form/div[1]/span/div[1]').click()
    sleep(0.2)
    driver.find_element_by_xpath('/html/body/app-root/app-home/div[3]/div/app-payment-options/div[4]/div[2]/div[1]/div[1]/app-payment/div[1]/div/form/div[2]/app-bank/div/div/table/tr/span/td/div/div').click()
    sleep(0.2)
    driver.find_element_by_xpath('/html/body/app-root/app-home/div[3]/div/app-payment-options/div[4]/div[2]/div[1]/div[1]/app-payment/div[2]/button[2]').click()
    wait = WebDriverWait(driver,600)
    wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="ptm-upi"]'))).click()
    sleep(0.2)
    driver.find_element_by_xpath('//*[@id="ptm-upi"]/div[2]/div/div/div/div[2]/section/div/div[2]/div[2]/div/div/div/input').send_keys(options3.get())
    driver.find_element_by_xpath('//*[@id="ptm-upi"]/div[2]/div/div/div/div[2]/section/div/div[4]/section/button').click()
    status.configure(text='Wating for Bank Confirmation')
    wait = WebDriverWait(driver,500)
    wait.until(EC.presence_of_element_located((By.XPATH,'/html/body/app-root/app-home/div[3]/div/app-payment-response/div[1]/div/div/app-booking-confirmation/div/div[2]/div[4]/div[1]/app-train-header/div/div[1]')))
    final_pnr = driver.find_element_by_xpath('/html/body/app-root/app-home/div[3]/div/app-payment-response/div[1]/div/div/app-booking-confirmation/div/div[2]/div[4]/div[1]/app-train-header/div/div[1]/div[2]/strong/span').text
    status.configure(text=final_pnr)
    Label(my_w, text=final_pnr,font = ('calibri', 10, 'bold'),bg='Yellow').place(x=9, y=140)
#bank details entry
def bank():
    r_tk = Tk()
    global ir_upi
    r_tk.maxsize(width=200 ,  height=100)
    r_tk.minsize(width=200 ,  height=100)
    r_tk.title("Bank")
    Label(r_tk, text='ENTER UPI ID').place(x=60, y=10)
    ir_upi= Entry(r_tk)
    ir_upi.place(x=40, y=40)
    Button(r_tk, text='SAVE', width=10, command=save_bank).place(x=60, y=70)
#irctc user id password window
def irctc_id():
    ir_tk = Tk()
    global ir_id
    global ir_pass
    global listBox
    ir_tk.maxsize(width=800 ,  height=350)
    ir_tk.minsize(width=800 ,  height=350)
    ir_tk.title("IRCTC ID PASSWORD")
    Label(ir_tk, text='IRCTC ID').place(x=500, y=50)
    ir_id = Entry(ir_tk)
    ir_id.place(x=600, y=50)
    Label(ir_tk, text='PASSWORD').place(x=500, y=100)
    ir_pass = Entry(ir_tk)
    ir_pass.place(x=600, y=100)
    Button(ir_tk, text='SAVE', width=15, command=save_idp).place(x=600, y=150)
    cols = ('User ID', 'Password')
    listBox = ttk.Treeview(ir_tk, columns=cols, show='headings')
    listBox.place(x=50, y=50)

    for col in cols:
        listBox.heading(col, text=col)
    show()
    ir_tk.mainloop()
#input form journey details 
def form():
    root = Tk()
    root.geometry('800x500')
    root.title("Ticket Details")
    global entry_1
    global entry_2
    global entry_3
    global entry_4
    global entry_5
    global entry_6
    global entry_7
    global entry_8
    global entry_9
    global entry_10
    global entry_11
    global entry_12
    global entry_13
    global entry_14
    global entry_15
    global entry_16
    global entry_17
    global entry_18
    global entry_19
    global entry_22

    label_journey = Label(root, text="Journey Details",width=20,font=("bold", 15))
    label_journey.place(x=0,y=1)

    label_1 = Label(root, text="From :",width=20,font=("bold", 10))
    label_1.place(x=0,y=50)

    entry_1 = Entry(root)
    entry_1.place(x=110,y=50)

    label_2 = Label(root, text="To :",width=20,font=("bold", 10))
    label_2.place(x=0,y=100)

    entry_2 = Entry(root)
    entry_2.place(x=110,y=100)

    label_3 = Label(root, text="Date :",width=20,font=("bold", 10))
    label_3.place(x=250,y=50)

    #entry_3 = Entry(root)
    entry_3 = DateEntry(root, date_pattern='dd/mm/yyyy')
    entry_3.place(x=360,y=50)

    label_4 = Label(root, text="Class :",width=20,font=("bold", 10))
    label_4.place(x=250,y=100)

    entry_4=StringVar(root)
    entry_4.set("Sleeper (SL)")
    menu=OptionMenu(root,entry_4, 'Anubhuti Class (EA)','AC First Class (1A)','Exec. Chair Car (EC)','AC 2 Tier (2A)','First Class (FC)','AC 3 Tier (3A)','AC 3 Economy (3E)','AC Chair car (CC)','Sleeper (SL)','Second Sitting (2S)')
    menu.place(x=360,y=95)

    label_5 = Label(root, text="Quota :",width=20,font=("bold", 10))
    label_5.place(x=500,y=50)

    entry_5=StringVar(root)
    entry_5.set("TATKAL")
    menu=OptionMenu(root,entry_5, 'GENERAL','LADIES','LOWER BERTH/SR.CITIZEN','DIVYAANG','TATKAL','PREMIUM TATKAL')
    menu.place(x=610,y=45)

    label_6 = Label(root, text="Train No :",width=20,font=("bold", 10))
    label_6.place(x=500,y=100)

    entry_6 = Entry(root)
    entry_6.place(x=615,y=100)

    label_passanger = Label(root, text="Passanger Details",width=20,font=("bold", 15))
    label_passanger.place(x=0,y=150)

    label_7 = Label(root, text="Name :",width=20,font=("bold", 10))
    label_7.place(x=0,y=200)

    entry_7 = Entry(root)
    entry_7.place(x=110,y=200)

    label_8 = Label(root, text="Age :",width=20,font=("bold", 10))
    label_8.place(x=220,y=200)

    entry_8 = Entry(root)
    entry_8.place(x=330,y=200)

    label_9 = Label(root, text="Gender :",width=20,font=("bold", 10))
    label_9.place(x=440,y=200)

    entry_9=StringVar(root)
    entry_9.set('MALE')
    menu=OptionMenu(root,entry_9, 'MALE','FEMALE','TRANSGENDER')
    menu.place(x=550,y=195)

    label_10 = Label(root, text="Name :",width=20,font=("bold", 10))
    label_10.place(x=0,y=250)

    entry_10 = Entry(root)
    entry_10.place(x=110,y=250)

    label_11 = Label(root, text="Age :",width=20,font=("bold", 10))
    label_11.place(x=220,y=250)

    entry_11 = Entry(root)
    entry_11.place(x=330,y=250)

    label_12 = Label(root, text="Gender :",width=20,font=("bold", 10))
    label_12.place(x=440,y=250)

    entry_12=StringVar(root)
    entry_12.set('MALE')
    menu=OptionMenu(root,entry_12, 'MALE','FEMALE','TRANSGENDER')
    menu.place(x=550,y=245)

    label_13 = Label(root, text="Name :",width=20,font=("bold", 10))
    label_13.place(x=0,y=300)

    entry_13 = Entry(root)
    entry_13.place(x=110,y=300)

    label_14 = Label(root, text="Age :",width=20,font=("bold", 10))
    label_14.place(x=220,y=300)

    entry_14 = Entry(root)
    entry_14.place(x=330,y=300)

    label_15 = Label(root, text="Gender :",width=20,font=("bold", 10))
    label_15.place(x=440,y=300)

    entry_15=StringVar(root)
    entry_15.set('MALE')
    menu=OptionMenu(root,entry_15, 'MALE','FEMALE','TRANSGENDER')
    menu.place(x=550,y=295)

    label_16 = Label(root, text="Name :",width=20,font=("bold", 10))
    label_16.place(x=0,y=350)

    entry_16 = Entry(root)
    entry_16.place(x=110,y=350)

    label_17 = Label(root, text="Age :",width=20,font=("bold", 10))
    label_17.place(x=220,y=350)

    entry_17 = Entry(root)
    entry_17.place(x=330,y=350)

    label_18 = Label(root, text="Gender :",width=20,font=("bold", 10))
    label_18.place(x=440,y=350)

    entry_18=StringVar(root)
    entry_18.set('MALE')
    menu=OptionMenu(root,entry_18, 'MALE','FEMALE','TRANSGENDER')
    menu.place(x=550,y=345)

    label_19 = Label(root, text="Mobile No :",width=20,font=("bold", 10))
    label_19.place(x=0,y=400)

    entry_19 = Entry(root)
    entry_19.place(x=120,y=400)

    label_22 = Label(root, text="Form Name :",width=20,font=("bold", 10))
    label_22.place(x=450,y=450)

    entry_22 = Entry(root)
    entry_22.place(x=600,y=450)

    saveB = Button(root, text="SAVE", width=20, font=("bold", 15), command=save_form)
    saveB.place(x=220,y=450)


    root.mainloop()
#insert journey details in db
def save_form():
    e_1=entry_1.get()


    e_2=entry_2.get()


    e_3=entry_3.get()


    e_4=entry_4.get()


    e_5=entry_5.get()


    e_6=entry_6.get()

    
    e_7=entry_7.get()


    e_8=entry_8.get()


    e_9=entry_9.get()


    e_10=entry_10.get()


    e_11=entry_11.get()


    e_12=entry_12.get()


    e_13=entry_13.get()


    e_14=entry_14.get()


    e_15=entry_15.get()
 
    
    e_16=entry_16.get()


    e_17=entry_17.get()
   

    e_18=entry_18.get()
 

    e_19=entry_19.get()



    e_22=entry_22.get()

    
    if e_1==''or e_2=='':
        messagebox.showerror("Empty Fields","Fill the empty field!!!")
    else:
        cur.execute("INSERT INTO Form VALUES (:tfrom ,:tto ,:date ,:class ,:quota ,:train ,:p1name , :p1age , :p1gender ,:p2name ,:p2age ,:p2gender ,:p3name ,:p3age ,:p3gender ,:p4name ,:p4age ,:p4gender ,:mobile ,:formname)", {
                                    'tfrom':e_1,
                                    'tto':e_2,
                                    'date':e_3,
                                    'class':e_4,
                                    'quota':e_5,
                                    'train':e_6,
                                    'p1name':e_7,
                                    'p1age':e_8,
                                    'p1gender':e_9,
                                    'p2name':e_10,
                                    'p2age':e_11,
                                    'p2gender':e_12,
                                    'p3name':e_13,
                                    'p3age':e_14,
                                    'p3gender':e_15,
                                    'p4name':e_16,
                                    'p4age':e_17,
                                    'p4gender':e_18,
                                    'mobile':e_19,
                                    'formname':e_22,
                })
    messagebox.showinfo('confirmation', 'Record Saved')
    con.commit()
#fetch id pass in irctc window
def show():
    mysqldb = sqlite3.connect('irctcid.db')
    mycursor = mysqldb.cursor()
    mycursor.execute("SELECT userid,password FROM irctcid")
    records = mycursor.fetchall()

    for i, (id,stname) in enumerate(records, start=1):
        listBox.insert("", "end", values=(id, stname))
        mysqldb.close()
#save user id pass in db
def save_idp():
    iruser=ir_id.get()
    irpass=ir_pass.get()
    if iruser==''or irpass=='':
        messagebox.showerror("Empty Fields","Fill the empty field!!!")
    else:
        cur.execute("INSERT INTO irctcid VALUES (:userid, :password)", {
                                    'userid': ir_id.get(),
                                    'password': ir_pass.get(),

                    })
    
        messagebox.showinfo('confirmation', 'Record Saved')
    con.commit()
#save bank details
def save_bank():
    irupi=ir_upi.get()

    if irupi=='':
        messagebox.showerror("Empty Fields","Fill the empty field!!!")
    else:
        cur.execute("INSERT INTO paytm_upi VALUES (:upiid)", {
                                    'upiid': ir_upi.get(),

                    })
    
        messagebox.showinfo('confirmation', 'Record Saved')
    con.commit()
#check for key
def key():
    value_key=user_key.get()
    if value_key=='':
        messagebox.showerror("Empty Fields","Fill the empty field!!!")
    else:
        cur.execute('SELECT * from key where key="%s"'%(value_key))
        if cur.fetchone():
            messagebox.showinfo('Sucess',"Login success")
            log_tk.destroy()
            home_page()
        else:
            messagebox.showerror('Error',"Wrong username or password!!!")
#login page
def login_form():
    global log_tk
    global user_key
    user_key = StringVar
    log_tk = Tk()
    log_tk.maxsize(width=200 ,  height=80)
    log_tk.minsize(width=200 ,  height=80)
    log_tk.title('Login')
    note = Label(text='Key')
    note.pack()
    user_key = Entry(log_tk)
    user_key.pack()
    submit = Button(log_tk, text='Login', command=key)
    submit.pack()
    log_tk.mainloop()
home_page()




















