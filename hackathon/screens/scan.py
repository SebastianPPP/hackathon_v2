from ..state import State
import reflex as rx

def scan_screen():
    """Ekran Skanowania AI (OCR)"""
    return rx.vstack(
        rx.heading("Skanuj Paragon (AI OCR)", class_name="text-xl font-bold text-emerald-400"),
        rx.text("Zrób zdjęcie paragonu z kaucjomatu, aby system automatycznie naliczył punkty.", class_name="text-xs text-slate-400 text-center"),
        
        rx.box(
            rx.vstack(
                rx.text("📸", class_name="text-6xl mb-2"),
                rx.upload(
                    accept={"image/*": [".png", ".jpg", ".jpeg"]},
                    on_drop=State.handle_photo(rx.upload_files(upload_id="photo")),
                    id="photo",
                    class_name="w-full",
                    style={"display": "none"}
                ),
                rx.cond(
                    State.photo_data != "",
                    rx.image(
                        src=State.photo_data,
                        class_name="w-full rounded-xl mt-4 border border-slate-700"
                    ),
                    rx.text("")
                ),
                align="center"
            ),
            class_name="w-full p-8 bg-slate-950/40 border-2 border-dashed border-slate-700 rounded-xl flex flex-col items-center justify-center my-4"
        ),
        
        rx.button(
            "📸 Zrób zdjęcie",
            on_click=rx.call_script("document.getElementById('photo').click()"),
            class_name="bg-emerald-600 hover:bg-emerald-500 text-white text-sm font-bold py-2 px-4 rounded-lg transition"
        ),
        rx.button(
            "💾 Zapisz wynik",
            on_click=State.save_scan,
            class_name="w-full bg-emerald-600 hover:bg-emerald-500 text-white font-bold py-3 rounded-xl transition"
        ),
        rx.box(
            rx.text(f"Zwrócone opakowania łącznie: {State.bottles_returned}", class_name="text-sm font-medium text-slate-300"),
            class_name="bg-slate-800/50 px-4 py-2 rounded-lg border border-slate-700"
        ),
        space="4",
        class_name="w-full px-4 pt-16 pb-24"
    )