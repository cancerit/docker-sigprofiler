#### to build an image with the corresponding reference genome

`docker build --build-arg REF={REFERENCE_GENOME} -t jw32/sigprofiler-docker:{BASE_IMAGE_VERSION}-{REFERENCE_GENOME} -f Dockerfile .`

