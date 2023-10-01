# Project Name

This project is a starter kit for generating new Cookiecutter projects.

## Getting Started

To get started, clone this repository and follow the instructions below.

### Prerequisites

- Python 3.8 or higher
- pip
- virtualenv

### Installing

1. Create a new virtual environment:

   ```
   virtualenv venv
   source venv/bin/activate
   ```

2. Install the project dependencies:

   ```
   pip install -r requirements.txt
   ```

### Usage

1. Start the FastAPI server:

   ```
   uvicorn backend.app:app --reload
   ```

2. Open the app in your web browser:

   ```
   http://localhost:8000
   ```

3. Enter the project details and click "Generate Project" to generate a new Cookiecutter project.

## Project Structure

- `backend/app.py`: FastAPI server that generates new Cookiecutter projects.
- `backend/templates/index.html`: HTML template for the web app.
- `frontend/app_starter.py`: Streamlit app that generates new Cookiecutter projects.
- `src/cookiecutter_starter/main.py`: Python script that generates a new Cookiecutter project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.