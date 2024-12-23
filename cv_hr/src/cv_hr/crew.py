import json
from crewai import Agent
from crewai.task import Task
from dotenv import load_dotenv
import os

load_dotenv()

class CrewAIManager:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("API key not found. Please add GEMINI_API_KEY to your .env file.")

        self.cv_evaluator = Agent(
            agent_id="cv_evaluator",
            api_key=api_key,
            role="CV Evaluator",
            goal="Evaluate CVs and score them based on job descriptions.",
            backstory="An AI expert in analyzing CVs and matching them with job requirements."
        )

        self.suggestion_generator = Agent(
            agent_id="suggestion_generator",
            api_key=api_key,
            role="Suggestion Generator",
            goal="Provide actionable feedback to improve CVs.",
            backstory="An AI specializing in tailoring CVs for specific job descriptions."
        )

    def evaluate_cv(self, job_description, cv_text):
        job_description = job_description.strip()
        cv_text = cv_text.strip()

        if not job_description or not cv_text:
            raise ValueError("Both job description and CV must be provided.")

        task = Task(
            name="evaluate_cv",
            description="Evaluate the relevance of a CV to a job description.",
            inputs={
                "job_description": job_description,
                "cv_text": cv_text
            },
            expected_output=(
                "A JSON string with a 'score' field (integer between 0-10) "
                "indicating the match quality, and a 'comments' field for feedback."
            )
        )

        try:
            response = self.cv_evaluator.execute_task(task=task)
            response_data = json.loads(response.strip("```json").strip("```"))

            if "score" not in response_data:
                raise ValueError("Response does not include a score field.")
            
            return response_data
        except json.JSONDecodeError:
            raise ValueError("Failed to parse the response. Ensure it is valid JSON.")
        except Exception as e:
            raise ValueError(f"An error occurred during evaluation: {e}")

    def generate_suggestions(self, job_description, cv_text):
        task = Task(
            name="generate_suggestions",
            description="Generate suggestions to improve the CV.",
            inputs={"job_description": job_description, "cv_text": cv_text},
            expected_output="A JSON string with a suggestions field containing a list of suggestions."
        )
        response = self.suggestion_generator.execute_task(task=task)
        cleaned_response = response.strip("```json").strip("```")

        try:
            response_data = json.loads(cleaned_response)
        except json.JSONDecodeError:
            raise ValueError(f"Unexpected response format: {response}")

        return response_data
