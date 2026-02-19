FROM python:3.13-slim
RUN pip install --no-cache-dir mkdocs-material
WORKDIR /docs
COPY mkdocs.yml .
COPY docs/ docs/
EXPOSE 8080
CMD ["mkdocs", "serve", "--dev-addr=0.0.0.0:8080"]
