"""Main application entry point."""

import os
from dotenv import load_dotenv

from src import app

# Load environment variables
load_dotenv()

if __name__ == "__main__":
    app.run(
        host=os.getenv("FLASK_HOST", "127.0.0.1"),
        port=int(os.getenv("FLASK_PORT", 5000)),
        debug=os.getenv("FLASK_DEBUG", "True").lower() == "true"
    ) 