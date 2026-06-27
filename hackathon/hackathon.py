from .state import State
import reflex as rx
from .screens.home import home_screen
from .screens.map import map_screen
from .screens.scan import scan_screen


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