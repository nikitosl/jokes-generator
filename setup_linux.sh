pip install --upgrade pip

conda install jaxlib=*=*cuda* jax cuda-nvcc -c conda-forge -c nvidia # work
# pip install --upgrade "jax[cuda]==0.3.15" -f https://storage.googleapis.com/jax-releases/jax_cuda_releases.html # to try
# pip install --upgrade "jax[cuda]" -f https://storage.googleapis.com/jax-releases/jax_cuda_releases.html # not work


pip install -r requirements.txt

curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | bash
apt-get install git-lfs
git lfs install

huggingface-cli login