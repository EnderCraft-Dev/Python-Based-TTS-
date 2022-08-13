from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import json
from uuid import uuid4
import gtts
import os
import os.path
from time import sleep
from threading import Thread
import sys

# global variables
global is_opened_1
is_opened_1 = False

global is_opened_2
is_opened_2 = False

global is_opened_3
is_opened_3 = False

global is_opened_4
is_opened_4 = False

global selected_lang
selected_lang = None

global pathname_to_save
pathname_to_save = None


# languages
langs = gtts.lang.tts_langs()
langs_json = json.dumps(gtts.lang.tts_langs(), indent=3)

# Icon for pyinstaller
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Exit button
def exit():
	if messagebox.askokcancel('Quit', 'Do you want to quit?'):
		app.destroy()

# TTS Dialog window
def text_to_speech_window():
	# Event to trigger when the window is closed
	def exit_2():
		if messagebox.askokcancel('Quit', 'Do you want to quit?'):
			win.destroy()
			global is_opened_1
			is_opened_1 = False

			global pathname_to_save
			pathname_to_save = None

	# SAVE FILE function
	def save_file():
		if pathname_to_save != None: # Pathname to save is used to write data on an existing file, if the file doesn´t exists, we call save_as() to ask the user to save the file first
			with open(pathname_to_save, 'w') as file: # If the file exists, we open the file and write data on it (The content of the text area)
				file.write(textbox.get("1.0", END))
				file.close()
			messagebox.showinfo("TTS Create Dialog", "File saved succesfully")
		else:
			save_as()

	# SAVE AS function
	def save_as():
		data = textbox.get("1.0", END)
		if(len(data) > 1): # We cannot save empty files, so, we check if the user written something on the textarea
			fname = filedialog.asksaveasfile(
				mode='w',
				defaultextension='ttsdialog',
				filetypes = (
			        ('TTS Files', '*.ttsdialog'),
			        ('All files', '*.*')
			    )
			)
			try:
				# This is basically the OPEN FILE function, but we write data on the file instead of reading it
				fname.write(data)
				win.title(f'TTS - {os.path.basename(fname.name)}')
				global pathname_to_save
				pathname_to_save = fname.name
			except:
				pass
		else:
			messagebox.showinfo('Dialog Editor', 'Cannot save an empty file')


	# OPEN FILE function
	def open_file():
		file = filedialog.askopenfile(
			mode='r',
			defaultextension='ttsdialog',
			filetypes = (
			        ('TTS Files', '*.ttsdialog'),
			        ('TTS Files', '*.TTSDIALOG')
			 ),
			initialdir=os.getcwd(),
			multiple=False
		)
		if file != None:
			textbox.insert("1.0", file.read()) # We insert the file data on the text area
			win.title(f'TTS - {os.path.basename(file.name)}') # We change the window's title
			global pathname_to_save # Pathname to save is used on SAVE function
			pathname_to_save = file.name
		else:
			pass

	# Funtion used to clear the text written on the text area
	def clear():
		textbox.delete("1.0", END)

	# Event to trigger when we close the TTS Dialog creator window
	def on_closing():
		if messagebox.askokcancel('Quit', 'Do you want to quit?'):
			win.destroy()
			global is_opened_1
			is_opened_1 = False

			global pathname_to_save
			pathname_to_save = None

	win = Toplevel(app)
	win.resizable(False, False)
	win.title('TTS - Create Dialog')
	win.geometry('750x400')
	win.protocol("WM_DELETE_WINDOW", on_closing)
	win.iconbitmap(resource_path('assets/icon.ico'))


	# textbox
	textbox = Text(win)
	textbox.pack()

	# scrollbar
	scroll = Scrollbar(win, command=textbox.yview)
	scroll.place(x=700, y=20, height=350)

	textbox['yscrollcommand'] = scroll.set

	# menu
	menu = Menu(win)
	filemenu = Menu(menu, tearoff=False)
	filemenu.add_command(label='Save File', command=save_file)
	filemenu.add_command(label='Save As', command=save_as)
	filemenu.add_command(label='Open File', command=open_file)

	menu.add_cascade(label='File', menu=filemenu)
	menu.add_command(label='Clear', command=clear)
	menu.add_command(label='Exit', command=exit_2)

	win['menu'] = menu



# Text to speech window
global filedata 
filedata = None

