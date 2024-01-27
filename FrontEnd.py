import analyzer

def buton_action_add_Stock():
    analyzer.handleStocks(inputSingle=input_stock.get(), single=True, add=True)
    refresh_dropdown()
    input_stock.delete(0, "end")

def buton_action_remove_Stock():
    key = inputBox.get()
    # key = dropDown.get() + "; random"
    analyzer.handleStocks(inputSingle=key, single=True, add=False)
    refresh_dropdown()

def buton_action_addStockFromList():
    analyzer.handleStocks(single=False, add=True)
    refresh_dropdown()

def buton_action_delStockFromList():
    analyzer.handleStocks(single=False, add=False)
    refresh_dropdown()
 
def refresh_dropdown():
    data = analyzer.load_stocks()
    listBox.delete(0, "end")
    for item in data:
        listBox.insert("end", item)
    ### Used for Drop down menue ###
    # # Reset var and delete all old options
    # dropDown.set('')
    # dropDown_menue['menu'].delete(0, 'end')
    # # Insert list of new options (analyzer.tk._setit hooks them up to var)
    # stocks = analyzer.load_stocks()
    # for choice in stocks:
    #     dropDown_menue['menu'].add_command(label=choice, 
    #                                        command=analyzer.tk._setit(dropDown, 
    #                                                          choice))
     
def buton_action_get_data():
    stocks = analyzer.load_stocks()
    key = inputBox.get()
    # key = dropDown.get()
    stock = stocks[key]
    print(key, stock)
    analyzer.get_data(stock, key, is_interval_min.get())

def button_update_all_stocks():
    stocks = analyzer.load_stocks()
    for key in stocks:
        print(key, stocks[key])
        analyzer.get_data(stocks[key], key, is_interval_min.get())
        analyzer.time.sleep(1)
    
def buton_action_get_indicator():
    key = inputBox.get()
    # key = dropDown.get()
    interval = analyzer.set_interval(is_interval_min.get())
    data1 = analyzer.is_data_already_read(key, interval)[2]
    data2 = analyzer.get_indicators(data1)
    analyzer.save_data(data2, key, interval)
    print("got indicator and saved them")
    
def buton_action_plot():
    key = inputBox.get()
    # key = dropDown.get()
    timeFrom = input_timeFrom.get()
    timeTo = input_timeTo.get()
    # print(timeFrom, timeTo)
    analyzer.plot_chart([timeFrom,timeTo], key, is_interval_min.get())

def buton_action_checkFilesInData():
    analyzer.check_loaded_files()

def buton_action_deleteStockWithoutDataFile():
    analyzer.checkIfFileForStock()
    
def update(data):
    listBox.delete(0, "end")
    for item in data:
        listBox.insert("end", item)
        
def fillout(e):
    inputBox.delete(0, "end")
    inputBox.insert(0, listBox.get("active"))
    
def check(e):
    typed = inputBox.get()
    stocks = analyzer.load_stocks()
    if typed == "":
        data = stocks
    else:
        data = []
        for item in stocks:
            if typed.lower() in item.lower():
                data.append(item)
    update(data)

def ammountOfStocks(e):
    ammountBox.delete(0, "end")
    ammountBox.insert(0, analyzer.amount_of_stocks())
    
window_hight = 250
window_width = 965
analysis = analyzer.tk.Tk()
analysis.geometry(f"{window_width}x{window_hight}\
+{int(analysis.winfo_screenwidth()/2-window_width/2)}\
+{int(analysis.winfo_screenheight()/2-window_hight/2)}")
is_interval_min = analyzer.tk.BooleanVar()

analysis.title("Analyse navigator")
stocks = analyzer.load_stocks()
options = [key for key in stocks]
options.append("Choose a stock!")
dropDown = analyzer.tk.StringVar(analysis)
dropDown.set(options[len(stocks)])

dropDown_menue = analyzer.tk.OptionMenu(analysis, dropDown, *options)

check_interval_min = analyzer.tk.Checkbutton(analysis, text="interval Minute", variable=is_interval_min)

Button_getData = analyzer.tk.Button(analysis, 
                        text="Get data", 
                        command=buton_action_get_data)
