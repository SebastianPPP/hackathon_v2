import os

import reflex as rx

is_production = os.getenv("REFLEX_ENV", "dev").lower() == "prod"

config = rx.Config(
    app_name="hackathon",
    db_url="sqlite:///reflex.db",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ]
)