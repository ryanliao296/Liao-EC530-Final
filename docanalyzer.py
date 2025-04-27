from flask import Flask, render_template, request
from openai import OpenAI
import os
import fitz  

client = OpenAI()

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    text = ""

    if request.method == "GET":
        return render_template("frontend.html", result="", input_text="")
    
    # Process POST requests
    elif request.method == "POST":
        task = request.form.get("task")
        prompt_text = ""

        # Handle PDF upload and extract text
        file = request.files.get("file")
        if file and file.filename.endswith(".pdf"):
            pdf_bytes = file.read()
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")
            text = "\n".join([page.get_text() for page in doc])
        else:
            text = request.form.get("text")

        # Customize quiz generation if task is quiz
        if task == "quiz":
            mc_count = request.form.get("mc_count", "0")
            sa_count = request.form.get("sa_count", "0")
            prompt_text = (
                f"Generate a quiz based on the following text. "
                f"Include {mc_count} multiple choice questions and {sa_count} short answer questions:\n{text}"
            )
        else:
            # Map other tasks to prompt
            prompt_map = {
                "summary": f"Summarize the following content in bullet points:\n{text}",
                "feedback": f"Provide constructive feedback for the following student submission:\n{text}",
                "grade": f"Grade the following student response using a scale of 1-10 and explain:\n{text}"
            }
            prompt_text = prompt_map.get(task, text)

        try:
            completion = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an educational assistant."},
                    {"role": "user", "content": prompt_text}
                ]
            )
            result = completion.choices[0].message.content
        except Exception as e:
            result = f"Error: {str(e)}"

        # Pass the current task value to the template
        return render_template("frontend.html", result=result, input_text=text, request=request)

if __name__ == "__main__":
    app.run(debug=True)