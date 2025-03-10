import requests
import tkinter as tk
from tkinter import ttk, messagebox
from ttkwidgets.autocomplete import AutocompleteCombobox
import matplotlib.pyplot as plt

# API Key & Base URL
API_KEY = "ca43e2d2918ca3f85e808a85"
BASE_URL = "https://v6.exchangerate-api.com/v6/"

# Fetch available currency codes dynamically with country names
def fetch_currencies():
    url = f"{BASE_URL}{API_KEY}/codes"
    response = requests.get(url)
    data = response.json()

    if response.status_code != 200:
        messagebox.showerror("Error", "Failed to fetch currency codes!")
        return {}

    return {code[0]: code[1] for code in data["supported_codes"]}  # {'USD': 'United States Dollar', ...}

# Fetch exchange rate
def get_exchange_rate(base_currency, target_currency):
    url = f"{BASE_URL}{API_KEY}/latest/{base_currency}"
    response = requests.get(url)
    data = response.json()

    if response.status_code != 200:
        messagebox.showerror("Error", "Failed to fetch exchange rates!")
        return None

    rates = data.get("conversion_rates", {})
    return rates.get(target_currency, None), rates

# Convert currency
def convert_currency():
    base_currency = base_currency_var.get().split(" - ")[0]
    target_currency = target_currency_var.get().split(" - ")[0]

    try:
        amount = float(amount_entry.get())
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid amount.")
        return

    rate, _ = get_exchange_rate(base_currency, target_currency)
    
    if rate:
        converted_amount = amount * rate
        result_label.config(text=f"{amount} {base_currency} = {converted_amount:.2f} {target_currency}")
    else:
        messagebox.showerror("Error", f"Conversion rate not found for {base_currency} to {target_currency}.")

# Show exchange rate graph
def show_exchange_graph():
    base_currency = base_currency_var.get().split(" - ")[0]
    _, rates = get_exchange_rate(base_currency, target_currency_var.get().split(" - ")[0])

    if not rates:
        return
    
    top_10_currencies = sorted(rates.items(), key=lambda x: x[1], reverse=True)[:10]

    currencies = [item[0] for item in top_10_currencies]
    values = [item[1] for item in top_10_currencies]

    plt.figure(figsize=(10, 5))
    plt.barh(currencies, values, color="#3498DB")
    plt.xlabel("Exchange Rate")
    plt.ylabel("Currency")
    plt.title(f"Exchange Rates for {base_currency}")
    plt.gca().invert_yaxis()
    plt.show()

# GUI Setup
root = tk.Tk()
root.title("Currency Converter")
root.geometry("500x500")
root.configure(bg="#2C3E50")  # Dark background
root.resizable(False, False)

# Fetch currency list dynamically
CURRENCY_DICT = fetch_currencies()
CURRENCIES = [f"{code} - {name}" for code, name in CURRENCY_DICT.items()]

# Styling
style = ttk.Style()
style.theme_use("clam")
style.configure("TLabel", foreground="white", background="#2C3E50", font=("Arial", 11))
style.configure("TButton", foreground="white", background="#3498DB", font=("Arial", 10, "bold"), padding=5)
style.configure("TCombobox", padding=5)

# Title
tk.Label(root, text="Currency Converter", font=("Arial", 16, "bold"), fg="white", bg="#2C3E50").pack(pady=10)

# Base Currency
ttk.Label(root, text="Base Currency:").pack(pady=2)
base_currency_var = tk.StringVar()
base_currency_dropdown = AutocompleteCombobox(root, textvariable=base_currency_var, completevalues=CURRENCIES, width=40)
base_currency_dropdown.pack()
base_currency_dropdown.set(CURRENCIES[0])

# Target Currency
ttk.Label(root, text="Target Currency:").pack(pady=2)
target_currency_var = tk.StringVar()
target_currency_dropdown = AutocompleteCombobox(root, textvariable=target_currency_var, completevalues=CURRENCIES, width=40)
target_currency_dropdown.pack()
target_currency_dropdown.set(CURRENCIES[1])

# Amount Entry
ttk.Label(root, text="Amount:").pack(pady=5)
amount_entry = ttk.Entry(root)
amount_entry.pack()

# Convert Button
convert_button = ttk.Button(root, text="Convert", command=convert_currency)
convert_button.pack(pady=10)

# Show Exchange Rates Graph Button
graph_button = ttk.Button(root, text="Show Exchange Rate Graph", command=show_exchange_graph)
graph_button.pack(pady=5)

# Result Label
result_label = tk.Label(root, text="", font=("Arial", 12, "bold"), fg="#F1C40F", bg="#2C3E50")
result_label.pack(pady=10)

# Run App
root.mainloop()
