from flask import Flask, request, render_template, send_file
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from reportlab.pdfgen import canvas
from flask import send_file
import io

from database import (
    create_database,
    get_projects,
    add_project,
    delete_project,
    update_project,
    get_department_counts
)

app = Flask(__name__)

create_database()


@app.route("/add-project", methods=["GET", "POST"])
def add_existing_project():

    if request.method == "POST":

        title = request.form["title"]
        description = request.form["description"]
        department = request.form["department"]

        add_project(title, description, department)

        return render_template(
            "success.html",
            message="Project Added Successfully",
            description="The project has been added to the ProjectTwin database and can now be used for similarity comparison."
        )

    return render_template("add_project.html")

@app.route("/projects")
def view_projects():

    projects = get_projects()

    selected_department = request.args.get("department", "")
    search = request.args.get("search", "").strip().lower()

    if selected_department:
        projects = [
            project for project in projects
            if project[3] == selected_department
        ]

    if search:
        projects = [
            project for project in projects
            if search in project[1].lower()
            or search in project[2].lower()
        ]

    return render_template(
        "projects.html",
        projects=projects,
        selected_department=selected_department,
        search=search
    )


@app.route("/delete-project/<int:project_id>")
def delete_existing_project(project_id):

    delete_project(project_id)

    return render_template("delete_success.html")


@app.route("/edit-project/<int:project_id>", methods=["GET", "POST"])
def edit_project(project_id):

    projects = get_projects()

    project = None

    for item in projects:

        if item[0] == project_id:
            project = item
            break

    if project is None:
        return "Project not found"

    if request.method == "POST":

        title = request.form["title"]
        description = request.form["description"]
        department = request.form["department"]

        update_project(
            project_id,
            title,
            description,
            department
        )

        return render_template(
            "success.html",
            message="Project Updated Successfully",
            description="The project details have been updated in the ProjectTwin database."
        )

    return render_template(
        "edit_project.html",
        project=project
    )


@app.route("/dashboard")
def dashboard():

    projects = get_projects()

    total_projects = len(projects)

    department_counts = get_department_counts()

    return render_template(
        "dashboard.html",
        total_projects=total_projects,
        department_counts=department_counts
    )


@app.route("/", methods=["GET", "POST"])
def home():

    results = []
    new_project = None

    if request.method == "POST":

        title = request.form["title"]
        description = request.form["description"]

        new_project = {
            "title": title,
            "description": description
        }

        database_projects = get_projects()

        if not database_projects:

            return render_template(
                "index.html",
                results=[],
                new_project=new_project
            )

        new_text = title + " " + description

        existing_texts = [
            project[1] + " " + project[2]
            for project in database_projects
        ]

        all_texts = existing_texts + [new_text]

        vectorizer = TfidfVectorizer()

        tfidf_matrix = vectorizer.fit_transform(all_texts)

        similarity_scores = cosine_similarity(
            tfidf_matrix[-1],
            tfidf_matrix[:-1]
        )[0]

        for project, score in zip(
            database_projects,
            similarity_scores
        ):

            results.append({
    "title": project[1],
    "department": project[3],
    "similarity": score * 100
})
        results.sort(
            key=lambda x: x["similarity"],
            reverse=True
        )

    return render_template(
        "index.html",
        results=results,
        new_project=new_project
    )


if __name__ == "__main__":
    app.run(debug=True)
@app.route("/download-report", methods=["POST"])
def download_report():

    title = request.form["title"]
    description = request.form["description"]
    similarity_title = request.form["similarity_title"]
    similarity_score = request.form["similarity_score"]

    buffer = io.BytesIO()

    pdf = canvas.Canvas(buffer)

    pdf.setTitle("ProjectTwin Similarity Report")

    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawString(50, 780, "ProjectTwin")

    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawString(50, 740, "Project Similarity Report")

    pdf.setFont("Helvetica", 11)

    pdf.drawString(50, 700, "Submitted Project:")
    pdf.drawString(180, 700, title)

    pdf.drawString(50, 670, "Description:")
    pdf.drawString(50, 650, description[:90])

    pdf.drawString(50, 610, "Highest Matching Project:")
    pdf.drawString(200, 610, similarity_title)

    pdf.drawString(50, 580, "Similarity Score:")
    pdf.drawString(160, 580, similarity_score + "%")

    pdf.setFont("Helvetica-Oblique", 9)
    pdf.drawString(
        50,
        530,
        "Note: Similarity indicates textual similarity and does not prove plagiarism."
    )

    pdf.save()

    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name="ProjectTwin_Similarity_Report.pdf",
        mimetype="application/pdf"
    )