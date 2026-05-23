# Secure Coding Review - Intentionally Vulnerable Python Application

## 📋 Project Overview

**Secure Coding Review** is an **intentionally vulnerable Python application** designed to demonstrate common security vulnerabilities found in real-world code. This project is perfect for **cybersecurity learners, internship candidates, and those preparing for security-focused roles**.

The application showcases **9 major security vulnerabilities** with detailed comments explaining each issue, its risk level, and potential attack vectors.

### Project Purpose
- **Educational**: Learn how vulnerabilities appear in real code
- **Portfolio Ready**: Demonstrate security awareness to employers
- **Interview Friendly**: Easy to explain vulnerabilities in technical interviews
- **Practical**: Uses industry-standard security analysis tools

### Target Audience
- Cybersecurity interns and entry-level professionals
- Computer Science students learning secure coding practices
- DevSecOps professionals learning vulnerability detection
- Candidates preparing for security-focused roles

---

## 🎯 Vulnerabilities Demonstrated

| # | Vulnerability | Type | Severity | CWE ID |
|---|---|---|---|---|
| 1 | Hardcoded Credentials | Information Disclosure | **CRITICAL** | CWE-798 |
| 2 | Weak Input Validation | Input Validation | HIGH | CWE-20 |
| 3 | SQL Injection | Injection | **CRITICAL** | CWE-89 |
| 4 | Weak Password Hashing (MD5) | Cryptography | HIGH | CWE-327 |
| 5 | Command Injection | Injection | **CRITICAL** | CWE-78 |
| 6 | Insufficient Email Validation | Input Validation | MEDIUM | CWE-20 |
| 7 | Insufficient Phone Validation | Input Validation | MEDIUM | CWE-20 |
| 8 | Sensitive Data in Logs | Information Disclosure | **CRITICAL** | CWE-532 |
| 9 | Path Traversal | Access Control | HIGH | CWE-22 |

---

## 🛠️ Tools Used

### 1. **Bandit** - Static Security Analysis
- **Purpose**: Scans Python code for common security issues
- **Installation**: `pip install bandit`
- **Usage**: `bandit -r app.py -f json -o report.json`
- **Report Format**: JSON for detailed vulnerability analysis

### 2. **Python 3.8+**
- **Version**: 3.8 or higher
- **Purpose**: Runtime environment

### 3. **Security Analysis Tools**
- Static code analysis for vulnerability detection
- Manual code review techniques
- OWASP Top 10 compliance checking

---

## 🔍 Detailed Vulnerability Breakdown

### Vulnerability #1: Hardcoded Credentials (CRITICAL)
```python
API_KEY = "sk-1234567890abcdefghijklmnop"
DATABASE_PASSWORD = "admin123"
SECRET_TOKEN = "my-secret-token-12345"
```
**Issue**: Credentials exposed in source code
**Risk**: Anyone with access to repository can use credentials
**Attack Vector**: Version control system exposure
**Severity**: CRITICAL - Immediate system compromise possible

### Vulnerability #2: Weak Input Validation (HIGH)
```python
def validate_username(self, username: str) -> bool:
    if len(username) < 3:
        return False
    return True  # Accepts ANY input!
```
**Issue**: No character validation or sanitization
**Risk**: SQL injection, XSS, command injection
**Attack Vector**: Special characters, quotes, semicolons
**Severity**: HIGH - Gateway for multiple attacks

### Vulnerability #3: SQL Injection (CRITICAL)
```python
query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
cursor.execute(query)
```
**Issue**: Direct string concatenation in SQL query
**Attack Example**: username = `admin' --`
**Result**: Bypasses authentication entirely
**Severity**: CRITICAL - Complete database compromise

### Vulnerability #4: Weak Password Hashing (HIGH)
```python
def hash_password(self, password: str) -> str:
    return hashlib.md5(password.encode()).hexdigest()
```
**Issue**: MD5 is cryptographically broken
**Risk**: Fast brute-force attacks, rainbow tables
**Timeline**: Can be cracked in seconds
**Severity**: HIGH - Compromises all user accounts

### Vulnerability #5: Command Injection (CRITICAL)
```python
command = f"grep {user_id} /etc/passwd"
result = subprocess.run(command, shell=True, capture_output=True)
```
**Issue**: User input in shell command
**Attack Example**: user_id = `1; rm -rf /`
**Result**: Arbitrary code execution
**Severity**: CRITICAL - System takeover possible

### Vulnerability #6: Sensitive Data in Logs (CRITICAL)
```python
print(f"[LOG] Processing payment - Card: {card_number}, CVV: {cvv}")
```
**Issue**: Credit card information logged in plaintext
**Risk**: Exposed in log files, monitoring systems
**Compliance**: PCI DSS violation
**Severity**: CRITICAL - Financial data exposure

### Vulnerability #7: Insufficient Email Validation (MEDIUM)
```python
def validate_email(email: str) -> bool:
    return "@" in email  # Way too weak!
```
**Issue**: Only checks for @ symbol
**Risk**: Accepts `@`, `test@`, invalid formats
**Severity**: MEDIUM - Data quality issue

