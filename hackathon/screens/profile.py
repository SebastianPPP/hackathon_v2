import reflex as rx
from ..state import State


def profile_screen():
    return rx.vstack(
        # Nagłówek
        rx.text("Mój Profil", class_name="text-xl font-black text-emerald-400"),

        # Zdjęcie profilowe
        rx.vstack(
            rx.cond(
                State.profile_photo != "",
                rx.image(src=State.profile_photo, class_name="w-24 h-24 rounded-full object-cover border-2 border-emerald-500"),
                rx.box(
                    rx.text("👤", class_name="text-5xl"),
                    class_name="w-24 h-24 rounded-full bg-slate-800 border-2 border-slate-700 flex items-center justify-center"
                )
            ),
            rx.upload(
                rx.button("Zmień zdjęcie", class_name="text-xs text-emerald-400 border border-emerald-600 px-3 py-1 rounded-lg hover:bg-emerald-600/10 transition"),
                accept={"image/*": [".png", ".jpg", ".jpeg"]},
                on_drop=State.handle_profile_photo(rx.upload_files(upload_id="profile")),
                id="profile",
            ),
            align="center",
            class_name="w-full py-4"
        ),

        # Pola formularza
        rx.vstack(
            # Nick
            rx.vstack(
                rx.text("Nick", class_name="text-xs text-slate-400 uppercase font-medium mb-1"),
                rx.input(
                    placeholder="twój nick",
                    value=State.profile_nick,
                    on_change=State.set_profile_nick,
                    class_name="w-full bg-slate-800 border border-slate-700 rounded-xl px-4 py-2 text-sm text-white placeholder-slate-500"
                ),
                align="start", class_name="w-full"
            ),
            # Miejscowość
            rx.vstack(
                rx.text("Miejscowość", class_name="text-xs text-slate-400 uppercase font-medium mb-1"),
                rx.input(
                    placeholder="miasto",
                    value=State.profile_city,
                    on_change=State.set_profile_city,
                    class_name="w-full bg-slate-800 border border-slate-700 rounded-xl px-4 py-2 text-sm text-white placeholder-slate-500"
                ),
                align="start", class_name="w-full"
            ),
            # Dzielnica
            rx.vstack(
                rx.text("Dzielnica", class_name="text-xs text-slate-400 uppercase font-medium mb-1"),
                rx.input(
                    placeholder="dzielnica",
                    value=State.profile_district,
                    on_change=State.set_profile_district,
                    class_name="w-full bg-slate-800 border border-slate-700 rounded-xl px-4 py-2 text-sm text-white placeholder-slate-500"
                ),
                align="start", class_name="w-full"
            ),
            # Nowe hasło
            rx.vstack(
                rx.text("Nowe hasło", class_name="text-xs text-slate-400 uppercase font-medium mb-1"),
                rx.input(
                    placeholder="••••••••",
                    type="password",
                    value=State.profile_password,
                    on_change=State.set_profile_password,
                    class_name="w-full bg-slate-800 border border-slate-700 rounded-xl px-4 py-2 text-sm text-white placeholder-slate-500"
                ),
                align="start", class_name="w-full"
            ),
            space="3", class_name="w-full"
        ),

        # Przycisk zapisz
        rx.button(
            "💾 Zapisz zmiany",
            on_click=State.save_profile,
            class_name="w-full bg-emerald-600 hover:bg-emerald-500 text-white font-bold py-3 rounded-xl transition mt-2"
        ),

        # Komunikat sukcesu
        rx.cond(
            State.profile_saved,
            rx.box(
                rx.text("✅ Zapisano!", class_name="text-sm text-emerald-400 text-center"),
                class_name="w-full bg-emerald-900/30 border border-emerald-500/30 rounded-xl p-3"
            ),
            rx.text("")
        ),

        space="3",
        class_name="w-full px-4 pt-16 pb-24"
    )