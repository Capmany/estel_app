FROM python:3.11

#ARG API_URL

WORKDIR /app
COPY . .

ENV VIRTUAL_ENV=/app/.venv_docker
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN python3.11 -m venv $VIRTUAL_ENV

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

 # Per desplegar el frontend
 # Deploy templates and prepare app
#RUN reflex init
 # Download all npm dependencies and compile frontend
#RUN reflex export --frontend-only --no-zip
 # Needed until Reflex properly passes SIGTERM on backend.
#STOPSIGNAL SIGKILL
 # Always apply migrations before starting the backend.
#CMD [ -d alembic ] && reflex db migrate; reflex run --env prod
 # FI si es vol també desplegar el frontend

# Per desplegar només el backend
CMD [ -d alembic ] && reflex db migrate; reflex run --env prod --backend-only
