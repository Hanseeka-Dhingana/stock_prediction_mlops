# 1. Use a lightweight Python version
FROM python:3.12-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy the requirements file first (for caching)
COPY requirements.txt .

# 4. Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of your code
COPY . .

# 6. Expose the port (Railway will set $PORT, but 8000 is default)
EXPOSE 8000

# 7. The command to run your API
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]