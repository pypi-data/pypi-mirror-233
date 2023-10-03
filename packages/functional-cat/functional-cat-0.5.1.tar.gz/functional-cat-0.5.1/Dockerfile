FROM nvidia/cuda:12.2.0-devel-ubuntu22.04

ARG packages
ARG VERSION

ENV DEBIAN_FRONTEND=noninteractive 
ENV CUDA_HOME=/usr/local/cuda
ENV PATH=${CUDA_HOME}/bin:${PATH}
ENV LD_LIBRARY_PATH=${CUDA_HOME}/lib64:$LD_LIBRARY_PATH

RUN apt update
RUN apt install python3 python3-pip -y

COPY ./setup.py /functional-cat/setup.py
COPY ./pyproject.toml /functional-cat/pyproject.toml
COPY ./functional_cat /functional-cat/functional_cat

WORKDIR /functional-cat
RUN SETUPTOOLS_SCM_PRETEND_VERSION=${VERSION} pip3 install ".${packages}"

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

WORKDIR /

SHELL ["/bin/bash", "-c"]