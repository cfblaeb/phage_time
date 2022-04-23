from pathlib import Path
from datetime import datetime, timedelta

fastq_in = "fastq_r10_2"
fastq_out = "fqr10/"
suffix = "*.gz"

# get the oldest and newest file in fastq_in
oldest_date = datetime.fromtimestamp(min([x.stat().st_mtime for x in Path(fastq_in).glob(suffix)]))
newest_date = datetime.fromtimestamp(max([x.stat().st_mtime for x in Path(fastq_in).glob(suffix)]))

time = 30
with open('phage_time.sh', 'w') as fi:
	fi.write("#!/bin/bash\n")
	fi.write("eval \"$('/zhome/89/0/75762/miniconda3/bin/conda' 'shell.bash' 'hook')\"\n")
	fi.write("conda activate e2\n")
	fi.write("cd /work1/laeb/phage_umi/\n")
	fi.write(f"rm -f {fastq_out}*\n")
	fi.write('echo -e "Time\\tReads\\tUmis" > phage_time.tsv\n')
	while True:

		timestamp = oldest_date + timedelta(minutes=time)
		fi.write(f"echo {time}\n")
		fi.write(f"find {fastq_in} ! -newermt '{timestamp.isoformat()}' -exec ln -sf ../'{{}}' {fastq_out} ';'\n")
		fi.write("snakemake -j 30 --configfile config_r10.yml --snakefile Snakefile\n")
		fi.write(f"echo -en '{time}\\t' >> phage_time.tsv\n")
		fi.write("head -n 1 r10_output/stats/umi_filter_reads_stats.txt | awk '{printf $3 \"\\t\"}' >> phage_time.tsv\n")
		fi.write("grep -o '>' r10_output/fasta/VHH_final.fasta | wc -l >> phage_time.tsv\n")
		fi.write("grep -o '>' r10_output/fasta/VHH_final.fasta | wc -l\n")
		if timestamp > newest_date:
			break

		time += 30
