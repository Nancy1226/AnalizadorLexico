from website import create_app
from website.auth import auth  # Importa auth

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
