import reflex as rx

# --- STAN APLIKACJI (Zarządzanie telefonem i AI) ---
class State(rx.State):
    is_started: bool = False
    sidebar_open: bool = False
    current_tab: str = "home"  # Kontroluje, co wyświetla się na ekranie telefonu
    eco_points: int = 1250
    bottles_returned: int = 42
    co2_saved: float = 3.4

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
        self.co2_saved = round(self.co2_saved + 0.08, 2)


# --- WIDOKI EKRANÓW (Zmieniane dynamicznie w telefonie) ---

def home_screen():
    """Ekran Główny Dashboardu"""
    return rx.vstack(
        # Banner psychologiczny (Poczucie sprawczości)
        rx.box(
            rx.heading("Twoja mikro-sprawczość", class_name="text-lg font-bold text-emerald-300 mb-1"),
            rx.text(
                "Każdy mały krok redukuje eko-lęk i buduje stabilniejszą przyszłość.",
                class_name="text-xs text-slate-400"
            ),
            class_name="bg-slate-800/60 border border-emerald-500/10 p-4 rounded-xl w-full"
        ),

        # Mini-Siatka ze statystykami na telefon (2 kolumny)
        rx.grid(
            rx.box(
                rx.text("Eco-Punkty", class_name="text-xs text-slate-400 uppercase font-medium"),
                rx.text(f"{State.eco_points} XP", class_name="text-2xl font-black text-emerald-400 mt-1"),
                rx.text("↑ Poziom 4", class_name="text-[10px] text-emerald-500 font-bold block"),
                class_name="bg-slate-800/80 border border-slate-700 p-4 rounded-xl"
            ),
            rx.box(
                rx.text("Oszczędzone CO₂", class_name="text-xs text-slate-400 uppercase font-medium"),
                rx.text(f"{State.co2_saved} kg", class_name="text-2xl font-black text-emerald-300 mt-1"),
                rx.text("= 1 zasadzone drzewo", class_name="text-[10px] text-slate-400 block"),
                class_name="bg-slate-800/80 border border-slate-700 p-4 rounded-xl"
            ),
            columns="2",
            gap="3",
            class_name="w-full"
        ),

        # Sekcja grywalizacyjna (Wirtualny las)
        rx.box(
            rx.vstack(
                rx.text("🌲 Twój Cyfrowy Las EcoSphere", class_name="text-xs font-bold text-emerald-400 tracking-wider uppercase"),
                rx.center(
                    rx.text("🌳 🪵 🌿 🌲 🌱", class_name="text-4xl py-4 animate-bounce"),
                    class_name="w-full bg-slate-950/40 rounded-lg border border-slate-800/50 my-2"
                ),
                rx.text("Zwróć jeszcze 2 butelki, aby posadzić kolejne drzewo!", class_name="text-center text-xs text-slate-400"),
                align="center",
                class_name="w-full"
            ),
            class_name="bg-slate-800/40 border border-slate-700/50 p-4 rounded-xl w-full"
        ),
        space="4",
        class_name="w-full px-4 pt-16 pb-24"
    )

def map_screen():
    """Ekran Mapy Miejskiej"""
    return rx.vstack(
        rx.heading("Mapa Kaucjomatów", class_name="text-xl font-bold text-emerald-400"),
        rx.text("Znajdź najbliższy wolny punkt zwrotu OZE w Gdańsku", class_name="text-xs text-slate-400 text-center"),
        rx.center(
            rx.vstack(
                rx.text("🗺️", class_name="text-5xl animate-pulse"),
                rx.text("[ Interaktywna mapa OpenStreetMap ]", class_name="text-xs text-emerald-500/80 font-mono mt-2"),
                align="center"
            ),
            class_name="w-full h-64 bg-slate-950/60 rounded-xl border border-slate-800 flex items-center justify-center"
        ),
        space="4",
        class_name="w-full px-4 pt-16 pb-24"
    )

def scan_screen():
    """Ekran Skanowania AI (OCR)"""
    return rx.vstack(
        rx.heading("Skanuj Paragon (AI OCR)", class_name="text-xl font-bold text-emerald-400"),
        rx.text("Zrób zdjęcie paragonu z kaucjomatu, aby system automatycznie naliczył punkty.", class_name="text-xs text-slate-400 text-center"),
        
        rx.box(
            rx.vstack(
                rx.text("📸", class_name="text-6xl mb-2"),
                rx.button(
                    "Symuluj zrobienie zdjęcia", 
                    on_click=State.scan_receipt_simulation,
                    class_name="bg-emerald-600 hover:bg-emerald-500 text-white text-sm font-bold py-2 px-4 rounded-lg transition"
                ),
                align="center"
            ),
            class_name="w-full p-8 bg-slate-950/40 border-2 border-dashed border-slate-700 rounded-xl flex flex-col items-center justify-center my-4"
        ),
        
        rx.box(
            rx.text(f"Zwrócone butelki w tej sesji: {State.bottles_returned}", class_name="text-sm font-medium text-slate-300"),
            class_name="bg-slate-800/50 px-4 py-2 rounded-lg border border-slate-700"
        ),
        space="4",
        class_name="w-full px-4 pt-16 pb-24"
    )


