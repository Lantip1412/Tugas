from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
import mysql.connector


class Register(Screen):
    def __init__(self, **kwargs):
        super(Register, self).__init__(**kwargs)
        Window.size = (500, 150)
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        grid = GridLayout(cols=2, spacing=10, size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))

        self.username_label = Label(text="Username", size_hint_y=None, height=40)
        self.username_input = TextInput(multiline=False, size_hint_y=None, height=40)
        self.password_label = Label(text="Password", size_hint_y=None, height=40)
        self.password_input = TextInput(multiline=False, password=True, size_hint_y=None, height=40)
        self.role_label = Label(text="Role", size_hint_y=None, height=40)
        self.role_spinner = Spinner(
            text='Select Role',
            values=('Admin', 'Customer'),
            size_hint=(None, None),
            size=(200, 40)
        )
        
        grid.add_widget(self.username_label)
        grid.add_widget(self.username_input)
        grid.add_widget(self.password_label)
        grid.add_widget(self.password_input)
        grid.add_widget(self.role_label)
        grid.add_widget(self.role_spinner)

        self.register_button = Button(text="Register", size_hint_y=None, height=50)
        self.register_button.bind(on_press=self.register_user)
        self.kembali_button = Button(text="Kembali", size_hint_y=None, height=50)
        self.kembali_button.bind(on_press=self.kembali)
        
        self.layout.add_widget(grid)
        self.layout.add_widget(self.register_button)
        self.layout.add_widget(self.kembali_button)
        
        self.add_widget(self.layout)

    def register_user(self, instance):
        Window.size = (500, 150)
        username = self.username_input.text
        password = self.password_input.text
        role = self.role_spinner.text

        if not username or not password or role == 'Select Role':
            self.show_popup("Error", "Please fill in all fields and select a role.")
        else:
            # Koneksi ke database
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",  # Ganti dengan password MySQL Anda
                database="tugas"
            )
            cursor = conn.cursor()

            # Menyimpan data ke database
            cursor.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)", (username, password, role))
            conn.commit()
            cursor.close()
            conn.close()

            # Reset input fields
            self.username_input.text = ""
            self.password_input.text = ""
            self.role_spinner.text = "Select Role"

            self.show_popup("Success", "Registration successful.")
            self.manager.current = "login"

    def show_popup(self, title, message):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10, size_hint=(None, None), size=(700, 250))
        popup_label = Label(text=message, size_hint=(None, None), height=50, pos_hint={'center_x': 0.5, 'center_y': 0.7})
        close_button = Button(text="Close", size_hint=(None, None), size=(100, 50), pos_hint={'center_x': 0.5, 'center_y': 0.3})
        
        layout.add_widget(popup_label)
        layout.add_widget(close_button)

        popup = Popup(title=title, content=layout, size_hint=(None, None), size=(700, 250))

        close_button.bind(on_press=popup.dismiss)

        popup.open()
    
    def kembali(self, instance):
        Window.size = (500, 150)
        self.clear_inputs()
        self.manager.current = 'login'

    def clear_inputs(self):
        self.username_input.text = ""
        self.password_input.text = ""
        self.role_spinner.text = "Select Role"

