FROM python:3.7.3
LABEL maintainer="cgphelp@sanger.ac.uk" \
      uk.ac.sanger.cgp="Cancer, Ageing and Somatic Mutation, Wellcome Sanger Institute" \
      version="0.1.0" \
      description="SigProfiler docker"
ENV NEWUSER=cgp \
    HOME=/opt/cgp
WORKDIR $HOME/build_dir
COPY . .
RUN echo "deb http://ftp.de.debian.org/debian stretch main contrib" >> /etc/apt/sources.list \
    && apt-get update \
    && apt-get -y install msttcorefonts
RUN useradd --shell /bin/bash -g 0 $NEWUSER 
RUN chmod +x setup.py \
    && ./setup.py develop
WORKDIR $HOME
USER $NEWUSER
CMD ["/bin/bash"]
