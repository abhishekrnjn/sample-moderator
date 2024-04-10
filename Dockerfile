FROM python:3.12-bookworm

ENV OPENAI_API_KEY "<your key>"

RUN pip install -U git+https://github.com/FujitsuResearch/atproto-python.git
RUN pip install -U langchain langchain-openai

RUN git clone -b main https://github.com/abhishekrnjn/sample-moderator.git
WORKDIR /sample-moderator

CMD ["python3"]