from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.graphics import Color, Rectangle
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
import csv
import datetime


prices = {"A": 460, "B": 60}
items = []

class ManagerDashboard(Screen):  
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        with self.canvas.before:
            Color(0.314, 0, 0, 1)  
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self.update_rect, pos=self.update_rect)

        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # Back button at the top-left corner
        back_button = Button(text="Back", size_hint=(None, None), size=(100, 50), pos_hint={'x': 0, 'top': 1})
        back_button.bind(on_press=self.open_main_menu)
        layout.add_widget(back_button)

        # Title label
        title_label = Label(text="Manager Dashboard", font_size=24, size_hint=(1, 0.1))
        layout.add_widget(title_label)

        # Scroll view for data
        self.scroll_view = ScrollView(size_hint=(1, 0.7))  # Adjust height to make space for "More Options"
        self.data_layout = GridLayout(cols=5, size_hint_y=None)
        self.data_layout.bind(minimum_height=self.data_layout.setter('height'))

        self.scroll_view.add_widget(self.data_layout)
        layout.add_widget(self.scroll_view)

        # "More Options" button
        more_options_button = Button(text="More Options", size_hint=(1, 0.1))
        more_options_button.bind(on_press=self.show_more_options)
        layout.add_widget(more_options_button)

        self.add_widget(layout)
        self.load_data()

    def update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def load_data(self):
        """Loads data from the CSV file into the dashboard."""
        columns = ["Item Number", "Item Name", "Transaction Number", "Date Sold", "Profit"]
        for col in columns:
            header_label = Label(text=col, bold=True, size_hint_y=None, height=30)
            self.data_layout.add_widget(header_label)

        try:
            with open("manager_data.csv", "r") as file:
                reader = csv.reader(file)
                next(reader)  # Skip header row
                for row in reader:
                    for cell in row:
                        cell_label = Label(text=cell, size_hint_y=None, height=30)
                        self.data_layout.add_widget(cell_label)
        except FileNotFoundError:
            popup = Popup(title="Error", content=Label(text="CSV file not found!"), size_hint=(0.6, 0.4))
            popup.open()
        except Exception as e:
            popup = Popup(title="Error", content=Label(text=f"Error loading data: {e}"), size_hint=(0.6, 0.4))
            popup.open()

    def refresh_data(self):
        """Refresh the data displayed in the manager dashboard."""
        self.data_layout.clear_widgets()  # Clear existing widgets
        self.load_data()

    def open_main_menu(self, instance):
        """Navigate back to the main menu."""
        self.manager.transition = SlideTransition(direction='right')  
        self.manager.current = 'main_menu'

    def on_enter(self):
        """Refresh data when the Manager Dashboard screen is displayed."""
        self.refresh_data()

    def show_more_options(self, instance):
        """Show more options like most/least sold items, total items sold, etc."""
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Make buttons larger
        button_size = (1, None)  # Make the buttons span full width, height will auto adjust

        # Most sold item
        most_sold_item_button = Button(text="Most Sold Item", size_hint_y=None, height=60)
        most_sold_item_button.bind(on_press=self.show_most_sold_item)
        layout.add_widget(most_sold_item_button)

        # Least sold item
        least_sold_item_button = Button(text="Least Sold Item", size_hint_y=None, height=60)
        least_sold_item_button.bind(on_press=self.show_least_sold_item)
        layout.add_widget(least_sold_item_button)

        # Total items sold
        total_items_sold_button = Button(text="Total Items Sold", size_hint_y=None, height=60)
        total_items_sold_button.bind(on_press=self.show_total_items_sold)
        layout.add_widget(total_items_sold_button)

        # Monthly sales
        monthly_sales_button = Button(text="Monthly Sales", size_hint_y=None, height=60)
        monthly_sales_button.bind(on_press=self.show_monthly_sales)
        layout.add_widget(monthly_sales_button)

        # Yearly sales
        yearly_sales_button = Button(text="Yearly Sales", size_hint_y=None, height=60)
        yearly_sales_button.bind(on_press=self.show_yearly_sales)
        layout.add_widget(yearly_sales_button)

        # Total sales
        total_sales_button = Button(text="Total Sales", size_hint_y=None, height=60)
        total_sales_button.bind(on_press=self.show_total_sales)
        layout.add_widget(total_sales_button)

        # Item code search
        item_code_input = TextInput(hint_text="Enter Item Code", size_hint_y=None, height=40)
        item_code_button = Button(text="Search Item", size_hint_y=None, height=40)
        item_code_button.bind(on_press=lambda instance: self.show_item_sales(item_code_input.text))
        layout.add_widget(item_code_input)
        layout.add_widget(item_code_button)

        # Close button
        close_button = Button(text="Close", size_hint_y=None, height=40)
        close_button.bind(on_press=lambda instance: self.close_popup())
        layout.add_widget(close_button)

        self.popup = Popup(title="More Options", content=layout, size_hint=(0.6, 0.6))
        self.popup.open()

    def close_popup(self):
        """Close the popup."""
        self.popup.dismiss()

    def get_sales_data(self):
        """Retrieve sales data from the CSV file."""
        sales_data = []
        try:
            with open("manager_data.csv", "r") as file:
                reader = csv.reader(file)
                next(reader)  # Skip header row
                for row in reader:
                    item_number = row[0]
                    date_sold = datetime.datetime.strptime(row[3], "%Y-%m-%d")
                    sales_data.append({
                        "item_number": item_number,
                        "date_sold": date_sold,
                        "profit": float(row[4].replace('$', '').replace(',', ''))
                    })
        except FileNotFoundError:
            return None
        except Exception as e:
            return None
        return sales_data

    def show_most_sold_item(self, instance):
        """Show the most sold item."""
        sales_data = self.get_sales_data()
        if not sales_data:
            self.show_error("Error loading sales data!")
            return
        
        item_sales = {}
        for data in sales_data:
            item_sales[data["item_number"]] = item_sales.get(data["item_number"], 0) + 1
        
        most_sold = max(item_sales, key=item_sales.get)
        self.show_popup(f"Most Sold Item: {most_sold} ({item_sales[most_sold]} sold)")

    def show_least_sold_item(self, instance):
        """Show the least sold item."""
        sales_data = self.get_sales_data()
        if not sales_data:
            self.show_error("Error loading sales data!")
            return
        
        item_sales = {}
        for data in sales_data:
            item_sales[data["item_number"]] = item_sales.get(data["item_number"], 0) + 1
        
        least_sold = min(item_sales, key=item_sales.get)
        self.show_popup(f"Least Sold Item: {least_sold} ({item_sales[least_sold]} sold)")

    def show_total_items_sold(self, instance):
        """Show total items sold."""
        sales_data = self.get_sales_data()
        if not sales_data:
            self.show_error("Error loading sales data!")
            return
        
        total_items_sold = len(sales_data)
        self.show_popup(f"Total Items Sold: {total_items_sold}")

    def show_monthly_sales(self, instance):
        """Show monthly sales."""
        sales_data = self.get_sales_data()
        if not sales_data:
            self.show_error("Error loading sales data!")
            return
        
        monthly_sales = {}
        for data in sales_data:
            month = data["date_sold"].strftime("%Y-%m")
            monthly_sales[month] = monthly_sales.get(month, 0) + data["profit"]
        
        sorted_months = sorted(monthly_sales.items())
        monthly_sales_text = "\n".join([f"{month}: ${amount:.2f}" for month, amount in sorted_months])
        self.show_popup(f"Monthly Sales:\n{monthly_sales_text}")

    def show_yearly_sales(self, instance):
        """Show yearly sales."""
        sales_data = self.get_sales_data()
        if not sales_data:
            self.show_error("Error loading sales data!")
            return
        
        yearly_sales = {}
        for data in sales_data:
            year = data["date_sold"].strftime("%Y")
            yearly_sales[year] = yearly_sales.get(year, 0) + data["profit"]
        
        sorted_years = sorted(yearly_sales.items())
        self.show_popup(f"Yearly Sales:\n{', '.join([f'{year}: ${amount:.2f}' for year, amount in sorted_years])}")

    def show_total_sales(self, instance):
        """Show total sales."""
        sales_data = self.get_sales_data()
        if not sales_data:
            self.show_error("Error loading sales data!")
            return
        
        total_sales = sum(data["profit"] for data in sales_data)
        self.show_popup(f"Total Sales: ${total_sales:.2f}")

    def show_item_sales(self, item_code):
        """Show sales of a specific item based on its code."""
        sales_data = self.get_sales_data()
        if not sales_data:
            self.show_error("Error loading sales data!")
            return
        
        item_sales = sum(1 for data in sales_data if data["item_number"] == item_code)
        
        if item_sales == 0:
            self.show_popup(f"No item found with code {item_code}")
        else:
            self.show_popup(f"Item {item_code} has sold {item_sales} times.")

    def show_error(self, message):
        """Show an error popup."""
        self.show_popup(f"Error: {message}")

    def show_popup(self, message):
        """Show a simple popup with a message."""
        popup = Popup(title="Result", content=Label(text=message), size_hint=(0.6, 0.4))
        popup.open()

class CashierScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.items_list = []
        self.total_price = 0
        self.transaction_number = 1  # Initialize transaction number

        # Set the background color using canvas.before
        with self.canvas.before:
            Color(0.314, 0, 0, 1)  # Dark red color
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self._update_rect, pos=self._update_rect)

        layout = BoxLayout(orientation='vertical', spacing=15, padding=20)

        # Title
        title_label = Label(text="Cashier Screen", font_size=24, size_hint_y=None, height=50)
        layout.add_widget(title_label)

        # Input field layout
        input_layout = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None, height=150)

        # Increase the font size and height of the TextInput for item code
        self.item_input = TextInput(hint_text="Enter Item Code (A or B)", multiline=False, font_size=48, height=75, size_hint=(1, None))
        input_layout.add_widget(self.item_input)

        # Add Item button (larger)
        add_button = Button(text="Add Item", size_hint=(1, None), height=80, font_size=24)
        add_button.bind(on_press=self.add_item)
        input_layout.add_widget(add_button)

        layout.add_widget(input_layout)

        # Total Label (increase font size)
        self.total_label = Label(text="Total: $0", font_size=32, size_hint_y=None, height=60)
        layout.add_widget(self.total_label)

        # Scrollable Cart View
        self.cart_scrollview = ScrollView(size_hint=(1, 0.4), size=(self.width, 200))
        self.cart_layout = BoxLayout(orientation='vertical', size_hint_y=None)
        self.cart_layout.bind(minimum_height=self.cart_layout.setter('height'))
        self.cart_scrollview.add_widget(self.cart_layout)
        layout.add_widget(self.cart_scrollview)

        # Checkout Button (larger)
        checkout_button = Button(text="Checkout", size_hint_y=None, height=80, font_size=24)
        checkout_button.bind(on_press=self.checkout)
        layout.add_widget(checkout_button)

        # Back to Main Menu Button (larger)
        back_button = Button(text="Back to Main Menu", size_hint_y=None, height=80, font_size=24)
        back_button.bind(on_press=self.open_main_menu)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def _update_rect(self, instance, value):
        # Update the size and position of the background rectangle when the screen resizes
        self.rect.pos = self.pos
        self.rect.size = self.size

    def read_inventory(self):
        """Reads the inventory from 'inventory.csv'."""
        inventory = {}
        try:
            with open('inventory.csv', mode='r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                for row in reader:
                    item_code = row[0]
                    item_name = row[1]
                    item_price = float(row[2])
                    item_quantity = int(row[3])
                    item_cost = float(row[4])
                    inventory[item_code] = {
                        'name': item_name,
                        'price': item_price,
                        'quantity': item_quantity,
                        'cost': item_cost
                    }
        except Exception as e:
            popup = Popup(title="Error", content=Label(text=f"Error reading inventory: {e}"), size_hint=(0.6, 0.4))
            popup.open()
        return inventory

    def add_item(self, instance):
        item_code = self.item_input.text.strip().upper()

        inventory = self.read_inventory()

        if item_code in inventory:
            item = inventory[item_code]
            if item['quantity'] > 0:
                # Decrease the quantity and update total
                item['quantity'] -= 1
                self.total_price += item['price']
                self.items_list.append(item_code)

                # Update the cart layout
                item_label = Label(text=f"Item: {item['name']} - ${item['price']}", size_hint_y=None, height=40)
                self.cart_layout.add_widget(item_label)

                # Clear the input field
                self.item_input.text = ""
                self.total_label.text = f"Total: ${self.total_price}"

                # Save the updated inventory to file
                self.update_inventory(inventory)

            else:
                popup = Popup(title="Out of Stock", content=Label(text="Item is out of stock!"), size_hint=(0.6, 0.4))
                popup.open()
        else:
            popup = Popup(title="Invalid Item", content=Label(text="Item not recognized!"), size_hint=(0.6, 0.4))
            popup.open()

    def update_inventory(self, inventory):
        """Updates the inventory CSV file with new quantities."""
        try:
            with open('inventory.csv', mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Item Number", "Item Name", "Item Price(Selling)", "Quantity of Items", "Item Cost"])
                for item_code, item_data in inventory.items():
                    writer.writerow([item_code, item_data['name'], item_data['price'], item_data['quantity'], item_data['cost']])
        except Exception as e:
            popup = Popup(title="Error", content=Label(text=f"Error saving inventory: {e}"), size_hint=(0.6, 0.4))
            popup.open()

    def checkout(self, instance):
        if self.items_list:
            # Generate the transaction number
            transaction_number = f"TX{self.transaction_number:05d}"

            # Record the sale and profit in manager_data.csv
            inventory = self.read_inventory()
            date_sold = datetime.datetime.now().strftime("%Y-%m-%d")
            for item_code in self.items_list:
                item = inventory[item_code]
                profit = item['price'] - item['cost']

                # Write the transaction data to manager_data.csv
                try:
                    with open('manager_data.csv', mode='a', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow([item_code, item['name'], transaction_number, date_sold, f"${profit:.2f}"])
                except Exception as e:
                    popup = Popup(title="Error", content=Label(text=f"Error saving transaction: {e}"), size_hint=(0.6, 0.4))
                    popup.open()

            # Increment transaction number for next sale
            self.transaction_number += 1

            # Show receipt popup
            popup = Popup(title="Receipt", content=Label(text=f"Items: {', '.join(self.items_list)}\nTotal: ${self.total_price}"), size_hint=(0.6, 0.4))
            popup.open()

            # Reset for next transaction
            self.items_list = []
            self.total_price = 0
            self.total_label.text = "Total: $0"
            self.cart_layout.clear_widgets()
        else:
            popup = Popup(title="Error", content=Label(text="No items in cart!"), size_hint=(0.6, 0.4))
            popup.open()

    def open_main_menu(self, instance):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'main_menu'

class MainMenu(Screen):  
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        label = Label(text="Welcome to 12th Man Grocery Store!\nWhat is your position?", font_size=48, halign="center", valign="middle", text_size=(None, None))   
        layout.add_widget(label)

        cashier_button = Button(text="Cashier", size_hint=(1, 0.3))
        cashier_button.bind(on_press=self.open_cashier_screen)
        layout.add_widget(cashier_button)

        manager_button = Button(text="Manager", size_hint=(1, 0.3))
        manager_button.bind(on_press=self.open_manager_screen)
        layout.add_widget(manager_button)

        with self.canvas.before:
            Color(0.314, 0, 0, 1)  # Background color
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self.update_rect, pos=self.update_rect)

        self.add_widget(layout)

    def update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def open_cashier_screen(self, instance):
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'cashier_screen'

    def open_manager_screen(self, instance):
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'manager_dashboard'


class POSApp(App):
    def build(self):
        screen_manager = ScreenManager()
        screen_manager.add_widget(MainMenu(name='main_menu'))
        screen_manager.add_widget(CashierScreen(name='cashier_screen'))
        screen_manager.add_widget(ManagerDashboard(name='manager_dashboard'))

        return screen_manager


if __name__ == '__main__':
    POSApp().run()