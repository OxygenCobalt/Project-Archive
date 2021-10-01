# PyCipher
# A rudimentary cipher program in python

# Import tkinter [Alot of tkinter elements arent included in the main package]
import tkinter as tk
import tkinter.font as tkFont
import tkinter.scrolledtext as tkText
import tkinter.ttk as ttk
from tkinter import font

# Auxillary Imports [Copy, Random Generation]
import pyperclip
import random

# Public Variables
class Public:
    decode_output_data = [] # Array of all outputs for brute force decode
    random_active = False # Random on/off
    brute_active = False # Brute force decode on/off

# Functions
class Functions:
    key = [']', '!', 'q', 'n', 'k', ';', 'D', '\\', 'F', '}', 
    'l', 'H', 'h', 'X', 'o', 'v', 'x', ':', 'C', '*', '1', 's', 
    'u', '>', 'm', 'L', 'G', '@', 'f', '$', '"', 'E', ')', 'O', 
    "'", '{', '&', ',', 'A', 'Z', 'Y', 'j', '2', '+', 'K', 'y', 
    'V', '(', '6', '[', 'd', 'p', '7', 'i', '0', 'J', 'S', '?', 
    ' ', '`', '-', 'M', 'N', 'P', '/', '|', 'T', 'W', '3', 'c', 
    'Q', 'I', '8', '4', '^', '=', 'U', 'z', 'a', 'B', '%', 'b', 
    't', 'g', '#', '<', 'R', '.', 'e', '5', 'w', '~', '9', 'r', 
    '_'] # Primary key, already randomized

    def encode(box, rbool, spinbox, output, btn_disable):
        # Encode a string into the encoded message based on rotation
        # If not random [rbool=False], read the spinbox [Encoding Number] for rotation

        string = list(box.get()) # Read Input Box
        if rbool: # If random [rbool=True]
            rot = random.randint(0, len(Functions.key)) # Create a random rotation
        elif not rbool: # If not random
            rot = spinbox.get() # Read spinbox [Encoding Number] for rotation
        for i, char in enumerate(string):
            string[i] = Functions.key.index(string[i]) # Find the index of the character in the string
            string[i] = (int(string[i]) + int(rot)) % len(Functions.key) # Add the rotation to the character [And avoid overflow]
            string[i] = Functions.key[string[i]] # Set character in string to the index of the key

        output.insert(tk.END, ''.join(string) + '\n') # Add new string to the output box
        btn_disable.config(state=tk.DISABLED) # Disable the encode button until the box is cleared

    def decode_update(output, var): 
        # Update output [During brute force mode]

        val = var.get() # Get current index
        val = val % len(Public.decode_output_data) # Prevent overflow w/array size
        output.delete('1.0', tk.END) # Clear existing characters
        output.insert(tk.END, Public.decode_output_data[val]) # Insert new string
        
    def decode(box, bbool, spinbox_get, spinbox_control, output, var, btn_disable):
        # Decode a given string

        string = list(box.get()) # Retreive encoded string from input box
        if bbool: # If brute force
            for i in range(92): # Decode for every singe combination [92 total]
                temp = string[:]
                for _i, c in enumerate(temp):
                    temp[_i] = Functions.key.index(temp[_i])
                    temp[_i] = (int(temp[_i]) - i) % len(Functions.key) # Very similar to encode, except subtracts instead of adds.
                    temp[_i] = Functions.key[temp[_i]]

                Public.decode_output_data.append(''.join(temp)) # Append "Decoded" string to output data to be used w/decode_update

            spinbox_control.config(state='readonly') # Dont disable decode index, prevent it from being disabled
            output.config(state=tk.NORMAL) # Enable output box
            Functions.decode_update(output, var) # Run decode update with the initial index given

        elif not bbool: # If not brute force
            rot = spinbox_get.get() # Read index given
            for i, c in enumerate(string):
                string[i] = Functions.key.index(string[i])
                string[i] = (int(string[i]) - int(rot)) % len(Functions.key) # Simply subtract by rotation 
                string[i] = Functions.key[string[i]]

            output.config(state=tk.NORMAL)
            output.insert(tk.END, ''.join(string)) # Insert output into box
            var.set(rot)

        btn_disable.config(state=tk.DISABLED) # Disable the decode button

    def encode_copy(box):
        # Retrive and copy encoded message

        string = box.get('1.0', tk.END)
        string = string[0:len(string) - 2] # Get string without excess characters added by program
        pyperclip.copy(string) # Use pyperclip to add to clipboard

    def decode_copy(box):
        # Retrive and copy decoded message

        string = box.get('1.0', tk.END)
        string = string[0:len(string) - 1]
        pyperclip.copy(string)

    def rbutton_check(v, spinbox):
        # Check if random has been checked or not

        status = v.get()
        if status == 0:
            Public.random_active = False # Enable/Disable random activity
            spinbox.config(state='readonly') # Limit spinbox usage to integers
        elif status == 1:
            Public.random_active = True
            spinbox.config(state=tk.DISABLED) # Disable spinbox altogether if active

    def bbutton_check(v):
        # Check if brute force decode has been checked or not

        status = v.get()
        if status == 0:
            Public.brute_active = False # Enable/Disable brute force decode
        elif status == 1:
            Public.brute_active = True

    def encode_clear(output_clear, btn_enable):
        # Clear output box for encode

        output_clear.delete('1.0', tk.END)
        btn_enable.config(state=tk.NORMAL)

    def decode_clear(output_clear, spinbox_clear, var, btn_enable):
        # Clear output box for decode

        output_clear.delete('1.0', tk.END)
        var.set(0)
        spinbox_clear.config(state=tk.DISABLED) # Disable brute force spinbox
        output_clear.config(state=tk.DISABLED) # Disable output box
        Public.decode_output_data = [] # Wipe brute force array
        btn_enable.config(state=tk.NORMAL) # Reenable decode button

    def switch_scenes(ebool, dbool, ebtn, dbtn, eframe, dframe):\
        # Switch scenes from encode to decode and vice versa

        if ebool: # If encode was pressed
            dbtn.config(relief='raised')
            ebtn.config(relief='sunken') # Press button "Down" to indicate active frame
            eframe.lift()
        elif dbool: # If decode was pressed
            dbtn.config(relief='sunken')
            ebtn.config(relief='raised') 
            dframe.lift()           

