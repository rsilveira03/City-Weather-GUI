import tkinter, requests, json, mplcursors, mysql.connector as sc
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

#SQL Connection
con = sc.connect(host="localhost",user="root",password="password",database="cs") 
mc = con.cursor()

def clearlistbox(name): #To clear any listbox
    name.delete(0,"end")

def updatelb(lb,lst): #update listbox
    clearlistbox(lb) #clears listbox
    for i in lst: 
        lb.insert("end",i)

def maxcityname():  #To find city with longest name 
    mc.execute("Select distinct city from weather;")
    x = mc.fetchall()
    lst = []
    for i in x:
        lst.append(len(i[0]))
    return (max(lst)+4)




#FUCTIONS FOR GRAPHING
def creategraph():  #To to create the graph after selecting the cities
    fig = plt.figure() #creates the graph win
    ax = fig.add_subplot(111) #creates axes
    cv = lb_graph.curselection() #tuple - indices of selected names
    for i in cv:
        dates = []
        levels = []
        desc = []
        item = lb_graph.get(i) #gets name with index i from lb
        mc.execute("select date_time,temperature,description from weather where city = %s order by date_time;",(item[0],))
        x = mc.fetchall()
        for i in x:
            dates.append(i[0])
            levels.append(float(i[1]))
            desc.append(i[2])          
        ax.plot_date(dates, levels, marker='o',label = item[0],linestyle = "-")
        p = len(dates)
        for i in range (p): #To show description 
            ax.annotate(desc[i],(dates[i],levels[i]))

    # Configure x-ticks
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y %H:%M'))
    ax.set_title('Temperature Graph')
    ax.set_ylabel('Temperature (°C)')
    ax.set_xlabel("Date & Time (dd/mm/YYYY HH:MM)")
    ax.grid()

    # Format the x-axis for dates (label formatting, rotation)
    fig.autofmt_xdate(rotation=45)
    fig.tight_layout()
    fig.legend(loc = "upper left")
    #For annoations
    mplcursors.cursor(hover=True)

    fig.show() #display graph

def c_graph():  #create window to select names of cities for creating graph
    global graph_win, lb_graph, list_graph_citynm
        
    try:   #To make sure that only one window is running at a time 
        if graph_win.state() == "normal":
            return
    except:
        pass
    #Creating window for selectionof city name for creating graph
    graph_win = tkinter.Tk()
    graph_win.title("Graph Data")
    graph_win.configure(bg="sky blue")
    graph_win.geometry('500x500')
  
    lbl = tkinter.Label(graph_win, text="Select City", font=("Arial Bold", 10), bg ="white").pack()

    frame = tkinter.Frame(graph_win)
    scrollbar =  tkinter.Scrollbar(frame, orient="vertical")
        
    lb_graph = tkinter.Listbox(frame,selectmode = "multiple", width="50", height = "10",yscrollcommand=scrollbar.set)
    #Applying scrollbar
    scrollbar.config(command=lb_graph.yview)
    scrollbar.pack(side="right", fill = "y") #adding scrollbar to lb
    frame.pack()
    lb_graph.pack()

    #Filling the listbox with city names
    mc.execute("Select distinct city from weather;")
    city = mc.fetchall()
    list_graph_citynm = []
    for i in city:
        list_graph_citynm.append(i)
    updatelb(lb_graph,list_graph_citynm)
    #Create graph button
    btncreategraph = tkinter.Button(graph_win, text="Create Graph",font=("Arial Bold",10),fg="blue", bg="pink",width="25", height="3",command = creategraph).pack()





#FUNCTIONS FOR DELETING
def update_lb_display_delete(): #update listbox in delete & display window
    global d
    clearlistbox(lb_display_delete)
    dash = "-"*65
    try:
        n = maxcityname()
    except:
        return
    align = "{:<%ss}{:<20s}{:<10s}{:<s}"%(n,) #creating columns to left align the text. The number indicates column size
    heading = align.format("Region","Date & Time","Temp","Description") #create headings for displaying data
    lb_display_delete.insert("end",dash,heading,dash)
    j,k = None,list_sql_extracted[0][0]
    for data in  list_sql_extracted:
        j,k = k,j
        k = data[0]
        if k!= j:   #Checking if city name is changed
            lb_display_delete.insert("end",dash)
        dt = datetime.strftime(data[1],"%d-%m-%Y %H:%M") #converts datetime to string
        st = align.format(data[0],dt,data[2],data[3]) #To align the record in lb
        d[st] = data            #To keep track of original and formatted record
        lb_display_delete.insert("end",st)

def del_one():  #To delete selected records from display and delete window from sql
    global list_sql_extracted,d
    items = lb_display_delete.curselection() #indices of whats selected
    for i in items:
        try:
            item = lb_display_delete.get(i)
            mc.execute("delete from weather where date_time = %s and city = %s",(d[item][1],d[item][0]))
            con.commit() #Makes change in sql table permanent
            list_sql_extracted.remove(d[item])  #removes selected string from list containg extracted sql data
        except:
            pass
    update_lb_display_delete()

