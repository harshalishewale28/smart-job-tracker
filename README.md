# 💼 CareerPilot – Smart Job Application Tracker

A Python-based web application that helps job seekers manage job applications, track recruitment progress, organize deadlines, and analyze their job search through an interactive dashboard.

## 🚀 Features

- 📊 **Interactive Dashboard** – View total applications, interviews, selections, and rejections.
- ➕ **Add Applications** – Save company names, job roles, locations, and application dates.
- ✏️ **Edit Applications** – Update application details and recruitment status.
- 🗑️ **Delete Applications** – Remove applications with confirmation.
- 🔍 **Search and Filter** – Find applications by company, role, location, or status.
- 📅 **Deadline Tracking** – Monitor upcoming application deadlines.
- 📈 **Data Visualization** – View application statistics and monthly activity using charts.
- 📥 **CSV Export** – Download application records for Excel or Google Sheets.
- 💾 **SQLite Database** – Store application records locally.
- 🎨 **Modern UI/UX** – Custom dashboard styling with a professional layout.

## 🛠️ Technologies Used

- Python
- Streamlit
- SQLite
- Pandas
- Plotly
- CSS

## 📁 Project Structure

```text
smart-job-tracker/
│
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

The `jobs.db` database is generated automatically when the application runs.

## ⚙️ Installation and Setup

### Prerequisites

Install Python and Git before starting.

- Python: https://www.python.org/downloads/
- Git: https://git-scm.com/downloads

### Step 1: Clone the Repository

Replace `YOUR_GITHUB_USERNAME` with your GitHub username.

```bash
git clone https://github.com/YOUR_GITHUB_USERNAME/smart-job-tracker.git
```

### Step 2: Open the Project Folder

```bash
cd smart-job-tracker
```

### Step 3: Create a Virtual Environment

For Windows:

```powershell
py -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

### Step 4: Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### Step 5: Run the Application

```bash
python -m streamlit run app.py
```

Open the local URL displayed in your terminal, usually:

```text
http://localhost:8501
```

## 📖 How to Use

1. Open the CareerPilot dashboard.
2. Navigate to **Add Application**.
3. Enter the company name, job role, location, and other details.
4. Save the application.
5. Use **Manage Applications** to search, filter, edit, or delete records.
6. Monitor recruitment statistics and upcoming deadlines on the dashboard.
7. Open **Reports & Export** to analyze your progress and download a CSV file.

## 📊 Dashboard Information

The dashboard displays:

- Total job applications
- Interview count
- Selected candidates and offers
- Rejected applications
- Application status distribution
- Recent applications
- Upcoming deadlines

## 🔮 Future Enhancements

- User authentication and secure login
- Email reminders for interviews and deadlines
- Resume and job description matching
- PostgreSQL cloud database integration
- Interview preparation tracker
- Advanced job search analytics
- Cloud deployment with persistent storage

## 🎯 Project Objective

The objective of CareerPilot is to simplify job application management through a centralized dashboard, structured record keeping, and useful analytics.

This project demonstrates Python programming, database operations, CRUD functionality, data visualization, and web application development.

## 👩‍💻 Author

**Harshali Shewale**

- GitHub: https://github.com/harshalishewale28
- LinkedIn: https://www.linkedin.com/in/harshali-shewale-755082374

## 📄 License

This project is intended for educational, learning, and portfolio purposes. Add an open-source license if you wish to specify formal reuse and distribution terms.
