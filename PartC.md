```markdown
# Python Exception Handling — Conceptual, Coding, and Debugging

---

# Q1 — Conceptual

## Execution Flow of `try`, `except`, `else`, and `finally`

Python's exception-handling system provides four blocks that control how errors are managed during program execution.

```

try
except
else
finally

````

Each block serves a specific purpose.

---

## 1. `try` Block

The `try` block contains code that **may potentially raise an exception**.

- Python executes the statements inside `try`.
- If **no error occurs**, execution continues to `else`.
- If **an exception occurs**, Python jumps to the matching `except` block.

Example:

```python
try:
    x = int("10")
````

---

## 2. `except` Block

The `except` block handles exceptions raised inside `try`.

* Executes **only if an exception occurs**
* Can catch **specific exceptions**

Example:

```python
try:
    x = int("abc")
except ValueError:
    print("Invalid integer")
```

---

## 3. `else` Block

The `else` block executes **only if the `try` block completes successfully without exceptions**.

Purpose:

* Separate the **main logic** from **error-prone code**

Example:

```python
try:
    x = int("20")
except ValueError:
    print("Conversion failed")
else:
    print("Conversion successful:", x)
```

Execution order if no exception:

```
try → else → finally
```

---

## 4. `finally` Block

The `finally` block **always executes**, regardless of whether an exception occurred.

Typical use cases:

* Closing files
* Releasing resources
* Cleanup operations

Example:

```python
try:
    f = open("data.txt")
except FileNotFoundError:
    print("File not found")
finally:
    print("Execution finished")
```

Execution order:

```
try → except → finally
```

or

```
try → else → finally
```

---

# Example Using All Four Blocks

```python
try:
    file = open("data.json", "r")
    data = file.read()

except FileNotFoundError:
    print("File does not exist")

else:
    print("File read successfully")

finally:
    print("Closing resources")
```

Execution scenarios:

### Case 1 — File exists

```
try → else → finally
```

### Case 2 — File missing

```
try → except → finally
```

---

## What Happens if an Exception Occurs Inside `else`?

If an exception occurs inside the `else` block:

* It is **not handled by the preceding `except` block**
* The error propagates outward unless another `try/except` exists
* `finally` still executes

Example:

```python
try:
    x = int("10")
except ValueError:
    print("Conversion error")
else:
    y = int("abc")   # Exception occurs here
finally:
    print("Cleanup")
```

Output:

```
Cleanup
ValueError traceback
```

The exception inside `else` is **not caught by the earlier `except`**.

---

# Q2 — Coding

## Function: `safe_json_load(filepath)`

Requirements:

* Safely read a JSON file
* Handle:

  * `FileNotFoundError`
  * `json.JSONDecodeError`
  * `PermissionError`
* Return parsed dictionary on success
* Return `None` on failure
* Log all errors

---

## Implementation

```python
import json
import logging

logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def safe_json_load(filepath):

    try:
        with open(filepath, "r") as f:
            data = json.load(f)

    except FileNotFoundError as e:
        logging.error(f"File not found: {filepath} | {e}")
        return None

    except json.JSONDecodeError as e:
        logging.error(f"Invalid JSON format in file: {filepath} | {e}")
        return None

    except PermissionError as e:
        logging.error(f"Permission denied for file: {filepath} | {e}")
        return None

    else:
        return data
```

---

## Example Usage

```python
data = safe_json_load("config.json")

if data:
    print("JSON Loaded:", data)
else:
    print("Failed to load JSON file")
```

---

# Q3 — Debug / Analyze

## Original Code

```python
def process_data(data_list):
    results = []
    for item in data_list:
        try:
            value = int(item)
            results.append(value * 2)
        except:
            print("Error occurred")
            continue
        finally:
            return results
    return results
```

---

# Problems in the Original Code

### 1. Bare `except` Block

```
except:
```

Issues:

* Catches **all exceptions**
* Includes system-level exceptions:

  * `KeyboardInterrupt`
  * `SystemExit`

Best practice: catch **specific exceptions**.

---

### 2. `return` Inside `finally`

```
finally:
    return results
```

Problem:

* `finally` executes **after every iteration**
* The function returns during the **first loop iteration**
* The rest of the list never gets processed.

---

### 3. Poor Error Message

```
print("Error occurred")
```

Issues:

* Does not show:

  * Which value failed
  * What the exception was

Debugging becomes difficult.

---

# Corrected Implementation

```python
def process_data(data_list):

    results = []

    for item in data_list:
        try:
            value = int(item)
            results.append(value * 2)

        except ValueError as e:
            print(f"Invalid value '{item}' skipped: {e}")
            continue

    return results
```

---

# Improved Behavior

Example input:

```python
data = ["10", "20", "abc", "40"]
```

Output:

```
Invalid value 'abc' skipped: invalid literal for int()
[20, 40, 80]
```

---

# Why This Design Is Correct

### Specific Exception Handling

```
except ValueError
```

Handles only invalid integer conversions.

---

### Loop Continues Properly

`return` is placed **after the loop**, allowing all items to be processed.

---

### Informative Error Logging

```
Invalid value 'abc' skipped
```

This helps debugging data pipelines.

---

# Key Takeaways

* `try` contains risky operations.
* `except` handles specific exceptions.
* `else` runs only if `try` succeeds.
* `finally` always executes.

Best practices:

* Avoid bare `except`
* Never place `return` inside `finally`
* Provide detailed error messages
* Catch only expected exceptions

---

```
```