### Vulnerability #8: Insufficient Phone Validation (MEDIUM)
```python
def validate_phone(phone: str) -> bool:
    return any(char.isdigit() for char in phone)
```
**Issue**: Accepts any string with digits
**Risk**: No format validation
**Severity**: MEDIUM - Data quality issue

### Vulnerability #9: Path Traversal (HIGH)
```python
def read_user_file(filename: str) -> str:
    with open(filename, 'r') as f:
        return f.read()
```
**Issue**: No path validation
**Attack Example**: filename = `../../etc/passwd`
**Result**: Read any file on system
**Severity**: HIGH - Information disclosure, system compromise

---

## ⚡ Quick Start

### 1. Clone/Setup Project
```bash
cd c:\CodeAlpha_SecureCodingReview
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Application
```bash
python app.py
```

### 4. Generate Bandit Security Report
```bash
bandit -r app.py -f json -o bandit_report.json
```

### 5. View Report
```bash
cat bandit_report.json
```

---

## 📊 Bandit Report Summary

### How to Interpret Bandit Results

**Severity Levels**:
- 🔴 **HIGH**: Serious security issue, immediate attention required
- 🟠 **MEDIUM**: Potentially exploitable, should be fixed
- 🟡 **LOW**: Informational, may have security implications

**Confidence Levels**:
- **HIGH**: Issue is definite
- **MEDIUM**: Issue likely
- **LOW**: Issue possible

### Sample Bandit Output
```
>> Issue: [B105:hardcoded_password_string]
   Severity: HIGH   Confidence: MEDIUM
   Location: app.py:35
   Test ID: B105
   Hardcoded password string identified
```

---

## 🔧 Remediation Steps

### 1. Remove Hardcoded Credentials
**VULNERABLE**:
```python
API_KEY = "sk-1234567890abcdefghijklmnop"
```

**SECURE**:
```python
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('API_KEY')
```

### 2. Implement Proper Input Validation
**VULNERABLE**:
```python
def validate_username(self, username: str) -> bool:
    if len(username) < 3:
        return False
    return True
```

**SECURE**:
```python
import re

def validate_username(self, username: str) -> bool:
    if not re.match(r'^[a-zA-Z0-9_]{3,20}$', username):
        return False
    return True
```

### 3. Use Parameterized SQL Queries
**VULNERABLE**:
```python
query = f"SELECT * FROM users WHERE username='{username}'"
cursor.execute(query)
```

**SECURE**:
```python
query = "SELECT * FROM users WHERE username=?"
cursor.execute(query, (username,))
```

### 4. Use Strong Password Hashing
**VULNERABLE**:
```python
return hashlib.md5(password.encode()).hexdigest()
```

**SECURE**:
```python
import bcrypt

return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
```

### 5. Prevent Command Injection
**VULNERABLE**:
```python
command = f"grep {user_id} /etc/passwd"
result = subprocess.run(command, shell=True)
```

**SECURE**:
```python
result = subprocess.run(['grep', user_id, '/etc/passwd'], 
                       shell=False, capture_output=True)
```

### 6. Sanitize Logs
**VULNERABLE**:
```python
print(f"Card: {card_number}, CVV: {cvv}")
```

**SECURE**:
```python
masked_card = card_number[-4:].rjust(len(card_number), '*')
print(f"Card: {masked_card}, CVV: ***")
```

### 7. Use Environment Variables
**VULNERABLE**:
```python
CONFIG = {
    "db_pass": "SuperSecret123!",
    "api_key": "sk_live_51234567890",
}
```

**SECURE**:
```python
CONFIG = {
    "db_pass": os.getenv('DB_PASSWORD'),
    "api_key": os.getenv('API_KEY'),
}
```

### 8. Validate File Paths
**VULNERABLE**:
```python
with open(filename, 'r') as f:
    return f.read()
```

**SECURE**:
```python
import os

def read_user_file(self, filename: str) -> str:
    base_path = '/safe/directory'
    full_path = os.path.normpath(os.path.join(base_path, filename))
    
    # Ensure path is within base_path
    if not full_path.startswith(base_path):
        raise ValueError("Invalid file path")
    
    with open(full_path, 'r') as f:
        return f.read()
```

### 9. Implement Email Validation
**VULNERABLE**:
```python
return "@" in email
```

**SECURE**:
```python
import re

def validate_email(email: str) -> bool:
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None
```

---

## 📸 Screenshots Section

### Running the Application
```
==============================================================
Secure Coding Review - Vulnerable Application
==============================================================

This application demonstrates common security vulnerabilities.
For educational purposes only.

[*] Testing vulnerable authentication...
    [DEBUG] Executing query: SELECT * FROM users WHERE username='user@example.com' AND password='5f4dcc3b5aa765d61d8327deb882cf99'
    Authentication result: False

[*] Testing weak email validation...
    Email 'valid@email.com': True
    Email 'invalid-email': False
    Email 'test@': True
    Email '@test.com': True

