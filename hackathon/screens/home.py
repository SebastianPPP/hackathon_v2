from ..state import State
import reflex as rx


def home_screen():
    """Ekran Główny Dashboardu"""
    return rx.vstack(
        # Górny pasek - punkty po prawej
        rx.flex(
            rx.box(),  # spacer
            rx.box(
                rx.text(f"🌿 {State.eco_points} XP", class_name="text-sm font-bold text-emerald-400 bg-slate-800 px-3 py-1 rounded-full border border-slate-700"),
            ),
            class_name="w-full justify-between items-center"
        ),

        # Logo na środku
        rx.vstack(
            rx.text("🌿", class_name="text-6xl"),
            rx.text("EcoSphere", class_name="text-2xl font-black tracking-widest text-emerald-400"),
            rx.text("Zadbaj o planetę, zbieraj punkty", class_name="text-xs text-slate-400"),
            align="center",
            class_name="w-full py-6"
        ),

        # Przyciski akcji
        rx.vstack(
            rx.button(
                rx.hstack(rx.text("📸"), rx.text("Skanuj paragon")),
                on_click=lambda: State.set_tab("scan"),
                class_name="w-full bg-emerald-600 hover:bg-emerald-500 text-white font-bold py-4 rounded-xl transition text-sm"
            ),
            rx.button(
                rx.hstack(rx.text("🗺️"), rx.text("Znajdź kaucjomat")),
                on_click=lambda: State.set_tab("map"),
                class_name="w-full border border-emerald-600 text-emerald-400 hover:bg-emerald-600/10 font-bold py-4 rounded-xl transition text-sm"
            ),
            space="3",
            class_name="w-full"
        ),

        # Wirtualny las
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