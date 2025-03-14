FROM python:3.12 as builder

# Bring poetry, our package manager
ARG POETRY_VERSION=1.8.1
RUN pip install --no-cache-dir \
    poetry==${POETRY_VERSION}

# Copy code in to build a package
COPY . /workdir/
WORKDIR /workdir

RUN poetry build -f wheel

# Start over with just the binary package install
FROM python:3.12-slim as runner

# Bring the wheel file
COPY --from=builder /workdir/dist /app

# Install the package
RUN pip install --no-cache-dir /app/*.whl

ENTRYPOINT ["reforger-backendless"]
