# PREPSYNC 

AI-powered platform that helps students discover and prepare for competitive exams based on their qualifications, with personalized recommendations and real-time updates.

🎯 PREPSYNC
AI-Powered Competitive Exam Companion

📌 Overview

PREPSYNC is an intelligent web application designed to help students discover, explore, and prepare for competitive exams based on their educational qualification — from 10th to Post-Graduation.
The platform centralizes essential exam information such as:
Eligibility criteria
Important dates
Application deadlines
Fee details
Syllabus links
Previous year papers
Official notifications
By integrating Artificial Intelligence, PREPSYNC provides personalized exam recommendations, trend analysis, and smart reminders — transforming how students approach exam preparation.

🚨 Problem Statement 

Students face major challenges during competitive exam preparation:
Scattered information across multiple websites
Confusion about eligibility after 10th / 12th / UG / PG
No centralized platform for authentic exam updates
Time-consuming manual search for syllabus and study resources
Lack of AI-based personalized guidance
There is a need for a centralized, intelligent system that provides structured data, accurate updates, and personalized suggestions.

💡 Proposed Solution

PREPSYNC solves these issues by combining:
Smart filtering
AI-based recommendations
Centralized exam database
User-friendly design
Users select their education level and instantly see eligible exams.
The AI engine analyzes preferences and suggests relevant exams in domains like Engineering, Management, and Government Jobs.

🛠️ Technologies Used

Frontend:
The user interface is developed using HTML, CSS, and JavaScript, which handle the design, layout, and user interactions of the application.
Backend:
Firebase is used as the backend service to manage authentication, data handling, and cloud-based functionality.
Database:
Firebase Firestore is used as a real-time cloud database to store user data, exam details, bookmarks, and notifications.
AI / Machine Learning:
Future AI features will be implemented using Python, along with Scikit-learn and TensorFlow Lite for building recommendation and prediction models.
APIs:
The system integrates YouTube API, Google Search API, and Notification APIs to provide additional features like resource suggestions and alerts.
Version Control:
Git and GitHub are used for code management and collaboration.
Design Tools:
Figma is used for UI/UX design and prototyping.

📁 Complete Project Structure

IBM/
├── frontend/
│   ├── assets/
│   ├── auth.js
│   ├── config.js
│   ├── edit-profile.html
│   ├── exam-details.html
│   ├── exam-syllabus.html
│   ├── forgot-password.html
│   ├── history.html
│   ├── index.html
│   ├── login.html
│   ├── redirect.html
│   ├── registration.html
│   ├── settings.html
│   └── styles.css
│
├── backend/
│   ├── __init__.py
│   ├── app.py
│   ├── config.py
│   ├── data.json
│   ├── init_db.py
│   ├── models.py
│   ├── requirements.txt
│   └── test_api.py
│
├── database/
│   ├── exams.json
│   └── excel_to_json.py
│
├── README.md
├── LICENSE
├── package-lock.json
└── .gitignore

🏗️ System Architecture

User selects education level
Data sent to Firebase Firestore
Filtering logic / AI engine processes request
Relevant exams displayed on dashboard
User clicks exam → Detailed view
User bookmarks → Saved in History
Notifications sent before deadlines

⚙️ Installation (For Development)

git clone https://github.com/bhavani245/IBM.git
cd IBM

📜 License
Licensed under the Apache License 2.0.
