import os
import shutil
import os.path
import time
import re
import prompt_toolkit
from prompt_toolkit.completion import PathCompleter
from beaupy.spinners import *
from beaupy import prompt, select
from rich.console import Console
import pyfiglet
from cli_dict import CliDict as dictionary

console = Console()


class util:
    def print_global_header(self):
        f = pyfiglet.figlet_format("fastq to bam", font="starwars", width=200)
        print(f)

    def print_local_header(self, name):
        console.print(f"[yellow]{name}[/yellow]")
        console.print(f"type n to skip entering any parameter")

    def clear_screen(self):
        os.system("clear")

    def regex_pattern(self, name):
        pattern = "(\[.+?\])(.*)(\[.+?\])(:)(.*)"
        match = re.findall(pattern, name)
        return match[0][1]

    def read_options(self, dict):
        gpl = []
        for key in dict:
            gpl.append(f"[yellow]{key}[/yellow]: [green]{dict[key]}[/green]")
        gpl.append("back")
        name = select(gpl)
        name = str(name) if name == "back" else self.regex_pattern(str(name))
        return name

    def read_suboption(self, param, help_message, default_param, ref_dict):
        console.print(f"{param}:{help_message}")
        gpl = []
        for species in ref_dict:
            gpl.append(
                f"[yellow]{species}[/yellow]: [green]{ref_dict[species]}[/green]"
            )
        gpl.append("back")
        name = select(gpl)
        name = (
            default_param if name == "back" else ref_dict[self.regex_pattern(str(name))]
        )
        return name

    def is_file_exist(self, file, default_param):
        lc = 0
        is_exist = True
        with open(file) as source:
            for line in source:
                line = line.rstrip().split(",")
                if lc == 0:
                    exp_header = ["sample", "lib", "fastq_1", "fastq_2"]
                    if exp_header != line:
                        console.print(
                            f'[red]the header should be:{",".join(exp_header)} but it is: {line}[/red]'
                        )
                        is_exist = False
                        time.sleep(1)
                    lc += 1
                else:
                    if not os.path.isfile(line[2]) or not os.path.isfile(line[3]):
                        console.print(
                            f"[red]fastq_1 or/and fastq_2 does not exits for {line}[/red]"
                        )
                        time.sleep(1)
                        is_exist = False
        return file if is_exist else default_param

    def read_file_prompt(self, param, help_message, default_param, ext):
        console.print(help_message)
        param_var = param + ":"
        param_f = prompt_toolkit.prompt(
            param_var,
            completer=PathCompleter(),
        )
        if param_f == "n":
            return default_param
        elif not os.path.isfile(param_f) or not param_f.endswith(ext):
            console.print(
                f"[red]{param_var}{param_f} does not exist or does not end with {ext}[/red]"
            )
            time.sleep(1)
            return default_param
        else:
            param_f = (
                self.is_file_exist(param_f, default_param)
                if param == "input"
                else param_f
            )
            param_f = os.path.abspath(str(param_f))
            return param_f

    def read_string_prompt(self, param, help_message, default_param):
        string_o = default_param
        console.print(help_message)
        param_var = param + ":"
        string_o = prompt(param_var, target_type=str)
        return string_o if string_o != "n" else default_param

    def read_int_prompt(self, param, help_message, default_param, min_i, max_i):
        console.print(help_message)
        param_var = param + ":"
        int_o = prompt(param_var)
        if int_o == "n":
            return default_param
        else:
            int_o = int(int_o)
        return int_o


