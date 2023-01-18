# Inctyper

## About

A simple tool for identifying plasmid inc type markers in assembled genomes.
The markers are source from the [plasmidfinder database](https://bitbucket.org/genomicepidemiology/plasmidfinder_db).

## Installing

- Install docker
- Clone the repository.
- Inside the repository run `docker build --rm -t inctyper .`

## Running
### Arguments

1. The path to the FASTA file
2. The NCBI taxonomic code for the genus of the organism.

### Example

```
docker run --rm -v $PWD:/data inctyper /data/my_klebsiella_genome.fasta 570
```
