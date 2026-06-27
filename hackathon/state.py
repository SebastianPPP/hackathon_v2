import reflex as rx

# --- STAN APLIKACJI (Zarządzanie telefonem i AI) ---
class State(rx.State):
    is_started: bool = False
    sidebar_open: bool = False
    current_tab: str = "home"  # Kontroluje, co wyświetla się na ekranie telefonu
    eco_points: int = 1250
    bottles_returned: int = 42
    co2_saved: float = 3.4

    def start_app(self):
        self.is_started = True

    def toggle_sidebar(self):
        self.sidebar_open = not self.sidebar_open

    def set_tab(self, tab_name: str):
        self.current_tab = tab_name

    def scan_receipt_simulation(self):
        """Symulacja zrobienia zdjęcia paragonu i odczytu przez AI (OCR)"""
        self.eco_points += 50
        self.bottles_returned += 1
        self.co2_saved = round(self.co2_saved + 0.08, 2)