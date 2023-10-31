FROM ubuntu:22.04

RUN apt-get update
RUN apt-get install -y python3 python3-pip git curl zip
RUN apt-get install -y build-essential clang libclang-dev gfortran zlib1g-dev default-jdk
RUN apt install -y python3.10-venv

ENV JAVA_HOME=/usr/lib/jvm/default-java

# Install heclib
RUN git clone -j2 --recurse-submodules https://github.com/HydrologicEngineeringCenter/hec-dss.git
WORKDIR /hec-dss/heclib/
RUN execute make clean ; make   
