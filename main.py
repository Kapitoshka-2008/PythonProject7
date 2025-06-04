"""Main entry point for the application."""

import os
from dotenv import load_dotenv
from src import app

def main():
    """Initialize and run the application."""
    # Load environment variables
    load_dotenv()
    
    # Configure application
    app.config.update(
        SECRET_KEY=os.getenv("SECRET_KEY", "dev"),
        DEBUG=os.getenv("FLASK_DEBUG", "True").lower() == "true"
    )
    
    # Run the application
    app.run(
        host=os.getenv("FLASK_HOST", "127.0.0.1"),
        port=int(os.getenv("FLASK_PORT", 5000)),
        debug=app.config["DEBUG"]
    )

if __name__ == "__main__":
    main() 