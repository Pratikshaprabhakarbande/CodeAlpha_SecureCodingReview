"""
Secure Coding Review - Intentionally Vulnerable Application
============================================================

This application demonstrates common security vulnerabilities found in real-world code.
It is intentionally created with security flaws for educational purposes.

VULNERABILITIES PRESENT:
1. Hardcoded Credentials (S105)
2. Weak Input Validation (CWE-20)
3. SQL Injection Vulnerability (CWE-89)
4. Insecure Password Hashing (S303)
5. Command Injection Risk (CWE-78)

WARNING: This code is for educational purposes ONLY.
DO NOT use this in production environments.
"""

import os
import hashlib
import subprocess
import sqlite3
from datetime import datetime

# =====================================================
# VULNERABILITY #1: HARDCODED CREDENTIALS (CRITICAL)
# =====================================================
# ISSUE: Username and password are hardcoded in source code
# RISK: Credentials exposed in version control systems
# SEVERITY: CRITICAL
API_KEY = "sk-1234567890abcdefghijklmnop"  # Hardcoded API key
DATABASE_PASSWORD = "admin123"  # Hardcoded database password
SECRET_TOKEN = "my-secret-token-12345"  # Hardcoded secret


class UserAuthenticator:
    """Handles user authentication with security vulnerabilities."""

    def __init__(self):
        """Initialize database connection."""
        # VULNERABILITY: Hardcoded database credentials
        self.db_user = "admin"
        self.db_pass = "password123"
        self.db_host = "localhost"
        self.db_name = "vulnerable_db"

    # =====================================================
    # VULNERABILITY #2: WEAK INPUT VALIDATION
    # =====================================================
    def validate_username(self, username: str) -> bool:
        """
        Validate username with minimal checks.

        ISSUE: No proper input validation
        RISK: Allows special characters, SQL injection, XSS
        SEVERITY: HIGH
        """
        # WEAK: Only checks length, no character validation
        if len(username) < 3:
            return False
        return True  # Accepts any input after length check

    # =====================================================
    # VULNERABILITY #3: WEAK PASSWORD HASHING (S303)
    # =====================================================
    def hash_password(self, password: str) -> str:
        """
        Hash password using weak MD5 algorithm.

        ISSUE: MD5 is cryptographically broken
        RISK: Passwords vulnerable to brute force and rainbow table attacks
        SEVERITY: HIGH
        """
        # VULNERABLE: Using MD5 hash (deprecated, fast brute-force attacks)
        return hashlib.md5(password.encode()).hexdigest()

    # =====================================================
    # VULNERABILITY #4: SQL INJECTION (CWE-89)
    # =====================================================
    def authenticate_user(self, username: str, password: str) -> bool:
        """
        Authenticate user against database.

        ISSUE: Direct string concatenation in SQL query
        RISK: SQL Injection vulnerability
        SEVERITY: CRITICAL
        """
        try:
            conn = sqlite3.connect(":memory:")
            cursor = conn.cursor()

            # VULNERABLE: String concatenation allows SQL injection
            # Example attack: username="admin' --" bypasses password check
            query = f"SELECT * FROM users WHERE username='{username}' AND password='{self.hash_password(password)}'"

            print(f"[DEBUG] Executing query: {query}")
            cursor.execute(query)
            result = cursor.fetchone()
            conn.close()

            return result is not None
        except Exception as e:
            print(f"Authentication error: {e}")
            return False

    # =====================================================
    # VULNERABILITY #5: COMMAND INJECTION (CWE-78)
    # =====================================================
    def get_user_info(self, user_id: str) -> dict:
        """
        Retrieve user information from system.

        ISSUE: User input directly used in shell command
        RISK: Command Injection vulnerability
        SEVERITY: CRITICAL
        """
        try:
            # VULNERABLE: Direct use of user_id in shell command
            # Example attack: user_id="1; rm -rf /" would delete system files
            command = f"grep {user_id} /etc/passwd"

            # Using shell=True makes it more dangerous
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            
            return {
                "status": "success",
                "data": result.stdout,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}


