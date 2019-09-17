FROM ubuntu:18.04 as taxonconfig

ARG DEBIAN_FRONTEND=noninteractive

RUN apt update \
      && apt install -y -q apt-transport-https software-properties-common \
      && apt install -y -q \
        curl \
        python3 \
      && rm -rf /var/lib/apt/lists/*

RUN curl -L https://github.com/shenwei356/taxonkit/releases/download/v0.3.0/taxonkit_linux_amd64.tar.gz | tar -xz && \
    chmod +x taxonkit && \
    cd /tmp && \
    curl -L ftp://ftp.ncbi.nih.gov/pub/taxonomy/taxdump.tar.gz | tar -xz && \
    mkdir /root/.taxonkit && \
    mv names.dmp /root/.taxonkit && \
    mv nodes.dmp /root/.taxonkit && \
    rm -rf /tmp/*

COPY config /config

COPY inctyper /

RUN python3 taxid_map.py /config /taxonkit

FROM ubuntu:18.04 as builder

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    ca-certificates \
    ncbi-blast+ \
    python3 \
    unzip \
    && rm -rf /var/lib/apt/lists/*

COPY inctyper/inc_builder.py /

RUN python3 inc_builder.py

FROM ubuntu:18.04

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    ncbi-blast+ \
    python3 \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /db /db

COPY --from=taxonconfig /genus_to_db.map /db/genus_to_db.map

COPY inctyper/inctyper_lib.py /

COPY inctyper/inc_typer.py /

RUN mkdir /data

ENTRYPOINT ["python3", "/inc_typer.py"]
