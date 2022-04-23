"""
generate sets of the following commands
	1. generate a timestamp thats 30 min older than prev
	2. find /work1/laeb/phage_umi/fastq_r10 ! -newermt "2022-04-21 06:00" -exec ln -s '{}' . ';'
	3. snakemake -j 30 --configfile config_r10.yml --snakefile Snakefile
	4. wc -l < r10_output/fasta/VHH_final.fasta
	5. r10_output/stats/umi_filter_reads_stats.txt
"""
from pathlib import Path
from datetime import datetime, timedelta

fastq_in = "/tmp/"
fastq_out = "/tmp3/"
suffix = "*"

# get the oldest file in fastq_in
oldest_date = datetime.fromtimestamp(min([x.stat().st_mtime for x in Path(fastq_in).glob(suffix)]))
newest_date = datetime.fromtimestamp(max([x.stat().st_mtime for x in Path(fastq_in).glob(suffix)]))

time = 30
with open('phage_time.sh', 'w') as fi:
	fi.write("#!/bin/bash\n")
	fi.write('echo -e "Time\\tReads\\tUmis" > phage_time.tsv\n')
	while True:

		timestamp = oldest_date + timedelta(minutes=time)
		fi.write(f"echo {time}\n")
		fi.write(f"find {fastq_in} ! -newermt '{timestamp.isoformat()}' -exec ln -s '{{}}' {fastq_out} ';'\n")
		fi.write("snakemake -j 30 --configfile config_r10.yml --snakefile Snakefile\n")
		fi.write(f"echo -en '{time}\\t' >> phage_time.tsv\n")
		fi.write("head -n 1 r10_output/stats/umi_filter_reads_stats.txt | awk '{printf $3 \"\\t\"}' >> phage_time.tsv\n")
		fi.write("grep -o '>' r10_output/fasta/VHH_final.fasta | wc -l >> phage_time.tsv\n")
		fi.write("grep -o '>' r10_output/fasta/VHH_final.fasta | wc -l\n")
		if timestamp > newest_date:
			break

		time += 30
		break
