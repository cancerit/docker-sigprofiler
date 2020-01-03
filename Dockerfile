FROM python:3.7.3
LABEL maintainer="cgphelp@sanger.ac.uk" \
      uk.ac.sanger.cgp="Cancer, Ageing and Somatic Mutation, Wellcome Sanger Institute" \
      version="0.1.0" \
      description="SigProfiler docker"
ENV NEWUSER=cgp \
    HOME=/opt/cgp
WORKDIR $HOME/build_dir
COPY . .
RUN useradd --shell /bin/bash -g 0 $NEWUSER \
    && echo "deb http://ftp.de.debian.org/debian stretch main contrib" >> /etc/apt/sources.list \
    && apt-get update \
    && apt-get -y install msttcorefonts \
	&& chmod +x ./build/install_ref.py setup.py \
    && ./setup.py develop \
    && ln -s /usr/local/lib/python3.7/site-packages/SigProfilerMatrixGenerator-1.0.21-py3.7.egg/SigProfilerMatrixGenerator/references/ \
    $HOME/references
WORKDIR $HOME
USER $NEWUSER
CMD ["/bin/bash"]
