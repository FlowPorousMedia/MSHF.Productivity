from src.app import server
from src.app.callbacks.main_callbacks import register_all_callbacks

if __name__ == "__main__":
    app = server.create_app()
    register_all_callbacks(app)
    app.run(debug=True)
