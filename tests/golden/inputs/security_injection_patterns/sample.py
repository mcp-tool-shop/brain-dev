# Golden test input: security injection patterns
# Each function contains a known vulnerability pattern.

import os
import pickle
import subprocess


def unsafe_query(user_id):
    """SQL injection via f-string."""
    cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")


def unsafe_command(host):
    """Command injection via os.system."""
    os.system(f"ping {host}")


def hardcoded_secret():
    """Hardcoded API key."""
    api_key = "sk-1234567890abcdef"
    return api_key


def safe_query(user_id):
    """Parameterized query — should NOT trigger."""
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))


def safe_command():
    """Static command — should NOT trigger."""
    subprocess.run(["ls", "-la"], check=True)
