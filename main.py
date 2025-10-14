import pkgutil, importlib

if not hasattr(pkgutil, "find_loader"):
    pkgutil.find_loader = importlib.util.find_spec


from src.app.server import app  # Import Dash instance

if __name__ == "__main__":
    app.run(debug=False)