global tts
tts = None
def tts_converter_window():
	# Event to trigger when the window is closed
	def exit_3():
		if messagebox.askokcancel('Quit', 'Do you want to quit?'):
			win.destroy()
			global is_opened_2
			is_opened_2 = False

			global filedata 
			filedata = None

			global tts
			tts = None

	# Open the file selection dialog box to choose a .ttsdialog file to convert to MP3
	def open_tts_file():
		file = filedialog.askopenfile(
			mode='r',
			defaultextension='ttsdialog',
			filetypes = (
			        ('TTS Files', '*.ttsdialog'),
			        ('TTS Files', '*.TTSDIALOG')
			 ),
			initialdir=os.getcwd(),
			multiple=False
		)
		try:
			selected_file.set(file.name)
			global filedata
			filedata = file.read() # filedata is global to be used on another external functions
		except:
			pass

	# Thread of the text_to_seech function
	def text_to_speech_thread():
		if filedata != None: # We check if the filedata != None to activate the thread, also we check if the user has selected a language to use
			if selected_lang != None:
				t = Thread(target=text_to_speech, args=(selected_lang,))
				t.start()
				progressbar.start(5)
			else:
				messagebox.showinfo("TTS Converter", "Select a language first")
		else:
			messagebox.showinfo("TTS Converter", "Select a TTS file to convert")

	# text_to_speech function to convert the .ttsfile content to MP3 data
	def text_to_speech(ln):
		if filedata != None: # Filedata = the content of the .ttsfile, so, if filedata != None we convert that data to MP3 data
			try:
				global tts # TTS will contain the data to be stored on an MP3 file
				tts = gtts.tts.gTTS(text=filedata, lang=ln)
				sleep(5)
				progressbar.stop()
				messagebox.showinfo("TTS Converter", "Ready to export MP3 File")
				global selected_lang
				selected_lang = None
			except:
				sleep(5)
				progressbar.stop()
				messagebox.showerror("TTS Converter", "Error. Check your internet connection and try again")
		else:
			messagebox.showinfo("TTS Converter", "Select a TTS file to convert")

	# Thread to export the data to MP3 file
	def export_mp3_thread():
		if tts != None: # TTS is the object that contains the MP3 data, it was declared above
			t = Thread(target=export_mp3)
			t.start()
		else:
			messagebox.showinfo("TTS Converter", "Convert the TTS FIle to MP3 ")

	# Function to export the TTS data to an MP3 file
	def export_mp3():
		file = filedialog.asksaveasfile(
			mode='wb',
				defaultextension='mp3',
				filetypes = (
			        ('MP3 Files', '*.mp3'),
			        ('All files', '*.*')
			    )
			)
		if file != None:
			try:
				# Code explaination:
				# 1.We ask the user to save an mp3 file first
				# 2.If the user saves the file, we create also an mp3 file with an UUID as name to store the data to be written on the mp3 file that the user saved
				# 3.We write the data of the mp3 file with the UUID on the mp3 file that the user saved
				# 4.We delete the mp3 file that contained the initial data
				# 5. We tell the user that the file was exported (In case of not having any error during the proccess)
				progressbar.start(5)
				sleep(3)
				mp3_data_name = str(uuid4())+".mp3"
				tts.save(mp3_data_name)

				file.write(open(mp3_data_name, 'rb').read())
				os.remove(mp3_data_name)

				progressbar.stop()
				messagebox.showinfo("TTS Converter", "File exported succesfully")
			except:
				progressbar.stop()
				os.remove(mp3_data_name)
				messagebox.showerror("TTS Converter", "Error saving the file")
		else:
			pass

	# Show available langs
	def show_langs():
		# Event to trigger when the langs window is closed
		def on_closing_langs():
			langs_window.destroy()
			global is_opened_3
			is_opened_3 = False

		# Langs window
		langs_window = Toplevel(win)
		langs_window.resizable(False, False)
		langs_window.geometry('750x400')
		langs_window.title("Available Languages")
		langs_window.protocol("WM_DELETE_WINDOW", on_closing_langs)
		langs_window.iconbitmap(resource_path('assets/icon.ico'))

		# textbox
		textbox = Text(langs_window)
		textbox.pack()

		textbox.insert("0.0", langs_json)
		textbox['state'] = 'disabled'

		# scrollbar
		scroll = Scrollbar(langs_window, command=textbox.yview)
		scroll.place(x=700, y=20, height=350)

		textbox['yscrollcommand'] = scroll.set

	# Checks if langs window is opened
	def show_langs_check():
		global is_opened_3
		if is_opened_3 == False:
			is_opened_3 = True
			show_langs()
		else:
			pass

	# Checks if the language selection box is opened
	def select_language_check():
		global is_opened_4
		if is_opened_4 == False:
			is_opened_4 = True
			select_language()
		else:
			pass
			
	# Event to trigger when the TTS Converter window is closed
	def on_closing():
		if messagebox.askokcancel('Quit', 'Do you want to quit?'):
			win.destroy()
			global is_opened_2
			is_opened_2 = False

			global filedata 
			filedata = None

			global tts
			tts = None

	# Language selection window
	def select_language():
		# Event to trigger when is closed
		def on_closing_langs_select():
			select_language.destroy()
			global is_opened_4
			is_opened_4 = False

		# Event to trigger when we press "SELECT" button
		def on_select():
			global selected_lang
			selected_lang = None
			_langs = [] # We store the available langs to check if the user entry matches a valid language
			if len(entryVar.get()) > 0:
				for l in langs:
					_langs.append(l) # Appends languages to _langs list

				# Checks if we have a match
				for _ in _langs:
					if _ == entryVar.get():
						selected_lang = _
					else:
						pass

				# Checks if the language selected was valid or not
				if selected_lang != None:
					messagebox.showinfo("Language Selection", f"Language selected: {langs[selected_lang]}")
					on_closing_langs_select()
				else:
					messagebox.showerror("Language Selection", "Enter a valid language")

			else:
				messagebox.showinfo("Language Selection", "Enter a language")

		# Language selection window
		select_language = Toplevel()
		select_language.geometry('240x70')
		select_language.resizable(False, False)
		select_language.title('Language')
		select_language['bg'] = 'lightgray'
		select_language.protocol("WM_DELETE_WINDOW", on_closing_langs_select)
		select_language.iconbitmap(resource_path('assets/icon.ico'))

		# entry
		entryVar = StringVar()
		name = Entry(select_language, textvariable=entryVar)
		name.pack(fill=BOTH, pady=10)

		send_btn = Button(select_language, text='SELECT', command=on_select)
		send_btn.pack()



	# TTS Converter window
	win = Toplevel(app)
	win.resizable(False, False)
	win.title('TTS - Convert')
	win.geometry('550x100')
	win.protocol("WM_DELETE_WINDOW", on_closing)
	win.iconbitmap(resource_path('assets/icon.ico'))

	# menu
	menu = Menu(win)

	# filemenu
	filemenu = Menu(menu, tearoff=False)
	filemenu.add_command(label='Open TTS File', command=open_tts_file)
	filemenu.add_separator()
	filemenu.add_command(label='Export MP3 File', command=export_mp3_thread)

	# toolsmenu
	toolsmenu = Menu(menu, tearoff=False)
	toolsmenu.add_command(label='Convert TTS File to MP3', command=text_to_speech_thread)
	toolsmenu.add_command(label='Available Languages', command=show_langs_check)
	toolsmenu.add_command(label='Select Language', command=select_language_check)
	toolsmenu.add_separator()
	toolsmenu.add_command(label='Exit', command=exit_3)

	menu.add_cascade(label='File', menu=filemenu)
	menu.add_cascade(label='Tools', menu=toolsmenu)

	win['menu'] = menu

	# progressbar
	progressbar = ttk.Progressbar(win, mode='indeterminate', length=200)
	progressbar.pack(pady=10)

	# selected files label
	selected_file = StringVar() # We set a textvariable here to show the selected ttsfile path on the screen
	selected_file.set("SELECT FILES")
	selected = Label(win, textvariable=selected_file, font="bold").pack(pady=10)




# Check if the windows are opened
def text_to_speech_window_check():
	global is_opened_1
	if is_opened_1 == False:
		is_opened_1 = True
		text_to_speech_window()
	else:
		pass


def tts_converter_window_check():
	global is_opened_2
	if is_opened_2 == False:
		is_opened_2 = True
		tts_converter_window()
	else:
		pass



# Main window
app = Tk()
app.title('TTS')
app.geometry('400x150')
app.resizable(False, False)
app['bg'] = 'lightgray'
app.protocol("WM_DELETE_WINDOW", exit)
app.iconbitmap(resource_path('assets/icon.ico'))

# options

create_dialog_btn = Button(app, text='Create Dialog', command=text_to_speech_window_check)
create_dialog_btn.pack(fill=BOTH, pady=10)

tts_btn = Button(app, text='Text To Speech', command=tts_converter_window_check)
tts_btn.pack(fill=BOTH, pady=0)

exit_btn = Button(app, text='Exit', width=20, command=exit)
exit_btn.pack(pady=10)



if __name__=="__main__":
	app.mainloop()