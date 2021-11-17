# KOCHAT Install ( Anaconda + python)
- Kochat Opensource는 Pytorch 기반하에 서비스가 실행된다. 
1. Pytorch Install
- 설치 참고 사이트 
    - https://tech.sangron.com/archives/611
    - https://jjeongil.tistory.com/1326
```
###  CUDA 설치 ###
# GPU 확인
$ lspci -k

# GUI 비활성화
$ sudo systemctl set-default multi-user

# CUDA Toolkit에 driver 동봉 되어 있으나, 별도로 설치 가능
# 별도 설치 후 Toolkit 설치 시 처음 경고는 무시하고 Continue 로 진행
$ sudo apt-get install nvidia-driver-460
$ sudo apt-get install dkms nvidia-modprobe


# 설치 확인
$ nvidia-smi

#Package Manger 설치
# - PyTorch 설치 시 Anaconda를 사용하든 pip를 사용하든 큰 차이는 없음.

# Anaconda 설치
$ curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
$ sh Miniconda3-latest-Linux-x86_64.sh
$ source ~/.bashrc

# 혹은

$ wget https://repo.anaconda.com/archive/Anaconda3-2020.11-Linux-x86_64.sh
$ chmod +x ./Anaconda3-2020.11-Linux-x86_64.sh
$ ./Anaconda3-2020.11-Linux-x86_64.sh
$ source ~/.bashrc

# 마지막에 conda init 물어보면 yes로 진행
# 만약 no로 한 경우

$ ./anaconda3/bin/conda init
$ source .bashrc

# PIP 설치
sudo apt install python3-pip
# Anaconda 사용하여 PyTorch 설치

#가상환경 만들기
$ conda create -n pytorch python=3.8
$ conda activate pytorch

비 활성 시

$ conda deactivate


# CUDA 10.2 버전 사용 시
$ conda install pytorch torchvision torchaudio cudatoolkit=10.2 -c pytorch
# Python 3.9 사용 시 ‘-c=conda-forge’ 추가할 것

# conda install pytorch torchvision torchaudio cudatoolkit=10.2 -c pytorch
# CUDA 11.1 버전 사용 시
$ conda install pytorch torchvision torchaudio cudatoolkit=11.1 -c pytorch -c conda-forge
# 맨 뒤에 -c conda-forge 옵션 반드시 필요.없을 시 cudatoolkit=11.1 package를 찾을 수 없다는 오류 발생

# 설치 확인
$ import torch
$ x = torch.rand(5, 3)
$ print(x)

Output:

tensor([[0.3380, 0.3845, 0.3217],
        [0.8337, 0.9050, 0.2650],
        [0.2979, 0.7141, 0.9069],
        [0.1449, 0.1132, 0.1375],
        [0.4675, 0.3947, 0.1426]])
# CUDA 동작 확인

$ import torch
$ torch.cuda.is_available()


# Remove Anaconda 

$ rm -rf ~/anaconda3  - 아나콘다 디렉터리 삭제

$ rm -rf ~/.anaconda_backup - 아나콘다 백업 디렉터리 삭제

$ sudo vim /etc/bash.bashrc # anaconda - PATH 삭제
 

$ conda install anaconda-clean

$ anaconda-clean --yes


## 터미널 창에서 conda 모드가 자동으로 실행되는게 싫은경우...
$conda config --set auto_activate_base False

```


