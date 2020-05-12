# this is the base image contains all the packages, but without any reference genome 
FROM python:3.7.3
LABEL maintainer="cgphelp@sanger.ac.uk" \
      uk.ac.sanger.cgp="Cancer, Ageing and Somatic Mutation, Wellcome Sanger Institute" \
      version="0.18.1" \
      description="SigProfiler docker"
# ENV NEWUSER=cgp \
#     HOME=/opt/cgp \
#     PYTHONPATH=/opt/cgp/new_lib/:$PYTHONPATH
WORKDIR $HOME/build_dir
COPY . .
RUN echo "deb http://ftp.de.debian.org/debian stretch main contrib" >> /etc/apt/sources.list \
    && apt-get update \
    && apt-get -y install msttcorefonts \
    && pip install --upgrade pip \
    && pip install pip-release/SigProfilerExtractor-1.0.9
# RUN useradd --shell /bin/bash -g 0 $NEWUSER \
#     && chown -R $NEWUSER $HOME 
RUN chmod +x setup.py \
    && ./setup.py install
# WORKDIR $HOME
# USER $NEWUSER
CMD ["/bin/bash"]
