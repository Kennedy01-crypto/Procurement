# app.py
from procurement_app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True) # debug=True is for development only