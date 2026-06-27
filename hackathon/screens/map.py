from ..state import State
import reflex as rx

def map_screen():
    """Ekran Mapy Miejskiej"""
    return rx.vstack(
        rx.heading("Mapa Kaucjomatów", class_name="text-xl font-bold text-emerald-400"),
        rx.text("Znajdź najbliższy wolny punkt zwrotu OZE w Gdańsku", class_name="text-xs text-slate-400 text-center"),
        rx.center(
            rx.vstack(
                rx.text("🗺️", class_name="text-5xl animate-pulse"),
                rx.text("[ Interaktywna mapa OpenStreetMap ]", class_name="text-xs text-emerald-500/80 font-mono mt-2"),
                align="center"
            ),
            class_name="w-full h-64 bg-slate-950/60 rounded-xl border border-slate-800 flex items-center justify-center"
        ),
        space="4",
        class_name="w-full px-4 pt-16 pb-24"
    )