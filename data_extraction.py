from pydantic import BaseModel, Field
from typing import List

# א. הגדרת האובייקט הבודד
class TechnicalDecision(BaseModel):
    """כאן אנחנו מגדירים מה השדות שכל החלטה חייבת לכלול"""
    decision_name: str = Field(description="שם ההחלטה או הנושא המרכזי")
    status: str = Field(description="סטטוס ההחלטה: מאושר, בבדיקה, או נדחה")
    priority: str = Field(description="רמת חשיבות: נמוכה, בינונית, גבוהה")
    date: str = Field(description="התאריך שבו התקבלה ההחלטה")

# ב. הגדרת המעטפת (כדי לקבל רשימה של החלטות)
class DecisionList(BaseModel):
    decisions: List[TechnicalDecision]


import os
import json
from dotenv import load_dotenv
from typing import List
from pydantic import BaseModel, Field
from llama_index.core import SimpleDirectoryReader
from llama_index.llms.cohere import Cohere
from llama_index.core.program import LLMTextCompletionProgram

# פתרון SSL לנטפרי
import ssl, urllib3
ssl._create_default_https_context = ssl._create_unverified_context
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

load_dotenv()

# 1. הגדרת המבנה לחילוץ (Schema)
class TechnicalDecision(BaseModel):
    decision_name: str = Field(description="שם ההחלטה")
    status: str = Field(description="סטטוס (מאושר/בבדיקה/נדחה)")
    priority: str = Field(description="חשיבות (נמוכה/בינונית/גבוהה)")

class DecisionList(BaseModel):
    decisions: List[TechnicalDecision]

# 2. אתחול המודל
llm = Cohere(model="command-r-08-2024", api_key=os.environ["COHERE_API_KEY"])

# 3. יצירת ה-Program (המנוע שמחלץ נתונים מובנים)
prompt_template_str = (
    "להלן טקסט מתוך תיעוד פרויקט. חלץ ממנו את כל ההחלטות הטכניות שהתקבלו "
    "והצג אותן במבנה JSON לפי הסכימה שהוגדרה.\n"
    "טקסט:\n{text}\n"
)

program = LLMTextCompletionProgram.from_defaults(
    output_cls=DecisionList,
    prompt_template_str=prompt_template_str,
    llm=llm,
    verbose=True,
)

# 4. הרצה על המסמכים
def extract_all_decisions():
    print("🧐 מתחיל חילוץ נתונים מובנים מהמסמכים...")
    documents = SimpleDirectoryReader("./mock_docs").load_data()
    
    # איחוד כל הטקסט למקור אחד (או עיבוד מסמך-מסמך)
    full_text = "\n".join([doc.text for doc in documents])
    
    output = program(text=full_text)
    
    # שמירה לקובץ JSON
    with open("extracted_data.json", "w", encoding="utf-8") as f:
        json.dump(output.dict(), f, ensure_ascii=False, indent=4)
    
    print("✅ החילוץ הושלם! הנתונים נשמרו ב-extracted_data.json")
    return output

if __name__ == "__main__":
    extract_all_decisions()