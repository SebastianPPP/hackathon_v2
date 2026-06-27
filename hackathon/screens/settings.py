import reflex as rx


def settings_screen():
    return rx.vstack(
        rx.text("Ustawienia", class_name="text-xl font-black text-emerald-400"),

        # Tryb jasny/ciemny
        rx.box(
            rx.flex(
                rx.vstack(
                    rx.text("Tryb", class_name="text-sm text-slate-300 font-medium"),
                    rx.text("Jasny / Ciemny", class_name="text-xs text-slate-400"),
                    align="start"
                ),
                rx.text("🌙 Ciemny", class_name="text-xs text-slate-400"),
                class_name="w-full justify-between items-center"
            ),
            class_name="w-full bg-slate-800/40 border border-slate-700/50 rounded-xl p-4"
        ),

        # Wielkość czcionki
        rx.box(
            rx.flex(
                rx.vstack(
                    rx.text("Wielkość czcionki", class_name="text-sm text-slate-300 font-medium"),
                    rx.text("Mała / Średnia / Duża", class_name="text-xs text-slate-400"),
                    align="start"
                ),
                rx.text("Średnia", class_name="text-xs text-slate-400"),
                class_name="w-full justify-between items-center"
            ),
            class_name="w-full bg-slate-800/40 border border-slate-700/50 rounded-xl p-4"
        ),

        # Język
        rx.box(
            rx.flex(
                rx.vstack(
                    rx.text("Język", class_name="text-sm text-slate-300 font-medium"),
                    rx.text("Polski / English", class_name="text-xs text-slate-400"),
                    align="start"
                ),
                rx.text("🇵🇱 Polski", class_name="text-xs text-slate-400"),
                class_name="w-full justify-between items-center"
            ),
            class_name="w-full bg-slate-800/40 border border-slate-700/50 rounded-xl p-4"
        ),

        space="3",
        class_name="w-full px-4 pt-16 pb-24"
    )