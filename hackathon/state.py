import reflex as rx
import asyncio

# --- STAN APLIKACJI (Zarządzanie telefonem i AI) ---
class State(rx.State):
    is_started: bool = False
    sidebar_open: bool = False
    is_logged_in: str = rx.LocalStorage("false", name="is_logged_in")    
    current_tab: str = "home"  
    eco_points: int = 1250
    bottles_returned: int = 42
    co2_saved: float = 3.4
    show_success: bool = False


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

    def logout(self):
        self.is_logged_in = "false"
        return rx.redirect("/")

    def login(self):
        self.is_logged_in = "true"
        print(f"po login: {self.is_logged_in}")
        return rx.redirect("/home")
    
    def check_auth(self):
        print(f"is_logged_in = {self.is_logged_in}")
        if self.is_logged_in != "true":
            return rx.redirect("/")
        
    def register(self):
        self.show_success = True
        return State.redirect_after_register
    
    async def register(self):
        self.show_success = True
        yield
        await asyncio.sleep(3)
        self.show_success = False
        yield rx.redirect("/")