class Login(Screen):
    def __init__(self, **kwargs):
        Window.size = (500, 150)
        super(Login, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        grid = GridLayout(cols=2, spacing=10, size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))


        self.username_label = Label(text="Username", size_hint_y=None, height=40)
        self.username_input = TextInput(multiline=False, size_hint_y=None, height=40)
        self.password_label = Label(text="Password", size_hint_y=None, height=40)
        self.password_input = TextInput(multiline=False, password=True, size_hint_y=None, height=40)
        
        grid.add_widget(self.username_label)
        grid.add_widget(self.username_input)
        grid.add_widget(self.password_label)
        grid.add_widget(self.password_input)

        self.login_button = Button(text="Login", size_hint_y=None, height=50)
        self.login_button.bind(on_press=self.login_user)
        self.daftar_button = Button(text="Daftar", size_hint_y=None, height=50)
        self.daftar_button.bind(on_press=self.register)

        self.layout.add_widget(grid)
        self.layout.add_widget(self.login_button)
        self.layout.add_widget(self.daftar_button)

        self.add_widget(self.layout)

    def login_user(self, instance):
        Window.size = (500, 150)
        # Koneksi ke database
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  # Ganti dengan password MySQL Anda
            database="tugas"
        )
        cursor = conn.cursor()
        username = self.username_input.text
        password = self.password_input.text

        query = "SELECT Password, role FROM users WHERE Username = %s"
        cursor.execute(query, (username,))
        result = cursor.fetchone()

        self.clear_inputs()

        if not username or not password :
            self.show_popup("Error", "Please fill in all fields")
        else :
            if result:
                stored_password, stored_role = result
                if password == stored_password:
                    if stored_role == 'Admin':
                        self.manager.current = 'menu'
                    else:
                        self.manager.current = 'view_customer'
            else:
                self.show_popup("Error", "Invalid username or password.")
    
    def register(self, instance):
        Window.size = (500, 150)
        self.clear_inputs()
        self.manager.current = 'register'


    def show_popup(self, title, message):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10, size_hint=(None, None), size=(700, 250))
        popup_label = Label(text=message, size_hint=(None, None), height=50, pos_hint={'center_x': 0.5, 'center_y': 0.7})
        close_button = Button(text="Close", size_hint=(None, None), size=(100, 50), pos_hint={'center_x': 0.5, 'center_y': 0.3})
        
        layout.add_widget(popup_label)
        layout.add_widget(close_button)

        popup = Popup(title=title, content=layout, size_hint=(None, None), size=(700, 250))

        close_button.bind(on_press=popup.dismiss)

        popup.open()

    def clear_inputs(self):
        self.username_input.text = ""
        self.password_input.text = ""

class MenuScreen(Screen):
    def __init__(self, **kwargs):
        Window.size = (500, 150)
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.view_data_button = Button(text="View Data")
        self.view_data_button.bind(on_press=self.view_data)

        self.daftar_customer_button = Button(text="Daftar Customer")
        self.daftar_customer_button.bind(on_press=self.daftar_customer)

        self.kembali_button = Button(text="Kembali")
        self.kembali_button.bind(on_press=self.kembali)

        layout.add_widget(self.view_data_button)
        layout.add_widget(self.daftar_customer_button)
        layout.add_widget(self.kembali_button)

        self.add_widget(layout)

    def view_data(self, instance):
        Window.size = (500, 150)
        self.manager.current = 'view_data'

    def daftar_customer(self, instance):
        Window.size = (500, 200)
        self.manager.current = 'daftar_customer'

    def kembali(self, instance):
        Window.size = (500, 150)
        self.manager.current = 'login'


class ViewDataScreen(Screen):
    def __init__(self, **kwargs):
        Window.size = (500, 500)
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Membuat GridLayout untuk tabel
        self.table_layout = GridLayout(cols=6)  # Sesuaikan jumlah kolom dengan kebutuhan

        # Menambahkan header tabel
        headers = ["No", "Nama", "Username", "Tanggal Lahir", "Email", "Gender"]
        for header in headers:
            self.table_layout.add_widget(Label(text=header, bold=True))

        layout.add_widget(self.table_layout)

        self.back_button = Button(text="Kembali", size_hint=(1, .1))
        self.back_button.bind(on_press=self.back_to_menu)
        layout.add_widget(self.back_button)

        self.add_widget(layout)

    def back_to_menu(self, instance):
        Window.size = (500, 150)
        self.manager.current = 'menu'

    def on_pre_enter(self, *args):
        self.show_data()

    def show_data(self):
        Window.size = (500, 500)
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  # Ganti dengan password MySQL Anda
            database="tugas"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT id, Nama, Username,Tgl_Lahir, Email, Gender FROM customers")
        results = cursor.fetchall()
        cursor.close()
        conn.close()

        # Menghapus widget lama dari tabel sebelum menambahkan data baru
        self.table_layout.clear_widgets()
        
        # Menambahkan header tabel lagi setelah clear
        headers = ["No", "Nama", "Username", "Tanggal Lahir", "Email", "Gender"]
        for header in headers:
            self.table_layout.add_widget(Label(text=header, bold=True))

        # Menambahkan data ke dalam tabel
        for row in results:
            for cell in row:
                self.table_layout.add_widget(Label(text=str(cell)))

