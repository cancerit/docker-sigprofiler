FROM jw32/sigprofiler-docker:0.18-base
ARG REF
WORKDIR /usr/home
COPY genome_install.py .
RUN python3 genome_install.py