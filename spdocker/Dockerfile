FROM python:3.7.3
WORKDIR /bin/app
# ENV USER=cgp
# ENV HOME=/opt/cgp
# RUN mkdir -p $HOME
# RUN addgroup $USER && \
#     adduser -G $USER -D -h $HOME $USER
# WORKDIR $HOME
COPY . .
RUN echo "deb http://ftp.de.debian.org/debian stretch main contrib" >> /etc/apt/sources.list \
    && apt-get update \
    && apt-get -y install msttcorefonts \
    && pip install --upgrade pip \
    && pip3 install -r requirements.txt \
	&& chmod +x install_ref.py setup.py\
    && ./install_ref.py \
    && ./setup.py develop 
    # && chown -R $USER:$USER .
CMD ["ls"]
