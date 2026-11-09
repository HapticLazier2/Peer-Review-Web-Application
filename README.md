# PeerProof

PeerProof solves a recurring problem in classrooms: giving students a way to peer-review each other's work, comment, and highlight issues, without handing the job off to an AI tool. When reviews are written by an LLM, students stop learning from the process and instructors can no longer trust the feedback. PeerProof brings that trust back.

It works in three steps:

 - **The instructor creates an assignment.** This can be a coding assignment, a written response, or anything the instructor would like.
 - **The student uploads their assignment** to the student portal. PeerProof protects each submission so that it stays clear to human readers but is much harder to paste into an AI tool.
 - **A reviewer, another student, completes the review,** highlighting issues directly in the work and replying with comments.

Overall, PeerProof creates a more secure pipeline for instructors to trust their students' reviews. Student reviewers objectively review and give honest feedback, and both the reviewer and the author learn more overall. While it will not solve the issue of LLM use, it will make the use of it more difficult overall.

## Installation

You need Python 3.12 or newer and Git.

```bash
git clone https://github.com/HapticLazier2/Peer-Review-Web-Application.git
cd Peer-Review-Web-Application
python -m venv .venv
```

Activate the virtual environment:

```bash
# Windows (PowerShell)
.venv\Scripts\Activate.ps1
# macOS / Linux
source .venv/bin/activate
```

Install the dependencies and set up the database:

```bash
pip install -r api/requirements.txt
cd api
python manage.py migrate
python manage.py createsuperuser
```

## Getting Started

Start the API from the `api` folder:

```bash
python manage.py runserver
```

1. Open **http://127.0.0.1:8000/admin/** and log in with your superuser.
2. Under **Users**, add an instructor (set **Role** to Instructor) and a few students.
3. Under **Courses**, create a course, choose the instructor, and select the students.

Then try the API in your browser. Each page has a **Content** box at the bottom for sending requests:

| Endpoint | What it does |
|---|---|
| /api/auth/login/ | Log in: POST {"username": "...", "password": "..."} |
| /api/auth/me/ | Shows who is logged in |
| /api/courses/ | Instructor's courses |
| /api/assignments/ | List assignments, or POST to create one (instructors only) |
| /api/auth/logout/ | Log out (POST) |

Run the test suite:

```bash
python manage.py test core
```

## AI Usage
AI was used in helping me get through alot of errors and logical flaws with the code. It was used to review the diagrams and comment on fixes for these problems
It was not used in the generation of code outside of fixing errors which happened in most files. 

**Disclosure**: I waited until last minute to do the Diagrams, the code was copied from a local gitea repository I use. I have been working on the project for a few weeks now.