# --- GŁÓWNY LAYOUT APLIKACJI MOBILNEJ ---

def index() -> rx.Component:
    return rx.center(
        # Kontener imitujący ekran smartfona
        rx.box(
            # 1. Wysuwany Sidebar
            rx.box(
                rx.vstack(
                    rx.flex(
                        rx.text("Opcje EcoSphere", class_name="font-bold text-emerald-400"),
                        rx.button("✕", on_click=State.toggle_sidebar, class_name="text-slate-400 text-sm"),
                        class_name="w-full justify-between items-center mb-6"
                    ),
                    rx.text("Mój Profil", class_name="text-sm text-slate-300 py-2 w-full border-b border-slate-800"),
                    rx.text("Odbierz bilet ZTM", class_name="text-sm text-slate-300 py-2 w-full border-b border-slate-800"),
                    rx.text("Ustawienia", class_name="text-sm text-slate-300 py-2 w-full border-b border-slate-800"),
                    class_name="p-4 h-full"
                ),
                class_name=rx.cond(
                    State.sidebar_open,
                    "absolute top-0 left-0 h-full w-56 bg-slate-950/95 border-r border-slate-800 z-50 transform translate-x-0 transition-transform duration-300 backdrop-blur-md",
                    "absolute top-0 left-0 h-full w-56 bg-slate-950/95 border-r border-slate-800 z-50 transform -translate-x-full transition-transform duration-300 backdrop-blur-md"
                )
            ),

            # 2. Górny mini-pasek systemowy aplikacji
            rx.flex(
                rx.button("☰", on_click=State.toggle_sidebar, class_name="text-emerald-400 text-lg font-bold focus:outline-none"),
                rx.text("EcoSphere", class_name="text-sm font-black tracking-widest text-emerald-400"),
                rx.box(class_name="w-5"), # Spacer dla symetrii
                class_name="absolute top-0 left-0 right-0 p-4 bg-slate-900/80 backdrop-blur border-b border-slate-800/50 justify-between items-center z-40"
            ),

            # 3. Dynamiczne renderowanie ekranu na podstawie wybranej karty (Bottom Bar)
            rx.box(
                rx.match(
                    State.current_tab,
                    ("home", home_screen()),
                    ("map", map_screen()),
                    ("scan", scan_screen()),
                    home_screen()
                ),
                class_name="h-full overflow-y-auto"
            ),

            # 4. DOLNY PASEK NAWIGACJI (Natywny Mobile Bottom Bar)
            rx.grid(
                rx.button(
                    rx.vstack(rx.text("🏠", class_name="text-lg"), rx.text("Home", class_name="text-[10px]"), space="0", align="center"),
                    on_click=lambda: State.set_tab("home"),
                    class_name=rx.cond(State.current_tab == "home", "text-emerald-400", "text-slate-500")
                ),
                rx.button(
                    rx.vstack(rx.text("🗺️", class_name="text-lg"), rx.text("Mapa", class_name="text-[10px]"), space="0", align="center"),
                    on_click=lambda: State.set_tab("map"),
                    class_name=rx.cond(State.current_tab == "map", "text-emerald-400", "text-slate-500")
                ),
                rx.button(
                    rx.vstack(rx.text("📸", class_name="text-lg"), rx.text("Skanuj", class_name="text-[10px]"), space="0", align="center"),
                    on_click=lambda: State.set_tab("scan"),
                    class_name=rx.cond(State.current_tab == "scan", "text-emerald-400", "text-slate-500")
                ),
                columns="3",
                class_name="absolute bottom-0 left-0 right-0 h-16 bg-slate-950/90 backdrop-blur border-t border-slate-800/80 py-2 justify-items-center items-center z-40"
            ),

            class_name="w-[380px] h-[720px] bg-slate-900 border border-slate-800 rounded-[40px] shadow-2xl relative overflow-hidden text-white"
        ),
        class_name="w-full min-h-screen bg-slate-950 flex items-center justify-center p-4"
    )

app = rx.App()
app.add_page(index)