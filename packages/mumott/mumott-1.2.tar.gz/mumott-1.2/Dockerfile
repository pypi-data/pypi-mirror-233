# Base image
FROM nvidia/cuda:11.7.1-devel-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive

# Base packages
RUN \
  apt-get update -qy && \
  apt-get upgrade -qy && \
  apt-get clean && \
  apt-get autoremove --purge -y

RUN \
  apt install software-properties-common -y && \
  add-apt-repository ppa:deadsnakes/ppa 

RUN apt-get install -y --no-install-recommends \
        libgl1 \
        libglib2.0-0 \
        build-essential \
        cmake \
        libgtk2.0 \
        libglu1-mesa-dev \
        freeglut3-dev \
        mesa-common-dev \
        libosmesa6-dev \
        libegl1-mesa-dev \
        libglvnd-dev \
        libgl1-mesa-dev \
        libgles2-mesa-dev \
        qtwayland5 \
        libwayland-egl-backend-dev \
        pkg-config \
        curl \
        git \
        graphviz \
        libboost-all-dev \
        libtool \
        pandoc \
        python3.9 \
        python3.9-dev \
        python3-pip \
        python3.9-distutils \
        zip \
        xvfb

RUN \
  python3.9 -m pip install --upgrade \
    pip \
  && \
  python3.9 -m pip install --upgrade \
    coverage \
    flake8 \
    nbmake \
    pytest \
    setuptools_scm \
    twine \
    xdoctest

RUN \
  python3.9 -m pip install --upgrade \
    sphinx==5.3.0 \
    sphinx_autodoc_typehints \
    sphinx-rtd-theme \
    sphinx_sitemap \
    sphinxcontrib-bibtex \
    nbsphinx \
    ipywidgets \
    ipympl \
    PyQt5==5.14.0 \
    fqdn \
    jsonpointer \
    isoduration \
    webcolors

RUN \
  python3.9 -m pip install --upgrade \
    colorcet \
    colorspacious \
    h5py \
    matplotlib \
    numba==0.56.3 \
    numpy \
    scipy \
    scikit-image \
    tqdm \
    cupy-cuda11x \
    cython

RUN \
  curl -L http://github.com/astra-toolbox/astra-toolbox/archive/refs/tags/v2.1.0.tar.gz -o astra.tar.gz && \
  tar -xf astra.tar.gz && \
  rm -rf astra.tar.gz && \
  cd /astra-toolbox-2.1.0/build/linux && \
  ./autogen.sh && \
  ./configure --with-cuda=/usr/local/cuda \
              --with-python=/usr/bin/python3.9 \
              --with-install-type=module \
  && \
  make && \
  make install && \
  cd / && \
  rm -rf /astra-toolbox-2.1.0 && \
  python3.9 -m pip cache purge

CMD /bin/bash
