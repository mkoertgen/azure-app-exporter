FROM python:3.10.2-slim-bullseye as base
WORKDIR /app

COPY requirements*.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

FROM base as test
RUN pip install --no-cache-dir -r requirements-dev.txt
RUN python -m pytest --cov


FROM base as final
ARG GIT_COMMIT=unknown
ARG BUILD_DATE=unknown
ARG BUILD_VERSION=0.1.0

ENV GIT_COMMIT ${GIT_COMMIT}
ENV BUILD_DATE ${BUILD_DATE}
ENV BUILD_VERSION ${BUILD_VERSION}

ENV TZ UTC

ENTRYPOINT [ "/app/docker-entrypoint.sh" ]
