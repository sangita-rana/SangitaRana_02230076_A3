import tkinter as tk
from tkinter import messagebox, simpledialog
import random

class BankAccount:
    def __init__(self, account_number, name, passcode, balance=0):
        self.account_number = account_number
        self.name = name
        self.passcode = passcode
        self.balance = balance
        self.transactions = []

    def deposit(self, amount):
        if amount <= 0: raise ValueError("Amount must be positive")
        self.balance += amount
        self.transactions.append(f"Deposited Nu.{amount:.2f}")

    def withdraw(self, amount):
        if amount <= 0: raise ValueError("Amount must be positive")
        if amount > self.balance: raise ValueError("Not enough balance")
        self.balance -= amount
        self.transactions.append(f"Withdrew Nu.{amount:.2f}")

    def transfer(self, amount, target):
        if amount <= 0 or target == self: raise ValueError("Invalid transfer")
        if amount > self.balance: raise ValueError("Not enough balance")
        self.balance -= amount
        target.balance += amount
        self.transactions.append(f"Sent Nu.{amount:.2f} to {target.name}")
        target.transactions.append(f"Received Nu.{amount:.2f} from {self.name}")

    def mobile_topup(self, amount, number):
        if amount <= 0: raise ValueError("Amount must be positive")
        if amount > self.balance: raise ValueError("Not enough balance")
        self.balance -= amount
        self.transactions.append(f"Mobile top-up Nu.{amount:.2f} to {number}")

