from cloudmesh.common.Shell import Shell
from cloudmesh.common.console import Console
import os
from cloudmesh.common.FlatDict import FlatDict
from textwrap import dedent
import yaml
from cloudmesh.common.util import banner
from cloudmesh.common.StopWatch import StopWatch
import socket

class Rivanna:

    def jupyter(self, port=8000):
        self.port = port

        # test if vpn is on

        # start login on machine and start jupyter
        "jupyter notebook --no-browser --port=<PORT>"
        # open tunnel
        "ssh -L 8080:localhost:<PORT> <REMOTE_USER>@<REMOTE_HOST>"
        # access to notebook on localhost

    def __init__(self, host="rivanna", debug=False):
        self.debug = debug
        self.data = dedent(
          """
          rivanna:
            parallel:
              partition: "parallel"
              account: "bii_dsc_community"
              nodes: 2
              ntask-per-node: 4
            v100:
              gres: "gpu:v100:1"
              partition: "bii-gpu"
              account: "bii_dsc_community"
            a100:
              gres: "gpu:a100:1"
              partition: "gpu"
              account: "bii_dsc_community"
            a100-dgx:
              gres: "gpu:a100:1"
              reservation: "bi_fox_dgx"
              partition: "bii-gpu"
              account: "bii_dsc_community"
            k80:
              gres: "gpu:k80:1"
              partition: "gpu"
              account: "bii_dsc_community"
            p100:
              gres: "gpu:p100:1"
              partition: "gpu"
              account: "bii_dsc_community"
            a100-pod:
              gres: "gpu:a100:1"
              account: "bii_dsc_community"
              constraint: "gpupod"
              partition: gpu
            rtx2080:
              gres: "gpu:rtx2080:1"
              partition: "gpu"
              account: "bii_dsc_community"
            rtx3090:
              gres: "gpu:rtx3090:1"
              partition: "gpu"
              account: "bii_dsc_community"          
          greene:
            v100:
              gres: "gpu:v100:1"
            a100:
              gres: "gpu:a100:1"
        """
        )
        self.directive = yaml.safe_load(self.data)

    def parse_sbatch_parameter(self, parameters):
        result = {}
        data = parameters.split(",")
        for line in data:
            key, value = line.split(":",1)
            result[key] = value
        return result

    def directive_from_key(self, key):
        return self.directive[key]

    def create_slurm_directives(self, host=None, key=None):
        directives = self.directive[host][key]
        block = ""

        def create_direcitve(name):
            return f"#SBATCH --{name}={directives[name]}\n"

        for key in directives:
            block = block + create_direcitve(key)

        return block


    def login(self, host, key):
        """
        ssh on rivanna by executing an interactive job command

        :param gpu:
        :type gpu:
        :param memory:
        :type memory:
        :return:
        :rtype:
        """

        def create_parameters(host, key):

            directives = self.directive[host][key]
            block = ""

            def create_direcitve(name):
                return f" --{name}={directives[name]}"

            for key in directives:
                block = block + create_direcitve(key)

            return block


        parameters = create_parameters(host, key)
        command = f'ssh -tt {host} "/opt/rci/bin/ijob{parameters}"'

        Console.msg(command)
        if not self.debug:
             os.system(command)
        return ""


    def cancel(self, job_id):
        """
        cancels the job with the given id

        :param job_id:
        :type job_id:
        :return:
        :rtype:
        """
        raise NotImplementedError

    def storage(self, directory=None):
        """
        get info about the directory

        :param directory:
        :type directory:
        :return:
        :rtype:
        """
        raise NotImplementedError

    def edit(self, filename=None, editor="emacs"):
        """
        start the commandline editor of choice on the file on rivanna in the current terminal

        :param filename:
        :type filename:
        :return:
        :rtype:
        """

    def browser(self, url):
        Shell.browser(filename=url)

    def create_singularity_image(self, name):
        """
        :param name:
        :type name:
        :return:
        :rtype:


        export SINGULARITY_CACHEDIR=/scratch/$USER/.singularity/
        export SINGULARITY_CACHEDIR=/$HOME/.singularity/


        """

        try:
            cache = os.environ["SINGULARITY_CACHEDIR"]
            banner("Cloudmesh Rivanna Singularity Build")

            image = os.path.basename(name.replace(".def", ".sif"))
        

            print("Image name       :", image)
            print("Singularity cache:", cache)
            print("Definition       :", name)
            print()
            StopWatch.start("build image")
            Shell.rm ("output_image.sif")
            Shell.mkdir(cache) # just in case
            Shell.copy(name,  "build.def")
            hostname = socket.gethostname()
            if hostname in ["udc-aj34-33", "udc-aj34-33"]:
                os.system("sudo /opt/singularity/3.7.1/bin/singularity build output_image.sif build.def")
            else:
                os.system("sudo singularity build output_image.sif build.def")
            Shell.copy("output_image.sif",  image)
            Shell.rm ("output_image.sif")
            Shell.rm ("build.def")
            StopWatch.stop("build image")
            size = Shell.run(f"du -sh {image}").split()[0]

            timer = StopWatch.get("build image")
            print()
            print(f"Time to build {image}s ({size}) {timer}s")
            print()


        except Exception as e:
            Console.error(e, traceflag=True)
            

