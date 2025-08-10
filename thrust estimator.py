import tkinter as tk
from tkinter import font, messagebox
import math
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Constants
G0 = 9.81  # Gravity m/s^2

# App Window
root = tk.Tk()
root.title("🚀 Rocket Δv & Thrust Estimator")
root.geometry("450x600")
root.resizable(True, False)
root.configure(bg="#121212")

# Fonts & Colors
title_font = font.Font(family="Consolas", size=20, weight="bold")
label_font = font.Font(family="Consolas", size=12)
entry_font = font.Font(family="Consolas", size=12)
button_font = font.Font(family="Consolas", size=12, weight="bold")

bg_color = "#121212"
fg_color = "#00FFDD"
entry_bg = "#222222"
btn_bg = "#005577"
btn_fg = "#FFFFFF"

# Variables for entries and results
isp_var = tk.StringVar()
fuel_var = tk.StringVar()
dry_var = tk.StringVar()
massflow_var = tk.StringVar()

delta_v_var = tk.StringVar(value="Δv: - m/s")
thrust_var = tk.StringVar(value="Thrust: - N")

# Functions

def calculate_delta_v(isp, fuel_mass, dry_mass):
    m0 = fuel_mass + dry_mass
    mf = dry_mass
    if m0 <= mf:
        raise ValueError("Total mass must be greater than dry mass.")
    return isp * G0 * math.log(m0 / mf)

def calculate_thrust(isp, mass_flow_rate):
    return mass_flow_rate * G0 * isp

def validate_float(value, name):
    try:
        val = float(value)
        if val <= 0:
            raise ValueError
        return val
    except:
        raise ValueError(f"Invalid input for {name}. Please enter a positive number.")

def on_calculate():
    try:
        isp = validate_float(isp_var.get(), "ISP")
        fuel = validate_float(fuel_var.get(), "Fuel Mass")
        dry = validate_float(dry_var.get(), "Dry Mass")
        mass_flow = validate_float(massflow_var.get(), "Mass Flow Rate")

        delta_v = calculate_delta_v(isp, fuel, dry)
        thrust = calculate_thrust(isp, mass_flow)

        delta_v_var.set(f"Δv: {delta_v:.2f} m/s")
        thrust_var.set(f"Thrust: {thrust:.2f} N")
    except ValueError as e:
        messagebox.showerror("Input Error", str(e))

def plot_graph():
    try:
        isp = validate_float(isp_var.get(), "ISP")
        dry = validate_float(dry_var.get(), "Dry Mass")

        fuel_masses = [x for x in range(100, int(float(fuel_var.get())*1.5), 100)]
        delta_vs = []
        for fm in fuel_masses:
            try:
                dv = calculate_delta_v(isp, fm, dry)
                delta_vs.append(dv)
            except:
                delta_vs.append(0)

        fig, ax = plt.subplots(figsize=(6,4))
        ax.plot(fuel_masses, delta_vs, color="#00FFDD", marker='o')
        ax.set_title("Delta-V vs Fuel Mass")
        ax.set_xlabel("Fuel Mass (kg)")
        ax.set_ylabel("Delta-V (m/s)")
        ax.grid(True, linestyle='--', alpha=0.6)

        # Embed plot in Tkinter window
        plot_window = tk.Toplevel(root)
        plot_window.title("Delta-V vs Fuel Mass Graph")
        plot_window.geometry("650x450")
        plot_window.configure(bg=bg_color)

        canvas = FigureCanvasTkAgg(fig, master=plot_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)

    except ValueError as e:
        messagebox.showerror("Input Error", str(e))
    except Exception as e:
        messagebox.showerror("Error", "Failed to generate graph.")

# Layout

title_label = tk.Label(root, text="🚀 Rocket Δv & Thrust Estimator", font=title_font, fg=fg_color, bg=bg_color)
title_label.pack(pady=15)

# Input Frame
input_frame = tk.LabelFrame(root, text="Input Parameters", font=label_font, fg=fg_color, bg=bg_color, bd=2, relief=tk.GROOVE, labelanchor="n")
input_frame.pack(padx=20, pady=10, fill="x")

def create_labeled_entry(parent, text, textvariable):
    frame = tk.Frame(parent, bg=bg_color)
    label = tk.Label(frame, text=text, font=label_font, fg=fg_color, bg=bg_color, width=15, anchor="w")
    entry = tk.Entry(frame, textvariable=textvariable, font=entry_font, bg=entry_bg, fg=fg_color, insertbackground=fg_color, width=20)
    frame.pack(fill="x", pady=5)
    label.pack(side="left")
    entry.pack(side="left", padx=5)
    return entry

isp_entry = create_labeled_entry(input_frame, "Specific Impulse (s):", isp_var)
fuel_entry = create_labeled_entry(input_frame, "Fuel Mass (kg):", fuel_var)
dry_entry = create_labeled_entry(input_frame, "Dry Mass (kg):", dry_var)
massflow_entry = create_labeled_entry(input_frame, "Mass Flow Rate (kg/s):", massflow_var)

# Set default values
isp_var.set("300")
fuel_var.set("5000")
dry_var.set("1000")
massflow_var.set("20")

# Buttons Frame
button_frame = tk.Frame(root, bg=bg_color)
button_frame.pack(pady=15)

calc_button = tk.Button(button_frame, text="Calculate", font=button_font, bg=btn_bg, fg=btn_fg, relief="raised", command=on_calculate, width=12)
calc_button.grid(row=0, column=0, padx=10)

graph_button = tk.Button(button_frame, text="Show Graph", font=button_font, bg=btn_bg, fg=btn_fg, relief="raised", command=plot_graph, width=12)
graph_button.grid(row=0, column=1, padx=10)

# Results Frame
result_frame = tk.LabelFrame(root, text="Results", font=label_font, fg=fg_color, bg=bg_color, bd=2, relief=tk.GROOVE, labelanchor="n")
result_frame.pack(padx=20, pady=10, fill="x")

delta_label = tk.Label(result_frame, textvariable=delta_v_var, font=("Consolas", 16), fg=fg_color, bg=bg_color)
delta_label.pack(pady=5)

thrust_label = tk.Label(result_frame, textvariable=thrust_var, font=("Consolas", 16), fg=fg_color, bg=bg_color)
thrust_label.pack(pady=5)

# Footer
footer = tk.Label(root, text="Designed by DM | Powered by Python", font=("Consolas", 10), fg="#444", bg=bg_color)
footer.pack(side="bottom", pady=10)

root.mainloop()
