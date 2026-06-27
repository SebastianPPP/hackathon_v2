import reflex as rx
from ..state import State


def login_screen():
    """Ekran logowania"""
    return rx.vstack(
        # Logo na górze
        rx.vstack(
            rx.text("🌿", class_name="text-6xl"),
            rx.text("EcoSphere", class_name="text-2xl font-black tracking-widest text-emerald-400"),
            rx.text("Zadbaj o planetę, zbieraj punkty", class_name="text-xs text-slate-400"),
            align="center",
            class_name="w-full py-8"
        ),

        # Pola logowania
        rx.vstack(
            rx.vstack(
                rx.text("Login", class_name="text-xs text-slate-400 uppercase font-medium mb-1"),
                rx.input(
                    placeholder="twój@email.pl",
                    class_name="w-full bg-slate-800 border border-slate-700 rounded-xl px-4 py-3 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-emerald-500"
                ),
                align="start",
                class_name="w-full"
            ),
            rx.vstack(
                rx.text("Hasło", class_name="text-xs text-slate-400 uppercase font-medium mb-1"),
                rx.input(
                    placeholder="••••••••",
                    type="password",
                    class_name="w-full bg-slate-800 border border-slate-700 rounded-xl px-4 py-3 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-emerald-500"
                ),
                align="start",
                class_name="w-full"
            ),
            space="4",
            class_name="w-full"
        ),

        # Przycisk logowania
        rx.button(
            "Zaloguj się",
            on_click=State.login,
            class_name="w-full bg-emerald-600 hover:bg-emerald-500 text-white font-bold py-3 rounded-xl transition mt-2"
        ),

        # Przycisk rejestracji
        rx.vstack(
            rx.text("Nie masz konta?", class_name="text-xs text-slate-400"),
            rx.button(
                "Zarejestruj się",
                class_name="w-full border border-emerald-600 text-emerald-400 hover:bg-emerald-600/10 font-bold py-3 rounded-xl transition"
            ),
            align="center",
            class_name="w-full"
        ),

        space="4",
        class_name="w-full px-6 pt-16 pb-24"
    )


def login_page() -> rx.Component:
    return rx.center(
        rx.box(
            login_screen(),
            class_name="w-[380px] h-[720px] bg-slate-900 border border-slate-800 rounded-[40px] shadow-2xl relative overflow-hidden text-white"
        ),
        class_name="w-full min-h-screen bg-slate-950 flex items-center justify-center p-4"
    )