class DaftarCustomerScreen(Screen):
    def __init__(self, **kwargs):
        Window.size = (500, 200)
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        grid = GridLayout(cols=2, spacing=10, size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))

        self.clear_input

        self.name_label = Label(text="Nama", size_hint_y=None, height=40)
        self.name_input = TextInput(multiline=False, size_hint_y=None, height=40)
        self.username_label = Label(text="Username", size_hint_y=None, height=40)
        self.username_input = TextInput(multiline=False, size_hint_y=None, height=40)
        self.tgl_lahir_label = Label(text="Tanggal Lahir (YYYY-MM-DD)", size_hint_y=None, height=40)
        self.tgl_lahir_input = TextInput(multiline=False, size_hint_y=None, height=40)
        self.email_label = Label(text="Email", size_hint_y=None, height=40)
        self.email_input = TextInput(multiline=False, size_hint_y=None, height=40)
        self.gender_label = Label(text="Gender", size_hint_y=None, height=40)
        self.gender_spinner = Spinner(
            text='Pilih Gender',
            values=('Laki-laki', 'Perempuan'),
            size_hint=(None, None),
            size=(200, 40)
        )

        grid.add_widget(self.name_label)
        grid.add_widget(self.name_input)
        grid.add_widget(self.username_label)
        grid.add_widget(self.username_input)
        grid.add_widget(self.tgl_lahir_label)
        grid.add_widget(self.tgl_lahir_input)
        grid.add_widget(self.email_label)
        grid.add_widget(self.email_input)
        grid.add_widget(self.gender_label)
        grid.add_widget(self.gender_spinner)

        self.register_button = Button(text="Register", size_hint_y=None, height=50)
        self.register_button.bind(on_press=self.register_customer)
        self.kembali_button = Button(text="Kembali", size_hint_y=None, height=50)
        self.kembali_button.bind(on_press=self.kembali)

        layout.add_widget(grid)
        layout.add_widget(self.register_button)
        layout.add_widget(self.kembali_button)

        self.add_widget(layout)
    def register_customer(self, instance):
        Window.size = (500, 200)
        nama = self.name_input.text
        username = self.username_input.text
        tgl_lahir = self.tgl_lahir_input.text
        email = self.email_input.text
        gender = self.gender_spinner.text

        if not nama or not username or not tgl_lahir or not email or gender == 'Pilih Gender':
            self.show_popup("Error", "Please fill in all fields and select a gender.")
        else:
            # Koneksi ke database
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",  # Ganti dengan password MySQL Anda
                database="tugas"
            )
            cursor = conn.cursor()

            self.clear_input()

            # Menyimpan data ke database
            cursor.execute("INSERT INTO customers (nama, username, tgl_lahir, email, gender) VALUES (%s, %s, %s, %s, %s)",
                            (nama, username, tgl_lahir, email, gender))
            conn.commit()
            cursor.close()
            conn.close()

            # Reset input fields
            self.name_input.text = ""
            self.username_input.text = ""
            self.tgl_lahir_input.text = ""
            self.email_input.text = ""
            self.gender_spinner.text = "Pilih Gender"

            self.show_popup("Success", "Registration successful.")
            self.manager.current = "menu"

    def show_popup(self, title, message):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10, size_hint=(None, None), size=(700, 250))
        popup_label = Label(text=message, size_hint=(None, None), pos_hint={'center_x': 0.5, 'center_y': 0.6})
        close_button = Button(text="Close", size_hint=(None, None), size=(100, 50), pos_hint={'center_x': 0.5, 'center_y': 0.4})
        
        layout.add_widget(popup_label)
        layout.add_widget(close_button)

        popup = Popup(title=title, content=layout, size_hint=(0.75, 0.5))

        close_button.bind(on_press=popup.dismiss)

        popup.open()

    def kembali(self, instance):
        self.manager.current = 'menu'

    def clear_input(self):
        self.name_input.text = ''
        self.username_input.text = ''
        self.tgl_lahir_input.text = ''
        self.email_input.text = ''
        self.gender_spinner.text = ''

class MyApp(App):

    def build(self):
        sm = ScreenManager()
        sm.add_widget(Login(name='login'))
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(ViewDataScreen(name='view_data'))
        # sm.add_widget(ViewDataScreen(name='view_customer'))
        sm.add_widget(DaftarCustomerScreen(name='daftar_customer'))
        sm.add_widget(Register(name='register'))
        return sm

if __name__ == '__main__':
    MyApp().run()
