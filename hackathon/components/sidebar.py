import reflex as rx
from ..state import State


def sidebar() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.flex(
                rx.text("Opcje EcoSphere", class_name="font-bold text-emerald-400"),
                rx.button("✕", on_click=State.toggle_sidebar, class_name="text-slate-400 text-sm"),
                class_name="w-full justify-between items-center mb-6"
            ),
            rx.button(
                "Mój Profil",
                on_click=lambda: [State.set_tab("profile"), State.toggle_sidebar()],
                class_name="text-sm text-slate-300 py-2 w-full text-left border-b border-slate-800"
            ),
            rx.button(
                "Odbierz nagrodę!",
                on_click=lambda: [State.set_tab("prize"), State.toggle_sidebar()],
                class_name="text-sm text-slate-300 py-2 w-full text-left border-b border-slate-800"
            ),
            rx.button(
                "Ustawienia",
                on_click=lambda: [State.set_tab("settings"), State.toggle_sidebar()],
                class_name="text-sm text-slate-300 py-2 w-full text-left border-b border-slate-800"
            ),
            rx.button("Wyloguj się", on_click=State.logout, class_name="text-sm text-red-400 py-2 w-full text-left border-b border-slate-800"),
            class_name="p-4 h-full"
        ),
        class_name=rx.cond(
            State.sidebar_open,
            "absolute top-0 left-0 h-full w-56 bg-slate-950/95 border-r border-slate-800 z-50 transform translate-x-0 transition-transform duration-300 backdrop-blur-md",
            "absolute top-0 left-0 h-full w-56 bg-slate-950/95 border-r border-slate-800 z-50 transform -translate-x-full transition-transform duration-300 backdrop-blur-md"
        )
    )