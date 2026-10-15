\# Lab 5 — Static Code Analysis Issues



| Issue | Type | Line(s) | Description | Fix Approach |

|---|---|---:|---|---|

| Unsafe subprocess call using `shell=True` | Security — High | 38 | Concatenating a hostname into a shell command may allow command injection. | Use `subprocess.run()` with a list of arguments and `shell=False`; validate the hostname. |

| Hardcoded administrator password | Security — Low | 8, 50 | A password stored directly in source code can be exposed to anyone who can read the file. | Read the password from an environment variable and handle a missing configuration securely. |

| Mutable default argument | Bug / Code quality | 10 | The default `audit\_trail=\[]` list is shared between calls, so entries may unexpectedly persist across calls. | Use `None` as the default and initialize a new list inside the function. |

| Bare exception handler | Security / Code quality | 22–24 | `except:` catches all exceptions and silently hides failures. | Catch the specific expected exception and handle it meaningfully. |

| Invalid urgency values | Input validation | 48–49 | The program accepts values outside the intended 1–5 range, including negative priorities. | Validate urgency and reject invalid input before creating a ticket. |

| Missing file encoding and explicit file handling | Code quality | 41–43 | Opening a file without specifying an encoding and manually closing it is less robust. | Use `with open(..., encoding="utf-8")` to manage the file safely. |

| Missing docstrings | Maintainability | Multiple | The module and functions do not explain their purpose. | Add a module docstring and clear function docstrings. |

| Inconsistent naming and `None` comparison | Style | 7, 30, 33 | `ticket\_counter` and `unresolvedHighPriority` do not follow conventional naming; comparing with `== None` is discouraged. | Use consistent naming and `is None`. |

| Unused variable | Code quality | 48 | The value assigned to `t2` is never used. | Remove the assignment or use the variable meaningfully. |

| PEP 8 formatting violations | Style | Multiple | Flake8 reports missing blank lines, a long line, and other formatting issues. | Apply consistent blank lines and line lengths, then rerun Flake8. |



\## Summary



The original Pylint score was 5.53/10. Bandit reported one high-severity and three low-severity findings. Flake8 reported formatting and code-quality violations. The fixes will be verified by rerunning all three tools.



## Verification After Fixes

| Tool | Before | After | Result |
|---|---|---|---|
| Pylint | 5.53/10 | 9.85/10 | Target above 9.5 achieved. One warning remains about using a global statement. |
| Bandit | 1 high and 3 low findings | 0 high and 3 low findings | The `shell=True` issue was removed. Low-severity subprocess warnings remain. |
| Flake8 | 12 reported violations | No reported violations | The updated file passes the Flake8 check. |

## Functional Testing

- The program ran with the default urgency of 3.
- An invalid urgency of -7 was rejected with an error message.
- Ticket closure was skipped when the administrator password was not configured.
- The program saved ticket data to a JSON file.




