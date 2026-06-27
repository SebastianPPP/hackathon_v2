import reflex as rx
from ..state import State


def bottombar() -> rx.Component:
    return rx.grid(
        # 🏠 HOME
        rx.button(
            rx.vstack(rx.text("🏠", class_name="text-lg"), rx.text("Home", class_name="text-[10px]"), space="0", align="center"),
            on_click=lambda: State.set_tab("home"),
            variant="ghost",
            class_name=rx.cond(State.current_tab == "home", "text-emerald-400 p-0 h-auto hover:bg-transparent", "text-slate-500 p-0 h-auto hover:bg-transparent")
        ),
        # 🎯 ZADANIA (Zamiast Mapy)
        rx.button(
            rx.vstack(rx.text("🎯", class_name="text-lg"), rx.text("Zadania", class_name="text-[10px]"), space="0", align="center"),
            on_click=lambda: State.set_tab("quests"),
            variant="ghost",
            class_name=rx.cond(State.current_tab == "quests", "text-emerald-400 p-0 h-auto hover:bg-transparent", "text-slate-500 p-0 h-auto hover:bg-transparent")
        ),
        # 📸 SKANUJ
        rx.button(
            rx.vstack(rx.text("📸", class_name="text-lg"), rx.text("Skanuj", class_name="text-[10px]"), space="0", align="center"),
            on_click=lambda: State.set_tab("scan"),
            variant="ghost",
            class_name=rx.cond(State.current_tab == "scan", "text-emerald-400 p-0 h-auto hover:bg-transparent", "text-slate-500 p-0 h-auto hover:bg-transparent")
        ),
        # 🏆 RANKING
        rx.button(
            rx.vstack(rx.text("🏆", class_name="text-lg"), rx.text("Ranking", class_name="text-[10px]"), space="0", align="center"),
            on_click=lambda: State.set_tab("ranking"),
            variant="ghost",
            class_name=rx.cond(State.current_tab == "ranking", "text-emerald-400 p-0 h-auto hover:bg-transparent", "text-slate-500 p-0 h-auto hover:bg-transparent")
        ),
        # 👤 PROFIL
        rx.button(
            rx.vstack(rx.text("👤", class_name="text-lg"), rx.text("Profil", class_name="text-[10px]"), space="0", align="center"),
            on_click=lambda: State.set_tab("profile"),
            variant="ghost",
            class_name=rx.cond(State.current_tab == "profile", "text-emerald-400 p-0 h-auto hover:bg-transparent", "text-slate-500 p-0 h-auto hover:bg-transparent")
        ),
        columns="5",  # Rozszerzone do 5, żeby zmieścić Profil i Zadania!
        class_name="absolute bottom-0 left-0 right-0 h-16 bg-slate-950/90 backdrop-blur border-t border-slate-800/80 py-2 justify-items-center items-center z-40"
    )