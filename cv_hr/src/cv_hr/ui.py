import tkinter as tk
from tkinter import messagebox
from crew import CrewAIManager

class ChatbotUI:
    def __init__(self, root):
        self.root = root
        self.root.title("HR Chatbot: CV Helper")
        self.root.geometry("600x600")
        
        self.manager = CrewAIManager()

        tk.Label(root, text="Job Description:").pack(anchor="w", padx=10, pady=5)
        self.job_description_entry = tk.Text(root, height=5, width=70)
        self.job_description_entry.pack(padx=10, pady=5)

        tk.Label(root, text="CV:").pack(anchor="w", padx=10, pady=5)
        self.cv_entry = tk.Text(root, height=10, width=70)
        self.cv_entry.pack(padx=10, pady=5)

        tk.Button(root, text="Evaluate CV", command=self.evaluate_cv).pack(pady=10)

        tk.Label(root, text="Output:").pack(anchor="w", padx=10, pady=5)
        self.output_text = tk.Text(root, height=15, width=70, state="disabled")
        self.output_text.pack(padx=10, pady=5)

    def evaluate_cv(self):
        job_description = self.job_description_entry.get("1.0", tk.END).strip()
        cv_text = self.cv_entry.get("1.0", tk.END).strip()

        if not job_description or not cv_text:
            messagebox.showerror("Input Error", "Please enter both a job description and a CV.")
            return

        try:
            result = self.manager.evaluate_cv(job_description, cv_text)
            score = result.get("score", "N/A")
            comments = result.get("comments", "No additional feedback provided.")

            self.output_text.config(state="normal")
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, f"CV Score: {score}/10\n\n")
            self.output_text.insert(tk.END, "Evaluation Comments:\n")
            self.output_text.insert(tk.END, f"{comments}\n")
            self.output_text.config(state="disabled")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatbotUI(root)
    root.mainloop()
