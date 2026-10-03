import sqlite3


DATABASE = "projecttwin.db"


def create_database():

    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            department TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def add_project(title, description, department="CSE"):

    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO projects (title, description, department)
        VALUES (?, ?, ?)
        """,
        (title, description, department)
    )

    connection.commit()
    connection.close()


def get_projects():

    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute(
        "SELECT id, title, description, department FROM projects"
    )

    projects = cursor.fetchall()

    connection.close()

    return projects


def delete_project(project_id):

    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM projects WHERE id = ?",
        (project_id,)
    )

    connection.commit()
    connection.close()


def update_project(project_id, title, description, department):

    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE projects
        SET title = ?, description = ?, department = ?
        WHERE id = ?
        """,
        (title, description, department, project_id)
    )

    connection.commit()
    connection.close()


def get_department_counts():

    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT department, COUNT(*)
        FROM projects
        GROUP BY department
        """
    )

    counts = cursor.fetchall()

    connection.close()

    return counts