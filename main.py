import os
os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'
from kivy.config import Config
Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '640')
Config.set('graphics', 'resizable', False)

from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.boxlayout import BoxLayout as KBoxLayout
from kivy.uix.scrollview import ScrollView as KScrollView
from kivy.metrics import dp
from kivy.uix.anchorlayout import AnchorLayout
from kivy.animation import Animation

from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDIconButton
import random
from kivy.clock import Clock
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton



from datetime import datetime
import calendar

from database import DatabaseManager


class MyreScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_user = ""
        self.transition = NoTransition()

class WelcomeScreen(Screen):
    def on_enter(self):
        anim = Animation(opacity=1, duration=0.9, t="out_quad")
        anim.start(self.ids.box)

class LoginScreen(Screen):
    captcha_verified = False
    dialog = None
    correct_answer = 0

    def on_enter(self):
        self.captcha_verified = False
        self.ids.captcha_checkbox.active = False
        self.ids.captcha_checkbox.disabled = False

    # ========= CAPTCHA =========
    def on_captcha_checked(self, checkbox, value):
        if value:
            checkbox.disabled = True
            Clock.schedule_once(self.show_captcha_challenge, 0.3)

    def show_captcha_challenge(self, *args):
        a = random.randint(1, 9)
        b = random.randint(1, 9)
        self.correct_answer = a + b

        self.captcha_input = MDTextField(
            hint_text=f"What is {a} + {b} ?",
            input_filter="int",
            mode="fill"
        )

        self.dialog = MDDialog(
            title="Verification",
            type="custom",
            content_cls=self.captcha_input,
            buttons=[
                MDFlatButton(text="VERIFY", on_release=self.verify_captcha)
            ],
        )
        self.dialog.open()

    def verify_captcha(self, *args):
        try:
            answer = int(self.captcha_input.text)
        except:
            answer = -1

        if answer == self.correct_answer:
            self.captcha_verified = True
        else:
            self.captcha_verified = False
            self.ids.captcha_checkbox.active = False

        self.ids.captcha_checkbox.disabled = False
        self.dialog.dismiss()

    # ========= LOGIN =========
    def try_login(self):
        if not self.captcha_verified:
            self.show_error_dialog(
                "Verification Required",
                "Please verify that you are not a robot."
            )
            return

        username = self.ids.username.text
        password = self.ids.password.text

        if not username or not password:
            self.show_error_dialog("Error", "Username and password must be filled!")
            return

        db = DatabaseManager()
        if db.login_user(username, password):
            self.manager.current_user = username
            self.manager.current = "home"
            self.ids.username.text = ""
            self.ids.password.text = ""
        else:
            self.show_error_dialog("Login Failed", "Username or password is wrong!")

    # ========= DIALOG =========
    def show_error_dialog(self, title, text):
        self.dialog = MDDialog(
            title=title,
            text=text,
            buttons=[
                MDFlatButton(text="OK", on_release=self.close_dialog)
            ],
        )
        self.dialog.open()

    def close_dialog(self, *args):
        self.dialog.dismiss()


