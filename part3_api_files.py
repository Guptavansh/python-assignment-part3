# ============================================================
# Part 3 — File I/O, APIs & Exception Handling
# ============================================================

import requests
from datetime import datetime

# ============================================================
# Task 1: File Read & Write Basics
# ============================================================

print("========== TASK 1: FILE READ & WRITE ==========\n")

# --- Part A: Write ---
# Five provided lines written to file using write mode
notes = [
    "Topic 1: Variables store data. Python is dynamically typed.",
    "Topic 2: Lists are ordered and mutable.",
    "Topic 3: Dictionaries store key-value pairs.",
    "Topic 4: Loops automate repetitive tasks.",
    "Topic 5: Exception handling prevents crashes.",
]

# 'w' mode creates the file if it doesn't exist, or overwrites it
with open("python_notes.txt", "w", encoding="utf-8") as f:
    for line in notes:
        f.write(line + "\n")

print("File written successfully.")

# Append two more lines using append mode
with open("python_notes.txt", "a", encoding="utf-8") as f:
    f.write("Topic 6: Functions make code reusable and organised.\n")
    f.write("Topic 7: Libraries extend Python's capabilities greatly.\n")

print("Lines appended.")

# --- Part B: Read ---
print("\n-- Reading File Contents --")

with open("python_notes.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()  

# Print each line numbered, strip() removes the trailing newline
for i, line in enumerate(lines, start=1):
    print(f"{i}. {line.strip()}")

print(f"\nTotal lines in file: {len(lines)}")

# Ask user for a keyword and search for it
keyword = input("\nEnter a keyword to search: ")
matches = [line.strip() for line in lines if keyword.lower() in line.lower()]

if matches:
    print(f"\nLines containing '{keyword}':")
    for match in matches:
        print(f"  → {match}")
else:
    print(f"  No lines found containing '{keyword}'.")



# ============================================================
# Task 2: API Integration
# ============================================================

print("\n========== TASK 2: API INTEGRATION ==========\n")


print("-- Fetching 20 Products --\n")

try:
    response = requests.get(
        "https://dummyjson.com/products?limit=20",
        timeout=5
    )
    data     = response.json()
    products = data["products"]

   
    print(f"{'ID':<5} {'Title':<35} {'Category':<15} {'Price':>10} {'Rating':>8}")
    print("-" * 78)

    for p in products:
        print(f"{p['id']:<5} {p['title']:<35} {p['category']:<15} ${p['price']:>9.2f} {p['rating']:>8}")

except requests.exceptions.ConnectionError:
    print("Connection failed. Please check your internet.")
except requests.exceptions.Timeout:
    print("Request timed out. Try again later.")
except Exception as e:
    print(f"Unexpected error: {e}")


print("\n-- Products with Rating >= 4.5 (sorted by price descending) --\n")

try:
   
    high_rated = [p for p in products if p["rating"] >= 4.5]

    
    high_rated_sorted = sorted(high_rated, key=lambda p: p["price"], reverse=True)

    print(f"{'ID':<5} {'Title':<35} {'Price':>10} {'Rating':>8}")
    print("-" * 62)

    for p in high_rated_sorted:
        print(f"{p['id']:<5} {p['title']:<35} ${p['price']:>9.2f} {p['rating']:>8}")

except Exception as e:
    print(f"Error during filtering: {e}")


print("\n-- Laptops Category --\n")

try:
    response = requests.get(
        "https://dummyjson.com/products/category/laptops",
        timeout=5
    )
    laptop_data = response.json()
    laptops     = laptop_data["products"]

    for laptop in laptops:
        print(f"  {laptop['title']:<35} ${laptop['price']:.2f}")

except requests.exceptions.ConnectionError:
    print("Connection failed. Please check your internet.")
except requests.exceptions.Timeout:
    print("Request timed out. Try again later.")
except Exception as e:
    print(f"Unexpected error: {e}")

# --- Step 4: POST request — add a new product ---
print("\n-- POST Request: Add New Product --\n")

try:
    new_product = {
        "title":       "My Custom Product",
        "price":       999,
        "category":    "electronics",
        "description": "A product I created via API"
    }

    response = requests.post(
        "https://dummyjson.com/products/add",
        json=new_product,
        timeout=5
    )

    result = response.json()
    print(f"  Server Response:")
    print(f"  ID          : {result.get('id')}")
    print(f"  Title       : {result.get('title')}")
    print(f"  Price       : ${result.get('price')}")
    print(f"  Category    : {result.get('category')}")
    print(f"  Description : {result.get('description')}")

except requests.exceptions.ConnectionError:
    print("Connection failed. Please check your internet.")
except requests.exceptions.Timeout:
    print("Request timed out. Try again later.")
except Exception as e:
    print(f"Unexpected error: {e}")


# ============================================================
# Task 3: Exception Handling
# ============================================================

print("\n========== TASK 3: EXCEPTION HANDLING ==========\n")

# --- Part A: Guarded Calculator ---
def safe_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return "Error: Cannot divide by zero"
    except TypeError:
        return "Error: Invalid input types"

print("-- Safe Divide Tests --")
print(f"  safe_divide(10, 2)     : {safe_divide(10, 2)}")
print(f"  safe_divide(10, 0)     : {safe_divide(10, 0)}")
print(f"  safe_divide('ten', 2)  : {safe_divide('ten', 2)}")

# --- Part B: Guarded File Reader ---
def read_file_safe(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()
        return content
    except FileNotFoundError:
        print(f"  Error: File '{filename}' not found.")
        return None
    finally:
        # finally always runs — whether file was found or not
        print(f"  File operation attempt complete.")

print("\n-- Safe File Reader Tests --")

print("\n  Testing with 'python_notes.txt' :")
content = read_file_safe("python_notes.txt")
if content:
    print(f"  File read successfully — {len(content.splitlines())} lines found.")

print("\n  Testing with 'ghost_file.txt' :")
read_file_safe("ghost_file.txt")

# --- Part C: Robust API calls ---
print("\n-- Part C: Robust API calls already implemented in Task 2 --")
print("  Every requests.get() and requests.post() is wrapped in try/except.")
print("  Handles: ConnectionError, Timeout, and unexpected exceptions.")

# --- Part D: Input Validation Loop ---
print("\n-- Product ID Lookup (type 'quit' to exit) --\n")

while True:
    user_input = input("Enter a product ID to look up (1-100), or 'quit' to exit: ")

    # Exit condition
    if user_input.lower() == "quit":
        print("  Exiting product lookup.")
        break

  
    if not user_input.isdigit():
        print("  ⚠ Warning: Please enter a valid integer.")
        continue

    product_id = int(user_input)

    # Validate range
    if product_id < 1 or product_id > 100:
        print("  ⚠ Warning: Product ID must be between 1 and 100.")
        continue

    
    try:
        response = requests.get(
            f"https://dummyjson.com/products/{product_id}",
            timeout=5
        )

        if response.status_code == 404:
            print(f"  Product not found.")
        elif response.status_code == 200:
            product = response.json()
            print(f"  Title : {product['title']}")
            print(f"  Price : ${product['price']}")
        else:
            print(f"  Unexpected response: {response.status_code}")

    except requests.exceptions.ConnectionError:
        print("  Connection failed. Please check your internet.")
    except requests.exceptions.Timeout:
        print("  Request timed out. Try again later.")
    except Exception as e:
        print(f"  Unexpected error: {e}")


# ============================================================
# Task 4: Logging to File
# ============================================================

print("\n========== TASK 4: ERROR LOGGING ==========\n")

# --- Logger function ---
def log_error(function_name, error_type, message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] ERROR in {function_name}: {error_type} — {message}\n"

    
    with open("error_log.txt", "a", encoding="utf-8") as f:
        f.write(log_entry)

    print(f"  Logged: {log_entry.strip()}")

#
# Make a request to a genuinely unreachable URL to trigger ConnectionError
print("-- Triggering ConnectionError --")

try:
    response = requests.get(
        "https://this-host-does-not-exist-xyz.com/api",
        timeout=5
    )
except requests.exceptions.ConnectionError as e:
    log_error("fetch_products", "ConnectionError", "No connection could be made")
except requests.exceptions.Timeout:
    log_error("fetch_products", "Timeout", "Request timed out")
except Exception as e:
    log_error("fetch_products", "UnexpectedError", str(e))

# Trigger 2: HTTP 404 error
print("\n-- Triggering HTTP 404 Error --")

try:
    response = requests.get(
        "https://dummyjson.com/products/999",
        timeout=5
    )

    
    if response.status_code != 200:
        log_error(
            "lookup_product",
            "HTTPError",
            f"{response.status_code} Not Found for product ID 999"
        )
    else:
        product = response.json()
        print(f"  Found: {product['title']}")

except requests.exceptions.ConnectionError:
    log_error("lookup_product", "ConnectionError", "No connection could be made")
except requests.exceptions.Timeout:
    log_error("lookup_product", "Timeout", "Request timed out")
except Exception as e:
    log_error("lookup_product", "UnexpectedError", str(e))

# --- Print full contents of error_log.txt ---
print("\n-- Contents of error_log.txt --\n")

try:
    with open("error_log.txt", "r", encoding="utf-8") as f:
        log_contents = f.read()
    print(log_contents)
except FileNotFoundError:
    print("  error_log.txt not found — no errors were logged.")
