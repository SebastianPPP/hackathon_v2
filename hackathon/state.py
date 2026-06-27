import reflex as rx
from reflex.model import Model
from datetime import datetime
from typing import List
import random
import httpx
import os
import base64
import json
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from google import genai

# Ładowanie zmiennych środowiskowych z pliku .env
load_dotenv()

# Inicjalizacja klienta Google GenAI (automatycznie zaciąga klucz ze środowiska)
client = genai.Client()

# ==========================================
# 1. MODELE BAZY DANYCH I STRUKTURDANYCH
# ==========================================

class Kaucjomat(BaseModel):
    id: int
    name: str
    address: str
    lat: float
    lng: float
    rating: float
    fill_level: int  
    distance_calculated: float = 0.0


class UserProfile(Model, table=True):
    """Tabela użytkowników w bazie danych z polami konfiguracji"""
    username: str
    password_hash: str
    nick: str
    city: str = "Gdańsk"
    district: str = ""
    eco_points: int = 0
    bottles_returned: int = 0
    co2_saved: float = 0.0
    # Pola ustawień zapisywane permanentnie w bazie:
    settings_theme: str = "Ciemny"
    settings_font_size: str = "Średnia"
    settings_language: str = "Polski"


class ScanHistory(Model, table=True):
    """Tabela historii zwrotów/skanowań odpadów"""
    user_id: int
    item_name: str
    points_gained: int
    scanned_at: datetime = datetime.utcnow()


class VoucherAnalysis(BaseModel):
    """Definicja zaawansowanego schematu dla Gemini OCR z podziałem na frakcje"""
    is_clear_voucher: bool = Field(description="Czy zdjęcie przedstawia czytelny i wyraźny voucher z butelkomatu?")
    pet_bottles_count: int = Field(default=0, description="Liczba zwróconych butelek plastikowych (PET)")
    aluminum_cans_count: int = Field(default=0, description="Liczba zwróconych puszek aluminiowych")
    glass_bottles_count: int = Field(default=0, description="Liczba zwróconych butelek szklanych")
    total_refund: float = Field(default=0.0, description="Łączna kwota zwrotu / kaucji wypłacona użytkownikowi")


