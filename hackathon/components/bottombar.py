import reflex as rx
from ..state import State


def bottombar() -> rx.Component:
    return rx.grid(
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
        rx.button(
            rx.vstack(rx.text("🏆", class_name="text-lg"), rx.text("Ranking", class_name="text-[10px]"), space="0", align="center"),
            on_click=lambda: State.set_tab("ranking"),
            class_name=rx.cond(State.current_tab == "ranking", "text-emerald-400", "text-slate-500")
        ),
        columns="4",
        class_name="absolute bottom-0 left-0 right-0 h-16 bg-slate-950/90 backdrop-blur border-t border-slate-800/80 py-2 justify-items-center items-center z-40"
    )