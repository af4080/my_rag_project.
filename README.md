.

.

:

---

# 🤖 עוזר פרויקט חכם: Agentic RAG & Data Extraction

פרויקט זה מציג מערכת בינה מלאכותית מתקדמת לניהול ותחקור החלטות טכניות. המערכת משלבת אחזור מידע ממסמכים (RAG), חילוץ נתונים מובנים ל-JSON, וסוכן (Agent) חכם שמקבל החלטות בזמן אמת על סמך השאילתה.

## 🎯 עמידה בדרישות הפרויקט

המערכת עונה על **כל** דרישות המטלה בצורה מלאה:

* **LlamaIndex & Cohere:** שימוש במודל שפה ובוקטורים של Cohere לאורך כל התהליך.
* **Agentic System:** בניית סוכן חכם המשתמש בלוגיקת ReAct (מחשבה -> פעולה -> תצפית).
* **Structured Data Extraction:** חילוץ אוטומטי של נתונים מובנים מתוך טקסט חופשי לפורמט JSON באמצעות Pydantic Schema.
* **Event-Driven Workflow:** ניהול תהליך השליפה והאימות באמצעות מערכת אירועים (Events).
* **Multi-Tool Usage:** הסוכן יודע לנתב שאילתות בין כלי החיפוש בטקסט (RAG) לבין כלי קריאת הנתונים המובנים (JSON).
* **ממשק משתמש (UI):** פיתוח ממשק צ'אט אינטראקטיבי באמצעות Streamlit.

## 📸 צילום מסך של המערכת


*(יש לשמור את צילום המסך שהעלית קודם בשם screenshot.png בתיקיית הפרויקט)*

## 🏗️ מבנה הפרויקט

* `ingest_data.py`: טעינת מסמכי Markdown, יצירת אינדוקס וקטורי ושמירה בתיקיית `storage`.
* `data_extraction.py`: סריקת המסמכים וחילוץ החלטות לתוך קובץ ה-JSON המובנה `extracted_data.json`.
* `rag_workflow.py`: הגדרת זרימת העבודה מבוססת האירועים (Events) לשליפה וסיכום מידע.
* `agent_system.py`: הגדרת הסוכן (Agent), הכלים שלו (Tools) ולוגיקת הניתוב.
* `app.py`: קוד הממשק הגרפי (Streamlit).

## 🛠️ הוראות הרצה

1. **התקנת ספריות:** `pip install llama-index llama-index-llms-cohere llama-index-embeddings-cohere streamlit pydantic python-dotenv`
2. **הגדרת מפתח API:** יש ליצור קובץ `.env` עם המפתח: `COHERE_API_KEY=your_key_here`.
3. **הכנת הנתונים:**
* הריצי `python ingest_data.py` לעיבוד המסמכים.
* הריצי `python data_extraction.py` לחילוץ הנתונים ל-JSON.


4. **הפעלת הממשק:**
`streamlit run app.py`

---
.
3. קחי את התמונה שהעלית לי קודם (זאת עם ה-Redis), ושמרי אותה באותה תיקייה תחת השם `screenshot.png`.

**נראה שסגרת את כל הפינות! את מרגישה מוכנה לארוז הכל ל-ZIP ולהגיש?**
