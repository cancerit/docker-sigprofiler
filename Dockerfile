FROM python:3.7.3
WORKDIR /bin/app
LABEL maintainer="cgphelp@sanger.ac.uk" \
      uk.ac.sanger.cgp="Cancer, Ageing and Somatic Mutation, Wellcome Trust Sanger Institute" \
      version="0.1.0" \
      description="SigProfiler docker"
ENV USER=cgp \
    HOME=/opt/cgp
RUN mkdir -p $HOME \
    && addgroup $USER \
    && adduser -G $USER -D -h $HOME $USER
WORKDIR $HOME
COPY . .
RUN echo "deb http://ftp.de.debian.org/debian stretch main contrib" >> /etc/apt/sources.list \
    && apt-get update \
    && apt-get -y install msttcorefonts \
	&& chmod +x ./build/install_ref.py setup.py \
    && ./build/install_ref.py \
    && ./setup.py develop \
    && chown -R $USER:$USER . \
    && rm -rf *
USER cgp
CMD ["/bin/bash"]