class RegisterScreen(Screen):
    captcha_verified = False
    dialog = None
    correct_answer = 0

    def on_enter(self):
        self.captcha_verified = False
        self.ids.reg_captcha_checkbox.active = False
        self.ids.reg_captcha_checkbox.disabled = False

    # ========= CAPTCHA =========
    def on_captcha_checked(self, checkbox, value):
        if value:
            checkbox.disabled = True
            Clock.schedule_once(self.show_captcha_challenge, 0.3)

    def show_captcha_challenge(self, *args):
        a = random.randint(1, 9)
        b = random.randint(1, 9)
        self.correct_answer = a + b

        self.captcha_input = MDTextField(
            hint_text=f"What is {a} + {b} ?",
            input_filter="int",
            mode="fill"
        )

        self.dialog = MDDialog(
            title="Verification",
            type="custom",
            content_cls=self.captcha_input,
            buttons=[
                MDFlatButton(text="VERIFY", on_release=self.verify_captcha)
            ],
        )
        self.dialog.open()

    def verify_captcha(self, *args):
        try:
            answer = int(self.captcha_input.text)
        except:
            answer = -1

        if answer == self.correct_answer:
            self.captcha_verified = True
        else:
            self.captcha_verified = False
            self.ids.reg_captcha_checkbox.active = False

        self.ids.reg_captcha_checkbox.disabled = False
        self.dialog.dismiss()

    # ========= REGISTER =========
    def try_register(self):
        if not self.captcha_verified:
            self.show_error_dialog("CAPTCHA", "Please verify that you are not a robot.")
            return

        username = self.ids.reg_username.text
        password = self.ids.reg_password.text
        confirm = self.ids.reg_confirm.text

        if not username or not password:
            self.show_error_dialog("Error", "Username and password must be filled!")
            return

        if password != confirm:
            self.show_error_dialog("Error", "Password does not match!")
            return

        db = DatabaseManager()
        if db.register_user(username, password):
            self.show_success_dialog(
                "Success",
                "Registration successful! Please login."
            )
        else:
            self.show_error_dialog("Error", "Username already used!")

    # ========= DIALOG =========
    def show_error_dialog(self, title, text):
        self.dialog = MDDialog(
            title=title,
            text=text,
            buttons=[
                MDFlatButton(text="OK", on_release=self.close_dialog)
            ],
        )
        self.dialog.open()

    def show_success_dialog(self, title, text):
        self.dialog = MDDialog(
            title=title,
            text=text,
            buttons=[
                MDFlatButton(text="OK", on_release=self.go_to_login)
            ],
        )
        self.dialog.open()

    def close_dialog(self, *args):
        self.dialog.dismiss()

    def go_to_login(self, *args):
        self.dialog.dismiss()
        self.manager.current = "login"


class HomeScreen(Screen):
    def on_enter(self, *args):
        self.load_todos()
        self.load_jadwal_hari_ini()
        self.load_tugas()

    def load_todos(self):
        todo_container = self.ids.todo_container
        todo_container.clear_widgets()

        db = DatabaseManager()
        todos = db.get_todos(self.manager.current_user)

# Pisahkan pending & completed
        pending_todos = [t for t in todos if t.get('status') != 'completed']
        completed_todos = [t for t in todos if t.get('status') == 'completed']

