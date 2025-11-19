from src.app import server
from src.app.callbacks.main_callbacks import register_all_callbacks
from src.app.services.layout_helper import serve_layout

app = server.create_app()

app.layout = serve_layout

register_all_callbacks(app)

server = app.server

if __name__ == "__main__":
    app.run(debug=True)
