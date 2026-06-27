# Zmień import na samym górze pliku:
import reflex as rx
from reflex.model import Model  # <--- Dodaj ten konkretny import
from datetime import datetime
from typing import List
import random
import httpx
import os
from dotenv import load_dotenv
from google import genai
load_dotenv()
client = genai.Client()
# ==========================================
# 1. MODELE BAZY DANYCH (SKŁADNIA REFLEX 0.9)
# ==========================================

class UserProfile(Model, table=True):  # <--- Teraz table=True zadziała poprawnie z tym importem!
    """Tabela użytkowników w bazie danych"""
    username: str
    password_hash: str
    nick: str
    city: str = "Gdańsk"
    district: str = ""
    eco_points: int = 0
    bottles_returned: int = 0
    co2_saved: float = 0.0


class ScanHistory(Model, table=True):  # <--- Tutaj też zmieniamy
    """Tabela historii zwrotów/skanowań odpadów"""
    user_id: int
    item_name: str
    points_gained: int
    scanned_at: datetime = datetime.utcnow()

# ==========================================
# 2. STAN APLIKACJI
# ==========================================

class State(rx.State):
    is_started: bool = False
    sidebar_open: bool = False
    is_logged_in: str = rx.LocalStorage("false", name="is_logged_in")
    current_tab: str = "home"
    
    eco_points: int = 0
    bottles_returned: int = 0
    co2_saved: float = 0.0
    photo_data: str = ""
    daily_fact: str = ""

    # --- Pola formularza logowania ---
    login_username: str = ""
    login_password: str = ""

    # --- Pola formularza rejestracji ---
    reg_nick: str = ""
    reg_username: str = ""
    reg_password: str = ""
    reg_confirm_password: str = ""
    reg_city: str = ""
    reg_district: str = ""

    profile_photo: str = ""
    profile_nick: str = ""
    profile_city: str = ""
    profile_district: str = ""
    profile_password: str = ""
    profile_saved: bool = False
    
    show_success: bool = False
    
    # Bezpieczna deklaracja typu listy akceptowana przez starsze wersje Reflexa
    current_user: List[UserProfile] = []

    def start_app(self):
        self.is_started = True

    def toggle_sidebar(self):
        self.sidebar_open = not self.sidebar_open

    def set_tab(self, tab_name: str):
        self.current_tab = tab_name

    def scan_receipt_simulation(self):
        """Symulacja zrobienia zdjęcia paragonu i odczytu przez AI (OCR)"""
        self.eco_points += 50
        self.bottles_returned += 1

    # --- Setters ---
    def change_username(self, val: str): self.login_username = val
    def change_password(self, val: str): self.login_password = val
    
    def change_reg_nick(self, val: str): self.reg_nick = val
    def change_reg_username(self, val: str): self.reg_username = val
    def change_reg_password(self, val: str): self.reg_password = val
    def change_reg_confirm_password(self, val: str): self.reg_confirm_password = val
    def change_reg_city(self, val: str): self.reg_city = val
    def change_reg_district(self, val: str): self.reg_district = val

    # --- Kontrola dostępu ---
    def check_auth(self):
        """Zabezpieczenie przed ponownym logowaniem aktywnych sesji"""
        if self.is_logged_in == "true":
            return rx.redirect("/home")

    # --- Logika biznesowa ---
    def login(self):
        """Weryfikacja logowania z bazy danych"""
        if not self.login_username or not self.login_password:
            return rx.window_alert("Wypełnij wszystkie pola!")

        with rx.session() as session:
            user = session.exec(
                UserProfile.select().where(UserProfile.username == self.login_username)
            ).first()

            if user and user.password_hash == self.login_password:
                self.current_user = [user]
                self.is_logged_in = "true"
                self.eco_points = user.eco_points
                self.bottles_returned = user.bottles_returned
                self.co2_saved = user.co2_saved
                return rx.redirect("/home")
            else:
                return rx.window_alert("Błędny login lub hasło!")

    def register(self):
        """Proces rejestracji nowego użytkownika"""
        if not self.reg_nick or not self.reg_username or not self.reg_password:
            return rx.window_alert("Wypełnij wymagane pola (Login, Email, Hasło)!")
            
        if self.reg_password != self.reg_confirm_password:
            return rx.window_alert("Hasła nie są identyczne!")

        with rx.session() as session:
            existing = session.exec(
                UserProfile.select().where(UserProfile.username == self.reg_username)
            ).first()
            if existing:
                return rx.window_alert("Użytkownik o tym adresie Email już istnieje!")

            new_user = UserProfile(
                username=self.reg_username,
                password_hash=self.reg_password,
                nick=self.reg_nick,
                city=self.reg_city if self.reg_city else "Gdańsk",
                district=self.reg_district,
                eco_points=0,
                bottles_returned=0,
                co2_saved=0.0
            )
            session.add(new_user)
            session.commit()
            
            self.reg_nick = ""
            self.reg_username = ""
            self.reg_password = ""
            self.reg_confirm_password = ""
            
            return [rx.window_alert("Konto utworzone pomyślnie! Zaloguj się."), rx.redirect("/")]

    def logout(self):
        """Wylogowanie - czyszczenie listy stanowej zamiast przypisywania None"""
        self.current_user = []
        self.is_logged_in = "false"
        self.login_username = ""
        self.login_password = ""
        return rx.redirect("/")
    
    async def handle_photo(self, files: list[rx.UploadFile]):
        """Obsługa przesyłania zdjęcia butelki/paragonu i naliczenie punktów"""
        for file in files:
            data = await file.read()
            self.photo_data = f"data:image/jpeg;base64,{__import__('base64').b64encode(data).decode()}"
        self.eco_points += 50
        self.bottles_returned += 1
        self.co2_saved = round(self.co2_saved + 0.08, 2)

    
    async def save_scan(self):
        self.eco_points += 50
        self.bottles_returned += 1
        self.co2_saved = round(self.co2_saved + 0.08, 2)
        self.daily_fact = "Ładowanie ciekawostki..."
        self.current_tab = "ciekawostki"
        yield
        
        # Treść promptu
        prompt = (
            f"Podaj jedną krótką ciekawostkę ekologiczną po polsku związaną z recyklingiem butelek. "
            f"Użytkownik właśnie zwrócił {self.bottles_returned} butelek i zaoszczędził {self.co2_saved} kg CO₂. "
            f"Maksymalnie 2 zdania."
        )
        
        try:
            # Asynchroniczne wywołanie darmowego i szybkiego modelu Gemini 2.5 Flash
            response = await client.aio.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
            )
            
            # Przypisanie wygenerowanego tekstu
            self.daily_fact = response.text
        except Exception as e:
            self.daily_fact = "Nie udało się załadować ciekawostki, ale dobra robota!"
            print(f"Błąd Gemini API: {e}")

    def set_profile_nick(self, value: str):
        self.profile_nick = value

    def set_profile_city(self, value: str):
        self.profile_city = value

    def set_profile_district(self, value: str):
        self.profile_district = value

    def set_profile_password(self, value: str):
        self.profile_password = value

    async def handle_profile_photo(self, files: list[rx.UploadFile]):
        for file in files:
            data = await file.read()
            import base64
            self.profile_photo = f"data:image/jpeg;base64,{base64.b64encode(data).decode()}"

    async def save_profile(self):
        self.profile_saved = True
        yield
        import asyncio
        await asyncio.sleep(2)
        self.profile_saved = False

