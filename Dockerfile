# Use nextflow/nextflow:22.10.8 as a base image
FROM nextflow/nextflow:22.10.8

# Install dependencies
RUN apt-get update && apt-get install -y \
    curl \
    sudo \
    python3.9 \
    python3-pip

RUN git clone https://github.com/mirand863/gcsplit.git && cd gcsplit && bash install.sh && source ~/.bashrc

# Install flytekit and scikit-learn
RUN pip3 install flytekit scikit-learn

# Install Flyte
RUN curl -sL https://ctl.flyte.org/install | sudo bash -s -- -b /usr/local/bin
