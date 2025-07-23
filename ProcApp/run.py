# run.py
from procurement_app import create_app

app = create_app()

if __name__ == '__main__':
    # The debug=True argument is great for development
    app.run(debug=True)