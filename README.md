# Mini List Application

This is a simple Flask application that allows users to create and manage a mini list of items.

## Project Structure

```
mini-list-app
├── app
│   ├── __init__.py
│   ├── routes.py
│   ├── static
│   │   └── styles.css
│   └── templates
│       └── index.html
├── requirements.txt
├── run.py
└── README.md
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd mini-list-app
   ```

2. **Create a virtual environment:**
   ```
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. **Install the required packages:**
   ```
   pip install -r requirements.txt
   ```

## Running the Application

To run the application, execute the following command:

```
python run.py
```

The application will be available at `http://127.0.0.1:5000/`.

## Usage

- Navigate to the home page to view and manage your list.
- Add items to the list using the provided form.
- The current list of items will be displayed on the page.

## License

This project is licensed under the MIT License.