# Gabungkan: pending di atas, completed di bawah
        sorted_todos = pending_todos + completed_todos

        for todo in sorted_todos:
             box = MDBoxLayout(
                orientation='horizontal',
                adaptive_height=True,
                spacing="10dp",
                padding=("8dp","6dp")
    )

             checkbox = MDCheckbox(
                size_hint=(None, None),
                size=("40dp", "40dp"),
                active=True if todo.get('status') == 'completed' else False
    )
             checkbox.bind(active=lambda instance, value, t=todo: self.toggle_todo(t, value))

             label = MDLabel(
                text=todo.get('aktivitas', ''),
                halign="left",
                size_hint_x=0.8
    )

             if todo.get('status') == 'completed':
                 label.theme_text_color = "Secondary"

             edit_icon = MDIconButton(
                icon="pencil",
                size_hint=(None, None),
                size=("32dp", "32dp"),
                icon_size="16dp",
                on_release=lambda x, t=todo: self.edit_todo(t)
    )

             box.add_widget(checkbox)
             box.add_widget(label)
             box.add_widget(edit_icon)

             card = MDCard(
                orientation='horizontal',
                padding="6dp",
                size_hint_y=None,
                height="56dp",
                elevation=0,
                md_bg_color=[0, 0, 0, 0]
    )
             card.add_widget(box)
             todo_container.add_widget(card)


    def toggle_todo(self, todo, value):
        db = DatabaseManager()
        new_status = 'completed' if value else 'pending'
        db.update_todo_status(self.manager.current_user, todo['aktivitas'], new_status)
        self.load_todos()

    def add_todo(self):
        content = MDBoxLayout(orientation="vertical", spacing="12dp", size_hint_y=None, height="50dp")
        aktivitas_field = MDTextField(hint_text="Activity", mode="fill")
        content.add_widget(aktivitas_field)

        def save_todo(_):
            if aktivitas_field.text:
                db = DatabaseManager()
                db.add_todo(self.manager.current_user, aktivitas_field.text)
                self.dialog.dismiss()
                self.load_todos()

        self.dialog = MDDialog(
            title="Add Activity",
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(text="CANCEL", on_release=lambda x: self.dialog.dismiss()),
                MDFlatButton(text="ADD", on_release=save_todo),
            ],
        )
        self.dialog.open()

    def edit_todo(self, todo):
        content = MDBoxLayout(orientation="vertical", spacing="12dp", size_hint_y=None, height="50dp")
        aktivitas_field = MDTextField(hint_text="Activity", mode="fill", text=todo.get('aktivitas', ''))
        content.add_widget(aktivitas_field)

        def save_todo(_):
            if aktivitas_field.text:
                db = DatabaseManager()
                db.update_todo_aktivitas(self.manager.current_user, todo['aktivitas'], aktivitas_field.text)
                self.dialog.dismiss()
                self.load_todos()

        def delete_todo(_):
            db = DatabaseManager()
            db.delete_todo(self.manager.current_user, todo['aktivitas'])
            self.dialog.dismiss()
            self.load_todos()

        self.dialog = MDDialog(
            title="Edit Activity",
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(text="DELETE", on_release=delete_todo, text_color=(1, 0, 0, 1)),
                MDFlatButton(text="CANCEL", on_release=lambda x: self.dialog.dismiss()),
                MDFlatButton(text="SAVE", on_release=save_todo),
            ],
        )
        self.dialog.open()

    def load_jadwal_hari_ini(self):
        jadwal_container = self.ids.jadwal_container
        jadwal_container.clear_widgets()

        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        today = datetime.today().weekday()
        hari_ini = days[today]

        db = DatabaseManager()
        jadwal_list = db.get_jadwal_hari_ini(self.manager.current_user, hari_ini)

        if not jadwal_list:
            card = MDCard(orientation='vertical', padding="8dp", size_hint_y=None, height="56dp", elevation=0, md_bg_color=[0, 0, 0, 0])
            card.add_widget(MDLabel(text="No schedule today", halign="left"))
            jadwal_container.add_widget(card)
        else:
            for jadwal in jadwal_list:
                card = MDCard(orientation='vertical', padding="8dp", size_hint_y=None, height="80dp", spacing="2dp", elevation=0, md_bg_color=[0, 0, 0, 0])
                title_box = MDBoxLayout(orientation='horizontal', adaptive_height=True, spacing="10dp")
                title_label = MDLabel(text=jadwal.get('mata_kuliah', ''), theme_font_style="H6", halign="left", size_hint_x=1)
                title_box.add_widget(title_label)
                card.add_widget(title_box)
                card.add_widget(MDLabel(text=f"Time: {jadwal.get('waktu', '')} | Room: {jadwal.get('ruangan', '')} | Lecturer: {jadwal.get('dosen', '')}", halign="left", theme_text_color="Secondary"))
                jadwal_container.add_widget(card)

    def load_tugas(self):
        tugas_container = self.ids.tugas_container
        tugas_container.clear_widgets()
        db = DatabaseManager()
        tugas_list = db.get_tugas_by_user(self.manager.current_user)

        for tugas in tugas_list:
            card = MDCard(
                orientation='vertical',
                padding="12dp",
                spacing="10dp",
                size_hint_y=None,
                height="120dp",
                elevation=0,
                md_bg_color=[0, 0, 0, 0]
            )

            title_box = MDBoxLayout(orientation='horizontal', adaptive_height=True, spacing="10dp")
            checkbox = MDCheckbox(
                size_hint=(None, None),
                size=("40dp", "40dp"),
                active=True if tugas.get('status') == 'completed' else False
            )
           
            checkbox.bind(active=lambda instance, value, t=tugas: self.toggle_tugas(t, value))

            title_label = MDLabel(text=tugas.get('nama_tugas', ''), 
                                  theme_font_style="H6", 
                                  halign="left", valign="center", 
                                  size_hint_x=0.7, 
                                  size_hint_y=None, 
                                  height="40dp", text_size=(None, None))
            
            if tugas.get('status') == 'completed':
                title_label.theme_text_color = "Secondary"

            edit_icon = MDIconButton(
                icon="pencil",
                size_hint=(None, None),
                size=("32dp", "32dp"),
                icon_size="16dp",
                on_release=lambda x, t=tugas: self.edit_tugas(t)
            )
            title_box.add_widget(checkbox)
            title_box.add_widget(title_label)
            title_box.add_widget(edit_icon)

            card.add_widget(title_box)

            mk_label = MDLabel(
                text=f"Subject: {tugas.get('mata_kuliah', '')}",
                halign="left",
                text_color=(1,1,1,1),
                size_hint_y=None,
                height="20dp",
                text_size=(None, None),
                shorten=True,
                shorten_from="right"
            )
            card.add_widget(mk_label)

            deadline_raw = tugas.get('deadline', '')
           
            deadline_label = MDLabel(
                text=f"Deadline: {deadline_raw}",
                halign="left",
                text_color=(1,1,1,1),
                size_hint_y=None,
                height="20dp",
                text_size=(None, None),
                shorten=True,
                shorten_from="right"
            )
            card.add_widget(deadline_label)
            tugas_container.add_widget(card)

    def toggle_tugas(self, tugas, value):
        db = DatabaseManager()
        new_status = 'completed' if value else 'pending'
        db.update_tugas_status(self.manager.current_user, tugas['nama_tugas'], new_status)
        self.load_tugas()

    def add_tugas(self):
        self.selected_time = None
        self.selected_date = None

        content = MDBoxLayout(orientation="vertical", spacing="12dp", size_hint_y=None, height="250dp")
        nama_field = MDTextField(hint_text="Task/Project Name", mode="fill")
        mk_field = MDTextField(hint_text="Subject", mode="fill")
        date_field = MDTextField(hint_text="Deadline (DD-MM-YYYY)", mode="fill")
        time_field = MDTextField(hint_text="Time (HH:MM)", mode="fill")

        content.add_widget(nama_field)
        content.add_widget(mk_field)
        content.add_widget(date_field)
        content.add_widget(time_field)

        def save_tugas(_):
            if not (nama_field.text and mk_field.text and date_field.text and time_field.text):
                self.dialog = MDDialog(
                    title="Error",
                    text="All fields must be filled.",
                    buttons=[MDFlatButton(text="OK", on_release=lambda x: self.dialog.dismiss())]
                )
                self.dialog.open()
                return
            
            final_deadline = f"{date_field.text}\n{time_field.text} WIB"

            db = DatabaseManager()
            db.add_tugas(
                self.manager.current_user,
                nama_field.text,
                mk_field.text,
                final_deadline
            )

            self.dialog.dismiss()
            self.load_tugas()

        self.dialog = MDDialog(
            title="Add Task/Project",
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(text="CANCEL", on_release=lambda x: self.dialog.dismiss()),
                MDFlatButton(text="ADD", on_release=save_tugas),
            ],
        )
        self.dialog.open()

    def edit_tugas(self, tugas):
        self.selected_time = None
        self.selected_date = None

        content = MDBoxLayout(orientation="vertical", spacing="12dp", size_hint_y=None, height="250dp")
        nama_field = MDTextField(hint_text="Task/Project Name", mode="fill", text=tugas.get('nama_tugas', ''))
        mk_field = MDTextField(hint_text="Subject", mode="fill", text=tugas.get('mata_kuliah', ''))
        date_field = MDTextField(hint_text="Deadline (DD-MM-YYYY)", mode="fill")
        time_field = MDTextField(hint_text="Time (HH:MM)", mode="fill")

        deadline_str = tugas.get('deadline', '')
        if deadline_str:
            try:
                lines = deadline_str.split('\n')
                if len(lines) >= 2:
                    date_part = lines[0]
                    time_part = lines[1].replace('WIB', '')
                    date_field.text = date_part
                    time_field.text = time_part
            except:
                pass

        content.add_widget(nama_field)
        content.add_widget(mk_field)
        content.add_widget(date_field)
        content.add_widget(time_field)

        def save_tugas(_):
            if not (nama_field.text and mk_field.text and date_field.text and time_field.text):
                self.dialog = MDDialog(
                    title="Error",
                    text="All fields must be filled with the correct format.",
                    buttons=[MDFlatButton(text="OK", on_release=lambda x: self.dialog.dismiss())]
                )
                self.dialog.open()
                return

            final_deadline = f"{date_field.text}\n{time_field.text} WIB"

            db = DatabaseManager()
            db.update_tugas(
                self.manager.current_user,
                tugas['nama_tugas'],
                nama_field.text,
                mk_field.text,
                final_deadline
            )

            self.dialog.dismiss()
            self.load_tugas()

        def delete_tugas(_):
            db = DatabaseManager()
            db.delete_tugas(self.manager.current_user, tugas['nama_tugas'])
            self.dialog.dismiss()
            self.load_tugas()

        self.dialog = MDDialog(
            title="Edit Task/Project",
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(text="DELETE", on_release=delete_tugas, text_color=(1, 0, 0, 1)),
                MDFlatButton(text="CANCEL", on_release=lambda x: self.dialog.dismiss()),
                MDFlatButton(text="SAVE", on_release=save_tugas),
            ],
        )
        self.dialog.open()

