from crew import CrewAIManager

def main():
    manager = CrewAIManager()

    # Collect input from the user
    job_description = input("Enter the job description: ")
    cv_text = input("Enter the CV text: ")

    # Evaluate the CV
    print("Evaluating your CV...")
    match_score = manager.evaluate_cv(job_description, cv_text)
    print(f"Your CV scored {match_score['score']}/10.")  # Access 'score' field from dictionary

    # Generate suggestions
    print("Generating suggestions to improve your CV...")
    suggestions = manager.generate_suggestions(job_description, cv_text)
    print("Suggestions to improve your CV:")
    for suggestion in suggestions["suggestions"]:  # Access 'suggestions' field from dictionary
        print(f"- {suggestion}")

if __name__ == "__main__":
    main()
