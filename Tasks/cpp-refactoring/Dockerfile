FROM gcc:5

WORKDIR /app

RUN apt-get update
RUN apt-get install -y libjsoncpp-dev

COPY . .

ENV LD_LIBRARY_PATH=/usr/lib
RUN echo ${LD_LIBRARY_PATH}


RUN chmod -R 777 .
ENTRYPOINT [ "/app/entrypoint.sh" ]

# CMD ["sh","-c","make run"]

