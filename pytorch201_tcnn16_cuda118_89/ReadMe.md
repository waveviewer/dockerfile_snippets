# Envs
* Ubuntu 22.04
* PyTorch 2.01
* CUDA 11.8-CUDA Arch 89
* Aliyun Apt source
* python 3.10
* colmap(cuda+PixelPerfect SFM+pycolmap)
* tiny-cuda-nn tag v1.6
* yceres v1.0


# Usage

```
docker run --gpus all \                                         # Give the container access to nvidia GPU (required).
            -v /folder/of/your/data:/workspace/ \               # Mount a folder from the local machine into the container to be able to process them (required).
            -v /home/<YOUR_USER>/.cache/:/home/user/.cache/ \   # Mount cache folder to avoid re-downloading of models everytime (recommended).
            -p 7007:7007 \                                      # Map port from local machine to docker container (required to access the web interface/UI).
            --rm \                                              # Remove container after it is closed (recommended).
            -it \                                               # Start container in interactive mode.
            --shm-size=12gb \                                   # Increase memory assigned to container to avoid memory limitations, default is 64 MB (recommended).
            dromni/nerfstudio:<tag>                             # Docker image name if you pulled from docker hub.
            <--- OR --->
            nerfstudio                                          # Docker image tag if you built the image from the Dockerfile by yourself using the command from above.
```


```
cd neural_reconstruction
docker run --gpus all \
-v .:/workspace \
-v /home/ps/.cache/:/home/user/.cache/ \
-it \
--shm-size=12gb \
-w /workspace/ \
--net host \
--name neural_recon \
waveviewer/torch2_cu118_tcnn_base:latest
```

```
# start an existing stopped container
docker start neural_recon

# open shell
docker exec -it neural_recon /bin/bash
```