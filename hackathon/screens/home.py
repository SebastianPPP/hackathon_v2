from ..state import State
import reflex as rx


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