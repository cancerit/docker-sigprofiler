# SigProfiler docker image
[![Build Status](https://travis-ci.org/cancerit/docker-sigprofiler.svg?branch=master)](https://travis-ci.org/cancerit/docker-sigprofiler)
[![Build Status](https://travis-ci.org/cancerit/docker-sigprofiler.svg?branch=develop)](https://travis-ci.org/cancerit/docker-sigprofiler)

SigProfiler is a set of tools that extract mutational signatures from `vcf files` or `mutational matrices`. This project is created as a downstream tool in the `SigProfiler` python framework. This tool encapsulated the original `SigProfiler packages` developed by [The Alexandrov Lab](https://alexandrov.cloud.ucsd.edu/) into [docker](https://www.docker.com/) containers to frozen the computational environment when doing the signature extractions. When using the docker container, the SigProfiler tools are executing in an isolated run-time environment which has the minium dependency on the host system. Therefore, it helps end-users to generate consistent results. 

-------
## Docker container

[![Docker Repository on Quay](https://quay.io/repository/superjw/docker-sigprofiler/status "Docker Repository on Quay")](https://quay.io/repository/superjw/docker-sigprofiler)

The SigProfiler docker containers are available at [`quay.io`](https://quay.io/repository/superjw/docker-sigprofiler)

---

