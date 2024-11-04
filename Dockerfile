FROM python:3.12-slim AS taxonconfig

ARG DEBIAN_FRONTEND=noninteractive

RUN apt update \
      && apt install -y -q --no-install-recommends apt-transport-https software-properties-common curl \
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

FROM python:3.12-slim AS builder

RUN apt-get update \
    && apt-get install -y -q --no-install-recommends \
    ca-certificates \
    curl \
    unzip \
    && rm -rf /var/lib/apt/lists/*

RUN  mkdir -p /tmp/blast \
      && mkdir /opt/blast \
      && curl ftp://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/2.9.0/ncbi-blast-2.9.0+-x64-linux.tar.gz \
      | tar -zxC /tmp/blast --strip-components=1 \
      && cd /tmp/blast/bin \
      && mv blastn makeblastdb blastp /opt/blast/ \
      && cd .. \
      && rm -rf /tmp/blast

ENV PATH /opt/blast:$PATH

COPY inctyper/incbuilder.py /

RUN python3 incbuilder.py

FROM python:3.12-slim AS production

COPY --from=builder /db /db

COPY --from=builder /opt/blast/blastn /opt/blast/blastn

COPY --from=taxonconfig /genus_to_db.map /db/genus_to_db.map

COPY inctyper/inctyper_lib.py /

COPY inctyper/inctyper.py /

ENV PATH /opt/blast:$PATH

RUN mkdir /data

ENTRYPOINT ["python3", "/inctyper.py"]
