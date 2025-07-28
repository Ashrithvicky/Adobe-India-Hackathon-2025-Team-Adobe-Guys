# Use the official slim Python base image for AMD64
FROM --platform=linux/amd64 python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy all necessary files and directories into the container
COPY process_pdfs.py ./
COPY sample_dataset/schema/output_schema.json ./sample_dataset/schema/output_schema.json
COPY sample_dataset/pdfs ./sample_dataset/pdfs
COPY sample_dataset/outputs ./sample_dataset/outputs

# Create necessary folders for runtime input/output
RUN mkdir -p /app/input /app/output

# Install only required dependencies
RUN pip install --no-cache-dir pymupdf

# Default command to run the script
CMD ["python", "process_pdfs.py"]
