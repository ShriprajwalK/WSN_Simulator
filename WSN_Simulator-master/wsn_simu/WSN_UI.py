import sys
import csv
try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

try:
    import ttk
    py3 = False
except ImportError:
    import tkinter.ttk as ttk
    py3 = True


"""Importing the sensor data CSV and reading the different sensor parameters which are to be incorporated later"""
filename = "Sensor Data.csv"
titles = []
rows = []
sensor_and_type = []
with open(filename, 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        break
    for row in csvreader:
        rows.append(row)
        sensor_and_type.append(row[0] + "  (" + row[1] + ")")


'''Start of UI code'''

def init(top, gui, *args, **kwargs):
    global w, top_level, root
    w = gui
    top_level = top
    root = top

def destroy_window():
    global top_level
    top_level.destroy()
    top_level = None

def set_Tk_var():
    global spinbox
    spinbox = tk.StringVar()
    global combobox
    combobox = tk.StringVar()
    global tch64
    tch64 = tk.StringVar()

def start_gui():
    '''Starting point when module is the main routine.'''
    global val, w, root
    root = tk.Tk()
    set_Tk_var()
    top = Simulator_UI(root)
    init(root,top)
    root.mainloop()


w = None



def create_Simulator_UI(root, *args, **kwargs):
    '''Starting point when module is imported by another program.'''
    global w, w_win, rt
    rt = root
    w = tk.Toplevel(root)
    set_Tk_var()
    top = Simulator_UI(w)
    init(w, top, *args, **kwargs)
    return (w, top)


def destroy_Simulator_UI():
    global w
    w.destroy()
    w = None


first_row=["Length of the area", "," ,"Breadth of the area", ",", "Maximum budget (in INR)", ",", "WSN Model", ",", "X co-ordinate of sink node (Low Latency Model)", ",", "Y co-ordinate of sink node (Low Latency Model)", ",", "Sensor 1", ",", "Sensor 2", ",", "Sensor 3\n"]
second_row=["", "," ,"", ",", "", ",", "", ",", "0", ",", "0", ",", "", ",", "", ",", ""]


def write_to_file():
    file_of_values = open("input_file.csv", "w+")
    file_of_values.writelines(first_row)
    file_of_values.writelines(second_row)
    file_of_values.close()


def writing_to_second_row(index, value):
    second_row[index]=value
    #print("This is being taken in as the inputs", value)
    write_to_file()


class Simulator_UI:
    def __init__(self, top=None):
        _bgcolor = '#d9d9d9'
        _fgcolor = '#000000'
        _compcolor = '#d9d9d9'
        _ana1color = '#d9d9d9'
        _ana2color = '#ececec'
        font10 = "-family Roboto -size 9 -weight normal -slant roman "  \
            "-underline 0 -overstrike 0"
        font13 = "-family Roboto -size 36 -weight bold -slant roman "  \
            "-underline 0 -overstrike 0"
        font16 = "-family Roboto -size 12 -weight normal -slant roman "  \
            "-underline 0 -overstrike 0"
        font18 = "-family Roboto -size 18 -weight bold -slant roman "  \
            "-underline 0 -overstrike 0"
        font20 = "-family Roboto -size 13 -weight normal -slant roman "  \
            "-underline 0 -overstrike 0"
        font22 = "-family Roboto -size 16 -weight normal -slant roman "  \
            "-underline 0 -overstrike 0"
        font23 = "-family Roboto -size 11 -weight normal -slant roman "  \
            "-underline 0 -overstrike 0"
        font24 = "-family Roboto -size 17 -weight bold -slant roman "  \
            "-underline 0 -overstrike 0"
        font25 = "-family Roboto -size 10 -weight normal -slant roman "  \
            "-underline 0 -overstrike 0"
        font28 = "-family Roboto -size 24 -weight normal -slant roman "  \
            "-underline 0 -overstrike 0"
        self.style = ttk.Style()
        if sys.platform == "win32":
            self.style.theme_use('winnative')
        self.style.configure('.', background=_bgcolor)
        self.style.configure('.', foreground=_fgcolor)
        self.style.configure('.', font="TkDefaultFont")
        self.style.map('.', background=[('selected', _compcolor), ('active', _ana2color)])

        top.geometry("1366x705+2+0")
        top.title("WSN Simulator")
        top.configure(background="#474747", highlightbackground="#d9d9d9", highlightcolor="black")
        #071E3D

        def getting_all_values():
            #print("Getting Values...")
            writing_to_second_row(0, str(self.length_input.get()))
            writing_to_second_row(2, str(self.breadth_input.get()))
            writing_to_second_row(4, str(self.max_budget.get()))
            writing_to_second_row(6, self.model.get())
            writing_to_second_row(8, self.low_latency_x_coordinate.get())
            writing_to_second_row(10, self.low_latency_y_coordinate.get())
            #writing_to_second_row(12, self.first_sensor.get())
            #writing_to_second_row(14, self.second_sensor.get())
            #writing_to_second_row(16, self.third_sensor.get())
            #print("Written to file.")
            root.destroy()

        self.welcome_message = tk.Message(top)
        self.welcome_message.place(relx=0.0, rely=0.0, relheight=0.133, relwidth=0.997)
        self.welcome_message.configure(text='''WSN Simulator''', width=1362, background="#19647E", justify='center', highlightbackground="#d9d9d9", highlightcolor="black", font=font13, foreground="#FFC857")


        self.dimension_inputs = tk.LabelFrame(top)
        self.dimension_inputs.place(relx=0.0, rely=0.156, relheight=0.149, relwidth=0.996)
        self.dimension_inputs.configure(text='''Dimension Details''', background="#474747", width=1360, relief='groove', highlightbackground="#f0f0f0", borderwidth="3", font=font18, foreground="#ffffff")
        #071E3D

        self.length_input = tk.IntVar()
        self.length_of_the_area = tk.Spinbox(self.dimension_inputs, from_=250.0, to=10000.0, textvariable=self.length_input)
        self.length_of_the_area.place(relx=0.279, rely=0.476, relheight=0.362, relwidth=0.092, bordermode='ignore')
        self.length_of_the_area.configure(cnf=None, width=125, activebackground="#f9f9f9", selectforeground="#2c302e", selectbackground="#c4c4c4", justify='center', insertbackground="black", increment="100.0", highlightcolor="black", highlightbackground="black", foreground="black", disabledforeground="#a3a3a3", buttonbackground="#d9d9d9", font=font23, background="#ffffff")


        self.breadth_input = tk.IntVar()
        self.breadth_of_the_area = tk.Spinbox(self.dimension_inputs, from_=250.0, to=10000.0,textvariable=self.breadth_input)
        self.breadth_of_the_area.place(relx=0.868, rely=0.476, relheight=0.362, relwidth=0.092, bordermode='ignore')
        self.breadth_of_the_area.configure(cnf=None,  foreground="black", width=125, selectforeground="#2c302e", selectbackground="#c4c4c4", justify='center', insertbackground="black", increment="100.0", highlightcolor="black", highlightbackground="black", activebackground="#f9f9f9", font=font23, disabledforeground="#a3a3a3", background="#ffffff", buttonbackground="#d9d9d9")


        self.enter_length_message = tk.Message(self.dimension_inputs)
        self.enter_length_message.place(relx=0.029, rely=0.476, relheight=0.362, relwidth=0.228, bordermode='ignore')
        self.enter_length_message.configure(text='''Enter the length of the area (in metres)''', width=310, background="#474747", justify='center', highlightcolor="black", highlightbackground="#d9d9d9", font=font16, foreground="#ffffff")
        #A3BAC3

        self.enter_breadth_message = tk.Message(self.dimension_inputs)
        self.enter_breadth_message.place(relx=0.625, rely=0.476, relheight=0.362, relwidth=0.228, bordermode='ignore')
        self.enter_breadth_message.configure(text='''Enter the breadth of the area (in metres)''', width=310, background="#474747", justify='center', highlightcolor="black", highlightbackground="#d9d9d9", font=font16, foreground="#ffffff")
        #A3BAC3

        self.budget_input = tk.LabelFrame(top)
        self.budget_input.place(relx=0.0, rely=0.312, relheight=0.177, relwidth=0.996)
        self.budget_input.configure(relief='groove', width=1360, highlightcolor="black", highlightbackground="#f0f0f0", background="#474747", text='''Budget Details''', foreground="#ffffff", borderwidth="3", font=font18)

        self.max_budget = tk.IntVar()
        self.maximum_budget = tk.Spinbox(self.budget_input, from_=0.0, to=100000000000.0, textvariable=self.max_budget)
        self.maximum_budget.place(relx=0.64, rely=0.4, relheight=0.384, relwidth=0.114, bordermode='ignore')
        self.maximum_budget.configure(width=155, justify='center', selectforeground="#2c302e", activebackground="#fff78f", increment="1000.0", insertbackground="black", selectbackground="#c4c4c4", highlightcolor="black", highlightbackground="black", foreground="black", font=font23, disabledforeground="#a3a3a3", buttonbackground="#d9d9d9", background="#ffffff")


        self.enter_budget_message = tk.Message(self.budget_input)
        self.enter_budget_message.place(relx=0.191, rely=0.4, relheight=0.384, relwidth=0.419, bordermode='ignore')
        self.enter_budget_message.configure(text='''Enter the maximum budget of your intended network (in INR)''', width=570, highlightcolor="black", justify='center', background="#474747", font=font22, foreground="#ffffff", highlightbackground="#d9d9d9")
        #C1224F

        self.wsn_model_inputs = tk.LabelFrame(top)
        self.wsn_model_inputs.place(relx=0.0, rely=0.496, relheight=0.489, relwidth=0.996)
        self.wsn_model_inputs.configure(background="#474747", width=1360, highlightcolor="black", highlightbackground="#f0f0f0", relief='groove', text='''WSN Model Details''', borderwidth="3", font=font18, foreground="#ffffff")
        #071E3D

        self.choose_wsn_model_message = tk.Message(self.wsn_model_inputs)
        self.choose_wsn_model_message.place(relx=0.044, rely=0.145, relheight=0.11, relwidth=0.419, bordermode='ignore')
        self.choose_wsn_model_message.configure(text='''Choose the WSN model based on your preference''', width=570, background="#474747", font=font22, justify='center', foreground="#ffffff", highlightbackground="#d9d9d9", highlightcolor="black")
        #DC493A

        self.model=tk.StringVar()
        self.sensor_one = ttk.Combobox(self.wsn_model_inputs, values=["high reliability model","high lifetime model","low latency model","None"], textvariable=self.model)
        self.sensor_one.place(relx=0.647, rely=0.145, relheight=0.11, relwidth=0.146, bordermode='ignore')
        self.sensor_one.configure(width=223, takefocus="", cursor="fleur", foreground="red", background="green",font=font16, justify='center')

        """
        self.high_reliability_model_button = tk.Radiobutton(self.wsn_model_inputs)
        self.high_reliability_model_button.place(relx=0.647, rely=0.145, relheight=0.11, relwidth=0.146, bordermode='ignore')
        self.high_reliability_model_button.configure(text='''High Reliability Model''', highlightbackground="#d9d9d9", width=198, activebackground="#ececec", disabledforeground="#a3a3a3", activeforeground="#000000", background="#d9d9d9", font=font16, foreground="#000000", highlightcolor="black")


        self.high_lifetime_model_button = tk.Radiobutton(self.wsn_model_inputs)
        self.high_lifetime_model_button.place(relx=0.816, rely=0.145, relheight=0.11, relwidth=0.138, bordermode='ignore')
        self.high_lifetime_model_button.configure(indicator = 0, text='''High Lifetime Model''', activebackground="#ececec", foreground="#000000", width=188, activeforeground="#000000", highlightcolor="black", highlightbackground="#d9d9d9", background="#d9d9d9", disabledforeground="#a3a3a3")


        self.low_latency_model_button = tk.Radiobutton(self.wsn_model_inputs)
        self.low_latency_model_button.place(relx=0.478, rely=0.145, relheight=0.11, relwidth=0.146, bordermode='ignore')
        self.low_latency_model_button.configure(text='''Low Latency Model''', activebackground="#ececec", activeforeground="#000000", background="#d9d9d9", highlightcolor="black", highlightbackground="#d9d9d9", disabledforeground="#a3a3a3", font=font16, foreground="#000000")
        """

        self.low_latency_info = tk.Message(self.wsn_model_inputs)
        self.low_latency_info.place(relx=0.103, rely=0.348, relheight=0.067, relwidth=0.36, bordermode='ignore')
        self.low_latency_info.configure(text='''Enter X/Y co-ordinates separated by ; in case of None''', background="#474747", justify='center', font=font20, foreground="#ffffff", width=490, highlightbackground="#d9d9d9", highlightcolor="black")
        #DC493A

        self.low_latency_model_x_co_ordinate = tk.Message(self.wsn_model_inputs)
        self.low_latency_model_x_co_ordinate.place(relx=0.478, rely=0.348, relheight=0.067, relwidth=0.066, bordermode='ignore')
        self.low_latency_model_x_co_ordinate.configure(text='''X Co-ordinate''', width=90, background="#474747", justify='center', font=font10, foreground="#ffffff", highlightbackground="#d9d9d9", highlightcolor="black")


        self.low_latency_model_y_co_ordinate = tk.Message(self.wsn_model_inputs)
        self.low_latency_model_y_co_ordinate.place(relx=0.654, rely=0.348, relheight=0.067, relwidth=0.066, bordermode='ignore')
        self.low_latency_model_y_co_ordinate.configure(text='''Y Co-ordinate''', width=90, highlightcolor="black", justify='center', highlightbackground="#d9d9d9", background="#474747",font=font10, foreground="#ffffff")

        self.low_latency_x_coordinate = tk.StringVar()
        self.low_latency_model_x_value = tk.Spinbox(self.wsn_model_inputs, from_=0.0, to=10000.0, textvariable=self.low_latency_x_coordinate)
        self.low_latency_model_x_value.place(relx=0.566, rely=0.348, relheight=0.067, relwidth=0.063, bordermode='ignore')
        self.low_latency_model_x_value.configure(width=85, selectforeground="black", selectbackground="#c4c4c4", activebackground="#f9f9f9", background="white",buttonbackground="#d9d9d9", disabledforeground="#a3a3a3", font=font25,foreground="black", highlightbackground="black", highlightcolor="black", increment="10.0", insertbackground="black", justify='center')


        self.low_latency_y_coordinate = tk.StringVar()
        self.low_latency_model_y_value = tk.Spinbox(self.wsn_model_inputs, from_=0.0, to=10000.0, textvariable=self.low_latency_y_coordinate)
        self.low_latency_model_y_value.place(relx=0.743, rely=0.348, relheight=0.067, relwidth=0.063, bordermode='ignore')
        self.low_latency_model_y_value.configure(activebackground="#f9f9f9", background="white", buttonbackground="#d9d9d9", disabledforeground="#a3a3a3",font=font25, foreground="black", highlightbackground="black", highlightcolor="black", increment="10.0", insertbackground="black", justify='center', selectbackground="#c4c4c4", selectforeground="black")


        #self.types_of_sensors_info = tk.Message(self.wsn_model_inputs)
        #self.types_of_sensors_info.place(relx=0.103, rely=0.493, relheight=0.125, relwidth=0.36, bordermode='ignore')
        #self.types_of_sensors_info.configure(background="#DC493A", cursor="fleur", font=font20, foreground="#ffffff", highlightbackground="#d9d9d9", highlightcolor="#ffffff", text='''Choose the type(s) of sensors to be implemented in the network''', width=490, justify='center')


        #self.first_sensor=tk.StringVar()
        #self.sensor_one = ttk.Combobox(self.wsn_model_inputs, values=sensor_and_type, textvariable=self.first_sensor)
        #self.sensor_one.place(relx=0.485, rely=0.522, relheight=0.081, relwidth=0.164, bordermode='ignore')
        #self.sensor_one.configure(width=223, takefocus="", cursor="fleur")


        #self.second_sensor=tk.StringVar()
        #self.sensor_two = ttk.Combobox(self.wsn_model_inputs, values=sensor_and_type, textvariable=self.second_sensor)
        #self.sensor_two.place(relx=0.662, rely=0.522, relheight=0.081, relwidth=0.157, bordermode='ignore')
        #self.sensor_two.configure(width=223, takefocus="", cursor="fleur")


        #self.third_sensor=tk.StringVar()
        #self.sensor_three = ttk.Combobox(self.wsn_model_inputs, values=sensor_and_type, textvariable=self.third_sensor)
        #self.sensor_three.place(relx=0.831, rely=0.522, relheight=0.081, relwidth=0.149, bordermode='ignore')
        #self.sensor_three.configure(width=223, takefocus="", cursor="fleur")


        #self.style.map('TCheckbutton', background=[('selected', _bgcolor), ('active', _ana2color)])
        #self.agreement_check = ttk.Checkbutton(top)
        #self.agreement_check.place( relx=0.015, rely=0.936, relwidth=0.337, relheight=0.0, height=21)
        #self.agreement_check.configure(text='''I agree to the Terms and Conditions and wish to proceed and view the simulation''', variable=tch64, width=461)


        #self.credits_button = tk.Button(top)
        #self.credits_button.place(relx=0.015, rely=0.851, height=44, width=167)
        #self.credits_button.configure(activebackground="#c339ed", activeforeground="#000000", background="#c339ed", compound='center', disabledforeground="#a3a3a3", font=font28, foreground="#f8ff21", highlightbackground="#d9d9d9", highlightcolor="black", pady="0", text='''Credits''')


        self.submit_button = tk.Button(top)
        self.submit_button.place(relx=0.688, rely=0.894, height=44, width=167)
        self.submit_button.configure(text='''Submit''', command=getting_all_values, activebackground="#c339ed", background="#c339ed", activeforeground="#000000", compound='center', disabledforeground="#a3a3a3", font=font28, foreground="#f8ff21", highlightbackground="#d9d9d9", highlightcolor="black", pady="0")


        self.clear_button = tk.Button(top)
        self.clear_button.place(relx=0.849, rely=0.894, height=44, width=167)
        self.clear_button.configure(text='''Close''', command=sys.exit, activebackground="#c339ed", activeforeground="white", background="#c339ed", compound='center', disabledforeground="#a3a3a3", font=font28, foreground="#f8ff21", highlightbackground="#d9d9d9", highlightcolor="black", pady="0")


#if __name__ == '__main__':
 #  start_gui()
