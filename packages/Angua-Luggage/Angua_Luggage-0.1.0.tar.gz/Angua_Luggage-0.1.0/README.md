#Angua_Luggage is a post-pipeline processing helper

##Installing

For now, create a conda environment with the following packages: pysam Biopython pandas rpy2 seqtk conda-build Megan Blast mmseqs2 bbmap bioconductor-gviz bioconductor-plyranges bioconductor-orfik pfam_scan bwa-mem2 moose-perl bedtools pigz pysam spades trinity fastqc multiqc
I would recommend using mamba for this. It resolves much more quickly.
If you're just using Angua and you're Sam, forget the extras other than maybe pandas! 
Whichever environment you use, activate it and navigate to where you've placed the downloaded directory. Navigate into the top layer of the directory and enter:
pip install -e Angua_Luggage.

This is temporary until a Conda recipe is available.

##Quick-start

To run Angua as normal:

Angua main [RAW_READS] [OUTPUT_DIR] -pa2t [MEGAN PROTEIN DB] -na2t [MEGAN NUC DIR] -nt-db [NUCLEOTIDE BLAST DB] -nr-db [PROTEIN BLAST DB] --cluster -bba [BBDUK ADAPTER FILE]

You can do this from the directory containing the raw directory or using absolute paths to the raw and output directory; both should work.

Angua automatically creates .finished files to track its progress and allow you to pick up where you left off. Remove these if you want to repeat a step for whatever reason.

##Luggage use cases

Angua_Luggage is a Bioinformatics tool bringing together a few useful pieces of software to analyse the output of the Angua pipeline (other pipeline outputs can be used in theory). If you use another pipeline, Luggage might still work for you; as long as you have contigs and Blast files in XML format/.rma6 format Megan files, Luggage should be of use to you.

Luggage has two main functions. One is to quickly summarise pipeline (Blastn/X/Megan) output in .csv format (and output contigs matching desired species, if possible). The other is to automate some basic annotations of contigs: pfam domains and ORFs, alongside coverage. This is to aid in triage in case of several novel viruses, or just a quick way of looking at coverage for diagnostic purposes.

##Inputs to Luggage

In all cases Luggage will need a directory. If you just have one file, please put it in a directory by itself first.

