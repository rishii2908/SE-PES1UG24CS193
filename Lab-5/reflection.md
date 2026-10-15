\# Lab 5 — Reflection



\## 1. How did static analysis improve the code?



Static analysis helped identify code-quality issues, potential security risks, and style violations without executing the program. Pylint highlighted missing docstrings, a mutable default argument, broad exception handling, naming problems, and an unused variable. Bandit identified the risky use of `shell=True` and a hardcoded administrator password. Flake8 detected formatting violations. Fixing these issues improved readability, reliability, and security.



\## 2. Which issue was the most important, and why?



The `subprocess` call using `shell=True` was the most important issue because constructing a shell command with external input can create a command-injection risk. I changed the call to use a list of arguments with `shell=False` and added basic hostname validation. The updated Bandit report no longer contains a high-severity finding, although it still reports three low-severity subprocess-related warnings that require review.



\## 3. What challenges did you face while fixing the issues?



One challenge was balancing code quality with security and preserving the program's behavior. For example, removing the mutable default argument required initializing a new audit list when no list is supplied. Moving the administrator password to an environment variable also meant that ticket closure would not work until the variable was configured. I tested the program with both default and invalid urgency inputs to check the changes.



\## 4. How will you use static analysis in future projects?



I will run static analysis tools regularly during development rather than waiting until the end of a project. I will use Pylint to identify maintainability and logic issues, Bandit to review potential security risks, and Flake8 to enforce consistent formatting. I will also review the severity and context of warnings instead of blindly suppressing them, and rerun the tools after fixes to verify the results.



