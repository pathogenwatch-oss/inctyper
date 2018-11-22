FROM python:3.6-stretch as builder

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    ncbi-blast+ \
    unzip \
    && rm -rf /var/lib/apt/lists/*

COPY src/inc_builder.py /

RUN python inc_builder.py

COPY config /

COPY src/taxid_map.py /

RUN python taxid_map.py config && \
    mv

FROM python:3.6-stretch

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    ncbi-blast+ \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /db /db

COPY src/map_species.py /

COPY src/inc_typer.py /

RUN mkdir /data

ENTRYPOINT ["python", "/inc_typer.py"]