# Main application code
class Application:
    def __init__(self):
        # Establish all elements

        self.root = tk.Tk() # Root Frame

        # Window details [Static Frame]
        self.root.minsize(width=400, height=400)
        self.root.maxsize(width=400, height=400)
        self.root.resizable(False, False)
        self.root.title('PyCipher')
        self.root.tk.call('wm', 'iconphoto', self.root._w, tk.PhotoImage(file='icon.png'))  # Load icon image [Which TK is apparently really bad at.] 
        self.standard_font = tkFont.Font(family='Helevecta', size=10, weight='bold') # Main font

        # Encode Elements
        self.encode_frame = tk.Frame(self.root) # Encode menu
        self.rbutton_status = tk.IntVar() # Random button status
        self.encode_rotationbox = tk.Spinbox(self.encode_frame, increment=1, from_=0, to_=93) # Index spinbox
        self.encode_text = tk.Label(self.encode_frame, text='Place text to encode here', font=self.standard_font) # Guidance Text
        self.encode_entry = tk.Entry(self.encode_frame) # Input box
        self.encode_output = tkText.ScrolledText(self.encode_frame) # Output text box

        self.encode_btn = tk.Button( # Main encode button
            self.encode_frame, 
            bd=1, 
            text='Encode!', 
            command=lambda: Functions.encode(
                self.encode_entry, 
                Public.random_active, 
                self.encode_rotationbox, 
                self.encode_output, 
                self.encode_btn
            ))
        self.encode_copy_btn = tk.Button( # Copy button
            self.encode_frame, 
            bd=1,  
            text='Copy', 
            command=lambda: 
            Functions.encode_copy(self.encode_output)
        )
        self.encode_clear_btn = tk.Button( # Clear button
            self.encode_frame, 
            bd=1, text='Clear', 
            command=lambda: Functions.encode_clear(self.encode_output, self.encode_btn)
        )
        self.encode_random_checkbutton = tk.Checkbutton( # Random on/off
            self.encode_frame, 
            text='Random', 
            variable=self.rbutton_status, 
            command=lambda: Functions.rbutton_check(self.rbutton_status, self.encode_rotationbox)
        )

        # Decode Elements
        self.decode_frame = tk.Frame(self.root)
        self.bbutton_status = tk.IntVar()
        self.output_rotationbox_status = tk.IntVar()
        self.decode_rotationbox = tk.Spinbox(self.decode_frame, increment=1, from_=0, to_=93)
        self.decode_text = tk.Label(self.decode_frame, text='Place text to decode here', font=self.standard_font)
        self.decode_entry = tk.Entry(self.decode_frame)
        self.decode_output = tkText.ScrolledText(self.decode_frame)
        self.decode_output_text = tk.Label(self.decode_frame, text='Output at rotation', font=self.standard_font) # Guidance text for brute force

        self.decode_output_rotationbox = tk.Spinbox( # Brute force update spinbox
            self.decode_frame, 
            increment=1,
            from_=0, 
            to_=93, 
            textvariable=self.output_rotationbox_status, 
            command=lambda: Functions.decode_update(
                self.decode_output, 
                self.output_rotationbox_status
                ), 
            wrap=True
        )
        self.decode_btn = tk.Button( # Main decode button
            self.decode_frame, 
            text='Decode!', 
            bd=1, 
            command=lambda: Functions.decode(
                self.decode_entry, 
                Public.brute_active, 
                self.decode_rotationbox, 
                self.decode_output_rotationbox, 
                self.decode_output, 
                self.output_rotationbox_status, 
                self.decode_btn
        ))
        self.decode_brute_checkbutton = tk.Checkbutton( # Brute force on/off
            self.decode_frame, 
            text='Brute Force',
            variable=self.bbutton_status, 
            command=lambda: Functions.bbutton_check(self.bbutton_status)
        )
        self.decode_copy_btn = tk.Button(
            self.decode_frame, 
            bd=1, 
            text='Copy', 
            command=lambda: Functions.decode_copy(self.decode_output)
        )
        self.decode_clear_btn = tk.Button(
            self.decode_frame, 
            bd=1, 
            text='Clear', 
            command=lambda: Functions.decode_clear(
                self.decode_output, 
                self.decode_output_rotationbox, 
                self.bbutton_status, 
                self.decode_btn
        ))

        self.main_encode_activate = tk.Button( # Encode switch button
            self.root, text='Encode', 
            command=lambda: Functions.switch_scenes(
                True, 
                False, 
                self.main_encode_activate, 
                self.main_decode_activate, 
                self.encode_frame, self.decode_frame),
                bd=1
        )
        self.main_decode_activate = tk.Button( # Decode switch button
            self.root, 
            text='Decode', 
            command=lambda: Functions.switch_scenes(
                False, 
                True, 
                self.main_encode_activate, 
                self.main_decode_activate, 
                self.encode_frame, 
                self.decode_frame), 
                bd=1
        )

    def build(self):
        # Set up all elements at specific x/y coordinates

        # Configure certain buttons
        self.encode_frame.lift()
        self.main_encode_activate.config(relief='sunken')
        self.encode_rotationbox.config(state='readonly')
        self.decode_rotationbox.config(state='readonly')
        self.decode_output.config(state=tk.DISABLED)
        self.decode_output_rotationbox.config(state=tk.DISABLED)

        self.main_encode_activate.place(height=30, width=200)
        self.encode_frame.place(height=470, width=400, y=30)
        self.encode_rotationbox.place(height=20, width=55, x=237, y=80)
        self.encode_text.place(height=30, width=200, x=100, y=0)
        self.encode_entry.place(height=20, width=200, x=100, y=25)
        self.encode_output.place(height=200, width=300, x=57, y=120)
        self.encode_btn.place(height=30, width=100, x=100, y=63)
        self.encode_copy_btn.place(height=30, width=100, x=100, y=325)
        self.encode_clear_btn.place(height=30, width=100, x=200, y=325)
        self.encode_random_checkbutton.place(height=20, width=100, x=215, y=55)

        self.main_decode_activate.place(height=30, width=200, x=200)
        self.decode_frame.place(height=470, width=400, y=30)
        self.decode_rotationbox.place(height=20, width=55, x=237, y=80)
        self.decode_text.place(height=30, width=200, x=100, y=0)
        self.decode_entry.place(height=20, width=200, x=100, y=25)
        self.decode_output.place(height=150, width=300, x=57, y=175)
        self.decode_output_text.place(height=30, width=200, x=57, y=140)
        self.decode_output_rotationbox.place(height=20, width=55, x=237, y=147)
        self.decode_btn.place(height=30, width=100, x=100, y=63)
        self.decode_brute_checkbutton.place(height=20, width=100, x=215, y=55)
        self.decode_copy_btn.place(height=30, width=100, x=100, y=333)
        self.decode_clear_btn.place(height=30, width=100, x=200, y=333)

if __name__ == '__main__':
    # Main loop

    a = Application()
    a.build()
    a.root.mainloop()

# OxygenCobalt