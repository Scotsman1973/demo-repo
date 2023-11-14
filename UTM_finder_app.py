import tkinter as tk # the GUI toolbox
import re # library for input validation function
import math # the library for mathematical calculations


root = tk.Tk()  # must match the bottom two lines of code in order for this to work

# The names of the two variables to be input, allows floats to deal with lat and long
# the latitude
p1lat = tk.StringVar()
# the longitude
p1long = tk.StringVar()



class Window(tk.Frame):

    def __init__(self, master=None):

        tk.Frame.__init__(self, master)

        self.master = master

        self.pack()


        # The GUI can be dragged larger or smaller horizontally or vertically, True for resizable, False for fixed
        self.master.resizable(True, True)

        # sets the fonts to be used in this GUI

        title_font = ('Arial', 16)

        font = ('Arial', 10)

        # Improved color
        self.master.tk_setPalette(background='#ececec')

        # GUI title bar
        self.master.title("UTM/UPS zone finder")

        # Positions the GUI in the screen sweet spot

        x = (self.master.winfo_screenwidth() -
             self.master.winfo_reqwidth()) / 2
        y = (self.master.winfo_screenheight() -
             self.master.winfo_reqheight()) / 3
        x = str(int(x))
        y = str(int(y))

        self.master.geometry("+{}+{}". format(x, y))

        def validate(string):
            regex = re.compile(r"[0-9.-]*$")
            result = regex.match(string)
            return (string != ""
                and string.count('.') <= 1
                and string.count('-') <= 1
                and result is not None
                and result.group(0) != "")

        def on_validate(P):
            return validate(P)

        def click_quit():
            print("The user clicked 'cancel'")
            self.master.destroy()

        def clear_fields():
            utm_output.delete('1.0', 'end')
            p1lat.set('')
            p1long.set('')
            

        def callback():

            # this makes sure the output textbox is clear when the callback function is started
            utm_output.delete('1.0', 'end')

            point1Latitude = ""
            point1Longitude = ""

            try:

                # makes sure the input is a valid float
                if  -90 <= float(p1lat.get()) <= 90:
                    point1Latitude = float(p1lat.get())
                else:
                    p1lat.set('Invalid entry')

                # makes sure the input is a valid float
                if -180 <= float(p1long.get()) <= 180:
                    point1Longitude = float(p1long.get())
                else:
                    p1long.set('Invalid entry')

                 # this statement just logically makes 180 the same as -180.  I chose that way around because the next statement adds 180
                if point1Longitude == 180.0:
                    point1Longitude = -180.0

                # only goes into the next stage if both the inputs were valid floats
                if  (-90 <= point1Latitude <= 90 and
                    -180 <= point1Longitude <= 180 and
                    isinstance(point1Latitude, float) and
                    isinstance(point1Longitude, float)):

                    # this routine defines the polar regions and divides the area in between into 60 by adding 180, bring the calculation back to 360/6
                    # math.floor rounds the answer down to the nearest integer, but that makes it zones 0 - 59, so add 1 and it becomes zones 1-60
                    if point1Latitude < -80.0:
                        utm_zone = "South Pole"

                    elif point1Latitude > 84.0:
                        utm_zone = "North Pole"

                    # this statement just logically makes 180 the same as -180.  I chose that way around because the next statement adds 180
                

                    else:
                        utm_zone_calc = (point1Longitude + 180) /6
                        utm_zone_calc = math.floor(utm_zone_calc)
                        utm_zone = utm_zone_calc + 1


                        if -80.0 <= point1Latitude <= 0.0:
                            utm_zone_letter = "S"
                        else:
                            utm_zone_letter = "N"
                                

                        utm_zone = str(utm_zone) + str(utm_zone_letter)

                    # this section handles the exceptions around Norway and Svalbard
                    if (56.0 < point1Latitude <= 64.0 and
                        0.0 <= point1Longitude < 3.0):
                        utm_zone = '31N'

                    if (56.0 < point1Latitude <= 64.0 and
                        3.0 <= point1Longitude < 12.0):
                        utm_zone = '32N'

                    if (72.0 < point1Latitude <= 84.0 and
                        0.0 <= point1Longitude < 9.0):
                        utm_zone = '31N'

                    if (72.0 < point1Latitude <= 84.0 and
                        9.0 <= point1Longitude < 21.0):
                        utm_zone = '33N'

                    if (72.0 < point1Latitude <= 84.0 and
                        21.0 <= point1Longitude < 33.0):
                        utm_zone = '35N'

                    if (72.0 < point1Latitude <= 84.0 and
                        33.0 <= point1Longitude < 42.0):
                        utm_zone = '37N'

                    
                    # this sends the output to the GUI
                    utm_output.insert(tk.INSERT,  utm_zone)

                    # this sends the output to the terminal
                    print('                       ')
                    print('New set of coordinates')
                    print('The latitude you entered is ' + str(point1Latitude))
                    print('The longitude you entered is ' + str(point1Longitude))
                    print('Universal Transverse Mercator (UTM)')
                    print('Universal Polar Stereographic (UPS)')
                    print('Exceptions around Norway and Svalbard are accounted for')
                    print('N/S denotes north or south hemisphere')
                    print('The UTM/UPS zone is: ' + str(utm_zone))

                else:
                    
                    return

            except:

                ValueError


        # Title
        title = tk.Label(self, text = "App for finding the UTM/UPS zone of a given latitude and longitude.", font = title_font)
        # explanation text for GUI
        text1 = tk.Label(self, text="Please enter the latitude (-90 t0 90) and longitude (-180 to 180).", font = font)
        # explanation text for GUI
        text2 = tk.Label(self, text = "Characters other than the numbers 0 - 9 and . and - will not be accepted.", font = font)
        # explanation text for GUI
        text3 = tk.Label(self, text = "Universal Transverse Mercator (UTM), Universal Polar Stereographic (UPS)", font = font)
        # explanation text for GUI
        text4 = tk.Label(self, text = "Exceptions around Norway and Svalbard are accounted for, N/S denotes north or south hemisphere", font = font)
    
        # positioning of title text
        title.grid(row=0, padx=10, pady=10)
        # positioning portions of explanatory text
        text1.grid(row=1, padx=10, pady=10)
        text2.grid(row=2, padx=10, pady=10)
        text3.grid(row=3, padx=10, pady=10)
        text4.grid(row=4, padx=10, pady=10)
        # create frame for entry lables and boxes

        entry_frame = tk.Frame(self)
        entry_frame.grid(row = 5)

        # Labels for input boxes
        label1 = tk.Label(entry_frame, text="Latitude (must be between -90 and 90)", font=font)
        label2 = tk.Label(entry_frame, text="Longitude (must be between -180 and 180)", font=font)
    
        # The two entryboxes for input, allows floats to deal with lat and long
        # the latitude
        p1lat_entrybox = tk.Entry(entry_frame, validate="key", textvariable = p1lat)
        vcmd = (p1lat_entrybox.register(on_validate), '%P')
        p1lat_entrybox.config(validatecommand=vcmd)
        # the longitude
        p1long_entrybox = tk.Entry(entry_frame, validate="key", textvariable = p1long)
        vcmd = (p1long_entrybox.register(on_validate), '%P')
        p1long_entrybox.config(validatecommand=vcmd)

        # positioning of input labels and boxes
        label1.grid(row=0, column=0, padx=(20, 0), pady=10)
        p1lat_entrybox.grid(row=0, column=1, padx=(0, 20), pady=10)
        label2.grid(row=1, column=0, padx=(20, 0), pady=10)
        p1long_entrybox.grid(row=1, column=1, padx=(0, 20), pady=10)
        
        # frame for buttons

        button_frame = tk.Frame(self)
        button_frame.grid(row = 6)

        button1 = tk.Button(button_frame, text="Calculate UTM/UPS zone", default='active',
                        command=callback)  # Variables are being attached to callback
        # variables come from the entry boxes and are passed into another function, callback
        button2 = tk.Button(button_frame, text="Clear fields", command=clear_fields)
        button3 = tk.Button(button_frame, text="Quit", command=click_quit)

        button1.grid(row=0, column=0, sticky='e', padx=20, pady=(5, 10))
        button2.grid(row=0, column=1, sticky='w', padx=20, pady=(5, 10))
        button3.grid(row=0, column=2, sticky='w', padx=20, pady=(5, 10))

        # create a frame for the results boxes

        results_frame = tk.Frame(self)
        results_frame.grid(row = 7)

        # Result label
        result_label1 = tk.Label(results_frame, text="The UTM/UPS zone is: ", font=font)
        # box for calculated distance
        utm_output = tk.Text(results_frame, width = 12, height = 1, background = "light grey")


        # positioning the results output label 1
        result_label1.grid(row=0, column=0, padx=(10, 0), pady=10)
        
        # positioning the output box
        utm_output.grid(row = 0, column = 1)



app = Window(root)

root.mainloop()