[*] Testing weak phone validation...
    Phone '1234567890': True
    Phone 'abc': False
    Phone '555-1234': True
    Phone '': False

[*] Configuration values (SECURITY RISK - Hardcoded secrets):
    db_pass: SuperSecret123!
    api_key: sk_live_51234567890
    jwt_secret: my-super-secret-key-123

[!] Review the code comments for detailed vulnerability descriptions.
[!] Run 'bandit -r . -f json -o bandit_report.json' to generate report.
==============================================================
```

### Bandit Security Analysis Output
```
>> Issue: [B101:assert_used]
>> Issue: [B105:hardcoded_password_string]
   Severity: HIGH   Confidence: MEDIUM
   Location: app.py:35

>> Issue: [B106:hardcoded_password_funcarg]
   Severity: MEDIUM   Confidence: LOW
   Location: app.py:48

>> Issue: [B602:paramiko_calls]
   Severity: HIGH   Confidence: MEDIUM
   Location: app.py:89
```

---

## 🎓 Learning Outcomes

After working with this project, you will understand:

1. ✅ **Hardcoded Credentials**: Why they're dangerous and how to prevent them
2. ✅ **Input Validation**: Why weak validation enables multiple attacks
3. ✅ **SQL Injection**: How attackers bypass authentication
4. ✅ **Weak Cryptography**: Why MD5/SHA1 are unsuitable for passwords
5. ✅ **Command Injection**: How shell metacharacters enable RCE
6. ✅ **Data Protection**: Why sensitive data shouldn't be logged
7. ✅ **Path Traversal**: How directory traversal exposes files
8. ✅ **Static Analysis**: How to use Bandit for vulnerability detection

---

## 💼 Interview Preparation

### How to Present This Project

**Opening Statement**:
> "I created a deliberately vulnerable Python application to understand common security issues. It demonstrates 9 critical vulnerabilities with detailed comments explaining each issue, remediation steps, and includes Bandit static analysis."

**Key Talking Points**:
1. **What**: Educational vulnerable app with 9 security issues
2. **Why**: To learn security through practical examples
3. **How**: Used Bandit for static analysis and detection
4. **Result**: Professional documentation of vulnerabilities and fixes

### Interview Questions You Should Be Ready For

1. **"Which vulnerability is the most critical?"**
   - Answer: SQL Injection or Command Injection - both allow complete system compromise

2. **"How would you exploit the SQL Injection?"**
   - Answer: Username: `admin' --` to comment out the password check

3. **"What's wrong with MD5 hashing?"**
   - Answer: It's fast (bad for passwords), produces collisions, vulnerable to rainbow tables. Use bcrypt or Argon2 instead.

4. **"How would you fix the hardcoded credentials?"**
   - Answer: Use environment variables, .env files, or a secrets manager like AWS Secrets Manager

5. **"What does Bandit do?"**
   - Answer: Static security analysis tool that scans Python code for common vulnerabilities

---

## 🔐 Security Disclaimer

⚠️ **WARNING**: This application contains intentional security vulnerabilities and is designed for **educational purposes only**.

- **DO NOT** use this code in production
- **DO NOT** run this on public servers
- **DO NOT** expose credentials or run with real data
- **DO** study the vulnerabilities and remediation steps
- **DO** use Bandit on your own code regularly

---

## 📚 Additional Resources

### OWASP
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [CWE Top 25](https://cwe.mitre.org/top25/)
- [Secure Coding Guidelines](https://owasp.org/www-community/attacks/)

### Tools
- [Bandit Documentation](https://bandit.readthedocs.io/)
- [OWASP ZAP](https://www.zaproxy.org/)
- [SonarQube](https://www.sonarqube.org/)

### Learning Paths
- [HackTheBox](https://www.hackthebox.com/)
- [TryHackMe](https://tryhackme.com/)
- [PortSwigger Web Security Academy](https://portswigger.net/web-security)

---

## 📝 Project Structure

```
CodeAlpha_SecureCodingReview/
├── app.py                    # Vulnerable application
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── review_report.md          # Detailed vulnerability report
└── bandit_report.json        # Generated Bandit analysis
```

---

## 🚀 Next Steps

1. ✅ Run the application: `python app.py`
2. ✅ Install Bandit: `pip install -r requirements.txt`
3. ✅ Generate security report: `bandit -r app.py -f json`
4. ✅ Review vulnerabilities in code comments
5. ✅ Study remediation steps in this README
6. ✅ Create a secure version of each vulnerable function
7. ✅ Document your findings in review_report.md

---

## 👨‍💻 Author Notes

This project demonstrates that security isn't an afterthought—it must be built in from the start. Each vulnerability showcased here appears in real-world applications, making this a valuable learning tool for anyone pursuing a career in cybersecurity.

**Perfect for**:
- Portfolio projects
- GitHub showcase
- LinkedIn internship demonstrations
- Technical interview preparation
- Academic coursework
- Security training and workshops

---

## 📄 License

This educational project is provided as-is for learning purposes. Use responsibly.

---

**Last Updated**: May 2026
**Project Status**: ✅ Complete & Ready for Portfolio

