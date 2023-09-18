# Args to specify
ARG CUDA_VERSION=11.8.0
ARG OS_VERSION=22.04
ARG USER_ID=1005 
ARG CUDA_ARCHITECTURES=89

Guide
* https://hub.docker.com/r/nvidia/cuda
* https://pytorch.org/get-started/locally/ 

# Components

* python3.11
* Rust & Terminal tools
* tiny-cuda-nn 1.7
* pytorch latest-stable
* cuda 11.8
* miniconda3
* Apt, conda, pytorch, rust mirrors from SJTU