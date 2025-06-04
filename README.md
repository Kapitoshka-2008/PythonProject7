# Financial Transaction Analyzer

A web application for analyzing financial transactions, built with Flask and Pandas.

## Features

- View and analyze financial transactions
- Track expenses and income
- Filter transactions by date periods
- View top transactions

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create .env file:
```bash
cp .env.example .env
```
Edit .env file with your configuration.

## Usage

1. Start the application:
```bash
python src/app.py
```

2. Open your browser and navigate to `http://localhost:5000`

## Development

### Running Tests
```bash
pytest
```

### Code Style
The project uses:
- Black for code formatting
- isort for import sorting
- flake8 for linting

To format code:
```bash
black .
isort .
```

## License

MIT License 