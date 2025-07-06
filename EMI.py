import tkinter as tk
from tkinter import messagebox
import pandas as pd
import os
from datetime import datetime

def calculate_emi():
    try:
        # Step 1: Get values from GUI inputs
        P = float(entry_principal.get())
        annual_rate = float(entry_rate.get())
        n = int(entry_months.get())

        # Step 2: EMI formula
        r = annual_rate / 12 / 100
        EMI = round(P * r * (1 + r) ** n / ((1 + r) ** n - 1), 2)

        # Step 3: Generate amortization schedule
        balance = P
        schedule = []

        for month in range(1, n + 1):
            interest = round(balance * r, 2)
            principal = round(EMI - interest, 2)
            balance = round(balance - principal, 2)
            schedule.append({
                "Month": month,
                "EMI": EMI,
                "Principal Paid": principal,
                "Interest Paid": interest,
                "Remaining Balance": max(balance, 0)
            })

        # Step 4: Create DataFrame and save with unique filename
        df = pd.DataFrame(schedule)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"EMI_Schedule_{int(P)}_{annual_rate}percent_{n}months_{timestamp}.csv"

        # Save in same folder as script
        current_dir = os.path.dirname(os.path.abspath(__file__))
        full_path = os.path.join(current_dir, filename)
        df.to_csv(full_path, index=False)

        # Step 5: Notify user
        print(f"✅ File saved at: {full_path}")
        messagebox.showinfo("Success", f"EMI: ₹{EMI}\n\nSchedule saved at:\n{full_path}")

    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numeric values!")
    except Exception as e:
        messagebox.showerror("Unexpected Error", f"Error: {str(e)}")
        print("⚠️ Error:", str(e))

# === GUI Setup ===
root = tk.Tk()
root.title("EMI Calculator")

# Input fields
tk.Label(root, text="Principal Amount (₹):").grid(row=0, column=0, sticky='e')
entry_principal = tk.Entry(root)
entry_principal.grid(row=0, column=1)

tk.Label(root, text="Annual Interest Rate (%):").grid(row=1, column=0, sticky='e')
entry_rate = tk.Entry(root)
entry_rate.grid(row=1, column=1)

tk.Label(root, text="Loan Duration (Months):").grid(row=2, column=0, sticky='e')
entry_months = tk.Entry(root)
entry_months.grid(row=2, column=1)

# Button
tk.Button(root, text="Calculate EMI", command=calculate_emi).grid(row=3, columnspan=2, pady=10)

root.mainloop()