class JadwalKuliahScreen(Screen):
    def on_enter(self, *args):
        self.load_jadwal()

    def load_jadwal(self):
        jadwal_container = self.ids.jadwal_list_container
        jadwal_container.clear_widgets()
        db = DatabaseManager()
        jadwal_list = db.get_jadwal_by_user(self.manager.current_user)
        for jadwal in jadwal_list:
            card = MDCard(orientation='vertical', 
                          padding="8dp", size_hint_y=None, height="110dp", spacing="6dp", elevation=0, md_bg_color=[0, 0, 0, 0])

            title_box = MDBoxLayout(orientation='horizontal', adaptive_height=True, spacing="10dp")
            title_label = MDLabel(text=jadwal.get('mata_kuliah', ''), theme_font_style="H6", halign="left", size_hint_x=0.8)
            edit_icon = MDIconButton(
                icon="pencil",
                size_hint=(None, None),
                size=("32dp", "32dp"),
                icon_size="16dp",
                on_release=lambda x, j=jadwal: self.edit_jadwal(j)
            )
            title_box.add_widget(title_label)
            title_box.add_widget(edit_icon)

            card.add_widget(title_box)
            card.add_widget(MDLabel(text=f"Day: {jadwal.get('hari','')} | Time: {jadwal.get('waktu','')}", halign="left"))
            card.add_widget(MDLabel(text=f"Room: {jadwal.get('ruangan','')} | Lecturer: {jadwal.get('dosen','')}", 
                                    theme_text_color="Secondary", halign="left"))
            jadwal_container.add_widget(card)

    def show_add_jadwal_dialog(self):
        content = MDBoxLayout(orientation="vertical", spacing="12dp", size_hint_y=None, height="320dp")
        hari_field = MDTextField(hint_text="Day (e.g., Monday)", mode="fill")
        mk_field = MDTextField(hint_text="Subject", mode="fill")
        waktu_field = MDTextField(hint_text="Time (e.g., 08:00-10:00)", mode="fill")
        ruangan_field = MDTextField(hint_text="Room", mode="fill")
        dosen_field = MDTextField(hint_text="Lecturer", mode="fill")
        content.add_widget(hari_field)
        content.add_widget(mk_field)
        content.add_widget(waktu_field)
        content.add_widget(ruangan_field)
        content.add_widget(dosen_field)

        def save_jadwal(_):
            if all([hari_field.text, mk_field.text, waktu_field.text]):
                db = DatabaseManager()
                db.add_jadwal(
                    self.manager.current_user,
                    hari_field.text,
                    mk_field.text,
                    waktu_field.text,
                    ruangan_field.text,
                    dosen_field.text
                )
                self.dialog.dismiss()
                self.load_jadwal()
                home_screen = self.manager.get_screen('home')
                home_screen.load_jadwal_hari_ini()

        self.dialog = MDDialog(
            title="Add Class Schedule",
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(text="CANCEL", on_release=lambda x: self.dialog.dismiss()),
                MDFlatButton(text="ADD", on_release=save_jadwal),
            ],
        )
        self.dialog.open()

    def edit_jadwal(self, jadwal):
        content = MDBoxLayout(orientation="vertical", spacing="12dp", size_hint_y=None, height="320dp")
        hari_field = MDTextField(hint_text="Day (e.g., Monday)", mode="fill", text=jadwal.get('hari', ''))
        mk_field = MDTextField(hint_text="Subject", mode="fill", text=jadwal.get('mata_kuliah', ''))
        waktu_field = MDTextField(hint_text="Time (e.g., 08:00-10:00)", mode="fill", text=jadwal.get('waktu', ''))
        ruangan_field = MDTextField(hint_text="Room", mode="fill", text=jadwal.get('ruangan', ''))
        dosen_field = MDTextField(hint_text="Lecturer", mode="fill", text=jadwal.get('dosen', ''))
        content.add_widget(hari_field)
        content.add_widget(mk_field)
        content.add_widget(waktu_field)
        content.add_widget(ruangan_field)
        content.add_widget(dosen_field)

        def save_jadwal(_):
            if all([hari_field.text, mk_field.text, waktu_field.text]):
                db = DatabaseManager()
                db.update_jadwal(
                    self.manager.current_user,
                    jadwal['mata_kuliah'],
                    hari_field.text,
                    mk_field.text,
                    waktu_field.text,
                    ruangan_field.text,
                    dosen_field.text
                )
                self.dialog.dismiss()
                self.load_jadwal()
                home_screen = self.manager.get_screen('home')
                home_screen.load_jadwal_hari_ini()

        def delete_jadwal(_):
            db = DatabaseManager()
            db.delete_jadwal(self.manager.current_user, jadwal['mata_kuliah'])
            self.dialog.dismiss()
            self.load_jadwal()
            home_screen = self.manager.get_screen('home')
            home_screen.load_jadwal_hari_ini()

        self.dialog = MDDialog(
            title="Edit Class Schedule",
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(text="DELETE", on_release=delete_jadwal, text_color=(1, 0, 0, 1)),
                MDFlatButton(text="CANCEL", on_release=lambda x: self.dialog.dismiss()),
                MDFlatButton(text="SAVE", on_release=save_jadwal),
            ],
        )
        self.dialog.open()


class CalendarScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_month = datetime.now().month
        self.current_year = datetime.now().year
        self.dialog_open = False

    def on_enter(self, *args):
        self.load_month_dropdown()
        self.load_calendar()

    def load_month_dropdown(self):
        months = [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ]
        dropdown = self.ids.month_dropdown
        dropdown.items = months
        dropdown.text = months[self.current_month - 1]

    def on_month_select(self, instance, value):
        months = [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ]
        if value in months:
            self.current_month = months.index(value) + 1
            self.load_calendar()

    def load_calendar(self):
        calendar_grid = self.ids.calendar_grid
        calendar_grid.clear_widgets()
        db = DatabaseManager()
        activities = db.get_kalender_by_month(
            self.manager.current_user,
            self.current_month,
            self.current_year
        )
        cal = calendar.monthcalendar(self.current_year, self.current_month)
        days = ['M', 'T', 'W', 'T', 'F', 'S', 'S']
        for day in days:
            label = MDLabel(text=day, halign="center", theme_text_color="Secondary", size_hint=(None, None), size=("96dp", "20dp"))
            calendar_grid.add_widget(label)
        for week in cal:
            for day in week:
                if day == 0:
                    calendar_grid.add_widget(MDLabel(text=""))
                else:
                    date_str = f"{self.current_year}-{self.current_month:02d}-{day:02d}"
                    box = MDCard(
                        orientation="vertical",
                        size_hint=(None, None),
                        size=("96dp", "96dp"),
                        padding=("4dp", "4dp", "4dp", "4dp"),
                        radius=8,
                        elevation=2,
                        md_bg_color=[0, 0, 0, 0]
            )

                    date_label = MDLabel(text=str(day), halign="center", size_hint_y=None, height="24dp", 
                                         theme_font_style="H6", padding=("0dp", "0dp", "0dp", "-3dp"))
                    box.add_widget(date_label)
                    scroll_view = KScrollView(size_hint=(None, None), size=("88dp", "56dp"), do_scroll_x=True, do_scroll_y=True, bar_width="5dp")
                    scroll_view.background_normal = ''
                    scroll_view.background_color = [0,0,0,0]
                    activities_box = KBoxLayout(orientation='vertical', size_hint=(None, None), size=("200dp", 0), spacing="2dp")

                    if date_str in activities:
                        num_activities = len(activities[date_str])
                        total_height = num_activities * dp(20) + (num_activities - 1) * dp(2) if num_activities > 0 else 0
                        activities_box.height = total_height


                        for act in activities[date_str]:
                            act_label = MDLabel(text=f"• {act['aktivitas']}", halign="left", theme_font_style="Caption", size_hint_y=None, 
                                                height="20dp", size_hint_x=None, width="200dp")
                            activities_box.add_widget(act_label)
                    scroll_view.add_widget(activities_box)
                    box.add_widget(scroll_view)
                    plus_layer = AnchorLayout(
                        anchor_x="right",
                        anchor_y="top",
                        size_hint_y=None,
                        height="16dp",
                        padding=("0dp", "-10dp", "-12dp", "0dp"),  
                    )
                    add_btn = MDIconButton(icon="plus", icon_size="14dp", on_release=lambda x, d=date_str: self.show_add_activity_dialog(d))
                    plus_layer.add_widget(add_btn)
                    box.add_widget(plus_layer)
                    calendar_grid.add_widget(box)

    def refresh_activities(self):
        self.activities_box.clear_widgets()
        db = DatabaseManager()
        activities = db.get_kalender_by_month(self.manager.current_user, self.current_month, self.current_year)
        if self.tanggal in activities and activities[self.tanggal]:
            for act in activities[self.tanggal]:
                card = MDCard(orientation='horizontal', padding="6dp", size_hint_y=None, height="48dp", radius=[8], elevation=0, md_bg_color=[0, 0, 0, 0])
                act_label = MDLabel(text=f"{act['aktivitas']} {act['waktu'] or ''}", halign="left", size_hint_x=0.8, theme_text_color="Primary")
                delete_btn = MDIconButton(icon="delete", size_hint=(None, None), size=("32dp", "32dp"), 
                                          icon_size="20dp", on_release=lambda x, t=self.tanggal, a=act['aktivitas']: self.delete_activity(t, a))
                card.add_widget(act_label)
                card.add_widget(delete_btn)
                self.activities_box.add_widget(card)
        else:
            no_act_label = MDLabel(text="No activities", halign="center", theme_text_color="Secondary")
            self.activities_box.add_widget(no_act_label)

    def show_add_activity_dialog(self, tanggal):
        try:
            if self.dialog_open:
                return  

            self.tanggal = tanggal  

            content = MDBoxLayout(orientation="vertical", spacing="12dp", size_hint_y=None, height="450dp")

            aktivitas_field = MDTextField(hint_text="Activity", mode="fill")
            waktu_field = MDTextField(hint_text="Time (optional)", mode="fill")
            content.add_widget(aktivitas_field)
            content.add_widget(waktu_field)

            def add_activity_inline(_):
                if not aktivitas_field.text:
                    error_dialog = MDDialog(
                        title="Error",
                        text="Activity cannot be empty.",
                        buttons=[MDFlatButton(text="OK", on_release=lambda x: error_dialog.dismiss())],
                    )
                    error_dialog.open()
                    return

                try:
                    db = DatabaseManager()
                    db.add_kalender_aktivitas(self.manager.current_user, tanggal, aktivitas_field.text, waktu_field.text)
                    aktivitas_field.text = ""
                    waktu_field.text = ""
                    self.refresh_activities()
                    self.load_calendar()
                except Exception as e:
                    error_dialog = MDDialog(
                        title="Error",
                        text=f"Failed to add activity: {str(e)}",
                        buttons=[MDFlatButton(text="OK", on_release=lambda x: error_dialog.dismiss())],
                    )
                    error_dialog.open()

            content.add_widget(MDFlatButton(text="ADD", on_release=add_activity_inline))

            db = DatabaseManager()
            activities = db.get_kalender_by_month(self.manager.current_user, self.current_month, self.current_year)
            content.add_widget(MDLabel(text="Existing activities:", theme_font_style="H6"))
            activities_scroll = KScrollView(size_hint=(1, None), height="250dp")  
            self.activities_box = MDBoxLayout(orientation='vertical', spacing="5dp", adaptive_height=True)  
            if tanggal in activities and activities[tanggal]:
                for act in activities[tanggal]:
                    card = MDCard(orientation='horizontal', padding="6dp", size_hint_y=None, height="48dp", radius=[8], 
                                  elevation=0, md_bg_color=[0, 0, 0, 0])
                    act_label = MDLabel(text=f"{act['aktivitas']} {act['waktu'] or ''}", halign="left", size_hint_x=0.8, theme_text_color="Primary")
                    delete_btn = MDIconButton(icon="delete", size_hint=(None, None), size=("32dp", "32dp"), icon_size="20dp", 
                                              on_release=lambda x, t=tanggal, a=act['aktivitas']: self.delete_activity(t, a))
                    card.add_widget(act_label)
                    card.add_widget(delete_btn)
                    self.activities_box.add_widget(card)
            else:
                no_act_label = MDLabel(text="No activities", halign="center", theme_text_color="Secondary")
                self.activities_box.add_widget(no_act_label)
            activities_scroll.add_widget(self.activities_box)
            content.add_widget(activities_scroll)

            def dismiss_dialog(_):
                self.dialog.dismiss()
                self.dialog_open = False

            def save_and_close(_):
                dismiss_dialog(None)
                self.load_calendar()

            self.dialog = MDDialog(
                title=f"Activities for {tanggal}",
                type="custom",
                content_cls=content,
                buttons=[
                    MDFlatButton(text="CANCEL", on_release=dismiss_dialog),
                    MDFlatButton(text="SAVE", on_release=save_and_close),
                ],
            )
            self.dialog.open()
            self.dialog_open = True
        except Exception as e:
            print(f"Error in show_add_activity_dialog: {e}")
            error_dialog = MDDialog(
                title="Error",
                text=f"An error occurred: {str(e)}",
                buttons=[MDFlatButton(text="OK", on_release=lambda x: error_dialog.dismiss())],
            )
            error_dialog.open()

    def delete_activity(self, tanggal, aktivitas):
        try:
            db = DatabaseManager()
            db.delete_kalender_aktivitas(self.manager.current_user, tanggal, aktivitas)
            self.refresh_activities()
            self.load_calendar()
        except Exception as e:
            print(f"Error deleting activity: {e}")
            error_dialog = MDDialog(
                title="Error",
                text=f"Failed to delete activity: {str(e)}",
                buttons=[MDFlatButton(text="OK", on_release=lambda x: error_dialog.dismiss())],
            )
            error_dialog.open()

