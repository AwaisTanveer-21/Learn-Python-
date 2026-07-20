import tkinter as tk
from tkinter import filedialog, messagebox

import qrcode
from PIL import Image, ImageTk
import cv2
from pyzbar.pyzbar import decode


# ==============================
# Main Window
# ==============================

root = tk.Tk()
root.title("QR Code Generator & Scanner")
root.geometry("650x700")
root.resizable(False, False)
root.configure(bg="#EAF6F6")


# ==============================
# Variables
# ==============================

text_var = tk.StringVar()


# ==============================
# Generate QR Code
# ==============================

def generate_qr():

    text = text_var.get().strip()

    if text == "":
        messagebox.showerror("Error", "Please Enter Text")
        return

    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=5
    )

    qr.add_data(text)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black",
                        back_color="white")

    img.save("Generated_QR.png")

    image = Image.open("Generated_QR.png")
    image = image.resize((280,280))

    photo = ImageTk.PhotoImage(image)

    qr_label.config(image=photo)
    qr_label.image = photo

    messagebox.showinfo(
        "Success",
        "QR Code Generated Successfully!\nSaved as Generated_QR.png"
    )


# ==============================
# Save QR
# ==============================

def save_qr():

    try:

        file = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG Image","*.png")]
        )

        if file == "":
            return

        img = Image.open("Generated_QR.png")
        img.save(file)

        messagebox.showinfo(
            "Saved",
            "QR Code Saved Successfully."
        )

    except:
        messagebox.showerror(
            "Error",
            "Generate QR First."
        )


# ==============================
# Read QR
# ==============================

def read_qr():

    file = filedialog.askopenfilename(
        filetypes=[
            ("PNG","*.png"),
            ("JPEG","*.jpg"),
            ("All Files","*.*")
        ]
    )

    if file == "":
        return

    image = cv2.imread(file)

    decoded = decode(image)

    if len(decoded) == 0:

        messagebox.showerror(
            "Error",
            "No QR Code Found."
        )

        return

    data = decoded[0].data.decode("utf-8")

    result_box.delete("1.0", tk.END)
    result_box.insert(tk.END, data)

    image = Image.open(file)
    image = image.resize((280,280))

    photo = ImageTk.PhotoImage(image)

    qr_label.config(image=photo)
    qr_label.image = photo


# ==============================
# Clear
# ==============================

def clear_all():

    text_var.set("")

    result_box.delete("1.0", tk.END)

    qr_label.config(image="")


# ==============================
# Heading
# ==============================

title = tk.Label(
    root,
    text="QR Code Generator & Scanner",
    font=("Arial",20,"bold"),
    bg="#EAF6F6",
    fg="#222"
)

title.pack(pady=15)


# ==============================
# Input
# ==============================

tk.Label(
    root,
    text="Enter Text",
    font=("Arial",12,"bold"),
    bg="#EAF6F6"
).pack()

entry = tk.Entry(
    root,
    textvariable=text_var,
    font=("Arial",14),
    width=40
)

entry.pack(pady=10)


# ==============================
# Buttons
# ==============================

frame = tk.Frame(root,bg="#EAF6F6")
frame.pack()

tk.Button(
    frame,
    text="Generate QR",
    width=15,
    bg="#27AE60",
    fg="white",
    font=("Arial",11,"bold"),
    command=generate_qr
).grid(row=0,column=0,padx=5,pady=5)

tk.Button(
    frame,
    text="Save QR",
    width=15,
    bg="#3498DB",
    fg="white",
    font=("Arial",11,"bold"),
    command=save_qr
).grid(row=0,column=1,padx=5,pady=5)

tk.Button(
    frame,
    text="Read QR",
    width=15,
    bg="#8E44AD",
    fg="white",
    font=("Arial",11,"bold"),
    command=read_qr
).grid(row=0,column=2,padx=5,pady=5)

tk.Button(
    frame,
    text="Clear",
    width=15,
    bg="#E74C3C",
    fg="white",
    font=("Arial",11,"bold"),
    command=clear_all
).grid(row=0,column=3,padx=5,pady=5)


# ==============================
# QR Image
# ==============================

qr_label = tk.Label(root,bg="#EAF6F6")
qr_label.pack(pady=20)


# ==============================
# Result
# ==============================

tk.Label(
    root,
    text="Decoded Text",
    font=("Arial",12,"bold"),
    bg="#EAF6F6"
).pack()

result_box = tk.Text(
    root,
    height=8,
    width=55,
    font=("Arial",12)
)

result_box.pack(pady=10)


# ==============================
# Footer
# ==============================

footer = tk.Label(
    root,
    text="Python Tkinter QR Generator & Scanner",
    bg="#EAF6F6",
    fg="gray"
)

footer.pack(pady=10)


root.mainloop()