class SetGeneralParameters:
    def __init__(self, param_general):
        self.d = dictionary()
        self.u = util()
        self.help_general = self.d.help_general
        self.param_general = param_general
        self.ref_path_dict = self.d.ref_path_dict

    def main_function(self):
        self.u.print_global_header()
        self.u.print_local_header("setting the general parameters")
        name = self.u.read_options(self.param_general)
        map_ext_dict = {
            "input": ".csv",
            "slurm_template": ".sh",
        }
        int_param_dict = {
            "num_cpus": [1, 99],
        }
        str_list = ["outdir","user-email"]
        option_list = ["reference"]
        while name != "back":
            if name in map_ext_dict:
                update_param = self.u.read_file_prompt(
                    name,
                    self.help_general[name],
                    self.param_general[name],
                    map_ext_dict[name],
                )
            if name in str_list:
                update_param = self.u.read_string_prompt(
                    name, self.help_general[name], self.param_general[name]
                )
            if name in int_param_dict:
                update_param = self.u.read_int_prompt(
                    name,
                    self.help_general[name],
                    self.param_general[name],
                    int_param_dict[name][0],
                    int_param_dict[name][1],
                )
            if name in option_list:
                console.print(name)
                update_param = self.u.read_suboption(
                    name,
                    self.help_general[name],
                    self.param_general[name],
                    self.ref_path_dict,
                )
            console.print(name)
            self.param_general[name] = update_param
            self.u.clear_screen()
            self.u.print_global_header()
            self.u.print_local_header("setting the general parameters")
            name = self.u.read_options(self.param_general)
        self.u.clear_screen()
        return self.param_general


class SetToolParameters:
    def __init__(self, param_tools):
        self.d = dictionary()
        self.u = util()
        self.help_tools = self.d.help_tools
        self.param_tools = param_tools

    def main_function(self):
        self.u.print_global_header()
        self.u.print_local_header("setting the parameters of the tools")
        name = self.u.read_options(self.param_tools)
        while name != "back":
            update_param = self.u.read_string_prompt(
                name, self.help_tools[name], self.param_tools[name]
            )
            self.param_tools[name] = update_param
            self.u.clear_screen()
            self.u.print_global_header()
            self.u.print_local_header("setting the general parameters")
            name = self.u.read_options(self.param_tools)
        self.u.clear_screen()
        return self.param_tools


