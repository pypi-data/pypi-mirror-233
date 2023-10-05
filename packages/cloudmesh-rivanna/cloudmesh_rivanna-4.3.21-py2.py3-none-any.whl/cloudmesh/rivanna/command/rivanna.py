import shutil

import yaml

from cloudmesh.shell.command import command
from cloudmesh.shell.command import PluginCommand
from cloudmesh.rivanna.rivanna import Rivanna
from cloudmesh.common.console import Console
from cloudmesh.common.util import path_expand
from pprint import pprint
from cloudmesh.common.debug import VERBOSE
from cloudmesh.shell.command import map_parameters
from cloudmesh.common.parameter import Parameter
from cloudmesh.common.variables import Variables
from cloudmesh.common.util import banner
from cloudmesh.common.Shell import Shell

class RivannaCommand(PluginCommand):

    # noinspection PyUnusedLocal
    @command
    def do_rivanna(self, args, arguments):
        """
        ::

          Usage:
                rivanna storage info DIRECTORY [--info]
                rivanna login [--sbatch=SBATCH] [--host=HOST] [KEY] [--debug]
                rivanna slurm info
                rivanna slurm [--sbatch=SBATCH] [--host=HOST] [KEY] [--debug]
                rivanna tutorial [KEYWORD]
                rivanna vpn on
                rivanna vpn off
                rivanna vpn info
                rivanna vpn status
                rivanna ticket
                rivanna singularity build DEFFILE
                rivanna jupyter --port=PORT

          This command simplifys access to rivanna.

          Arguments:
              DIRECTORY  a location of a directory on rivanna

          Options:
              -f      specify the file

          Description:

            rivanna storage info DIRECTORY [--info]
                A command that can be executed remotely and obtains information about the storage associated
                with a directory on rivanna

            rivanna login [--allocation=ALLOCATION] [--gres=GRES] [--cores=CORES] [--host=HOST] [--constraint=CONSTRAINT] [--reservation=RESERVATION] [--time=TIME]
                A command that logs into from your current computer into an interactive node on rivanna
                with a given GPU. Values for GPU are

                a100 or a100-80 -- uses a A100 with 80GB
                a100-40 -- uses a A100 with 40GB
                a100-localscratch  -- uses a A100 with 80GB and access to localscratch

                others to be added from rivannas hardware description

            rivanna tutorial singularity
                shows the rivanna singularity information on infomall.org

            rivanna tutorial hpc
                shows the general rivanna hpc information on infomall.org

            rivanna tutorial pod
                shows the general rivanna pod information on infomall.org

            rivanna tutorial globue
                shows the general rivanna globus information on infomall.org

            rivanna tutorial rclone
                shows the general rivanna rclone information on infomall.org

            rivanna vpn on
                switches the vpn on

            rivanna vpn off
                switches the vpn off

            rivanna vpn info
                prints the information about the current connection to the
                internet. INformation includes

                  "ip": "128.143.1.11",
                  "hostname": "vpn-user-1-11.itc.virginia.edu",
                  "city": "Charlottesville",
                  "region": "Virginia",
                  "country": "US",
                  "loc": "38.0293,-78.4767",
                  "org": "AS225 University of Virginia",
                  "postal": "22902",
                  "timezone": "America/New_York",
                  "readme": "https://ipinfo.io/missingauth"

            rivanna vpn status
                prints True if vpn is enabled, False if not


          Installation:

            pip install cloudmesh-rivana
            cms help

        """


        # arguments.FILE = arguments['--file'] or None

        # switch debug on

        variables = Variables()
        variables["debug"] = True

        map_parameters(arguments,
                       "port",
                       "host",
                       "sbatch",
                       "debug")

        host = arguments.host = arguments.host or "rivanna"

        # VERBOSE(arguments)

        key = arguments.KEY
        # VERBOSE(arguments)


        rivanna = Rivanna()
        rivanna.debub = arguments.debug

        def VPN():
            from cloudmesh.vpn.vpn import Vpn
            vpn = Vpn(None,
                      timeout=30)
            return vpn

        if arguments.jupyter:

            port = arguments.port or 8000
            rivanna.jupyter(port=port)

        elif arguments.storage:

            Console.error("not implemented")

        elif arguments.singularity and arguments.build:

            buidlfile = arguments.DEFFILE

            rivanna.create_singularity_image(buidlfile)

        elif arguments.login:

            key = arguments.KEY

            rivanna.directive[host][key].update({"time": "30:00"})

            if arguments.sbatch:

                data = rivanna.parse_sbatch_parameter(arguments.sbatch)
                rivanna.directive[host][key].update(data)

            d = rivanna.directive[host][key]

            time = arguments.time or "30:00"

            rivanna.login(host, key)

        elif arguments.slurm and arguments.info:

           print(yaml.dump(rivanna.directive))

        elif arguments.slurm and arguments.KEY and not arguments.login:

            key = arguments.KEY

            if arguments.sbatch:
                data = rivanna.parse_sbatch_parameter(arguments.sbatch)
                rivanna.directive[host][key].update(data)


            d = rivanna.directive[host][key]
            slurm_directive = rivanna.create_slurm_directives(host=host, key=key)

            print(slurm_directive)


        elif arguments.vpn and arguments.on:

            vpn = VPN()

            Console.ok("Connecting ... ")
            vpn.connect()
            if vpn.enabled():
                Console.ok("ok")
            else:
                Console.error("failed")

        elif arguments.vpn and arguments.off:

            vpn = VPN()

            Console.ok("Disconnecting ... ")
            vpn.disconnect()
            if not vpn.enabled():
                Console.ok("ok")
            else:
                Console.error("failed")

        elif arguments.vpn and arguments.status:

            vpn = VPN()

            print(vpn.enabled())

        elif arguments.vpn and arguments.info:

            vpn = VPN()

            print(vpn.info())

        elif arguments.tutorial:

            keyword = arguments.KEYWORD

            if keyword in ["pod"]:
                rivanna.browser("https://infomall.org/uva/docs/tutorial/rivanna-superpod/")

            elif keyword in ["rclone"]:
                rivanna.browser("https://infomall.org/uva/docs/tutorial/rclone/")

            elif keyword in ["globus"]:
                rivanna.browser("https://infomall.org/uva/docs/tutorial/globus/")

            elif keyword in ["singularity"]:
                rivanna.browser("https://infomall.org/uva/docs/tutorial/singularity/")

            elif keyword in ["training"]:
                rivanna.browser("https://infomall.org/uva/docs/tutorial/cybertraining/")

            elif keyword in ["hpc", "system"]:
                rivanna.browser("https://infomall.org/uva/docs/tutorial/rivanna/")



            else:
                rivanna.browser("https://infomall.org/uva/docs/tutorial/")

        elif arguments.ticket:

            rivanna.browser("https://www.rc.virginia.edu/form/support-request/")

        return ""
