import reflex as rx
from ..state import State


def quest_card(title: str, category: str, desc: str, reward: str, badge_color: str, action_component: rx.Component) -> rx.Component:
    """Uniwersalny komponent karty zadania"""
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.box(
                    rx.text(category, class_name="text-[10px] font-bold text-white uppercase tracking-wider"),
                    class_name=f"{badge_color} px-2.5 py-1 rounded-full"
                ),
                rx.text(f"✨ {reward}", class_name="text-xs font-bold text-amber-400"),
                justify="between", class_name="w-full mb-1"
            ),
            rx.text(title, class_name="text-base font-bold text-white"),
            rx.text(desc, class_name="text-xs text-slate-400 mb-3"),
            
            # Wstrzyknięty element interakcji (suwak, przyciski, progress)
            action_component,
            
            align="start", space="1"
        ),
        class_name="w-full bg-slate-800/40 border border-slate-700/50 rounded-2xl p-4 shadow-md mb-3"
    )


def quest_screen():
    return rx.vstack(
        # Nagłówek panelu zadań
        rx.vstack(
            rx.text("🎯 Eco-Wyzwania", class_name="text-xl font-black text-emerald-400 mb-1"),
            rx.text("Wykonuj zadania, zdobywaj bonusowe punkty i awansuj w rankingu!", class_name="text-xs text-slate-400 text-center mb-4"),
            class_name="w-full"
        ),

        rx.scroll_area(
            rx.vstack(
                # TYPE 1: QUEST SPORTOWY
                quest_card(
                    "Spacer po zielone punkty 🏃‍♂️",
                    "Sport",
                    "Zrób spacer min. 5 km i przy okazji odwiedź najbliższy wolny kaucjomat!",
                    "300 XP",
                    "bg-blue-600",
                    rx.vstack(
                        rx.hstack(
                            rx.text(f"Postęp: {State.quest_walk_progress} / 5.0 km", class_name="text-xs text-slate-300 font-medium"),
                            class_name="w-full justify-between"
                        ),
                        # Zmień dotychczasowe: rx.progress(value=State.quest_walk_progress * 20, ...)
# Na poniższe:

                        rx.progress(
                            value=State.quest_walk_percentage, 
                            class_name="w-full h-2 bg-slate-700 accent-blue-500 rounded-full my-1"
                        ),
                        rx.button(
                            "Simulate Step 🦶", 
                            on_click=State.advance_walk,
                            class_name="mt-1 bg-blue-600/80 hover:bg-blue-600 text-white font-bold text-[11px] px-3 py-1 rounded-lg transition"
                        ),
                        class_name="w-full"
                    )
                ),

                # TYPE 2: QUEST ILOŚCIOWY (MILESTONES)
                quest_card(
                    "Mistrz Recyklingu 🍾",
                    "Ilościowy",
                    "Zwracaj butelki do automatów i odblokowuj coraz wyższe progi punktów bonusowych.",
                    "Do 700 XP",
                    "bg-amber-600",
                    rx.vstack(
                        rx.text(f"Suma oddanych opakowań: {State.bottles_returned} szt.", class_name="text-xs text-slate-300 font-medium mb-2"),
                        rx.grid(
                            rx.button("Próg 5 (+100)", on_click=lambda: State.claim_quantity_reward(1), class_name=rx.cond(State.quest_bottles_tier >= 1, "bg-emerald-600 text-[10px] py-1 px-2 rounded-lg text-white font-bold", "bg-slate-700 text-slate-400 text-[10px] py-1 px-2 rounded-lg")),
                            rx.button("Próg 10 (+250)", on_click=lambda: State.claim_quantity_reward(2), class_name=rx.cond(State.quest_bottles_tier >= 2, "bg-emerald-600 text-[10px] py-1 px-2 rounded-lg text-white font-bold", "bg-slate-700 text-slate-400 text-[10px] py-1 px-2 rounded-lg")),
                            rx.button("Próg 15 (+450)", on_click=lambda: State.claim_quantity_reward(3), class_name=rx.cond(State.quest_bottles_tier >= 3, "bg-emerald-600 text-[10px] py-1 px-2 rounded-lg text-white font-bold", "bg-slate-700 text-slate-400 text-[10px] py-1 px-2 rounded-lg")),
                            rx.button("Próg 20 (+700)", on_click=lambda: State.claim_quantity_reward(4), class_name=rx.cond(State.quest_bottles_tier >= 4, "bg-emerald-600 text-[10px] py-1 px-2 rounded-lg text-white font-bold", "bg-slate-700 text-slate-400 text-[10px] py-1 px-2 rounded-lg")),
                            columns="2",
                            spacing="2",
                            class_name="w-full"
                        ),
                        class_name="w-full"
                    )
                ),

                # TYPE 3: ZAGADKA / QUIZ EKO
                quest_card(
                    "Eko-Łamigłówka Dnia 🧠",
                    "Zagadka",
                    "Ile razy można przetwarzać aluminium (np. puszki po napojach) w procesie recyklingu?",
                    "150 XP",
                    "bg-purple-600",
                    rx.vstack(
                        rx.cond(
                            State.riddle_answered,
                            rx.box(
                                rx.text(f"Zadanie ukończone! Twoja odpowiedź została zapisana.", class_name="text-xs font-semibold text-purple-400 text-center"),
                                class_name="w-full bg-purple-950/20 border border-purple-500/20 rounded-xl p-3 text-center"
                            ),
                            rx.vstack(
                                rx.button("A) Nieskończenie wiele razy ♻️", on_click=lambda: State.check_riddle("A"), class_name="w-full bg-slate-700/60 hover:bg-purple-900/40 text-left text-xs p-2.5 rounded-xl text-slate-300 transition"),
                                rx.button("B) Maksymalnie 7 razy 🛑", on_click=lambda: State.check_riddle("B"), class_name="w-full bg-slate-700/60 hover:bg-purple-900/40 text-left text-xs p-2.5 rounded-xl text-slate-300 transition"),
                                rx.button("C) Tylko 1 raz 🧪", on_click=lambda: State.check_riddle("C"), class_name="w-full bg-slate-700/60 hover:bg-purple-900/40 text-left text-xs p-2.5 rounded-xl text-slate-300 transition"),
                                class_name="w-full", space="2"
                            )
                        ),
                        class_name="w-full"
                    )
                ),
                class_name="w-full"
            ),
            class_name="w-full h-[480px] pr-2"
        ),

        space="4",
        class_name="w-full px-4 pt-16 pb-24"
    )