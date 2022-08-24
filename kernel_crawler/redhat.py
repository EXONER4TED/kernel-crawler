from . import repo
from .container import Container
import re
import subprocess
from subprocess import PIPE

class RedhatContainer(repo.ContainerDistro):
    def __init__(self, image):
        super(RedhatContainer, self).__init__(image)

    def get_kernel_versions(self):
        kernels = {}
        # c = Container(self.image)
        # cmd_out = c.run_cmd("repoquery --show-duplicates kernel-devel")

        cmd = ['repoquery', '--show-duplicates', 'kernel-devel']
        process = subprocess.run(
            cmd,
            capture_output=True,
            check=False
        )

        cmd_out = process.stdout.decode('utf-8')
        print(cmd_out, flush=True)

        for log_line in cmd_out:
            m = re.search("(?<=kernel-devel-0:).*", log_line)
            if m:
                kernels[m.group(0)] = []
        return kernels

    def to_driverkit_config(self, release, deps):
        return repo.DriverKitConfig(release, "redhat", list(deps))
