"""Development server entry point.

Equivalent to the original app.py's:
    if __name__ == "__main__":
        app.run(host="0.0.0.0", port=5050, debug=False, use_reloader=False)
"""
from app import app
from config import Config

if __name__ == "__main__":
    app.run(
        host=Config.HOST,
        port=Config.PORT,
        debug=Config.DEBUG,
        use_reloader=Config.USE_RELOADER,
    )
