import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.metrics import dp
import requests

# URL of the Flask server
BASE_URL = "http://127.0.0.1:5000"

def check_login(nama, email):
    url = f'{BASE_URL}/login'
    response = requests.post(url, json={'nama': nama, 'email': email})
    return response.json().get('status') == 'success'

def get_pdf_blob(nama):
    url = f'{BASE_URL}/download_pdf'
    response = requests.post(url, json={'nama': nama})
    result = response.json()
    if result.get('status') == 'success':
        return result.get('pdf_blob').encode('latin1')
    return None

def save_blob_to_file(blob_data, file_name):
    with open(file_name, 'wb') as file:
        file.write(blob_data)

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        
        # Layout utama menggunakan BoxLayout
        self.layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))
        
        # Layout untuk form menggunakan BoxLayout (vertikal)
        self.form_layout = BoxLayout(orientation='vertical', spacing=dp(10), size_hint_y=None)
        self.form_layout.bind(minimum_height=self.form_layout.setter('height'))

        # Nama
        self.form_layout.add_widget(Label(text='Nama:', font_size='16sp', size_hint_y=None, height=dp(30)))
        self.nama = TextInput(multiline=False, size_hint_y=None, height=dp(40))
        self.form_layout.add_widget(self.nama)

        # Email
        self.form_layout.add_widget(Label(text='Email:', font_size='16sp', size_hint_y=None, height=dp(30)))
        self.email = TextInput(multiline=False, size_hint_y=None, height=dp(40))
        self.form_layout.add_widget(self.email)
        
        # Menambahkan form layout ke layout utama
        self.layout.add_widget(self.form_layout)

        # Tombol login
        self.login_button = Button(text='Login', size_hint_y=None, height=dp(40), size_hint_x=0.5, pos_hint={'center_x': 0.5})
        self.login_button.bind(on_press=self.validate_user)
        self.layout.add_widget(self.login_button)

        # Tombol untuk keluar aplikasi
        self.exit_button = Button(text='Exit', size_hint_y=None, height=dp(40), size_hint_x=0.5, pos_hint={'center_x': 0.5})
        self.exit_button.bind(on_press=self.exit_app)
        self.layout.add_widget(self.exit_button)

        self.add_widget(self.layout)

    def validate_user(self, instance):
        nama = self.nama.text
        email = self.email.text
        if check_login(nama, email):
            self.manager.get_screen('home').update_welcome_message(nama)
            self.manager.get_screen('home').user_name = nama
            self.manager.current = 'home'
        else:
            popup = Popup(title='Login Failed', content=Label(text='Invalid username or email'), size_hint=(None, None), size=(dp(300), dp(200)))
            popup.open()

    def exit_app(self, instance):
        App.get_running_app().stop()


class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))
        self.welcome_label = Label(text='Welcome to Home Screen', font_size='24sp')
        self.layout.add_widget(self.welcome_label)

        self.download_button = Button(text='Download PDF', size_hint_y=None, height=dp(50))
        self.download_button.bind(on_press=self.download_pdf)
        self.layout.add_widget(self.download_button)

        # Tombol untuk kembali ke Login Screen
        self.back_button = Button(text='Back to Login', size_hint_y=None, height=dp(50))
        self.back_button.bind(on_press=self.go_to_login)
        self.layout.add_widget(self.back_button)

        self.add_widget(self.layout)
        self.user_name = ''

    def update_welcome_message(self, nama):
        self.welcome_label.text = f'Welcome, {nama}!'

    def download_pdf(self, instance):
        blob_data = get_pdf_blob(self.user_name)
        if blob_data:
            file_name = f'{self.user_name}_hasilcheckup.pdf'
            save_blob_to_file(blob_data, file_name)
            popup = Popup(title='Download Success', content=Label(text=f'File saved as {file_name}'), size_hint=(None, None), size=(dp(300), dp(200)))
            popup.open()
        else:
            popup = Popup(title='Download Failed', content=Label(text='No PDF found for this user'), size_hint=(None, None), size=(dp(300), dp(200)))
            popup.open()

    def go_to_login(self, instance):
        self.manager.current = 'login'


class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(HomeScreen(name='home'))
        return sm

if __name__ == '__main__':
    MyApp().run()
