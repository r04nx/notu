# Notu - Beautiful Note Taking App

<p align="center">
  <img src="app/static/img/screenshots/Screenshot from 2025-05-20 21-17-01.png" alt="Notu Dashboard" width="800">
</p>

Notu is an elegant and feature-rich note-taking application built with Flask and PostgreSQL. It features a beautiful UI with natural theme images from Unsplash, a powerful TinyMCE editor for rich text notes, and a modern authentication system.

## ✨ Features

- 📝 **Rich Text Editing**: Full-featured TinyMCE editor with templates, media embedding, and formatting options
- 🔐 **User Authentication**: Secure login, registration, and profile management
- 🌄 **Beautiful UI**: Natural theme images from Unsplash and smooth animations
- 🎨 **Customizable Notes**: Change colors and background images for each note
- 📌 **Pin Important Notes**: Keep critical information at the top of your list
- 🏷️ **Tag System**: Organize notes with a flexible tagging system
- 🔍 **Search Functionality**: Quickly find notes with the built-in search
- 🌙 **Dark Mode**: Toggle between light and dark themes
- 📱 **Responsive Design**: Works beautifully on all devices

## 📸 Screenshots

<table>
  <tr>
    <td><img src="app/static/img/screenshots/Screenshot from 2025-05-20 21-17-39.png" alt="Login Page" width="400"></td>
    <td><img src="app/static/img/screenshots/Screenshot from 2025-05-20 21-18-43.png" alt="Note Editor" width="400"></td>
  </tr>
  <tr>
    <td><img src="app/static/img/screenshots/Screenshot from 2025-05-20 21-18-52.png" alt="Profile Page" width="400"></td>
    <td><img src="app/static/img/screenshots/Screenshot from 2025-05-20 21-18-58.png" alt="Dark Mode" width="400"></td>
  </tr>
</table>

## 🚀 Installation

1. Clone the repository:
```bash
git clone https://github.com/r04nx/notu.git
cd notu
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the dependencies:
```bash
pip install -r requirements.txt
```

4. Set up the PostgreSQL database:
   - Create a new PostgreSQL database named `notu_db`
   - Update the `.env` file with your database credentials

5. Initialize the database:
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

6. Create an admin user (optional):
```bash
python create_admin.py
```

## ⚙️ Configuration

Create a `.env` file in the app directory to configure your application:

```
FLASK_APP=app
FLASK_ENV=development
SECRET_KEY=your_secret_key_here
DATABASE_URL=postgresql://username:password@localhost:5432/notu_db
UNSPLASH_ACCESS_KEY=your_unsplash_access_key_here
```

- Replace `your_secret_key_here` with a secure random string
- Update the database URL with your PostgreSQL credentials
- (Optional) Add your Unsplash API key to enable dynamic background images

## 🏃‍♂️ Running the Application

```bash
python run.py
```

The application will be available at http://127.0.0.1:5000/

## 🛠️ Development

To run the application in development mode with auto-reload:

```bash
export FLASK_ENV=development
python run.py
```

## 🧪 Technologies Used

- **Backend**: Flask, SQLAlchemy, Flask-Login
- **Database**: PostgreSQL
- **Frontend**: HTML, CSS, JavaScript, jQuery
- **Editor**: TinyMCE
- **UI**: Font Awesome, Google Fonts, Animate.css
- **API Integration**: Unsplash API

## 📄 License

MIT

## 👤 Author

- GitHub: [@r04nx](https://github.com/r04nx)

