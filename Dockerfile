FROM continuumio/anaconda3
WORKDIR /chatbot-app
COPY envname.yml .
RUN conda env create --file envname.yml
SHELL ["conda", "run", "-n", "flaskProject", "/bin/bash", "-c"]
RUN echo "Make sure flask is installed:"
RUN python -c "import flask"
COPY ./chat_model ./chat_model
COPY ./label_encoder.pickle ./label_encoder.pickle
COPY ./tokenizer.pickle ./tokenizer.pickle
COPY ./intents.json ./intents.json
COPY ./trainer.py ./trainer.py
COPY ./app.py ./app.py

ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "flaskProject", "python3", "app.py"]
