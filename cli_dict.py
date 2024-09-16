class CliDict:
    def __init__(self):
        self.help_general = {
            "input": "csv file with four columns: sample_id,lib_id,read_1,read_2(see ./example_files/example_input.csv)",
            "outdir": "path to the directory, where all the outputs will be stored. If the directory is not present, it will be created.",
            "reference": "the fastq files will be aligned to the reference assembly of this species",
            "slurm_template": "path to the slurm template",
            "num_cpus": "maximum number of cpus to be used for the alignment process",
            "user-email":"email on which the notification will be sent once the job is ended"
        }

        self.param_general = {
            "input": "null",
            "outdir": "fqtobam",
            "reference": "null",
            "num_cpus": 16,
            "slurm_template": "null",
            "user-email":"null"
        }

        self.help_tools = {
            "trim-galore": "to trim the adapter",
            "sickle": "to filter the fastq files",
            "bwa-mem": "to align the paired-end fastq files",
            "samtools-view": "to convert aligned sam to bam file",
            "sambamba-sort": "to sort the bam file",
            "sambamba-markdup": "to mark duplicate the bam file",
            "fastqc": "summary statistics of the fastqc file",
            "qualimap":"summary statistics of the bam file"
        }

        self.param_tools = {
            "trim-galore": " --paired ",
            "sickle": " -t sanger -g ",
            "bwa-mem": "null",
            "samtools-view": " -q 20",
            "sambamba-sort": "null",
            "sambamba-markdup": " -r ",
            "fastqc": "null",
            "qualimap":"null",
        }


        self.dict_list = [self.param_general, self.param_tools]
        self.ref_path_dict = {
            "cattle": "/dss/dssfs03/u8401/u8401-dss-0001/references/bos_taurus/genome/ars_ucd/1.2/genome.fa.gz"
        }

        self.citation_dict = {
            "apply_indi_filters": [
                "./bibtex/plink.bibtex",
                "./bibtex/vcftools.bibtex",
            ],
            "apply_snp_filters": [
                "./bibtex/plink.bibtex",
                "./bibtex/vcftools.bibtex",
            ],
            "ld_filt": ["./bibtex/plink.bibtex"],
            "pca": ["./bibtex/eigensoft.bibtex"],
            "admixture": ["./bibtex/admixture.bibtex"],
            "pairwise_global_fst": ["./bibtex/plink.bibtex", "./bibtex/toytree.bibtex"],
            "ibs_dist": ["./bibtex/plink.bibtex", "./bibtex/ete3.bibtex"],
            "treemix": ["./bibtex/treemix.bibtex"],
            "selscan": ["./bibtex/selscan.bibtex"],
            "beagle5": ["./bibteX/beagle.bibtex"],
            "shapeit5": ["./bibtex/shapeit5.bibtex"],
            "fst": ["./bibtex/vcftools.bibtex"],
            "tajimas_d": ["./bibtex/vcftools.bibtex"],
            "pi_val": ["./bibtex/vcftools.bibtex"],
            "ihs": [
                "./bibtex/ihs.bibtex",
                "./bibtex/selscan.bibtex",
                "./bibtex/ehh.bibtex",
            ],
            "xpehh": [
                "./bibtex/xpehh.bibtex",
                ".bibtex/selscan.bibtex",
                "./bibtex/ehh.bibtex",
            ],
        }
