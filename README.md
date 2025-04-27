# Teacher Doc Analyzer

A web application that helps teachers analyze educational documents, generate quizzes, provide feedback, and grade student submissions.

## Features

- **Document Analysis**: Process PDF documents or pasted text
- **Multiple Functions**:
  - Summarize content in bullet points
  - Generate quizzes with customizable multiple choice and short answer questions
  - Provide constructive feedback on student submissions
  - Grade student responses on a scale of 1-10 with explanations
- **PDF Export**: Export results to PDF for easy sharing or printing
- **Responsive UI**: Clean, user-friendly interface built with Tailwind CSS

## Installation

1. Clone the repository:
```bash
git clone https://github.com/ryanliao296/Liao-EC530-Final.git
cd Liao-EC530-Final
```
2. Install Dependencies
```bash
pip install flask openai pymupdf
```

3. Create a templates folder and place the frontend.html file inside:

## Usage
1. Start the application:
```bash
python docanalyzer.py
```

2. Open your web browser and navigate to:
```bash
http://127.0.0.1:5000
```

3. Upload a PDF document or paste text into the provided text area

4. Select one of the following tasks:
- **Summarize:** Generate a bullet-point summary
- **Generate Quiz:** Create a quiz with specified numbers of multiple choice and short answer questions
- **Provide Feedback:** Get constructive feedback for students submissions
- **Grade:** Evaluate student responses on a scale of 1-10 with explanations

5. Click "Generate" to process the request

6. View results and optionally export to PDF by clicking the PDF button

## Building and Running the Docker Container Image

1. Build the Docker Image
```bash
docker build -t docanalyzer .
```
2. Run the Docker Image
Pass your API key as an environment variable
```bash
docker run -p 5000:5000 -e OPENAI_API_KEY=<your-openai-api-key> docanalyzer
```

3. Access the app
Open your browser and go to:
```bash
http://localhost:5000
```
