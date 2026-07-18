import tkinter as tk
from tkinter import ttk, messagebox
import re
from cryptography.fernet import Fernet
import random
import string

# Generate/Load Encryption Key
try:
    with open("secret.key", "rb") as key_file:
        key = key_file.read()
except FileNotFoundError:
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)

cipher = Fernet(key)


# Password Strength Function
def check_strength(*args):
    password = password_var.get()
    strength = 0
    remarks = ""
    color = "#3C9DE7"

    if len(password) == 0:
        strength_label.config(text="")
        return

    if len(password) >= 8 & len(password)<= 23:
        strength += 1
    if re.search("[a-z]", password) and re.search("[A-Z]", password):
        strength += 1
    if re.search("[0-9]", password):
        strength += 1
    if re.search("[!@#$%^&*(),.?\":{}|<> ]", password):
        strength += 1

    if strength == 1:
        remarks = "Weak"
        color = "#E74C3C"
    elif strength == 2:
        remarks = "Fair"
        color = "#F1C40F"
    elif strength == 3:
        remarks = "Good"
        color = "#3498DB"
    elif strength == 4:
        remarks = "Strong"
        color = "#2ECC71"

    strength_label.config(text="Strength : " + remarks, fg=color)

# Save Email and Encrypted Password
def save_data():
    email = email_var.get()
    password = password_var.get()

    if not email or not password:
        messagebox.showerror("Error", "Fill all fields")
        return

    encrypted = cipher.encrypt(password.encode()).decode()

    with open("passwords.txt", "a") as file:
        file.write(email + "|" + encrypted + "\n")

    # Show details in terminal (backend)
    print("\n========== Encryption Details ==========")
    print("Email              :", email)
    print("Original Password  :", password)
    print("Encrypted Password :", encrypted)
    print("Decrypted Password :", cipher.decrypt(encrypted.encode()).decode())
    print("Encryption Key     :", key.decode())
    print("=========================================\n")

    messagebox.showinfo("Success", "Password Saved Successfully")

    email_var.set("")
    password_var.set("")

    if email == "" or password == "":
        messagebox.showerror("Error", "Please fill all fields")
        return

    encrypted_password = cipher.encrypt(password.encode()).decode()

    with open("passwords.txt", "a") as file:
        file.write("email" + email + "\n" +"encrypt" + encrypted_password + "\n")

    messagebox.showinfo("Success", "Encrypted Password Saved")

    email_var.set("")
    password_var.set("")
    
# for suggestion of password
def generate_password():
    characters = string.ascii_letters + string.digits + "@#$%&*"
    password = ""

    for i in range(10):
        password += random.choice(characters)

    password_var.set(password)


# Show Decrypted Password
def decrypt_password():
    try:
        with open("passwords.txt", "r") as file:
            lines = file.readlines()

        if not lines:
            messagebox.showinfo("Info", "No saved passwords.")
            return

        last = lines[-1]
        email, encrypted = last.strip().split("|")

        decrypted = cipher.decrypt(encrypted.encode()).decode()

        messagebox.showinfo(
            "Last Saved",
            f"Email : {email}\nPassword : {decrypted}"
        )

    except Exception:
        messagebox.showerror("Error", "Unable to decrypt password.")


# GUI
root = tk.Tk()
root.title("ShieldPass Analyzer")
root.geometry("420x330")
root.configure(padx=20, pady=20)

title = tk.Label(
    root,
    text="Password Strength Analyzer",
    font=("Helvetica", 14, "bold")
)
title.pack(pady=10)

# Email
email_var = tk.StringVar()

tk.Label(root, text="Email").pack()

email_entry = tk.Entry(root, textvariable=email_var, width=35)
email_entry.pack(pady=5)

# Password
password_var = tk.StringVar()
password_var.trace_add("write", check_strength)

tk.Label(root, text="Password").pack()

entry = tk.Entry(
    root,
    textvariable=password_var,
    show="*",
    width=35
)
entry.pack(pady=5)

strength_label = tk.Label(root, text="", font=("Helvetica", 11, "bold"))
strength_label.pack()

def toggle_password():
    if entry.cget("show") == "*":
        entry.config(show="")
        show_btn.config(text="Hide")
    else:
        entry.config(show="*")
        show_btn.config(text="Show")
        
show_btn = tk.Button(root, text="Show", command=toggle_password)
show_btn.pack(pady=5)

# Buttons
save_btn = tk.Button(
    root,
    text="Save",
    bg="#2ECC71",
    fg="white",
    command=save_data
)
save_btn.pack(pady=10)

tk.Button(root,
        text="Generate Password",
        command=generate_password).pack(pady=5)

root.mainloop()