Button_updadate_all = analyzer.tk.Button(analysis,
                        text="Update all Stocks",
                        command=button_update_all_stocks)
Button_getIndicator = analyzer.tk.Button(analysis, 
                        text="Get indicator", 
                        command=buton_action_get_indicator)
Button_Plot = analyzer.tk.Button(analysis, 
                        text="Plot", 
                        command=buton_action_plot)
buton_addStockFromList = analyzer.tk.Button(analysis,
                        text="Add stock from List",
                        command=buton_action_addStockFromList)
buton_delStockFromList = analyzer.tk.Button(analysis,
                        text="Delete stock from List",
                        command=buton_action_delStockFromList)
Button_saveStock = analyzer.tk.Button(analysis, 
                        text="Save Stock", 
                        command=buton_action_add_Stock)
Button_ramoveStock = analyzer.tk.Button(analysis, 
                        text="Remove choosed Stock(dropdown)", 
                        command=buton_action_remove_Stock)
Button_checkFilesInData = analyzer.tk.Button(analysis,
                        text="Check Files in Data!",
                        command=buton_action_checkFilesInData)
Button_deleteStockWithoutDataFile = analyzer.tk.Button(analysis,
                        text="Delete Stocks without File in Data.",
                        command=buton_action_deleteStockWithoutDataFile)

Button_exit = analyzer.tk.Button(analysis, 
                        text="Exit", 
                        command=analysis.quit, 
                        bg="red", 
                        fg="black", 
                        font="sans 16 bold")

input_stock = analyzer.tk.Entry(analysis)
input_timeFrom = analyzer.tk.Entry(analysis)
input_timeTo = analyzer.tk.Entry(analysis)

info_inputStock = analyzer.tk.Label(analysis, 
            text="Add stock: Preffered format!\n Name (eg.: Varta), ID (eg.: VAR1.DE)")
info_timeFrom = analyzer.tk.Label(analysis, 
            text="From: Days before Today")
info_timeTo = analyzer.tk.Label(analysis, 
            text="To: Days before Today")
inputBox = analyzer.tk.Entry(analysis)
listBox = analyzer.tk.Listbox(analysis)
ammountBox = analyzer.tk.Entry(analysis)

# dropDown_menue.grid(row=0, column=0, columnspan=5, sticky="ew")
inputBox.grid(row=0, column=0, columnspan=4, sticky="ew")
ammountBox.grid(row=0, column=5)
listBox.grid(row=1, column=5, rowspan=5)

info_inputStock.grid(row=1, column=0, sticky="ew")
input_stock.grid(row=1, column=1, columnspan=2, sticky="ew")

Button_ramoveStock.grid(row=2, column=0, sticky="ew")
Button_saveStock.grid(row=2, column=1, columnspan=1, sticky="ew")
buton_addStockFromList.grid(row=2, column=2, columnspan=1, sticky="ew")
buton_delStockFromList.grid(row=2, column=3, columnspan=1, sticky="ew")

Button_checkFilesInData.grid(row=3, column=1, sticky="ew")
Button_deleteStockWithoutDataFile.grid(row=3, column=2, columnspan=2, sticky="ew")

Button_getData.grid(row=4, column=0, sticky="ew")
Button_updadate_all.grid(row=4,column=1, sticky="ew")
Button_getIndicator.grid(row=4, column=2, sticky="ew")
check_interval_min.grid(row=4, column=3, sticky="ew")

info_timeFrom.grid(row=5, column=0, sticky="ew")
input_timeFrom.grid(row=5, column=1, sticky="ew")
info_timeTo.grid(row=5, column=2, sticky="ew")
input_timeTo.grid(row=5, column=3, sticky="ew")
Button_Plot.grid(row=5, column=4, sticky="ew")

Button_exit.grid(row=6, column=2, sticky="ew")

listBox.bind("<Up>", fillout)
listBox.bind("<Down>", fillout)
listBox.bind("<<ListboxSelect>>", fillout)
inputBox.bind("<KeyRelease>", check)
ammountBox.bind("<KeyRelease>", ammountOfStocks)


update(stocks)

analysis.mainloop()