# Use a lightweight Python image
FROM python:3.9-slim

# Set the working directory
WORKDIR /

# Copy the bot code into the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Command to run the bot
CMD ["python", "main.py"]
