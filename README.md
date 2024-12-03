# Smart AI Recruitment System

The **Smart AI Recruitment System** is a Python-based desktop application designed to automate the recruitment process by parsing resumes, extracting candidate details, matching them to predefined job roles, and providing a summary of their eligibility.

## Features

### 1. Resume Parsing
- Extracts candidate details such as:
  - **Name**
  - **Phone Number**
  - **Email**
  - **Degree**
- Uses `PyPDF2` to read PDF resumes and regular expressions for data extraction.

### 2. Job Role Matching
- Matches candidates to predefined job roles based on the skills mentioned in their resumes.
- Fallback role: Assigns "Trainee" if no role is matched.

### 3. Database Management
- Uses `sqlite3` to manage candidate and job role data.
- Two tables:
  - **Candidates**: Stores candidate details.
  - **JobRoles**: Stores predefined job roles and their required skills.
- Preloaded job roles include:
  - Software Developer
  - Data Analyst
  - AI Engineer
  - Web Developer

### 4. GUI
- Built with `tkinter` for an interactive user interface.
- Features:
  - Resume upload via a file dialog.
  - Summary display in a scrollable text box.
  - Buttons for uploading resumes and exiting the application.

## Installation and Setup

### Prerequisites
- Python 3.x
- Required Python libraries:
  - `tkinter` (comes with Python)
  - `sqlite3` (comes with Python)
  - `PyPDF2`

### Steps to Run
1. Clone this repository or download the script file.
2. Install required Python libraries:
   ```bash
   pip install PyPDF2
   ```
3. Run the script:
   ```bash
   python smart_ai_recruitment.py
   ```

## Usage
1. Launch the application by running the script.
2. Click on **Upload Resume** to select a PDF file.
3. The application will:
   - Parse the resume to extract details.
   - Match the candidate to a suitable job role.
   - Display a summary in the text box.
4. View the results and exit the application by clicking **Exit**.

## Database Structure
### 1. Candidates Table
| Column Name  | Data Type | Description                |
|--------------|-----------|----------------------------|
| id           | INTEGER   | Primary Key                |
| name         | TEXT      | Candidate's name           |
| phone        | TEXT      | Phone number               |
| email        | TEXT      | Email address              |
| degree       | TEXT      | Degree (e.g., BTech, MSc)  |
| skills       | TEXT      | Extracted skills           |
| status       | TEXT      | Eligibility status         |
| job_role     | TEXT      | Matched job role           |

### 2. JobRoles Table
| Column Name       | Data Type | Description                   |
|-------------------|-----------|-------------------------------|
| id                | INTEGER   | Primary Key                   |
| role              | TEXT      | Job role title (e.g., AI Engineer) |
| required_skills   | TEXT      | Required skills for the role |

## Screenshots
- **Main Screen**: Welcome message and buttons for uploading resumes and exiting.
- **Resume Upload**: File dialog to select a PDF resume.
- **Summary Display**: Scrollable text box showing the parsed details and job matching results.

## Future Enhancements
- Advanced skill extraction using Natural Language Processing (NLP).
- Automated email notifications to candidates.
- Integration with external job portals.
- Admin panel for adding or modifying job roles and requirements.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

---
Feel free to contribute or suggest improvements!