def c_dd():   #Display and delete data in database 
    global display_del_win, lb_display_delete, list_sql_extracted
    
    try: #To make sure that only one delete window is running at a time  
        if display_del_win.state() == "normal":
            return
    except:
        pass
    #Create display & delete window
    display_del_win = tkinter.Tk()
    display_del_win.title("Delete From Database")
    display_del_win.configure(bg="sky blue")
    display_del_win.geometry('500x500')
    
    lbl = tkinter.Label(display_del_win, text="Select Data To Be Deleted", font=("Arial Bold", 10), bg ="white").pack()

    frame = tkinter.Frame(display_del_win)
    scrollbary =  tkinter.Scrollbar(frame, orient="vertical")
    scrollbarx =  tkinter.Scrollbar(frame, orient="horizontal")
    
    lb_display_delete = tkinter.Listbox(frame,selectmode = "multiple", font = ("Consolas",10) , width="65", height = "23", yscrollcommand = scrollbary.set ,xscrollcommand=scrollbarx.set)

    #Applying scrollbar to lb_display_delete listbox
    scrollbary.config(command=lb_display_delete.yview)
    scrollbarx.config(command=lb_display_delete.xview)
    scrollbary.pack(side="right", fill = "y") 
    scrollbarx.pack(side="bottom", fill = "x")
    frame.pack()
    lb_display_delete.pack()

    #Filling the listbox with formated sql records
    mc.execute("Select * from weather order by city,date_time;")
    sql_info = mc.fetchall()
    list_sql_extracted = []
    for i in sql_info:
        list_sql_extracted.append(i)
    update_lb_display_delete()
    
    btn_del = tkinter.Button(display_del_win, text="Delete",font=("Arial Bold",10),fg="black", bg="lightgreen", width='25', height='3',command =del_one).pack()


#FUNCTIONS TO SAVE AND GET INFO
def c_savedata():  #save weather data from listbox lb_mwin in main window to sql database
    global list_sql_records, list_mw_info
    try:
        mc.execute("insert into weather values(%s,%s,%s,%s);",(list_sql_records[0],list_sql_records[1],list_sql_records[2],list_sql_records[3]))
        con.commit()
        list_mw_info.append('Save Successful')
    except IndexError:
        list_mw_info = ['No Data Collected']
    except:
        list_mw_info = ['Duplicate Entry Not Allowed | Invalid Data']
    updatelb(lb_mwin,list_mw_info)

def c_getweatherdata():  #update lb_mwin lstbox in main window with current weather data
    try:
        global list_mw_info, list_sql_records
        api_key = "683d869b7e0c3cb883aada5xxxxxx"
        base_url = "http://api.openweathermap.org/data/2.5/weather?"  
        city_name = entry_cn.get()  #Get city entered
        complete_url = base_url + "appid=" + api_key + "&q=" + city_name + "&units=metric"
        try:
            response = requests.get(complete_url) #Sends HTTP request
        except:
            list_mw_info = ["Connection Failed"]
            update_lb_mw()
            return
        x = response.json() #Gets info in the form of dictionary
        if x["cod"] != "404":
            y = x["main"]
            current_temp = y["temp"]
            z = x["weather"]
            description = z[0]["description"]
            city = x["name"]
            timestamp = x['dt']   #seconds elapsed since 1st Jan 1970 in Qatar
            timezone = x['timezone']  #Gives the time difference b/w the city's time and UTC time in seconds
            truetimestamp = timestamp - (10800 - timezone) #Timestamp of the city
            dt_object = datetime.fromtimestamp(truetimestamp).strftime("%Y/%m/%d %H:%M")  #converting timestamp to readable format
            list_sql_records = [city,dt_object,current_temp,description]
            list_mw_info = ["Area: %s"%(city,),"Temperature: %s"%(current_temp,),"Description: %s"%(description,),"Date: %s"%(dt_object)]
        else:
            list_mw_info = ["Region Not Found"]
    except KeyError:
        list_mw_info = ["No Input Given"]
    updatelb(lb_mwin,list_mw_info)





list_sql_records = []  #list containg the records to save in sql database
list_sql_extracted = []   #contains data extracted from sql
list_graph_citynm = []  #contains the names fo all cities for the listbox in graph window
list_mw_info = []   #contains text for lb_mwin listbox in  main window
d = {}   #To keep track of each formated string in the display and delete listbox along with its corresponding sql record

#Creating main window
window = tkinter.Tk()
window.title("CS Project - Weather Application")
window.configure(bg="sky blue")
window.geometry('500x500')

#Widgets on main window
lbl_entercn = tkinter.Label(window, text="Enter City Name", font=("Arial Bold", 10), bg ="White").pack()
entry_cn = tkinter.Entry(window, width="25")
entry_cn.pack()

btn_getweatherdata = tkinter.Button(window, text="Get Weather Data",font=("Arial Bold",10),fg="green", bg="white", width='25', height='2',command =c_getweatherdata).pack()
btn_savedata = tkinter.Button(window, text="Save Data",font=("Arial Bold",10),fg="blue", bg="pink",width="25", height="3",command = c_savedata).pack()

lb_mwin = tkinter.Listbox(window,font=("Arial",10),height="5", width="40")
lb_mwin.pack()

btn_dd = tkinter.Button(window, text="Display & Delete",font=("Arial Bold",10),fg="green", bg="orange",width="25", height="3",command = c_dd).pack()
btn_graph = tkinter.Button(window, text="Graph",font=("Arial Bold",10),fg="Maroon", bg="lightpink",width="25", height="3",command = c_graph).pack()
btn_exit = tkinter.Button(window, text="Exit",font=("Arial Bold",10),fg="green", bg="white", width='20', height='2',command =exit).pack()

window.mainloop() #To make the window run endlessly
