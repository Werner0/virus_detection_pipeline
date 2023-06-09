## Virus detection pipeline

A pipeline to detect viruses in metagenomic long reads

### Requirements: 

[metaFlye](https://github.com/fenderglass/Flye), [viralFlye](https://github.com/Dmitry-Antipov/viralFlye), [PFAM HMM models](https://www.ebi.ac.uk/interpro/download/pfam/), and mNGS long reads in FASTA format.

### Installation steps:

The following installation steps are only an example. Other approaches are also possible.

1. Clone the pipeline repository: `git clone https://github.com/Werner0/virus_detection_pipeline.git
`
2. Change to the pipeline directory: `cd virus_detection_pipeline`
3. Create a conda environment with: `conda env create -f virus_pipeline_conda.yml`
4. Activate the environment: `conda activate myclone`
5. Clone the [viralFlye](https://github.com/Dmitry-Antipov/viralFlye) repository: `git clone https://github.com/fenderglass/Flye.git`
6. Download [PFAM HMM models (Pfam-A.hmm.gz)](https://www.ebi.ac.uk/interpro/download/pfam/) to a directory of your choice
7. Unzip Pfam-A.hmm.gz 
8. Index the unzipped HMM models: `hmmpress Pfam-A.hmm`
9. Run `python virus_pipeline.py -h` for pipeline help output


### Pipeline output:

- `./viralflye_output` with virus candidates in `circulars_viralFlye.fasta` and `linears_viralFlye.fasta`, if found
- `./metaflye_output` with intermediary files including MAG contigs in `assembly.fasta`
- `./werner.log` or a log file by another name if the `-l` flag was used