class SaveSlurmScript:
    def __init__(self, param_general, param_tools):
        self.param_tools = param_tools
        self.param_general = param_general

    def template_to_list(self, slurm_template):
        template_list = []
        with open(slurm_template) as source:
            for line in source:
                line = line.rstrip()
                template_list.append(line)
        return template_list

    def csv_to_dict(self, input_csv):
        sample_fq_dict = {}
        header = 0
        with open(input_csv) as source:
            for line in source:
                if header == 0:
                    header += 1
                else:
                    line = line.rstrip().split(",")
                    sample_fq_dict[line[0]] = [line[1], line[2], line[3]]
        return sample_fq_dict

    def write_slurm_script(self):
        slurm_template_list = self.template_to_list(
            self.param_general["slurm_template"]
        )
        success = False
        sample_fastq_dict = self.csv_to_dict(self.param_general["input"])
        num_cpus = int(self.param_general["num_cpus"])
        for sample in sample_fastq_dict:
            lib1, fq1, fq2 = sample_fastq_dict[sample]
            with open(f"{sample}_fqtobam.sh", "w") as dest:
                for line in slurm_template_list:
                    if "-J" in line or "--job-name" in line:
                        line = f"{line}_{sample}"
                    dest.write(line)
                    dest.write("\n")
                if self.param_general["user-email"] != "null":
                    dest.write(f'#SBATCH --mail-user={self.param_general["user-email"]}\n')
                dest.write("\n")
                dest.write("#load module to launch conda\n")
                dest.write("module load anaconda3\n")
                dest.write(
                    "source activate /dss/dssfs03/u8401/u8401-dss-0001/tools/fqtobam/"
                )
                dest.write("\n")
                dest.write("#create a directory to store the files\n")
                # string for output directory
                outdir_str = f'$SCRATCH/$USER/{self.param_general["outdir"]}/{sample}'
                prefix = f"{sample}_{lib1}"
                dest.write(f"mkdir -p {outdir_str}\n")
                for tool in self.param_tools:
                    args = (
                        self.param_tools[tool]
                        if self.param_tools[tool] != "null"
                        else ""
                    )
                    if "trim-galore" in tool:
                        dest.write('echo "Starting Trim Galore"\n')
                        dest.write(
                            f"trim_galore -j {num_cpus} {args} -o {outdir_str} --basename {prefix} {fq1} {fq2}\n"
                        )
                    if "sickle" in tool:
                        dest.write('echo "Starting sickle"\n')
                        dest.write(
                            f"sickle pe {args} -f {outdir_str}/{prefix}_val_1.fq.gz -r {outdir_str}/{prefix}_val_2.fq.gz -o {outdir_str}/{prefix}_trimmed_1.fq.gz -p {outdir_str}/{prefix}_trimmed_2.fq.gz -s {outdir_str}/{prefix}_singleton.fq.gz\n"
                        )
                    if "bwa" in tool:
                        dest.write('echo "Starting bwa-mem"\n')
                        bwa_str = f'bwa mem -t {num_cpus} {args} {self.param_general["reference"]} {outdir_str}/{prefix}_trimmed_1.fq.gz {outdir_str}/{prefix}_trimmed_2.fq.gz'
                    if "samtools" in tool:
                        samtools_str = f"|samtools view -b -@ {num_cpus} {args} - > {outdir_str}/{prefix}.bam"
                        dest.write(f"{bwa_str}{samtools_str}\n")
                    if "sort" in tool:
                        dest.write('echo "sorting the bam file"\n')
                        dest.write(
                            f"sambamba sort -t {num_cpus} {args} -o {outdir_str}/{prefix}_sorted.bam {outdir_str}/{prefix}.bam\n"
                        )
                    if "markdup" in tool:
                        dest.write('echo "mark and remove duplicate reads"\n')
                        dest.write(
                            f"sambamba markdup -t {num_cpus} {args} {outdir_str}/{prefix}_sorted.bam {outdir_str}/{prefix}_sorted_rmdup.bam\n"
                        )
                    if "fastqc" in tool:
                        dest.write('echo "running fastqc"\n')
                        dest.write(
                            f"fastqc {args} -o {outdir_str}/ {outdir_str}/{prefix}_trimmed*.fq.gz\n"
                        )
                    if "qualimap" in tool:
                        dest.write('echo "running qualimap"\n')
                        dest.write(
                            f"qualimap bamqc -nt {num_cpus} {args} -bam {outdir_str}/{prefix}_sorted_rmdup.bam -outdir {outdir_str}/{prefix}\n"
                        )
                        success = True
        if success:
            console.print("slurm script is successfully written, you may exit now")
            time.sleep(3)


class FqToBamCli:
    def __init__(self):
        self.u = util()
        self.d = dictionary()
        self.bool_var = []
        self.dict_list = [dict_i.copy() for dict_i in self.d.dict_list]

    def main_function(self):
        self.u.clear_screen()
        self.u.print_global_header()
        analyses = [
            "general input, output and other global parameters",
            "the parameter of the tools",
            "save",
            "exit",
        ]
        console.print("[yellow]Set or view:[/yellow]")
        analysis = select(analyses)
        while analysis != "exit":
            self.u.clear_screen()
            if analysis == analyses[0]:
                g = SetGeneralParameters(self.dict_list[0])
                self.dict_list[0] = g.main_function()
            if analysis == analyses[1]:
                t = SetToolParameters(self.dict_list[1])
                self.dict_list[1] = t.main_function()
            if analysis == analyses[2]:
                s = SaveSlurmScript(self.dict_list[0], self.dict_list[1])
                s.write_slurm_script()
            self.u.print_global_header()
            console.print("[yellow]Set or view:[/yellow]")
            analysis = select(analyses)
        self.u.clear_screen()


fqtobamcli = FqToBamCli()
fqtobamcli.main_function()
