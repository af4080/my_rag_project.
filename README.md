:

---

#  Smart Project Assistant: Agentic RAG & Extraction

מערכת בינה מלאכותית מתקדמת המנהלת ותחקרת החלטות טכניות של פרויקט. המערכת משלבת חיפוש סמנטי (RAG), חילוץ נתונים מובנים (Data Extraction) וסוכן חכם (AI Agent) המקבל החלטות בזמן אמת.

##  מבט על המערכת (System Overview)


*הממשק מציג מענה חכם של הסוכן על בסיס נתונים שחולצו ומידע טקסטואלי.*

##  תכונות עיקריות (Key Features)

* **Agentic Routing:** סוכן חכם מבוסס `ReAct` היודע להחליט באופן עצמאי באיזה כלי להשתמש כדי לענות על שאלת המשתמש.
* **Semantic Search (RAG):** שליפת מידע מדויקת מתוך קבצי Markdown באמצעות אינדוקס וקטורי ו-Embeddings של Cohere.
* **Structured Data Extraction:** המרת טקסט חופשי לפורמט JSON מובנה (Schema-based) באמצעות Pydantic ו-LLM.
* **Event-Driven Workflow:** ניהול תהליך שליפה וולידציה מבוסס אירועים (Events) להבטחת איכות התשובה.
* **Streamlit UI:** ממשק צ'אט אינטראקטיבי המציג את "מחשבות" הסוכן ואת התוצאות הסופיות.

##  ארכיטקטורת המערכת (Architecture)

1. **Ingestion Layer (`ingest_data.py`):** טוען את קבצי ה-Markdown, הופך אותם לוקטורים ושומר אותם מקומית בתיקיית `storage`.
2. **Extraction Layer (`data_extraction.py`):** משתמש ב-`LLMTextCompletionProgram` כדי לחלץ רשימה מובנית של החלטות לקובץ `extracted_data.json`.
3. **Agent Logic (`agent_system.py`):** מגדיר `AgentRunner` המנהל שני כלים: `documentation_tool` (חיפוש טקסט) ו-`structured_data_viewer` (קריאת ה-JSON).
4. **Workflow Management (`rag_workflow.py`):** מיישם תהליך רב-שלבי הכולל שליפה (Retrieve), אימות (Validate) וניסוח (Synthesize) באמצעות אירועים מוגדרים מראש.

##  דוגמה לזרימת עבודה (Example Workflow)

כפי שניתן לראות בצילום המסך:

* **שאילתה:** המשתמש מבקש סיכום של ההחלטות והרקע שלהן.
* **פעולת הסוכן:** הסוכן מפעיל את כלי התיעוד.
* **תוצאה:** מוצגות שלוש החלטות (PostgreSQL, RTL, Redis) עם פירוט רלוונטי לכל אחת.

##  הוראות הפעלה (Setup)

1. הגדרת API Key בקובץ `.env`.
2. הרצת `python ingest_data.py` לאינדוקס המסמכים.
3. הרצת `python data_extraction.py` לחילוץ הנתונים.
4. הפעלת הממשק: `streamlit run app.py`.
