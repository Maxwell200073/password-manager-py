from json import JSONDecodeError
from tkinter import *
from tkinter import ttk, messagebox
import string
import random
import pyperclip
import json
# ---------------------------- CONSTANTS & VARIABLES ------------------------------- #

WIDTH = 450
HEIGHT = 360
PADDING = 50
PADDING_Y = 40
FONT = ('Open Sans', 10)


# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def generate_password():
    """Returns a 12 character random password"""
    new_password = ''.join(random.sample(string.ascii_letters + string.digits + string.punctuation, 12))
    password_text.delete(0, END)
    password_text.insert(0, new_password)
    pyperclip.copy(new_password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def write_json_to_file(data_to_save):
    """Writes argument passed to data.json"""
    with open('./data.json', 'w') as data_file:
        json.dump(data_to_save, data_file, indent=4)


def save_password():

    site = website_text.get()
    user_name = username_text.get()
    user_pass = password_text.get()

    new_data = {
        site: {
            'email': user_name,
            'password': user_pass
        }
    }

    # Validate fields are all filled in
    if len(site) > 0 and len(user_name) > 0 and len(user_pass) > 0:

        # Verify user wants to continue with choice
        if messagebox.askyesno(title="Are you sure?",
                               message=f'Are you sure you would like to use {user_pass} for {site}?'):

            try:
                with open('./data.json', 'r') as data_file:
                    # Reading old data
                    data = json.load(data_file)
                    # Updating new data
                    data.update(new_data)

            except JSONDecodeError:
                write_json_to_file(new_data)

            except FileNotFoundError:
                write_json_to_file(new_data)

            else:
                write_json_to_file(data)

            finally:
                # Clears website and password fields
                website_text.delete(0, END)
                password_text.delete(0, END)
                # Puts focus back on Website field
                website_text.focus()

    else:
        messagebox.showerror(title='Oops, Something was omitted', message='Please make sure all fields are filled in!')

# ---------------------------- Search Passwords ----------------------- #


def search_passwords():

    site = website_text.get()
    found = False

    try:
        with open('./data.json') as data_file:
            data = json.load(data_file)

    except FileNotFoundError:
        messagebox.showerror(title='File not found', message='File data.json was not found.')

    except JSONDecodeError:
        messagebox.showerror(title='File not found', message='File data.json was not found.')

    else:
        for key, value in data.items():
            if key == site:
                found = True
                pyperclip.copy(value['password'])
                messagebox.showinfo(title=f'{site}', message=f'Email: {value["email"]}\nPassword: {value["password"]}')

        if not found:
            messagebox.showerror(title='Something went wrong',
                                 message=f'Sorry, {site} was not found. Please check spelling and try again.')


# ---------------------------- UI SETUP ------------------------------- #

# Main Window
root = Tk()
root.title('Password Manager')
root.config(padx=PADDING, pady=PADDING_Y)
root.iconbitmap('logo.ico')


# Images
bgImg = PhotoImage(file='logo.png')


# Style
style = ttk.Style()
# print(style.theme_names())
style.theme_use('vista')


# Labels
bg = Label(root, image=bgImg)
bg.grid(row=0, column=1)

website = Label(text='Website:', font=FONT)
website.grid(row=1, column=0)

username = Label(text='Email/Username:', font=FONT)
username.grid(row=2, column=0)

password = Label(text='Password:', font=FONT)
password.grid(row=3, column=0)


# Entries
website_text = ttk.Entry(width=23, font=FONT)
website_text.grid(row=1, column=1, sticky='EW')
website_text.focus()

username_text = ttk.Entry(width=35, font=FONT)
username_text.grid(row=2, column=1, columnspan=2, sticky='EW')
username_text.insert(0, 'SampleEmail@outlook.com')

password_text = ttk.Entry(width=23, font=FONT)
password_text.grid(row=3, column=1, sticky='EW')


# Buttons
search_button = ttk.Button(text='Search', command=search_passwords)
search_button.grid(row=1, column=2)

generate_password = ttk.Button(text='Generate', command=generate_password)
generate_password.grid(row=3, column=2, sticky='EW')

add_button = ttk.Button(text='Add', width=36, command=save_password)
add_button.grid(row=4, column=1, columnspan=2, sticky='EW')

root.mainloop()
