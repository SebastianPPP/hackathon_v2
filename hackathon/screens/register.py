import reflex as rx
from ..state import State


def register_screen():
    return rx.vstack(
        # Logo
        rx.vstack(
            rx.text("🌿", class_name="text-6xl"),
            rx.text("EcoSphere", class_name="text-2xl font-black tracking-widest text-emerald-400"),
            rx.text("Utwórz konto", class_name="text-xs text-slate-400"),
            align="center",
            class_name="w-full py-4"
        ),

        # Pola formularza
        rx.vstack(
            rx.vstack(
                rx.text("Nick / Imię", class_name="text-xs text-slate-400 uppercase font-medium mb-1"),
                rx.input(value=State.reg_nick, on_change=State.change_reg_nick, placeholder="Twój nick", class_name="w-full bg-slate-800 border border-slate-700 rounded-xl px-4 py-2 text-sm text-white placeholder-slate-500"),
                align="start", class_name="w-full"
            ),
            rx.vstack(
                rx.text("Email / Login", class_name="text-xs text-slate-400 uppercase font-medium mb-1"),
                rx.input(value=State.reg_username, on_change=State.change_reg_username, placeholder="twój@email.pl", class_name="w-full bg-slate-800 border border-slate-700 rounded-xl px-4 py-2 text-sm text-white placeholder-slate-500"),
                align="start", class_name="w-full"
            ),
            rx.vstack(
                rx.text("Hasło", class_name="text-xs text-slate-400 uppercase font-medium mb-1"),
                rx.input(value=State.reg_password, on_change=State.change_reg_password, placeholder="••••••••", type="password", class_name="w-full bg-slate-800 border border-slate-700 rounded-xl px-4 py-2 text-sm text-white placeholder-slate-500"),
                align="start", class_name="w-full"
            ),
            rx.vstack(
                rx.text("Potwierdź hasło", class_name="text-xs text-slate-400 uppercase font-medium mb-1"),
                rx.input(value=State.reg_confirm_password, on_change=State.change_reg_confirm_password, placeholder="••••••••", type="password", class_name="w-full bg-slate-800 border border-slate-700 rounded-xl px-4 py-2 text-sm text-white placeholder-slate-500"),
                align="start", class_name="w-full"
            ),
            rx.vstack(
                rx.text("Miejscowość", class_name="text-xs text-slate-400 uppercase font-medium mb-1"),
                rx.input(value=State.reg_city, on_change=State.change_reg_city, placeholder="np. Gdańsk", class_name="w-full bg-slate-800 border border-slate-700 rounded-xl px-4 py-2 text-sm text-white placeholder-slate-500"),
                align="start", class_name="w-full"
            ),
            rx.vstack(
                rx.text("Dzielnica", class_name="text-xs text-slate-400 uppercase font-medium mb-1"),
                rx.input(value=State.reg_district, on_change=State.change_reg_district, placeholder="np. Wrzeszcz", class_name="w-full bg-slate-800 border border-slate-700 rounded-xl px-4 py-2 text-sm text-white placeholder-slate-500"),
                align="start", class_name="w-full"
            ),
            space="3", class_name="w-full"
        ),

        # Baner sukcesu rejestracji
        rx.cond(
            State.show_success,
            rx.box(
                rx.text("✅ Rejestracja przebiegła pomyślnie!", class_name="text-sm text-emerald-400 font-medium"),
                class_name="w-full bg-emerald-900/40 border border-emerald-500/30 rounded-xl px-4 py-3 text-center"
            ),
            rx.text("")
        ),

        # Przycisk rejestracji
        rx.button(
            "Zarejestruj się",
            on_click=State.register,
            class_name="w-full bg-emerald-600 hover:bg-emerald-500 text-white font-bold py-3 rounded-xl transition mt-4"
        ),

        # Powrót do logowania
        rx.vstack(
            rx.text("Masz już konto?", class_name="text-xs text-slate-400 mt-2"),
            rx.button(
                "Zaloguj się",
                on_click=lambda: rx.redirect("/"),
                class_name="w-full border border-emerald-600 text-emerald-400 hover:bg-emerald-600/10 font-bold py-2 rounded-xl transition"
            ),
            align="center", class_name="w-full"
        ),

        space="2",
        class_name="w-full px-6 pt-1 pb-24"
    )


def register_page() -> rx.Component:
    return rx.center(
        rx.box(
            rx.box(
                register_screen(),
                class_name="h-full overflow-y-auto"
            ),
            class_name="w-[380px] h-[720px] bg-slate-900 border border-slate-800 rounded-[40px] shadow-2xl relative overflow-hidden text-white"
        ),
        class_name="w-full min-h-screen bg-slate-950 flex items-center justify-center p-4"
    )