class ProfileScreen(Screen):
    def on_enter(self, *args):
        self.load_profile()

    def load_profile(self):
        db = DatabaseManager()
        profile = db.get_profile(self.manager.current_user)
        if profile:
            self.ids.nama_field.text = profile.get('nama', '')
            self.ids.nim_field.text = profile.get('nim', '')
            self.ids.ipk_field.text = profile.get('ipk', '')

    def save_profile(self):
        nama = self.ids.nama_field.text
        nim = self.ids.nim_field.text
        ipk = self.ids.ipk_field.text
        db = DatabaseManager()
        db.update_profile(self.manager.current_user, nama, nim, ipk)
        self.show_success_dialog("Success", "Profile saved successfully!")

    def show_success_dialog(self, title, text):
        self.dialog = MDDialog(title=title, text=text, buttons=[MDFlatButton(text="OK", on_release=lambda x: self.dialog.dismiss())])
        self.dialog.open()

    def logout(self):
        self.manager.current_user = ""
        self.manager.current = 'login'

class MyreApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "DeepPurple"
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.accent_palette = "Amber"
        Builder.load_file('myre.kv')
        sm = MyreScreenManager()
        sm.add_widget(WelcomeScreen(name='welcome'))  
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(RegisterScreen(name='register'))
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(JadwalKuliahScreen(name='jadwal'))
        sm.add_widget(CalendarScreen(name='calendar'))
        sm.add_widget(ProfileScreen(name='profile'))
        return sm

if __name__ == '__main__':
    db = DatabaseManager()
    MyreApp().run()