# NeevaMind: Early Alzheimer's Detection through AI-powered Journaling

NeevaMind is a web-based mental wellness platform designed to help users monitor early signs of cognitive decline. By analyzing daily journal entries using artificial intelligence, NeevaMind provides personalized cognitive insights and trends over time. The application is especially focused on assisting individuals at risk of Alzheimer's or other neurodegenerative conditions.

## Overview

The goal of this project is to empower early detection of Alzheimer's disease through natural language patterns in everyday writing. Users can log their daily thoughts, emotions, and routines, and receive real-time feedback based on subtle linguistic and behavioral signals.

This solution is built with a focus on accessibility, simplicity, and privacy. It supports both text and voice-based journaling and is optimized for multilingual users, including support for Indian regional languages.

## Key Features

* AI-powered cognitive analysis of journal entries
* Secure sign-up and login system
* Visual reports that track mental health trends
* End-to-end encryption and private data handling
* Responsive and accessible design

## Technologies Used

* Frontend: HTML5, CSS3, JavaScript (Vanilla)
* Backend: Python (Flask)
* AI Analysis: Cohere API
* Authentication: Basic email-password login
* Hosting: Local (XAMPP compatible)

## Folder Structure

```
neevamind
│
├── frontend/
│   ├── index.html            Main landing page and templates
│   ├── styles/
│   │   └── main.css          All styling including card layouts
│   └── js/
│       └── main.js           Handles routing and dynamic content
│
├── backend/
│   └── app.py                Flask server with journaling and AI logic
│
├── templates/                Optional: for server-rendered views (if used)
├── static/                   Static files (audio, images, etc.)
```

## How It Works

1. Users sign up with a secure account.
2. They write daily diary entries.
3. The app's AI engine analyzes entries for patterns in language, memory, attention, and mood.
4. Personalized feedback and long-term progress reports are displayed on the dashboard.
5. Data remains fully private and secure.

## Getting Started

1. Clone the repository
2. Run the Flask backend (`app.py`)
3. Open `index.html` in your browser
4. Begin journaling and exploring insights

## Customization and Deployment

* You can train the AI analysis module further using clinical or synthetic journaling datasets
* To deploy online, you may use platforms like Render, Heroku, or your own VPS
* For local deployment, ensure XAMPP or WAMP is configured to serve the frontend

## License

This project is intended for educational and non-commercial use. Please consult a licensed healthcare provider for clinical assessments or diagnoses.


