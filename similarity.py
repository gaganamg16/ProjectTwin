from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Existing college projects
existing_projects = [
    {
        "title": "Face Recognition Attendance System",
        "description": "A system that automatically records student attendance using facial recognition."
    },
    {
        "title": "Smart Library Management System",
        "description": "A web-based system for managing books, students, borrowing and returning."
    },
    {
        "title": "IoT Based Smart Waste Management",
        "description": "A smart system that monitors waste bins using sensors and optimizes waste collection."
    }
]


# New project submitted by a student
new_project = {
    "title": "Automated Student Attendance Using Face Recognition",
    "description": "A system that automatically records student attendance using face recognition technology."
}


# Combine title and description
new_text = new_project["title"] + " " + new_project["description"]

existing_texts = [
    project["title"] + " " + project["description"]
    for project in existing_projects
]


# Convert text into numerical vectors
vectorizer = TfidfVectorizer()

all_texts = existing_texts + [new_text]

tfidf_matrix = vectorizer.fit_transform(all_texts)


# Compare new project with existing projects
similarity_scores = cosine_similarity(
    tfidf_matrix[-1],
    tfidf_matrix[:-1]
)[0]


# Display results
results = []

for project, score in zip(existing_projects, similarity_scores):
    results.append({
        "title": project["title"],
        "similarity": score * 100
    })


# Sort from highest similarity to lowest
results.sort(key=lambda x: x["similarity"], reverse=True)


print("\n===== PROJECTTWIN RESULTS =====\n")

print("New Project:")
print(new_project["title"])

print("\nSimilar Projects:\n")

for result in results:
    print(
        f"{result['title']} "
        f"-> {result['similarity']:.2f}% similarity"
    )