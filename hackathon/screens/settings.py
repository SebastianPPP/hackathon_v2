import reflex as rx
from ..state import State


def settings_screen():
    return rx.vstack(
        rx.text("Ustawienia", class_name="text-xl font-black text-emerald-400"),

        # 🌙 Tryb jasny/ciemny
        rx.box(
            rx.flex(
                rx.vstack(
                    rx.text("Tryb", class_name="text-sm text-slate-300 font-medium"),
                    rx.text("Jasny / Ciemny", class_name="text-xs text-slate-400"),
                    align="start"
                ),
                rx.button(
                    rx.cond(State.settings_theme == "Ciemny", "🌙 Ciemny", "☀️ Jasny"),
                    on_click=State.toggle_theme,
                    class_name="bg-slate-700/50 text-xs text-slate-300 px-3 py-1.5 rounded-lg hover:bg-slate-700 transition"
                ),
                class_name="w-full justify-between items-center"
            ),
            class_name="w-full bg-slate-800/40 border border-slate-700/50 rounded-xl p-4"
        ),

        # 🔎 Wielkość czcionki
        rx.box(
            rx.flex(
                rx.vstack(
                    rx.text("Wielkość czcionki", class_name="text-sm text-slate-300 font-medium"),
                    rx.text("Mała / Średnia / Duża", class_name="text-xs text-slate-400"),
                    align="start"
                ),
                rx.select(
                    ["Mała", "Średnia", "Duża"],
                    value=State.settings_font_size,
                    on_change=State.set_font_size,
                    class_name="bg-slate-800 border border-slate-700 rounded-lg text-xs text-slate-300 p-1.5 w-24 text-center"
                ),
                class_name="w-full justify-between items-center"
            ),
            class_name="w-full bg-slate-800/40 border border-slate-700/50 rounded-xl p-4"
        ),

        # 🇵🇱 Język
        rx.box(
            rx.flex(
                rx.vstack(
                    rx.text("Język", class_name="text-sm text-slate-300 font-medium"),
                    rx.text("Polski / English", class_name="text-xs text-slate-400"),
                    align="start"
                ),
                rx.select(
                    ["Polski", "English"],
                    value=State.settings_language,
                    on_change=State.set_language,
                    class_name="bg-slate-800 border border-slate-700 rounded-lg text-xs text-slate-300 p-1.5 w-24 text-center"
                ),
                class_name="w-full justify-between items-center"
            ),
            class_name="w-full bg-slate-800/40 border border-slate-700/50 rounded-xl p-4"
        ),

        # 💾 PRZYCISK ZAPISU (Dodany na spód panelu)
        rx.button(
            "💾 Zapisz ustawienia",
            on_click=State.save_settings,
            class_name="w-full bg-emerald-600 hover:bg-emerald-500 text-white font-bold py-3 rounded-xl transition text-sm mt-4 shadow-lg shadow-emerald-900/20"
        ),

        space="3",
        class_name="w-full px-4 pt-16 pb-24"
    )