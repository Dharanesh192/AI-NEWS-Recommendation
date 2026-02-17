## 📰 About AI News Recommendation System

The AI News Recommendation System is an API-driven web application that collects data from external news website (`NEWS API` it provides yesterday's news due to its free version) providers and enhances it using ( `Gemini AI`) summarization.

This project demonstrates how modern applications:
- Fetch live data using APIs
- Process and filter information
- Apply AI models for summarization
- Display structured content dynamically

Instead of manually storing news in a database, the system dynamically pulls news articles using a News API and processes them using the Gemini AI API for intelligent summarization.

This makes the system lightweight, scalable, and easily extendable.

---

## 🧩 Tech Stack

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Python 
- **AI Logic:** Content-Based Filtering
- **Core Concept:** API  
- **Optional:** Electron (Desktop App Support)

---

## 🧠 Project Overview

This project focuses on building a smart news platform using external APIs.

The system connects to:
- A News API to collect articles
- Gemini API to summarize news using AI

The backend (Python) acts as a bridge between:
Frontend (HTML, CSS, JS) ⇄ Backend (Python) ⇄ External APIs

Main Objectives:
- Understand how APIs work in real-world applications
- Learn how to securely store and use API keys
- Implement AI-based text summarization
- Filter news based on categories
- Display structured and interactive news cards

This project is ideal for students who want to understand:
- API integration
- Backend-frontend communication
- AI service integration
- Environment variable security (.env)

---

## 🛠️ Features

- 📰 Fetch real-time news dynamically using News API
- 🤖 AI Summarization concept by **Gemini** 
- 🔎 Category-based filtering
- ⚡ Fast news uploading
- 📁 Structured cards displaying NEWS 
- 🧠 Simple recommendation algorithm (content-based filtering)
- 🎨 Clean and interactive UI
- 📈 Expandable for real-time API integration

---

## ▶️ How Run The Code 
- `Download/Copy` all the files from the folder AI_NEWS and api
- Create an `venv` and install all the python libraries from the `requirement.txt` file
- Check the file structure and `all the instructions detailedly given below`
- Active the `venv` and run the python file and then run the frontend
- You may want to `rewrite the code to work in your localhost`
- I alter this code for the deployment purpose
- Here is the deployment link of this project --> https://ai-news-11-report.vercel.app/

---

## 📜 Requirements

- Install **Python 3.10+**
- If you want you can create a **venv (virtual environment)** to install the required python libraries
  ```
  python -m venv venv
- To activate the .venv use
  ```
  venv\Scripts\activate
- Install the required python library from the **requirement.txt**
  ```
  pip install -r requirement.txt
- To deactivate the .venv use
  ```
  deactivate
- To get the NEWS and AI features you need **API Keys**
- To get the API key follow the steps given below

---

## 🗂️ Project structure
 -      NEWS AI/
        ├── NEWS.html
        ├── Stylish_NEWS.css
        ├── Live_action.js
        ├── app.py
        ├── requirement.txt
        ├── .venv (If you want)
        └── .env

- Use this command in **cmd** to create this project structure
  ```
  mkdir "NEWS AI"
  cd "NEWS AI"
  type nul > NEWS.html
  type nul > Stylish_NEWS.css
  type nul > Live_action.js
  type nul > app.py
  type nul > .env
  
---

## 🔎 What is an API 
- Think of it like a digital bridge between your website to other web service
- It is done by a **unique string of characters used to identify and authenticate**
- The API key is included in the request (usually in the header or URL) and the server verifies the key
- If valid, the server allows access to the requested data or service.
- If invalid or missing, the request is rejected.

## 🧐 Where To Get The NEWS API Keys ?
- Go to **https://newsapi.org/register** register your details to get a NEWS API Keys and cpoy that API key
- NEWS API is used to **collect and upload** the NEWS to our website
- It provide **yesterday's NEWS for Free** version if you want **latest news you to get the Subscription**

## 🤔 Where To Get The Gemini API Keys ?
- Go to google Studio **https://aistudio.google.com/welcome** in your browser and check **Get start** login with your google gmail
- After login in the bottom left you can see **Get API Key** and check on **Create API Key** on the top right
- Then you get your own API key and copy that API key

## 🤨 How to use the API keys
- API keys are very sensitive you can't use it directly in python file
- So you want to create a env flie **.env** and store the API keys in a variable
- Then in **python you need to add this line** to get the API key from the env file
  ```
  NEWS_API_KEY = os.getenv('The variable that store your NEWS API key')
  GEMINI_API_KEY = os.getenv('The variable that store your Gemini API key')
- **⚠️ Don't share your API keys with anyone**

## 🔐 Example .env File

- NEWS_API_KEY=your_news_api_key_here
- GEMINI_API_KEY=your_gemini_api_key_here

---

## 🏗️ System Architecture

    Frontend (HTML/CSS/JS)
            ⇅
    Backend (Python - Flask/FastAPI)
            ⇅
    External APIs
       • News API
       • Gemini API

---


## 💡 How It Works

1️⃣ First run the backend python `app.py` and then run the frontend `NEWS.html`

    python app.py

2️⃣ The backend:
- Uses the NEWS API key from the .env file
- Sends a request to the News API
- Retrieves news articles in JSON format

3️⃣ The backend processes the response:
- From the JSON file it extracts title, description, image, and content
- Sends article content to Gemini API

4️⃣ Gemini API:
- It generates an AI-based summary
- Returns summarized text to python

5️⃣ The backend combines:
- AI-generated summary with Original article details
- Return it to JS file then all the NEWS are displayed in the screen
   
6️⃣ The frontend dynamically displays:
- News image
- Title
- Category
- AI Summary
- Source link

7️⃣ All API keys are securely stored inside a `.env` file to prevent exposure.
