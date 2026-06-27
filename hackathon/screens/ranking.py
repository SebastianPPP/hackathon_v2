import reflex as rx
from ..state import State

def ranking_row(r: dict) -> rx.Component:
    """Komponent pojedynczego wiersza w tabeli rankingu"""
    return rx.flex(
        # Miejsce w rankingu z dynamicznym doborem koloru przez rx.cond
        rx.text(
            f"#{r['place']}",
            class_name="text-sm font-black w-8",
            color=rx.cond(
                r["place"] == 1,
                "var(--yellow-9)", # Złoty dla #1
                rx.cond(
                    r["place"] == 2,
                    "var(--slate-9)", # Srebrny/szary dla #2
                    rx.cond(
                        r["place"] == 3,
                        "var(--orange-9)", # Brązowy/pomarańczowy dla #3
                        "var(--slate-11)"  # Domyślny dla reszty
                    )
                )
            )
        ),
        # Nazwa gracza (wyróżniona, jeśli to aktualny użytkownik)
        rx.text(
            r["name"], 
            class_name=rx.cond(
                r["name"] == "Ty",
                "text-sm text-emerald-400 font-bold flex-1",
                "text-sm text-slate-300 flex-1"
            )
        ),
        # Łączna liczba oddanych opakowań
        rx.text(f"🍾 {r['bottles']}", class_name="text-xs text-slate-400 mr-3"),
        # Punkty doświadczenia (XP)
        rx.text(f"{r['points']} XP", class_name="text-sm font-bold text-emerald-400"),
        class_name="w-full items-center py-3 border-b border-slate-800/50"
    )


def ranking_screen():
    return rx.vstack(
        # Sekcja nagłówka
        rx.vstack(
            rx.text("🏆", class_name="text-4xl"),
            rx.text("Ranking EcoSphere", class_name="text-xl font-black text-emerald-400"),
            rx.text("Top gracze w Gdańsku", class_name="text-xs text-slate-400"),
            align="center",
            class_name="w-full py-4"
        ),

        # Tabela rankingu generowana dynamicznie na podstawie bazy danych
        rx.box(
            rx.cond(
                State.ranking_list.length() > 0,
                rx.vstack(
                    rx.foreach(State.ranking_list, ranking_row),
                    class_name="w-full"
                ),
                rx.text("Brak zarejestrowanych graczy.", class_name="text-xs text-slate-400 text-center py-4")
            ),
            class_name="w-full bg-slate-800/40 border border-slate-700/50 rounded-xl px-4"
        ),

        space="4",
        class_name="w-full px-4 pt-16 pb-24"
    )