class BankApp:
    def __init__(self, master):
        self.master = master
        # New color scheme
        self.bg_color = "#222831"         # dark background
        self.primary_color = "#1d6ed8"    # blue
        self.secondary_color = "#393e46"  # dark gray
        self.accent_color = "#f8b400"     # yellow accent

        master.title("Bank - Digital Banking")
        master.geometry("400x500")
        master.configure(bg=self.bg_color)

        tk.Label(
            master, text="Bank", font=("Helvetica", 20, "bold"),
            bg=self.primary_color, fg="white"
        ).pack(fill=tk.X, pady=10)
        ctrl = tk.Frame(master, bg=self.bg_color); ctrl.pack(pady=10)
        tk.Button(
            ctrl, text="Open Account", command=self.open_account,
            bg=self.accent_color, fg="black"
        ).pack(side=tk.LEFT, padx=5)
        tk.Button(
            ctrl, text="Login", command=self.login,
            bg=self.accent_color, fg="black"
        ).pack(side=tk.LEFT, padx=5)

        self.transaction_frame = tk.Frame(master, bg=self.bg_color)
        self.transaction_frame.pack(pady=10)
        self.buttons = {}
        for text, cmd in [
            ("Deposit", self.deposit), ("Withdraw", self.withdraw),
            ("Send Money", self.transfer), ("Mobile Top-Up", self.mobile_topup),
            ("Close Account", self.close_account)
        ]:
            btn = tk.Button(
                self.transaction_frame, text=text, command=cmd,
                state=tk.DISABLED, bg=self.primary_color, fg="white", activebackground=self.secondary_color
            )
            btn.pack(fill=tk.X, pady=2)
            self.buttons[text] = btn

        self.balance_label = tk.Label(
            master, text="No account selected", font=("Helvetica", 12), bg=self.bg_color, fg="white"
        )
        self.balance_label.pack(pady=10)
        txn_frame = tk.LabelFrame(
            master, text="Transaction History", bg=self.bg_color, fg="white"
        )
        txn_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        self.txn_text = tk.Text(
            txn_frame, height=10, state=tk.DISABLED, bg=self.secondary_color, fg="white"
        )
        self.txn_text.pack(fill=tk.BOTH, expand=True)
        tk.Button(
            master, text="Logout", command=self.logout,
            bg="#222831", fg="white", activebackground=self.secondary_color
        ).pack(side=tk.BOTTOM, pady=10)

        self.accounts = {}
        self.current = None

    def generate_account_number(self):
        while True:
            acc_num = str(random.randint(10000, 99999))
            if acc_num not in self.accounts: return acc_num

    def open_account(self):
        name = simpledialog.askstring("Open Account", "Enter account holder name:")
        if not name or any(acc.name == name for acc in self.accounts.values()):
            messagebox.showerror("Error", "Invalid or duplicate name"); return
        passcode = simpledialog.askstring("Set Passcode", "Set a numeric passcode (min 4 digits):", show="*")
        if not passcode or not passcode.isdigit() or len(passcode) < 4:
            messagebox.showerror("Error", "Invalid passcode."); return
        bal = simpledialog.askfloat("Open Account", "Enter opening balance (Nu.):", minvalue=500)
        if bal is not None:
            acc_num = self.generate_account_number()
            self.accounts[acc_num] = BankAccount(acc_num, name, passcode, bal)
            messagebox.showinfo("Success", f"Account opened for {name}\nAccount Number: {acc_num}\nInitial Balance: Nu.{bal:.2f}")

    def login(self):
        if not self.accounts:
            messagebox.showerror("Error", "No accounts exist yet"); return
        acc_num = simpledialog.askstring("Login", "Enter account number:")
        acc = self.accounts.get(acc_num)
        if acc and simpledialog.askstring("Passcode", "Enter your passcode:", show="*") == acc.passcode:
            self.current = acc
            self.update_display()
            for btn in self.buttons.values(): btn.config(state=tk.NORMAL)
        else:
            messagebox.showerror("Error", "Account not found or wrong passcode")

    def update_display(self):
        if self.current:
            self.balance_label.config(
                text=f"Account: {self.current.account_number}\nHolder: {self.current.name}\nBalance: Nu.{self.current.balance:.2f}")
            self.txn_text.config(state=tk.NORMAL)
            self.txn_text.delete(1.0, tk.END)
            txns = self.current.transactions[-10:] or ["No transactions yet"]
            for t in reversed(txns): self.txn_text.insert(tk.END, f"• {t}\n")
            self.txn_text.config(state=tk.DISABLED)

    def deposit(self):
        amt = simpledialog.askfloat("Deposit", "Enter amount (Nu.):", minvalue=0.01)
        if amt:
            try: self.current.deposit(amt); self.update_display(); messagebox.showinfo("Success", f"Deposited Nu.{amt:.2f}")
            except Exception as e: messagebox.showerror("Error", str(e))

    def withdraw(self):
        amt = simpledialog.askfloat("Withdraw", "Enter amount (Nu.):", minvalue=0.01)
        if amt:
            try: self.current.withdraw(amt); self.update_display(); messagebox.showinfo("Success", f"Withdrew Nu.{amt:.2f}")
            except Exception as e: messagebox.showerror("Error", str(e))

    def transfer(self):
        if len(self.accounts) < 2:
            messagebox.showerror("Error", "Need at least 2 accounts to transfer"); return
        target_acc_num = simpledialog.askstring("Send Money", "Enter recipient account number:")
        target = self.accounts.get(target_acc_num)
        if target and target != self.current:
            amt = simpledialog.askfloat("Send Money", "Enter amount (Nu.):", minvalue=0.01)
            if amt:
                try: self.current.transfer(amt, target); self.update_display(); messagebox.showinfo("Success", f"Transferred Nu.{amt:.2f} to {target.name}")
                except Exception as e: messagebox.showerror("Error", str(e))
        else:
            messagebox.showerror("Error", "Invalid recipient account")

    def mobile_topup(self):
        number = simpledialog.askstring("Mobile Top-Up", "Enter mobile number:")
        if number:
            amt = simpledialog.askfloat("Mobile Top-Up", "Enter amount (Nu.):", minvalue=0.01)
            if amt:
                try: self.current.mobile_topup(amt, number); self.update_display(); messagebox.showinfo("Success", f"Topped up Nu.{amt:.2f} to {number}")
                except Exception as e: messagebox.showerror("Error", str(e))

    def close_account(self):
        if self.current and messagebox.askyesno("Close Account", f"Close account for {self.current.name} ({self.current.account_number})?"):
            del self.accounts[self.current.account_number]
            self.logout()
            messagebox.showinfo("Success", "Account closed successfully")

    def logout(self):
        self.current = None
        self.balance_label.config(text="No account selected")
        self.txn_text.config(state=tk.NORMAL)
        self.txn_text.delete(1.0, tk.END)
        self.txn_text.config(state=tk.DISABLED)
        for btn in self.buttons.values(): btn.config(state=tk.DISABLED)
        messagebox.showinfo("Logout", "You have been logged out.")

if __name__ == "__main__":
    root = tk.Tk()
    app = BankApp(root)
    root.mainloop()