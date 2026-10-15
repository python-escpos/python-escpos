# Use the official UV image
FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy

# Set the working directory to /app
WORKDIR /app

# Copy the uv.lock file and the pyproject.toml file
COPY uv.lock pyproject.toml /app/

# Install the libcups library and Git, then clean up apt lists
RUN apt-get update -y && \
    apt-get install -y libcups2-dev git && \
    rm -rf /var/lib/apt/lists/*

# Install the dependencies
RUN uv sync --frozen --no-install-project --no-dev

# Copy the rest of the application code to the container
COPY . /app

# Expose the port the application will run on
EXPOSE 8080

# Set the default command to run the application
CMD ["uv", "run", "app.py"]
