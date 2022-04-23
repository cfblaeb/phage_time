# Purpose
Optimize the nanopore UMI protocol in regards to DNA input and sequencing run-time

### Data source (biology)
Using the nanopore UMI protocol to analyze DNA library. Small variable region in ~1 kb PCR product.
Data is produced by the minion and output is 4k reads per fastq file.
### Script
Run the nanopore UMI analysis pipeline on incrementally larger and larger datasets
1) Take data from the first 30 minutes.
2) Run the pipeline on that
3) Extract number of reads (input) and number of UMIs (output)
4) Add the next 30 minutes worth of data and repeat 

The python script generates a bash script with the actual commands.
This is done because I can write python scripts much faster than bash scripts.  
Q: But then why output a bash script? Why not just run it entirely in python?  
A: Because the supercomputer job system needs bash scripts