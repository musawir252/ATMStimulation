import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox

class User:
    def __init__(self, name, password, balance):
        self.name = name
        self.password = password
        self.balance = balance

    def get_name(self):
        return self.name

    def get_password(self):
        return self.password

    def get_balance(self):
        return self.balance

    def set_balance(self, balance):
        self.balance = balance

    def change_password(self, new_password):
        self.password = new_password

class Admin:
    def __init__(self, admin_password):
        self.admin_password = admin_password
        self.users = {}

    def verify_admin_password(self, entered_password):
        return entered_password == self.admin_password

    def add_user(self, username, password, initial_balance):
        self.users[username] = User(username, password, initial_balance)
        messagebox.showinfo("Success", "User added successfully.")

    def delete_user(self, username):
        if username in self.users:
            del self.users[username]
            messagebox.showinfo("Success", "User deleted successfully.")
        else:
            messagebox.showerror("Error", "User not found.")

    def show_user_list(self):
        user_list = "\n".join(self.users.keys())
        messagebox.showinfo("User List", f"User List:\n{user_list}")

    def get_user(self, username):
        return self.users.get(username)

class ATMApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ATM Simulation")

        self.admin = Admin("adminpass")
        self.current_user = None

        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self.root, text="ATM Simulation")
        self.label.pack()

        self.user_button = tk.Button(self.root, text="User Login", command=self.user_login)
        self.user_button.pack()

        self.admin_button = tk.Button(self.root, text="Admin Login", command=self.admin_login)
        self.admin_button.pack()

        self.exit_button = tk.Button(self.root, text="Exit", command=self.root.destroy)
        self.exit_button.pack()

    def user_login(self):
        self.current_user = None
        username = simpledialog.askstring("User Login", "Enter username:")
        password = simpledialog.askstring("User Login", "Enter password:")

        if self.current_user is None:
            self.current_user = self.authenticate_user(username, password)
            if self.current_user:
                self.user_menu()
            else:
                messagebox.showerror("Error", "Invalid username or password. Please try again.")
        else:
            messagebox.showwarning("Warning", "User is already logged in. Logout first to switch users.")

    def authenticate_user(self, username, password):
        # Perform user authentication
        # For simplicity, using hard-coded values
        if username == "user1" and password == "pass123":
            return User(username, password, 1000.0)
        return None

    def user_menu(self):
        self.user_menu_window = tk.Toplevel(self.root)
        self.user_menu_window.title("User Menu")

        self.deposit_button = tk.Button(self.user_menu_window, text="Deposit", command=self.perform_deposit)
        self.deposit_button.pack()

        self.withdraw_button = tk.Button(self.user_menu_window, text="Withdraw", command=self.perform_withdraw)
        self.withdraw_button.pack()

        self.check_balance_button = tk.Button(self.user_menu_window, text="Check Balance", command=self.check_balance)
        self.check_balance_button.pack()

        self.change_password_button = tk.Button(self.user_menu_window, text="Change Password", command=self.change_password)
        self.change_password_button.pack()

        self.logout_button = tk.Button(self.user_menu_window, text="Logout", command=self.logout)
        self.logout_button.pack()

    def perform_deposit(self):
        amount = simpledialog.askfloat("Deposit", "Enter deposit amount:")
        if amount is not None:
            self.current_user.set_balance(self.current_user.get_balance() + amount)
            messagebox.showinfo("Success", f"Deposit successful. New balance: ${self.current_user.get_balance()}")

    def perform_withdraw(self):
        amount = simpledialog.askfloat("Withdraw", "Enter withdrawal amount:")
        if amount is not None:
            if amount <= self.current_user.get_balance():
                self.current_user.set_balance(self.current_user.get_balance() - amount)
                messagebox.showinfo("Success", f"Withdrawal successful. New balance: ${self.current_user.get_balance()}")
            else:
                messagebox.showerror("Error", "Insufficient funds. Withdrawal failed.")

    def check_balance(self):
        messagebox.showinfo("Balance", f"Current balance: ${self.current_user.get_balance()}")

    def change_password(self):
        new_password = simpledialog.askstring("Change Password", "Enter new password:")
        if new_password is not None:
            self.current_user.change_password(new_password)
            messagebox.showinfo("Success", "Password changed successfully.")

    def logout(self):
        self.current_user = None
        messagebox.showinfo("Logout", "Logged out successfully.")

    def admin_login(self):
        entered_password = simpledialog.askstring("Admin Login", "Enter admin password:")
        if self.admin.verify_admin_password(entered_password):
            self.admin_menu()
        else:
            messagebox.showerror("Error", "Incorrect admin password. Please try again.")

    def admin_menu(self):
        self.admin_menu_window = tk.Toplevel(self.root)
        self.admin_menu_window.title("Admin Menu")

        self.add_user_button = tk.Button(self.admin_menu_window, text="Add User", command=self.add_user)
        self.add_user_button.pack()

        self.delete_user_button = tk.Button(self.admin_menu_window, text="Delete User", command=self.delete_user)
        self.delete_user_button.pack()

        self.view_user_list_button = tk.Button(self.admin_menu_window, text="View User List", command=self.admin.show_user_list)
        self.view_user_list_button.pack()

        self.logout_button = tk.Button(self.admin_menu_window, text="Logout", command=self.admin_menu_window.destroy)
        self.logout_button.pack()

    def add_user(self):
        username = simpledialog.askstring("Add User", "Enter username for the new user:")
        initial_balance = simpledialog.askfloat("Add User", "Enter initial balance:")
        password = simpledialog.askstring("Add User", "Enter password for the new user:")
        self.admin.add_user(username, password, initial_balance)

    def delete_user(self):
        username = simpledialog.askstring("Delete User", "Enter username to delete:")
        self.admin.delete_user(username)

if __name__ == "__main__":
    root = tk.Tk()
    app = ATMApp(root)
    root.mainloop()
