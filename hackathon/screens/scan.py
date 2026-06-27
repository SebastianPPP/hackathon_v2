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
                rx.button(
                    "Symuluj zrobienie zdjęcia", 
                    on_click=State.scan_receipt_simulation,
                    class_name="bg-emerald-600 hover:bg-emerald-500 text-white text-sm font-bold py-2 px-4 rounded-lg transition"
                ),
                align="center"
            ),
            class_name="w-full p-8 bg-slate-950/40 border-2 border-dashed border-slate-700 rounded-xl flex flex-col items-center justify-center my-4"
        ),
        
        rx.box(
            rx.text(f"Zwrócone butelki w tej sesji: {State.bottles_returned}", class_name="text-sm font-medium text-slate-300"),
            class_name="bg-slate-800/50 px-4 py-2 rounded-lg border border-slate-700"
        ),
        space="4",
        class_name="w-full px-4 pt-16 pb-24"
    )