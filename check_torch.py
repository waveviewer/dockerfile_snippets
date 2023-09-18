import torch


def gpu_info() -> str:
    info = ''
    for id in range(torch.cuda.device_count()):
        p = torch.cuda.get_device_properties(id)
        info += f'CUDA:{id} ({p.name}, {p.total_memory / (1 << 20):.0f}MiB)\n'
    return info


if __name__ == "__main__":
    print("============TorchCompileConfig============")
    print(torch.__config__.show())
    print("==========================================")
    print(f"GPU detection : {torch.cuda.is_available()}")
    print(gpu_info())
    pass