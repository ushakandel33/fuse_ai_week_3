SCHEMA_CONTEXT = """
Database Schema:

customers(customerNumber, customerName, phone, city, country)

orders(orderNumber, orderDate, status, customerNumber)

products(productCode, productName, productVendor, quantityInStock, buyPrice, MSRP, productLine)

employees(employeeNumber, firstName, lastName, officeCode, reportsTo, jobTitle)

offices(officeCode, city, country)

payments(customerNumber, checkNumber, paymentDate, amount)

orderdetails(orderNumber, productCode, quantityOrdered, priceEach)

productlines(productLine, textDescription)
"""

DECOMPOSITION_PROMPT = """
You are a Text-to-SQL decomposition system.

Convert the user question into JSON format.

Question:
{question}

Schema:
{schema}

Output JSON with:
- intent
- tables
- columns
- filters
- joins
"""

GENERATION_PROMPT = """
Generate PostgreSQL SQL query.

Schema:
{schema}

Decomposition:
{decomposition_json}

Rules:
- Only SELECT queries
- Use PostgreSQL syntax
- Use proper JOINs
- Use double quotes for camelCase columns
- Return ONLY SQL
"""

FIX_PROMPT = """
Fix the PostgreSQL SQL query.

Question:
{question}

Bad SQL:
{bad_sql}

PostgreSQL Error:
{error_msg}

Rules:
- Fix syntax
- Fix joins
- Fix missing quotes
- Return ONLY corrected SQL
"""