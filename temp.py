import customtkinter as ctk
from tkinter import messagebox


# ---------- Conversion functions ----------

def celsius_to_fahrenheit(c):
    return (c * 9 / 5) + 32


def celsius_to_kelvin(c):
    return c + 273.15


def fahrenheit_to_celsius(f):
    return (f - 32) * 5 / 9


def kelvin_to_celsius(k):
    return k - 273.15


def to_celsius(value, unit):
    if unit == "Celsius":
        return value
    elif unit == "Fahrenheit":
        return fahrenheit_to_celsius(value)
    else:
        return kelvin_to_celsius(value)


def from_celsius(celsius, unit):
    if unit == "Celsius":
        return celsius
    elif unit == "Fahrenheit":
        return celsius_to_fahrenheit(celsius)
    else:
        return celsius_to_kelvin(celsius)


# ---------- Colors ----------

BG = "#161a30"
CARD = "#1f2444"
FIELD = "#2b3159"
ACCENT = "#3ddad7"
ACCENT_DARK = "#28b8b5"
TEXT = "#f2f4ff"
SUBTEXT = "#9aa1c9"


# ---------- Custom Dropdown ----------

class CustomDropdown(ctk.CTkFrame):

    def __init__(self, parent, values):
        super().__init__(
            parent,
            width=180,
            height=40,
            fg_color=FIELD,
            corner_radius=15,
            cursor="hand2"
        )

        self.menu = None          # holds the single popup Toplevel (or None if closed)
        self.values = values
        self.current_value = values[0]

        self.text = ctk.CTkLabel(
            self,
            text=self.current_value,
            font=("Segoe UI", 12),
            text_color=TEXT,
            fg_color=FIELD,
            cursor="hand2"
        )
        self.text.place(relx=0.05, rely=0.5, anchor="w")

        self.arrow = ctk.CTkLabel(
            self,
            text="˅",
            font=("Segoe UI", 18, "bold"),
            text_color=ACCENT,
            fg_color=FIELD,
            cursor="hand2"
        )
        self.arrow.place(relx=0.92, rely=0.5, anchor="center")

        self.bind("<Button-1>", self.toggle_menu)
        self.text.bind("<Button-1>", self.toggle_menu)
        self.arrow.bind("<Button-1>", self.toggle_menu)

        # only arrow hover
        self.arrow.bind("<Enter>", lambda e: self.arrow.configure(text_color=ACCENT_DARK))
        self.arrow.bind("<Leave>", lambda e: self.arrow.configure(text_color=ACCENT))

    def toggle_menu(self, event=None):
        """Open the dropdown if closed, close it if already open (click-to-toggle)."""
        if self.menu is not None:
            self.close_menu()
        else:
            self.open_menu()

    def open_menu(self):
        item_height = 40
        self.menu = ctk.CTkToplevel(self)
        self.menu.geometry(
            f"180x{len(self.values) * item_height}"
            f"+{self.winfo_rootx()}+{self.winfo_rooty() + 45}"
        )
        self.menu.overrideredirect(True)
        self.menu.configure(fg_color=CARD)

        for item in self.values:
            option = ctk.CTkLabel(
                self.menu,
                text=item,
                height=item_height,
                font=("Segoe UI", 12),
                text_color=TEXT,
                fg_color=CARD,
                cursor="hand2"
            )
            option.pack(fill="x")
            option.bind("<Button-1>", lambda e, x=item: self.select(x))
            option.bind("<Enter>", lambda e, o=option: o.configure(fg_color=FIELD))
            option.bind("<Leave>", lambda e, o=option: o.configure(fg_color=CARD))

    def close_menu(self):
        if self.menu is not None:
            self.menu.destroy()
            self.menu = None

    def select(self, value):
        self.current_value = value
        self.text.configure(text=value)
        self.close_menu()

    def get(self):
        return self.current_value

    def set(self, value):
        self.current_value = value
        self.text.configure(text=value)


# ---------- Actions ----------

def convert():
    try:
        value = float(entry.get())
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid number.")
        return

    from_unit = from_combo.get()
    celsius = to_celsius(value, from_unit)

    c = celsius
    f = celsius_to_fahrenheit(celsius)
    k = celsius_to_kelvin(celsius)

    celsius_label.configure(text=f"Celsius:     {c:.2f} °C")
    fahrenheit_label.configure(text=f"Fahrenheit:  {f:.2f} °F")
    kelvin_label.configure(text=f"Kelvin:      {k:.2f} K")


# ---------- Window ----------

ctk.set_appearance_mode("dark")

window = ctk.CTk()
window.title("Temperature Converter")
window.geometry("880x540")
window.configure(fg_color=BG)
window.resizable(False, False)

units = ["Celsius", "Fahrenheit", "Kelvin"]


# ---------- Card ----------

card = ctk.CTkFrame(
    window,
    width=600,
    height=500,
    corner_radius=25,
    fg_color=CARD
)
card.pack_propagate(False)
card.place(relx=0.5, rely=0.5, anchor="center")


# ---------- Title ----------

ctk.CTkLabel(
    card,
    text="🌡 Temperature Converter",
    font=("Segoe UI", 22, "bold"),
    text_color=TEXT
).pack(pady=(30, 5))

ctk.CTkLabel(
    card,
    text="Convert between Celsius, Fahrenheit & Kelvin",
    font=("Segoe UI", 11),
    text_color=SUBTEXT
).pack(pady=(0, 15))


# ---------- Entry ----------

entry = ctk.CTkEntry(
    card,
    width=300,
    height=55,
    font=("Segoe UI", 18),
    justify="center",
    fg_color=FIELD,
    text_color=TEXT,
    corner_radius=20
)
entry.pack(pady=(0, 15))


# ---------- Dropdown Row ----------

row = ctk.CTkFrame(card, fg_color=CARD)
row.pack(pady=5)

from_box = ctk.CTkFrame(row, fg_color=CARD)
from_box.pack()

ctk.CTkLabel(from_box, text="From", text_color=SUBTEXT).pack(anchor="w")

from_combo = CustomDropdown(from_box, units)
from_combo.set("Celsius")
from_combo.pack(pady=5)


# ---------- Convert Button ----------

ctk.CTkButton(
    card,
    text="Convert",
    width=300,
    height=50,
    corner_radius=25,
    font=("Segoe UI", 14, "bold"),
    fg_color=ACCENT,
    text_color="#0f1330",
    hover_color=ACCENT_DARK,
    command=convert
).pack(pady=20)


# ---------- Results (all three units) ----------

results_box = ctk.CTkFrame(card, fg_color=FIELD, corner_radius=20)
results_box.pack(pady=(0, 10), ipady=15, padx=40, fill="x")

celsius_label = ctk.CTkLabel(
    results_box, text="Celsius:", font=("Consolas", 15, "bold"), text_color=ACCENT
)
celsius_label.pack(pady=4)

fahrenheit_label = ctk.CTkLabel(
    results_box, text="Fahrenheit:", font=("Consolas", 15, "bold"), text_color=ACCENT
)
fahrenheit_label.pack(pady=4)

kelvin_label = ctk.CTkLabel(
    results_box, text="Kelvin:", font=("Consolas", 15, "bold"), text_color=ACCENT
)
kelvin_label.pack(pady=4)


window.mainloop()