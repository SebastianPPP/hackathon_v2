import reflex as rx
from ..state import State, Kaucjomat

def kaucjomat_card(k: Kaucjomat):
    """Komponent pojedynczej karty kaucjomatu na liście wynikowej"""
    return rx.box(
        rx.hstack(
            rx.vstack(
                rx.text(k.name, class_name="font-bold text-sm text-white"),
                rx.text(k.address, class_name="text-xs text-slate-400"),
                rx.text(f"📍 Odległość: {k.distance_calculated} km", class_name="text-xs text-emerald-400 font-medium"),
                align="start", space="1"
            ),
            rx.vstack(
                rx.text(f"⭐ {k.rating}", class_name="text-xs text-amber-400 font-bold"),
                rx.box(
                    rx.text(f"{k.fill_level}%", class_name="text-[10px] text-white font-bold text-center"),
                    class_name=rx.cond(
                        k.fill_level > 80,
                        "bg-red-600/80 px-2 py-0.5 rounded-md",
                        "bg-emerald-600/80 px-2 py-0.5 rounded-md"
                    )
                ),
                align="end", space="2"
            ),
            justify="between", class_name="w-full"
        ),
        on_click=lambda: State.select_kaucjomat_marker(k.id),
        class_name="w-full bg-slate-800/60 hover:bg-slate-800 border border-slate-700/50 p-4 rounded-2xl transition cursor-pointer mb-2"
    )

def map_screen():
    return rx.vstack(
        # Nagłówek i Filtry Panelu Rywalizacji
        rx.vstack(
            rx.text("🗺️ Kaucjomaty w okolicy", class_name="text-xl font-black text-white mb-1"),
            rx.text(State.gps_status, class_name="text-[11px] text-slate-400 italic mb-2"),
            
            rx.text("Sortuj według:", class_name="text-xs text-slate-400 uppercase font-medium mb-1"),
            rx.select(
                ["najbliżej", "najwyższa ocena", "najmniej zapełnione"],
                value=State.filter_sort_by,
                on_change=State.set_filter_sort_by,
                class_name="w-full bg-slate-800 border border-slate-700 rounded-xl text-white text-sm p-2 mb-3"
            ),
            
            rx.hstack(
                rx.text("Maksymalne zapełnienie:", class_name="text-xs text-slate-400"),
                rx.text(f"{State.filter_max_fill}%", class_name="text-xs text-emerald-400 font-bold"),
                justify="between", class_name="w-full"
            ),
            rx.slider(
                value=[State.filter_max_fill],
                min=20, max=100, step=5,
                on_change=lambda val: State.set_filter_max_fill(val[0]),
                class_name="w-full accent-emerald-500 mb-3"
            ),
            
            class_name="w-full bg-slate-900 border border-slate-800 p-4 rounded-3xl mb-4"
        ),

        # Podgląd szczegółów zaznaczonego punktu i przekierowanie do Google Maps
        rx.cond(
            State.selected_kaucjomat.length() > 0,
            rx.box(
                rx.foreach(State.selected_kaucjomat, lambda k: rx.vstack(
                    rx.text("🔍 Wybrany kaucjomat:", class_name="text-xs text-emerald-400 font-black uppercase tracking-wider"),
                    rx.text(k.name, class_name="text-base font-bold text-white"),
                    rx.text(f"Adres: {k.address}", class_name="text-xs text-slate-300"),
                    rx.hstack(
                        rx.text(f"⭐ Ocena: {k.rating}/5", class_name="text-xs text-amber-400"),
                        rx.text(f"📦 Stan: {k.fill_level}% pełny", class_name="text-xs text-slate-400"),
                        space="4"
                    ),
                    # Przycisk otwierający Google Maps w nowej zakładce na podstawie adresu i koordynatów kaucjomatu
                    rx.link(
                        rx.button("Wyznacz trasę w Google Maps 🚀", class_name="w-full bg-emerald-600 hover:bg-emerald-500 font-bold py-2 rounded-xl text-xs transition mt-2 text-white text-center"),
                        href=f"https://www.google.com/maps/search/?api=1&query=" + k.name + " " + k.address,
                        is_external=True,
                        class_name="w-full decoration-none"
                    ),
                    class_name="w-full p-4 bg-emerald-950/40 border border-emerald-500/30 rounded-2xl"
                )),
                class_name="w-full mb-4"
            )
        ),

        # Dynamicznie generowana lista najlepszych ścieżek z algorytmu
        rx.text("📍 Proponowana kolejność punktów:", class_name="text-xs text-slate-400 uppercase font-medium mb-2"),
        rx.scroll_area(
            rx.cond(
                State.filtered_kaucjomaty.length() > 0,
                rx.vstack(
                    rx.foreach(State.filtered_kaucjomaty, kaucjomat_card),
                    class_name="w-full"
                ),
                rx.text("Brak wolnych kaucjomatów spełniających kryteria.", class_name="text-xs text-red-400 text-center py-4")
            ),
            class_name="w-full h-[300px] pr-2"
        ),

        on_mount=State.trigger_gps_fetch,
        class_name="w-full px-4 pt-4 pb-24"
    )