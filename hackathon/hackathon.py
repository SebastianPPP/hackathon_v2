import reflex as rx

# --- STAN APLIKACJI ---
class State(rx.State):
    is_started: bool = False  # Kontroluje, czy logo zostało kliknięte i interfejs jest aktywny
    sidebar_open: bool = False  # Kontroluje stan menu bocznego
    eco_points: int = 1250
    
    def start_app(self):
        self.is_started = True

    def toggle_sidebar(self):
        self.sidebar_open = not self.sidebar_open


# --- INTERFEJS UŻYTKOWNIKA aaa---
def index() -> rx.Component:
    return rx.box(
        # 1. MENU BOCZNE (Sidebar) - wysuwane z lewej strony
        rx.box(
            rx.vstack(
                rx.flex(
                    rx.heading("Menu", class_name="text-xl font-bold text-emerald-400"),
                    rx.button("✕", on_click=State.toggle_sidebar, class_name="text-slate-400 hover:text-white text-xl"),
                    class_name="w-full justify-between items-center mb-8"
                ),
                # Opcje menu w postaci czystego tekstu (Plain text) zgodnie z życzeniem
                rx.text("Profil użytkownika", class_name="text-lg text-slate-300 hover:text-emerald-400 cursor-pointer py-2 w-full border-b border-slate-800"),
                rx.text("Historia recyklingu", class_name="text-lg text-slate-300 hover:text-emerald-400 cursor-pointer py-2 w-full border-b border-slate-800"),
                rx.text("Ustawienia aplikacji", class_name="text-lg text-slate-300 hover:text-emerald-400 cursor-pointer py-2 w-full border-b border-slate-800"),
                class_name="p-6 h-full"
            ),
            class_name=rx.cond(
                State.sidebar_open,
                "fixed top-0 left-0 h-full w-64 bg-slate-950/95 border-r border-emerald-500/20 z-50 transform translate-x-0 transition-transform duration-300 backdrop-blur-md",
                "fixed top-0 left-0 h-full w-64 bg-slate-950/95 border-r border-emerald-500/20 z-50 transform -translate-x-full transition-transform duration-300 backdrop-blur-md"
            )
        ),

        # 2. GÓRNY PASEK (Pojawia się w pełni dopiero po kliknięciu w logo)
        rx.flex(
            # Lewa górna strona: Przycisk menu bocznego
            rx.button(
                "☰", 
                on_click=State.toggle_sidebar,
                class_name="text-2xl text-emerald-400 hover:text-emerald-300 p-2 focus:outline-none"
            ),
            
            # Prawa górna strona: Punkty (widoczne tylko, gdy aplikacja wystartowała)
            rx.box(
                rx.text(f"{State.eco_points} XP", class_name="text-emerald-400 font-bold tracking-wider px-4 py-2 bg-emerald-500/10 border border-emerald-500/30 rounded-full text-sm animate-fade-in"),
                class_name=rx.cond(State.is_started, "opacity-100 transition-opacity duration-500", "opacity-0 pointer-events-none")
            ),
            class_name="fixed top-0 left-0 right-0 p-4 justify-between items-center z-40"
        ),

        # 3. KONTENER GŁÓWNY (Ekran powitalny i animowane logo)
        rx.center(
            rx.vstack(
                # Dynamiczne logo (Przenosi się na górę i zmniejsza po kliknięciu)
                rx.box(
                    rx.vstack(
                        rx.box(
                            class_name="w-16 h-16 rounded-full bg-gradient-to-tr from-emerald-600 to-teal-400 flex items-center justify-center shadow-lg shadow-emerald-500/20 cursor-pointer hover:scale-105 transition-transform",
                            on_click=State.start_app
                        ),
                        rx.text(
                            "EcoSphere", 
                            class_name=rx.cond(State.is_started, "text-lg font-bold tracking-widest text-emerald-400 mt-2", "text-3xl font-black tracking-widest text-emerald-400 mt-4")
                        ),
                    ),
                    # Magiczny warunek Tailwind: steruje pozycją logo w zależności od stanu `is_started`
                    class_name=rx.cond(
                        State.is_started,
                        "transform -translate-y-[35vh] scale-75 transition-all duration-700 ease-in-out z-40",
                        "transform translate-y-0 scale-100 transition-all duration-700 ease-in-out z-40"
                    )
                ),

                # TEKST ZACHĘTY (Widoczny tylko na starcie, znika po kliknięciu w logo)
                rx.box(
                    rx.text("Kliknij logo, aby rozpocząć przygodę z recyklingiem", class_name="text-slate-400 text-sm tracking-wide animate-pulse text-center"),
                    class_name=rx.cond(State.is_started, "opacity-0 pointer-events-none hidden transition-opacity duration-300", "opacity-100 transition-opacity duration-500")
                ),

                # 4. NOWA LISTA: MAPA i SKANUJ (Pojawia się centralnie po tym, jak logo ucieka do góry)
                rx.box(
                    rx.vstack(
                        rx.button(
                            rx.flex(
                                rx.text("🗺️", class_name="text-2xl"),
                                rx.text("Mapa Kaucjomatów", class_name="text-lg font-semibold tracking-wide"),
                                space="4",
                                align="center"
                            ),
                            class_name="w-72 bg-slate-800/80 hover:bg-slate-700 border border-slate-700 hover:border-emerald-500/40 text-left p-4 rounded-xl transition duration-200"
                        ),
                        rx.button(
                            rx.flex(
                                rx.text("📸", class_name="text-2xl"),
                                rx.text("Skanuj Odpady (AI)", class_name="text-lg font-semibold tracking-wide"),
                                space="4",
                                align="center"
                            ),
                            class_name="w-72 bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white p-4 rounded-xl shadow-lg shadow-emerald-900/20 transition duration-200"
                        ),
                        space="4",
                        align="center",
                    ),
                    # Sprawia, że lista pojawia się płynnie dopiero po przejściu logo
                    class_name=rx.cond(
                        State.is_started, 
                        "opacity-100 transform translate-y-0 transition-all duration-700 delay-300 flex flex-col items-center", 
                        "opacity-0 transform translate-y-10 pointer-events-none fixed"
                    )
                ),
                align="center",
                justify="center",
                class_name="w-full"
            ),
            class_name="w-full h-screen"
        ),
        class_name="min-h-screen bg-slate-900 text-white font-sans overflow-hidden"
    )

# Inicjalizacja aplikacji
app = rx.App()
app.add_page(index)