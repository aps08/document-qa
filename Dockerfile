FROM python:3.11-slim

RUN groupadd -g 1234 docqateam && \
    useradd -m -u 1234 -g docqateam docqauser

USER docqauser

WORKDIR /app/docqauser

COPY requirements.txt .

RUN pip install --no-cache-dir --user -r requirements.txt && \
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc

COPY . .

EXPOSE 8000

CMD ["./start.sh"]