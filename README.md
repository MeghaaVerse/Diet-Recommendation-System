# Diet-Recommendation-System

A **Diet Recommendation Web App** that suggests healthy Indian meals based on user input (age, weight, goal, activity level), fetches nutrition info via nutrition csv file, and offers personalized diet plans, recipes, and downloadable PDFs.

---

## 🚀 Features


-  **Foods** for Breakfast, Lunch, and Dinner
-  **Nutrition information** (calories, proteins, etc.)
- 📁 **Download diet plan as PDF**
-  **Health tips** based on user goals (e.g., weight loss, gain)
- ⏱️ **User search history tracking** in CSV
-  Built with Flask, Pandas, and HTML templates

---

## 🧰 Tech Stack

| Tool/Tech        | Purpose                          |
|------------------|----------------------------------|
| Python           | Backend logic                    |
| Flask            | Web framework                    |
| Pandas           | Data manipulation (CSV)          |
| HTML/CSS         | Frontend templates               |
| xhtml2pdf        | PDF generation                   |


---

## 📂 Project Structure

```
project-folder/
│
├── app.py                 # Main Flask application
├── diet_data.csv          # Contains food & nutrition data
├── user_history.csv       # Auto-generated user history
│
├── templates/
│   ├── home.html          # Input form page
│   ├── result.html        # Diet recommendation result
│   ├── pdf_template.html  # For PDF generation
│   └── history.html       # View search history
│
├── static/
│   └── style.css          # custom styles
│
├── requirements.txt       # Python dependencies
└── README.md              # Project info
```

---

## 🛠️ Setup Instructions

### 1. Clone this Repository  
```bash
git clone https://github.com/your-username/diet-recommendation-system.git
cd diet-recommendation-system
```

### 2. Install Required Packages  
If you already have `requirements.txt`:
```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install flask pandas requests xhtml2pdf
```

### 3. Run the App  
```bash
python app.py
```

### 4. Open in Browser  
Visit:  
[http://127.0.0.1:5000/](http://127.0.0.1:5000/)

---



## 🙋‍♀️ Author

Built with ❤️ by **A Meghamala**  


## 🌟 Show Your Support

If you like this project:

- ⭐️ Star this repository
- 🔗 Share it with your friends
- 📧 Feel free to contribute or provide feedback

---


