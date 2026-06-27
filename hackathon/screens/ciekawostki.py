import reflex as rx
from ..state import State


CIEKAWOSTKI = [
    "Jedna plastikowa butelka może być przetworzona na włókna poliestrowe do produkcji ubrań!",
    "Recykling aluminium zużywa 95% mniej energii niż produkcja nowego aluminium.",
    "Średnia plastikowa butelka rozkłada się przez 450 lat.",
    "Polska jest jednym z liderów recyklingu szkła w Europie!",
    "Z 10 butelek PET można zrobić koszulkę polarową.",
]

def ciekawostki_screen():
    return rx.vstack(
        # Gratulacje
        rx.vstack(
            rx.text("🎉", class_name="text-6xl"),
            rx.text("Gratulacje!", class_name="text-2xl font-black text-emerald-400"),
            rx.text("Twój paragon został zapisany!", class_name="text-sm text-slate-400"),
            align="center",
            class_name="w-full py-6"
        ),

        # Punkty
        rx.box(
            rx.vstack(
                rx.text("Zdobyte punkty", class_name="text-xs text-slate-400 uppercase"),
                rx.text("+50 XP", class_name="text-3xl font-black text-emerald-400"),
                align="center"
            ),
            class_name="w-full bg-emerald-900/30 border border-emerald-500/30 rounded-xl p-4 text-center"
        ),

        # Ciekawostka
        rx.box(
            rx.vstack(
                rx.text("💡 Ciekawostka na dziś", class_name="text-xs font-bold text-emerald-400 uppercase tracking-wider"),
                rx.text(
                    State.daily_fact,
                    class_name="text-sm text-slate-300 text-center mt-2"
                ),
                align="center"
            ),
            class_name="w-full bg-slate-800/40 border border-slate-700/50 rounded-xl p-4"
        ),

        # Przycisk powrót
        rx.button(
            "Wróć do głównej",
            on_click=lambda: State.set_tab("home"),
            class_name="w-full bg-emerald-600 hover:bg-emerald-500 text-white font-bold py-3 rounded-xl transition"
        ),

        space="4",
        class_name="w-full px-4 pt-16 pb-24"
    )