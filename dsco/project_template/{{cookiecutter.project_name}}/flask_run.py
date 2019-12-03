"""App entry point."""
from {{ cookiecutter.project_name }} import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
