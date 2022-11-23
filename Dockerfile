FROM python:3.10-slim

# Set pip to have cleaner logs and no saved cache
ENV PIP_NO_CACHE_DIR=false

# Create the working directory
WORKDIR /sage

# Install project dependencies

RUN pip install -U pip wheel setuptools
RUN pip install poetry==1.2.2

# export requirements after copying req files
COPY pyproject.toml poetry.lock ./
RUN poetry export --without-hashes > requirements.txt
RUN pip uninstall poetry -y
RUN pip install -Ur requirements.txt

# Set SHA build argument
ARG git_sha="main"
ENV GIT_SHA=$git_sha

# Copy the source code in next to last to optimize rebuilding the image
COPY . .

# install the package using pep 517
RUN pip install . --no-deps

# this is a basic start command that will not be used in the future
CMD ["sh", "entrypoint.sh"]
