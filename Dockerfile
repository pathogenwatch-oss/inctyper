FROM python:3.6-stretch as taxonconfig

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

RUN python taxid_map.py /config /taxonkit

FROM python:3.6-stretch as builder

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    ncbi-blast+ \
    unzip \
    && rm -rf /var/lib/apt/lists/*

COPY inctyper/inc_builder.py /

RUN python inc_builder.py

FROM python:3.6-stretch

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    ncbi-blast+ \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /db /db

COPY --from=taxonconfig /genus_to_db.map /db/genus_to_db.map

COPY inctyper/inctyper_lib.py /

COPY inctyper/inc_typer.py /

RUN mkdir /data

ENTRYPOINT ["python", "/inc_typer.py"]
