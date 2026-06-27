import reflex as rx
from ..state import State


# Przykładowe dane - potem zastąpione bazą danych
MOCK_RANKING = [
    {"place": 1, "name": "Anna K.", "points": 3420, "bottles": 142},
    {"place": 2, "name": "Piotr M.", "points": 2890, "bottles": 98},
    {"place": 3, "name": "Kasia W.", "points": 2340, "bottles": 87},
    {"place": 4, "name": "Ty", "points": 1250, "bottles": 42},
    {"place": 5, "name": "Marek L.", "points": 980, "bottles": 31},
]


def ranking_row(place: int, name: str, points: int, bottles: int) -> rx.Component:
    return rx.flex(
        # Miejsce
        rx.text(
            f"#{place}",
            class_name=f"text-sm font-black w-8 " + (
                "text-yellow-400" if place == 1 else
                "text-slate-400" if place == 2 else
                "text-orange-400" if place == 3 else
                "text-slate-500"
            )
        ),
        # Nazwa
        rx.text(name, class_name="text-sm text-slate-300 flex-1"),
        # Butelki
        rx.text(f"🍾 {bottles}", class_name="text-xs text-slate-400 mr-3"),
        # Punkty
        rx.text(f"{points} XP", class_name="text-sm font-bold text-emerald-400"),
        class_name="w-full items-center py-3 border-b border-slate-800/50"
    )


def ranking_screen():
    return rx.vstack(
        rx.vstack(
            rx.text("🏆", class_name="text-4xl"),
            rx.text("Ranking EcoSphere", class_name="text-xl font-black text-emerald-400"),
            rx.text("Top gracze w Gdańsku", class_name="text-xs text-slate-400"),
            align="center",
            class_name="w-full py-4"
        ),

        # Tabela rankingu
        rx.box(
            *[ranking_row(r["place"], r["name"], r["points"], r["bottles"]) for r in MOCK_RANKING],
            class_name="w-full bg-slate-800/40 border border-slate-700/50 rounded-xl px-4"
        ),

        space="4",
        class_name="w-full px-4 pt-16 pb-24"
    )