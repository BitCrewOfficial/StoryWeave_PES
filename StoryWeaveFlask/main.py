from app import app, mongodb
from routes import home, signup, prompt, process

if __name__ == "__main__":
    app.run(debug=True)
