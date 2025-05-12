
````markdown
# 🎬 IMDb Clone

A feature-rich **IMDb Clone Web Application** built using **Flask**, allowing users to explore movie details, maintain a personal watchlist, and get smart recommendations based on their preferences.

---

## 🌟 Features

### 🔐 User Authentication
- **Login / Sign Up** system with Flask sessions.
- Each user has a **personal watchlist**.

### 📽️ Movie Search
- Search for movies by title using **TMDB API**.
- Displays:
  - 🎞️ Poster
  - 📝 Overview
  - 🌍 Language
  - ⭐ Rating
  - 🔞 Adult flag
  - 🎬 Director(s), 🎭 Cast (with profile pics and roles)

### ⭐ Personalized Watchlist
- Add and remove movies to/from your personal watchlist.
- Each movie shows:
  - Title
  - Overview
  - Language

### 🎯 Movie Recommendations
- Enter a movie name to get a list of **recommended movies**.
- Uses **TF-IDF (Term Frequency–Inverse Document Frequency)** to recommend similar movies.
- Displays:
  - Poster
  - Title
  - Rating

---

## ⚙️ Tech Stack

- **Backend:** Flask, Python
- **Frontend:** HTML, CSS, Jinja2
- **Database:** SQLite (or configurable)
- **APIs Used:** [TMDB API](https://www.themoviedb.org/documentation/api)
- **Machine Learning:** TF-IDF via scikit-learn

---

## 🚀 Getting Started

### 1. Clone the Repo

```bash
git clone https://github.com/your-username/imdb-clone.git
cd imdb-clone
````

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure API Key

Create a `.env` file and add your TMDB API key:

```
TMDB_API_KEY=your_tmdb_api_key_here
```

### 4. Run the App

```bash
flask run
```

Visit: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 📁 Project Structure

```
├── app.py
├── static/
│   ├── styles.css
│   ├── watchlist.css
│   └── recommendations.css
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── signup.html
│   ├── search.html
│   ├── watchlist.html
│   └── recommendations.html
├── models.py
├── utils/
│   └── recommender.py
├── .env
├── requirements.txt
└── README.md
```

---

## 🙏 Acknowledgements

* [TMDB API](https://www.themoviedb.org/documentation/api)
* [Font Awesome](https://fontawesome.com/)
* [Scikit-learn](https://scikit-learn.org/)

---

## 🛠 Future Improvements

* Google OAuth Login
* Responsive mobile-first design
* Deploy on Render/Heroku
* Add user profile and viewing history

---

## 👤 Author

Made with ❤️ by [Sanika Kamath ](https://github.com/sanikaa-16)
