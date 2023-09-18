ARG CUDA_VERSION=11.8.0
ARG OS_VERSION=22.04
# Define base image.
FROM nvidia/cuda:${CUDA_VERSION}-devel-ubuntu${OS_VERSION}

ARG USER_ID=1005

# metainformation
LABEL org.opencontainers.image.version = "0.0.1"
LABEL org.opencontainers.image.licenses = "Apache License 2.0"
LABEL org.opencontainers.image.base.name="docker.io/library/nvidia/cuda:${CUDA_VERSION}-devel-ubuntu${OS_VERSION}"

# Variables used at build time.
## CUDA architectures, required by Colmap and tiny-cuda-nn.
## NOTE: All commonly used GPU architectures are included and supported here. To speedup the image build process remove all architectures but the one of your explicit GPU. Find details here: https://developer.nvidia.com/cuda-gpus (8.6 translates to 86 in the line below) or in the docs.
# RTX3090 86 ; RTX 4090
ARG CUDA_ARCHITECTURES=89

# Set environment variables.
## Set non-interactive to prevent asking for user inputs blocking image creation.
ENV DEBIAN_FRONTEND=noninteractive
## Set timezone as it is required by some packages.
ENV TZ=Asia/Shanghai
## CUDA Home, required to find CUDA in some packages.
ENV CUDA_HOME="/usr/local/cuda"

# Install required apt packages and clear cache afterwards.
RUN chmod 777 /tmp && \
    sed -i 's/http:\/\/archive.ubuntu.com/https:\/\/mirror.sjtu.edu.cn/g' /etc/apt/sources.list && \
    apt-get update && apt-get upgrade -y 

RUN apt-get install -y --no-install-recommends \
    lsb-release \
    ca-certificates \
    software-properties-common \
    apt-transport-https \
    build-essential \
    cmake \
    curl \
    ffmpeg \
    git \
    sudo \
    vim \
    zsh \
    wget && \
    rm -rf /var/lib/apt/lists/*

RUN add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \ 
    apt install python3.11 python3.11-dev python3.11-venv python3.11-distutils -y

# Create non root user and setup environment.
RUN useradd -m -d /home/user -g root -G sudo -u ${USER_ID} user
RUN usermod -aG sudo user
# Set user password
RUN echo "user:user" | chpasswd
# Ensure sudo group users are not asked for a password when using sudo command by ammending sudoers file
RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

# Switch to new uer and workdir.
USER ${USER_ID}
WORKDIR /home/user

# Add local user binary folder to PATH variable.
ENV PATH="${PATH}:/home/user/.local/bin"
SHELL ["/bin/bash", "-c"]
RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3.11

# Upgrade pip and install packages.
RUN python3.11 -m pip config set global.index-url https://mirror.sjtu.edu.cn/pypi/web/simple
RUN python3.11 -m pip install --upgrade pip setuptools pathtools promise pybind11
# Install pytorch and submodules
RUN python3.11 -m pip install \
 torch torchvision torchaudio --index-url https://mirror.sjtu.edu.cn/pytorch-wheels/cu118

# Install tynyCUDNN (we need to set the target architectures as environment variable first).
ENV TCNN_CUDA_ARCHITECTURES=${CUDA_ARCHITECTURES}
RUN python3.11 -m pip install git+https://github.com/NVlabs/tiny-cuda-nn/#subdirectory=bindings/torch

RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH "$PATH:/home/user/.cargo/bin"
RUN echo -e "[source]\n\n[source.mirror]\nregistry = \"sparse+https://mirrors.sjtug.sjtu.edu.cn/crates.io-index/\"\n\n[source.crates-io]\nreplace-with = \"mirror\"" > ~/.cargo/config.toml
RUN cargo install fd-find ripgrep exa bat zoxide

RUN git clone https://mirrors.tuna.tsinghua.edu.cn/git/ohmyzsh.git && \
    cd ohmyzsh/tools && \
    REMOTE=https://mirrors.tuna.tsinghua.edu.cn/git/ohmyzsh.git sh install.sh

RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh
RUN bash ~/miniconda.sh -b -p $HOME/miniconda
RUN echo -e "default_channels:\n  - https://mirror.sjtu.edu.cn/anaconda/pkgs/r\n  - https://mirror.sjtu.edu.cn/anaconda/pkgs/main\ncustom_channels:\n  conda-forge: https://mirror.sjtu.edu.cn/anaconda/cloud/\n  pytorch: https://mirror.sjtu.edu.cn/anaconda/cloud/\nchannels:\n  - defaults" > ~/.condarc
RUN $HOME/miniconda/bin/conda init zsh

RUN echo 'eval "$(zoxide init zsh)"' >> ~/.zshrc && \
    echo 'export PATH="$HOME/.cargo/bin:$PATH"' >> ~/.zshrc && \
    echo 'export PATH=$HOME/.cargo/bin${PATH:+:${PATH}}' >> ~/.zshrc && \
    echo 'alias ls="exa --icons"' >> ~/.zshrc && \
    echo 'alias lsl="exa -lh --group --created --modified --time-style=long-iso --icons"' >> ~/.zshrc && \
    echo 'alias cd="z"' >> ~/.zshrc && \
    echo 'alias python="python3.11"' >> ~/.zshrc && \
    echo 'alias pip="python3.11 -m pip"' >> ~/.zshrc
