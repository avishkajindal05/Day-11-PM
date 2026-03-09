# Error Handling Checklist

## Program 1 — Student Management System

### Exceptions Caught
- ValueError
- OSError
- Exception

### Recovery Action
- Invalid inputs are rejected
- Duplicate records prevented
- File write failures handled safely

### User Message
User sees clear message such as:
"Invalid input: Marks must be between 0 and 100"

### Internal Logging
Errors written to:
student_errors.log

Example log entry:
2026-03-09 ERROR Add student failed: Duplicate student record


---

## Program 2 — Password Generator

### Exceptions Caught
- ValueError

### Recovery Action
User asked to re-enter password length.

### User Message
"Invalid input: Password length must be between 8 and 32"


---

## Program 3 — Product Catalog Tool

### Exceptions Caught
- ValueError

### Recovery Action
Invalid price ranges rejected.

### User Message
"Invalid input: Min price cannot exceed max price"


---

## Exception Handling Pattern Used

All programs follow:

try  
→ risky operation  

except  
→ handle expected error  

else  
→ run success logic  

finally  
→ cleanup / confirmation message