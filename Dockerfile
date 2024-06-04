FROM ubuntu:latest
LABEL authors="watermelon"

ENTRYPOINT ["top", "-b"]