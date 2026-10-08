FROM python:3.12-alpine
WORKDIR /app
COPY app/ /app/
RUN adduser -D appuser
USER appuser
ENV PYTHONUNBUFFERED=1 \
    STUDENT_NAME=Dmitriy \
    STUDENT_SURNAME=Boyarkin \
    STUDENT_GROUP=IT2-2312 \
    STUDENT_ID=37752
EXPOSE 8080
CMD ["python", "main.py"]
