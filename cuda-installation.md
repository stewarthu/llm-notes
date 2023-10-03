## Install Cuda on Ubuntu

There are two steps:

1. Install GPU driver
2. Install CUDA toolkit


## Driver

You can use GUI (additional drivers) or CLI:

```
sudo ubuntu-drivers list --gpgpu
sudo ubuntu-drivers install --gpgpu
sudo ubuntu-drivers  install nvidiia:530
nvidia-smi
```

Note there is an issue with secure boot, on local install this is straightforward.
But there is tricky if you try install on a box in the clound. 
Chech out the following link for Azure:

https://learn.microsoft.com/en-us/azure/virtual-machines/linux/n-series-driver-setup


## Install cuda with atp

You can follow Nvidia docs:

https://docs.nvidia.com/cuda/

```
## update header files
sudo apt-get install linux-headers-$(uname -r)

## add signing key
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.1-1_all.deb
sudo dpkg -i cuda-keyring_1.1-1_all.deb
sudo apt-get update

## checkout all the versions
apt-cache madison cuda

## install the lastest 
sudo apt-get install cuda

## or install some specific version
sudo apt-get install cuda=11.8.0-1
```

Remove CUDA Toolkit:
```
sudo apt-get --purge remove "*cuda*" "*cublas*" "*cufft*" "*cufile*" "*curand*" \
 "*cusolver*" "*cusparse*" "*gds-tools*" "*npp*" "*nvjpeg*" "nsight*" "*nvvm*"
```

Remove NVIDIA Drivers:
```
sudo apt-get --purge remove "*nvidia*" "libxnvctrl*"
```

Clean up the uninstall:
```
sudo apt-get autoremove
```

Check the installed version:
```
nvcc --version
```

## Install cuda with conda

```
conda install cuda -c nvidia/label/cuda-11.8.0
## now pytorch will automatically pick up the cuda version
conda install pytorch -c pytorch
```