class DataValidator:
    """Handles data validation with security issues."""

    # =====================================================
    # VULNERABILITY #6: WEAK INPUT VALIDATION
    # =====================================================
    @staticmethod
    def validate_email(email: str) -> bool:
        """
        Validate email with insufficient checking.

        ISSUE: No proper email validation
        RISK: Accepts invalid formats, potential for injection
        SEVERITY: MEDIUM
        """
        # WEAK: Only checks for @ symbol
        return "@" in email

    @staticmethod
    def validate_phone(phone: str) -> bool:
        """
        Validate phone number.

        ISSUE: No format validation
        RISK: Accepts any string with digits
        SEVERITY: MEDIUM
        """
        # WEAK: Only checks if string contains digits
        return any(char.isdigit() for char in phone)

    # =====================================================
    # VULNERABILITY #7: SENSITIVE DATA IN LOGS
    # =====================================================
    @staticmethod
    def process_payment(card_number: str, cvv: str, amount: float) -> bool:
        """
        Process payment (VULNERABLE).

        ISSUE: Sensitive data logged in plaintext
        RISK: Credit card information exposed in logs
        SEVERITY: CRITICAL
        """
        try:
            # VULNERABLE: Logging sensitive credit card information
            print(f"[LOG] Processing payment - Card: {card_number}, CVV: {cvv}, Amount: {amount}")
            
            # VULNERABLE: Weak validation of card number
            if len(card_number) != 16:
                return False

            # Simulate payment processing
            return True
        except Exception as e:
            print(f"[ERROR] Payment failed: {e}")
            return False


class ConfigManager:
    """Manages configuration with security issues."""

    # =====================================================
    # VULNERABILITY #8: HARDCODED SECRETS
    # =====================================================
    CONFIG = {
        "db_host": "localhost",
        "db_port": 5432,
        "db_user": "admin",
        "db_pass": "SuperSecret123!",  # Hardcoded password
        "api_endpoint": "https://api.example.com",
        "api_key": "sk_live_51234567890",  # Live API key hardcoded
        "debug_mode": True,  # Debug mode enabled in production
        "log_level": "DEBUG",  # Debug logging enabled
        "jwt_secret": "my-super-secret-key-123",  # JWT secret hardcoded
    }

    @staticmethod
    def get_config(key: str) -> str:
        """Get configuration value."""
        return ConfigManager.CONFIG.get(key, "")


class FileHandler:
    """Handles file operations with security issues."""

    # =====================================================
    # VULNERABILITY #9: PATH TRAVERSAL (CWE-22)
    # =====================================================
    @staticmethod
    def read_user_file(filename: str) -> str:
        """
        Read user-uploaded file.

        ISSUE: No path validation
        RISK: Path traversal vulnerability
        SEVERITY: HIGH
        """
        try:
            # VULNERABLE: No sanitization of filename
            # Example attack: filename="../../../etc/passwd"
            with open(filename, 'r') as f:
                return f.read()
        except FileNotFoundError:
            return "File not found"

    @staticmethod
    def save_user_data(filename: str, data: str) -> bool:
        """
        Save user data to file.

        ISSUE: No path validation, could overwrite system files
        SEVERITY: HIGH
        """
        try:
            # VULNERABLE: No path validation
            with open(filename, 'w') as f:
                f.write(data)
            return True
        except Exception as e:
            print(f"Error saving file: {e}")
            return False


# =====================================================
# MAIN APPLICATION
# =====================================================
def main():
    """Main application function."""
    print("=" * 60)
    print("Secure Coding Review - Vulnerable Application")
    print("=" * 60)
    print("\nThis application demonstrates common security vulnerabilities.")
    print("For educational purposes only.\n")

    # Initialize authenticator
    auth = UserAuthenticator()
    validator = DataValidator()
    config = ConfigManager()

    # Example 1: Vulnerable Authentication
    print("[*] Testing vulnerable authentication...")
    username = "user@example.com"
    password = "password123"
    is_authenticated = auth.authenticate_user(username, password)
    print(f"    Authentication result: {is_authenticated}\n")

    # Example 2: Weak email validation
    print("[*] Testing weak email validation...")
    emails = ["valid@email.com", "invalid-email", "test@", "@test.com"]
    for email in emails:
        is_valid = validator.validate_email(email)
        print(f"    Email '{email}': {is_valid}")
    print()

    # Example 3: Weak phone validation
    print("[*] Testing weak phone validation...")
    phones = ["1234567890", "abc", "555-1234", ""]
    for phone in phones:
        is_valid = validator.validate_phone(phone)
        print(f"    Phone '{phone}': {is_valid}")
    print()

    # Example 4: Configuration exposure
    print("[*] Configuration values (SECURITY RISK - Hardcoded secrets):")
    for key, value in config.CONFIG.items():
        if "pass" in key.lower() or "secret" in key.lower() or "key" in key.lower():
            print(f"    {key}: {value}")
    print()

    print("[!] Review the code comments for detailed vulnerability descriptions.")
    print("[!] Run 'bandit -r . -f json -o bandit_report.json' to generate report.")
    print("=" * 60)


if __name__ == "__main__":
    main()
