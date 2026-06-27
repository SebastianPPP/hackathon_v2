from .state import State
import reflex as rx
from .screens.home import home_screen
from .screens.scan import scan_screen
from .screens.login import login_screen, login_page
from .components.sidebar import sidebar
from .screens.register import register_page
from .screens.ranking import ranking_screen
from .components.bottombar import bottombar
from .screens.ciekawostki import ciekawostki_screen
from .screens.quest import quest_screen
from .screens.profile import profile_screen
from .screens.settings import settings_screen
from .screens.prize import prize_screen

def index() -> rx.Component:
    return rx.center(
        # Kontener imitujący ekran smartfona
        rx.box(
            # 1. Wysuwany Sidebar
            sidebar(),

            # 2. Górny mini-pasek systemowy aplikacji
            rx.flex(
                rx.button("☰", on_click=State.toggle_sidebar, variant="ghost", class_name="text-emerald-400 text-lg font-bold focus:outline-none hover:bg-transparent p-0"),
                rx.text("EcoSphere", class_name="text-sm font-black tracking-widest text-emerald-400"),
                rx.box(class_name="w-5"), # Spacer dla symetrii
                class_name="absolute top-0 left-0 right-0 p-4 bg-slate-900/80 backdrop-blur border-b border-slate-800/50 justify-between items-center z-40"
            ),

            # 3. Dynamiczne renderowanie ekranu na podstawie wybranej karty (Bottom Bar)
            rx.box(
                rx.match(
                    State.current_tab,
                    ("home", home_screen()),
                    ("quests", quest_screen()),        # <-- TUTAJ: Dodana obsługa ekranu zadań zamiast starej mapy
                    ("scan", scan_screen()),
                    ("ranking", ranking_screen()),
                    ("ciekawostki", ciekawostki_screen()),
                    ("profile", profile_screen()),
                    ("prize", prize_screen()),
                    ("settings", settings_screen()),
                    home_screen()
                ),
                class_name="h-full overflow-y-auto"
            ),

            # 4. DOLNY PASEK NAWIGACJI (Natywny Mobile Bottom Bar)
            bottombar(),

            class_name="w-[380px] h-[720px] bg-slate-900 border border-slate-800 rounded-[40px] shadow-2xl relative overflow-hidden text-white"
        ),
        class_name="w-full min-h-screen bg-slate-950 flex items-center justify-center p-4"
    )

app = rx.App()
app.add_page(register_page, route="/register")
app.add_page(login_page, route="/", on_load=State.check_auth)
app.add_page(index, route="/home")