# ==========================================
# 2. STAN GŁÓWNY APLIKACJI
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

    # --- Ustawienia aplikacji (Bufor formularza) ---
    settings_theme: str = "Ciemny"       
    settings_font_size: str = "Średnia"  
    settings_language: str = "Polski"    

    # --- Pola lokalizacyjne (Domyślnie Gdańsk Wrzeszcz) ---
    user_lat: float = 54.3812
    user_lng: float = 18.6042
    gps_status: str = "Oczekiwanie na GPS..."

    # --- Filtry kaucjomatów ---
    filter_sort_by: str = "najbliżej"
    filter_max_fill: int = 100         
    filter_min_rating: float = 1.0     

    # --- Statyczna baza kaucjomatów ---
    all_kaucjomaty: List[Kaucjomat] = [
        Kaucjomat(id=1, name="Kaucjomat EkoCentrum", address="Grunwaldzka 102, Gdańsk", lat=54.3832, lng=18.6012, rating=4.8, fill_level=45),
        Kaucjomat(id=2, name="Butelkomat Galeria Bałtycka", address="Dmowskiego 7, Gdańsk", lat=54.3801, lng=18.6085, rating=3.9, fill_level=85),
        Kaucjomat(id=3, name="Zielony Punkt Żabka", address="Jaśkowa Dolina 12, Gdańsk", lat=54.3785, lng=18.5990, rating=4.5, fill_level=20),
        Kaucjomat(id=4, name="Kaucjomat MegaRecycle", address="Kościuszki 45, Gdańsk", lat=54.3890, lng=18.6120, rating=4.2, fill_level=95),
        Kaucjomat(id=5, name="Eko-Punkt Biedronka", address="Chrobrego 11, Gdańsk", lat=54.3850, lng=18.5950, rating=4.7, fill_level=75),
    ]

    filtered_kaucjomaty: List[Kaucjomat] = []
    selected_kaucjomat: List[Kaucjomat] = []

    # --- Pola formularzy ---
    login_username: str = ""
    login_password: str = ""
    reg_nick: str = ""
    reg_username: str = ""
    reg_password: str = ""
    reg_confirm_password: str = ""
    reg_city: str = ""
    reg_district: str = ""

    # --- Profil ---
    profile_photo: str = ""
    profile_nick: str = ""
    profile_city: str = ""
    profile_district: str = ""
    profile_password: str = ""
    profile_saved: bool = False
    show_success: bool = False
    
    current_user_id: int = 0

    @rx.var
    def current_user(self) -> List[UserProfile]:
        if self.current_user_id == 0:
            return []
        with rx.session() as session:
            user = session.exec(UserProfile.select().where(UserProfile.id == self.current_user_id)).first()
            return [user] if user else []

    def start_app(self):
        self.is_started = True

    def toggle_sidebar(self):
        self.sidebar_open = not self.sidebar_open

    # --- Settery ustawień (Modyfikują stan lokalny) ---
    def toggle_theme(self):
        self.settings_theme = "Jasny" if self.settings_theme == "Ciemny" else "Ciemny"

    def set_font_size(self, val: str):
        self.settings_font_size = val

    def set_language(self, val: str):
        self.settings_language = val

    # --- TRWAŁY ZAPIS USTAWIEŃ W BAZIE ---
    def save_settings(self):
        if self.current_user_id == 0:
            return rx.window_alert("Musisz być zalogowany!")
        
        with rx.session() as session:
            db_user = session.exec(UserProfile.select().where(UserProfile.id == self.current_user_id)).first()
            if db_user:
                db_user.settings_theme = self.settings_theme
                db_user.settings_font_size = self.settings_font_size
                db_user.settings_language = self.settings_language
                session.add(db_user)
                session.commit()
                return rx.window_alert("⚙️ Ustawienia zostały pomyślnie zapisane w bazie danych!")

    # --- Logika Autentykacji ---
    def login(self):
        if not self.login_username or not self.login_password:
            return rx.window_alert("Wypełnij wszystkie pola!")

        with rx.session() as session:
            user = session.exec(UserProfile.select().where(UserProfile.username == self.login_username)).first()
            if user and user.password_hash == self.login_password:
                self.current_user_id = int(user.id)
                self.is_logged_in = "true"
                self.eco_points = user.eco_points
                self.bottles_returned = user.bottles_returned
                self.co2_saved = user.co2_saved
                # Ładujemy zapisane preferencje z bazy do pól formularza
                self.settings_theme = user.settings_theme
                self.settings_font_size = user.settings_font_size
                self.settings_language = user.settings_language
                return rx.redirect("/home")
            return rx.window_alert("Błędny login lub hasło!")

    def register(self):
        if not self.reg_nick or not self.reg_username or not self.reg_password:
            return rx.window_alert("Wypełnij wymagane pola!")
        if self.reg_password != self.reg_confirm_password:
            return rx.window_alert("Hasła nie są identyczne!")

        with rx.session() as session:
            existing = session.exec(UserProfile.select().where(UserProfile.username == self.reg_username)).first()
            if existing: return rx.window_alert("Użytkownik już istnieje!")

            new_user = UserProfile(
                username=self.reg_username, password_hash=self.reg_password, nick=self.reg_nick,
                city=self.reg_city if self.reg_city else "Gdańsk", district=self.reg_district,
                settings_theme="Ciemny", settings_font_size="Średnia", settings_language="Polski"
            )
            session.add(new_user)
            session.commit()
            self.reg_nick, self.reg_username, self.reg_password, self.reg_confirm_password = "", "", "", ""
            return [rx.window_alert("Konto utworzone pomyślnie! Zaloguj się."), rx.redirect("/")]

    # --- Skanowanie AI ---
    async def handle_photo(self, files: list[rx.UploadFile]):
        if self.current_user_id == 0: return rx.window_alert("Błąd: Zaloguj się!")
        for file in files:
            raw_data = await file.read()
            self.photo_data = f"data:image/jpeg;base64,{base64.b64encode(raw_data).decode()}"
            try:
                response = client.models.generate_content(
                    model='gemini-2.5-pro',
                    contents=[genai.types.Part.from_bytes(data=raw_data, mime_type="image/jpeg"), "Przeanalizuj voucher z kaucjomatu. Wyciągnij osobną liczbę butelek plastikowych PET, puszek i szkła."],
                    config=genai.types.GenerateContentConfig(response_mime_type="application/json", response_schema=VoucherAnalysis, temperature=0.1),
                )
                result = VoucherAnalysis.model_validate_json(response.text)
                if not result.is_clear_voucher: return rx.window_alert("Zdjęcie nieczytelne. Zrób zdjęcie w lepszej jakości! 📸")
                total_items = result.pet_bottles_count + result.aluminum_cans_count + result.glass_bottles_count
                if total_items > 0:
                    added_points = (result.pet_bottles_count * 50) + (result.aluminum_cans_count * 40) + (result.glass_bottles_count * 60)
                    added_co2 = round((result.pet_bottles_count * 0.08) + (result.aluminum_cans_count * 0.09) + (result.glass_bottles_count * 0.12), 2)
                    self.bottles_returned += total_items
                    self.eco_points += added_points
                    self.co2_saved = round(self.co2_saved + added_co2, 2)
                    with rx.session() as session:
                        db_user = session.exec(UserProfile.select().where(UserProfile.id == self.current_user_id)).first()
                        if db_user:
                            db_user.bottles_returned += total_items
                            db_user.eco_points += added_points
                            db_user.co2_saved = round(db_user.co2_saved + added_co2, 2)
                            session.add(db_user)
                            session.commit()
                    return rx.window_alert(f"🌱 Zapisano! Dodano: +{added_points} Eco-Punktów!")
                return rx.window_alert("Nie odnaleziono opakowań. Zrób zdjęcie w lepszej jakości.")
            except Exception as e:
                return rx.window_alert("Nie udało się odczytać dokumentu. Zrób zdjęcie w lepszej jakości!")

    async def save_scan(self):
        if self.current_user_id == 0:
            yield rx.window_alert("Błąd: Musisz być zalogowany!")
            return
        self.eco_points += 50
        self.bottles_returned += 1
        self.co2_saved = round(self.co2_saved + 0.08, 2)
        with rx.session() as session:
            db_user = session.exec(UserProfile.select().where(UserProfile.id == self.current_user_id)).first()
            if db_user:
                db_user.eco_points += 50
                db_user.bottles_returned += 1
                db_user.co2_saved = round(db_user.co2_saved + 0.08, 2)
                session.add(db_user)
                session.commit()
        self.daily_fact = "Ładowanie ekologicznej ciekawostki..."
        self.current_tab = "ciekawostki"
        yield
        try:
            response = await client.aio.models.generate_content(model='gemini-2.5-pro', contents="Podaj jedną krótką ciekawostkę o recyklingu po polsku. Maksymalnie 2 zdania.")
            self.daily_fact = response.text
        except Exception:
            self.daily_fact = "Recykling chroni naszą planetę! Dobra robota!"

    # --- Geolokalizacja ---
    def trigger_gps_fetch(self):
        self.gps_status = "Pobieranie pozycji GPS..."
        return rx.call_script(
            "new Promise((resolve) => {"
            "    if (!navigator.geolocation) { resolve(JSON.stringify({error: 'Brak wsparcia'})); }"
            "    navigator.geolocation.getCurrentPosition("
            "        (p) => resolve(JSON.stringify({lat: p.coords.latitude, lng: p.coords.longitude})),"
            "        (e) => resolve(JSON.stringify({error: e.message}))"
            "    );"
            "})", callback=State.handle_gps_callback
        )

    def handle_gps_callback(self, result_json: str):
        try:
            import json
            data = json.loads(result_json)
            if "error" in data: self.set_gps_error(data["error"])
            else: self.update_location(data["lat"], data["lng"])
        except Exception as e: self.set_gps_error(str(e))

    def update_location(self, lat: float, lng: float):
        self.user_lat, self.user_lng = float(lat), float(lng)
        self.gps_status = "Pozycja zsynchronizowana z GPS"
        self.search_best_kaucjomat()

    def set_gps_error(self, error_msg: str):
        self.user_lat, self.user_lng = 54.3812, 18.6042
        self.gps_status = "Użyto lokalizacji domyślnej (Gdańsk Wrzeszcz)"
        self.search_best_kaucjomat()

    def set_filter_sort_by(self, val: str): self.filter_sort_by = val; self.search_best_kaucjomat()
    def set_filter_max_fill(self, val: int): self.filter_max_fill = int(val); self.search_best_kaucjomat()
    def set_filter_min_rating(self, val: float): self.filter_min_rating = float(val); self.search_best_kaucjomat()

    def select_kaucjomat_marker(self, kaucjomat_id: int):
        for k in self.all_kaucjomaty:
            if k.id == kaucjomat_id:
                dx, dy = (k.lat - self.user_lat) * 111, (k.lng - self.user_lng) * 111
                k.distance_calculated = round((dx**2 + dy**2)**0.5, 2)
                self.selected_kaucjomat = [k]
                break

    def search_best_kaucjomat(self):
        result_list = []
        for k in self.all_kaucjomaty:
            dx, dy = (k.lat - self.user_lat) * 111, (k.lng - self.user_lng) * 111
            k.distance_calculated = round((dx**2 + dy**2)**0.5, 2)
            if k.fill_level > self.filter_max_fill or k.rating < self.filter_min_rating: continue
            result_list.append(k)
        if self.filter_sort_by == "najbliżej": result_list.sort(key=lambda x: x.distance_calculated)
        elif self.filter_sort_by == "najwyższa ocena": result_list.sort(key=lambda x: x.rating, reverse=True)
        elif self.filter_sort_by == "najmniej zapełnione": result_list.sort(key=lambda x: x.fill_level)
        self.filtered_kaucjomaty = result_list

    def set_tab(self, tab_name: str):
        self.current_tab = tab_name
        self.photo_data = ""
        self.profile_photo = ""

    def logout(self):
        self.current_user_id, self.is_logged_in, self.login_username, self.login_password = 0, "false", "", ""
        self.photo_data, self.profile_photo = "", ""
        return rx.redirect("/")

    def change_username(self, val: str): self.login_username = val
    def change_password(self, val: str): self.login_password = val
    def change_reg_nick(self, val: str): self.reg_nick = val
    def change_reg_username(self, val: str): self.reg_username = val
    def change_reg_password(self, val: str): self.reg_password = val
    def change_reg_confirm_password(self, val: str): self.reg_confirm_password = val
    def change_reg_city(self, val: str): self.reg_city = val
    def change_reg_district(self, val: str): self.reg_district = val
    def check_auth(self):
        if self.is_logged_in == "true" and self.router.page.path == "/": return rx.redirect("/home")
        if self.is_logged_in == "false" and self.router.page.path != "/": return rx.redirect("/")

    def set_profile_nick(self, value: str): self.profile_nick = value
    def set_profile_city(self, value: str): self.profile_city = value
    def set_profile_district(self, value: str): self.profile_district = value
    def set_profile_password(self, value: str): self.profile_password = value
    async def handle_profile_photo(self, files: list[rx.UploadFile]):
        for file in files: self.profile_photo = f"data:image/jpeg;base64,{base64.b64encode(await file.read()).decode()}"
    async def save_profile(self):
        self.profile_saved = True; yield; import asyncio; await asyncio.sleep(2); self.profile_saved = False

    # --- System Questów ---
    quest_walk_progress: float = 0.0      # Postęp spaceru w km (symulacja)
    riddle_answered: bool = False         # Czy użytkownik odpowiedział już na zagadkę
    riddle_selected_ans: str = ""         # Wybrana odpowiedź

    @rx.var
    def quest_bottles_tier(self) -> int:
        """Wylicza aktualny poziom (tier) zadania ilościowego na podstawie bazy danych"""
        # 5 szt = Tier 1, 10 szt = Tier 2, 15 szt = Tier 3, 20 szt = Tier 4
        if self.bottles_returned >= 20: return 4
        if self.bottles_returned >= 15: return 3
        if self.bottles_returned >= 10: return 2
        if self.bottles_returned >= 5: return 1
        return 0

    # 1. Quest Sportowy: Symulacja postępu GPS/Kroków
    def advance_walk(self):
        """Symuluje przejście dystansu (np. integracja z akcelerometrem/GPS)"""
        if self.quest_walk_progress >= 5.0:
            return rx.window_alert("To zadanie zostało już ukończone! 🏆")
            
        self.quest_walk_progress = round(self.quest_walk_progress + 1.2, 1)
        
        if self.quest_walk_progress >= 5.0:
            self.quest_walk_progress = 5.0
            self.eco_points += 300
            self._db_add_points(300)
            return rx.window_alert("🏅 Zadanie Sportowe Ukończone! Zdobywasz +300 Eco-Punktów za spacer 5km!")

    # 2. Quest Ilościowy: Odbiór nagrody za próg (wywoływany przyciskiem)
    def claim_quantity_reward(self, tier: int):
        """Przyznaje dodatkowy bonus XP za osiągnięcie kamieni milowych recyklingu"""
        # Sprawdzamy, czy użytkownik ma uprawnienia do danego Tieru
        if self.quest_bottles_tier < tier:
            return rx.window_alert("Nie osiągnąłeś jeszcze tego progu! Wrzuć więcej butelek. 🍾")
            
        # Przykładowe nagrody bonusowe za progi
        rewards = {1: 100, 2: 250, 3: 450, 4: 700}
        bonus = rewards.get(tier, 0)
        
        self.eco_points += bonus
        self._db_add_points(bonus)
        return rx.window_alert(f"🎉 Odebrano nagrodę dodatkową za próg! +{bonus} XP dopisane do bazy!")

    # 3. Quest-Zagadka: Weryfikacja odpowiedzi
    def check_riddle(self, answer: str):
        if self.riddle_answered:
            return rx.window_alert("Odpowiedziałeś już na tę zagadkę!")
            
        self.riddle_selected_ans = answer
        self.riddle_answered = True
        
        if answer == "A":
            self.eco_points += 150
            self._db_add_points(150)
            return rx.window_alert("🧠 Brawo! Prawidłowa odpowiedź! Zyskujesz +150 Eco-Punktów.")
        else:
            return rx.window_alert("Niestety to błędna odpowiedź! Spróbuj ponownie przy kolejnej zagadce. 🔬")

    def _db_add_points(self, points: int):
        """Pomocnicza metoda aktualizująca stan punktów bezpośrednio w bazie danych SQLite"""
        if self.current_user_id == 0: return
        with rx.session() as session:
            db_user = session.exec(UserProfile.select().where(UserProfile.id == self.current_user_id)).first()
            if db_user:
                db_user.eco_points += points
                session.add(db_user)
                session.commit()
    @rx.var
    def quest_walk_percentage(self) -> int:
        """Przelicza kilometry na procenty (0-100) jako czysty int dla rx.progress"""
        return int(self.quest_walk_progress * 20)
        
    @rx.var
    def ranking_list(self) -> List[dict]:
        """Pobiera użytkowników z bazy, sortuje po punktach i tworzy listę do rankingu"""
        with rx.session() as session:
            # Pobieramy wszystkich zarejestrowanych użytkowników z bazy
            users = session.exec(UserProfile.select()).all()
            
            if not users:
                return []
                
            # Sortujemy użytkowników malejąco według liczby punktów
            users_sorted = sorted(users, key=lambda u: u.eco_points, reverse=True)
            
            result = []
            for idx, user in enumerate(users_sorted):
                # Jeśli to aktualnie zalogowany użytkownik, podpisujemy go jako "Ty"
                is_me = (self.current_user_id != 0 and user.id == self.current_user_id)
                display_name = "Ty" if is_me else user.nick
                
                result.append({
                    "place": idx + 1,
                    "name": display_name,
                    "points": user.eco_points,
                    "bottles": user.bottles_returned
                })
                
            return result