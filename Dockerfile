FROM python:3.12-slim

WORKDIR /dbt

# Install system dependencies for PostgreSQL
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install dbt
RUN pip install --no-cache-dir \
    "dbt-postgres>=1.9"

# Clone dbt project at runtime from git repo
# Git repo will be mounted at /git/repo via git-sync
ENTRYPOINT ["dbt"]
CMD ["--version"]