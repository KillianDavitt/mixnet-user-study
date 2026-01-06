# --- Stage 1: Build frontend with Yarn + Webpack ---
FROM node:20-alpine AS frontend-build

WORKDIR . 

COPY package.json webpack.config.js  ./
RUN mkdir static
COPY static/ucl_logo.jpg static/ucl_logo.jpg
COPY static/custom.css static/custom.css
COPY src ./src
RUN yarn install
RUN yarn build



# --- Stage 2: Python Flask App ---
FROM python:3.11-slim
WORKDIR .
COPY requirements.txt app.py questions.csv schema.sql ./
COPY templates ./templates
RUN pip install --no-cache-dir -r requirements.txt


# Copy built frontend bundle into Flask static dir
# If your output folder is not dist, change accordingly.
COPY --from=frontend-build ./static ./static

RUN apt-get update && apt-get install -y sqlite3 && rm -rf /var/lib/apt/lists/*
RUN sqlite3 db.sqlite < schema.sql

EXPOSE 8080

CMD ["flask", "run", "--host=0.0.0.0", "--port=8080"]
