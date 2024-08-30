#!/usr/bin/python

"""Script to gather various profile information from a Solaris 10 system.

Example Usage:
    python generate_server_info.py
"""

import os
import subprocess
import socket
import sys
import re
import math
import datetime
import optparse
import traceback
import platform
import tempfile


def convert_size(size_bytes):
    """Convert the given size in bytes to an appropriate human-readable value.
    Args:
      size_bytes: An integer representing the size in bytes
    Returns:
      A string describing the units.
    """
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "K", "M", "G")
    size_index = min(int(math.floor(math.log(size_bytes, 1024))), len(size_name) - 1)
    factor = math.pow(1024, size_index)
    size_units = round(size_bytes / factor, 2)
    return "{0}{1}".format(size_units, size_name[size_index])


class ServerInfo(object):
    """Base class describing an operation to retrieve server information."""

    def __init__(self, description, results_file):
        """Create a server info with a description and logs to the given file.
        Args:
            description: The description of this server info.
            results_file: Write to this open file object
        """
        self.description = description
        self.results_file = results_file

    def log(self, message):
        """Log a message to the file, with a newline appended.
        Args:
            message: The message to log.
        """
        self.results_file.write(message + "\n")

    def log_file(self, file_path):
        """Write the file contents to the log.
        Args:
            file_path: The path of the file to log.
        """
        try:
            file = open(file_path)
            self.log("The contents of {0} are:\n{1}".format(file_path, file.read()))
        except:
            self.log("Unable to open {0}".format(file_path))

    def run_process_and_log_output(self, process_args):
        """Logs the output from a command line process after issuing the communicate
        command to it.
        Args:
            process: The process which needs it's output logged.
        """
        command_line = process_args if isinstance(process_args, basestring) else " ".join(process_args)
        self.log("Executing command: {0}".format(command_line))
        process = subprocess.Popen(process_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        if process.returncode != 0:
            self.log("Command failed with return code: {0}".format(process.returncode))

        if stdout:
            self.log("stdout:\n{0}".format(stdout))
        if stderr:
            self.log("stderr:\n{0}".format(stderr))

    def check_service(self, service):
        """Get the status of the given service.
        Args:
            service: The name of the service to check.
        Returns:
          The state of the service as described by svcs, or None if the service could not be found
        """
        stdout, stderr = subprocess.Popen(['svcs', service], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

        try:
            if stderr:
                # Couldn't find the service
                self.log("Uknown service {0}:\n{1}".format(service, stderr))
                return None
            lines = stdout.split('\n')
            return (lines[1].split())[0]
        except:
            self.log("Error checking service {0}:\n{1}".format(service, stderr))
            return None

    def set_service(self, service, enabled):
        """Set the given service to enabled or disabled.
        Args:
          service: The name of the service to set.
          enabled: Whether to enable or disable.
        """
        action = 'enable' if enabled else 'disable'
        subprocess.Popen(['svcadm', action, service]).communicate()


class DeviceInfo(ServerInfo):
    """Get information about hardware devices like RAM and processors."""

    def __init__(self, results_file):
        super(DeviceInfo, self).__init__('Checking RAM and CPU', results_file)

    def generate(self):
        """Run commands to get RAM and CPU info."""
        process = subprocess.Popen('prtconf', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        memory_re = re.compile("Memory size: (.*)")

        self.log("Determining RAM")
        found_ram = False

        for line in stdout.split('\n'):
            memory_match = memory_re.match(line)
            if memory_match:
                self.log(line)
                found_ram = True

        if not found_ram:
            self.log("Unable to determine installed RAM. Full prtconf output is:\n{0}".format(stdout))

        self.log("Looking for CPU(s)")
        process = subprocess.Popen(["psrinfo", "-p"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        self.log("Found {0} CPU(s)".format(stdout))
        self.run_process_and_log_output(["psrinfo", "-pv"])


class DiskInfo(ServerInfo):
    """Gather information on the storage devices attached to the system."""

    def __init__(self, results_file):
        super(DiskInfo, self).__init__('Checking disk layout', results_file)

    def generate(self):
        """Get information using df and format, toggle autofs and volfs since they can cause disk commands to hang if a CodeMeter stick
        is attached."""
        services = {'autofs': False, 'volfs': False}
        autofs_enabled = False

        code_meter_exec = "/opt/CodeMeter/Tools/cmu"

        if os.path.exists(code_meter_exec):
            self.run_process_and_log_output([code_meter_exec, "-l"])
        else:
            self.log("CodeMeter does not appear to be installed.")

        for service in services.keys():
            if self.check_service(service) == 'online':
                services[service] = True
                sys.stdout.write(' {0} is enabled, disabling for disk checks... '.format(service))
                sys.stdout.flush()
                self.log("Disabling {0} for disk checks".format(service))
                self.set_service(service, False)

        try:
            self.run_process_and_log_output(["df", "-h"])
            self.retrieve_disk_layouts()
        except:
            raise
        finally:
            # If a check fails we still want to raise an error, but we need to ensure we re-enable any services we turned off.
            for service in services.keys():
                if services[service]:
                    sys.stdout.write(' re-enabling {0}... '.format(service))
                    sys.stdout.flush()
                    self.log("Re-enabling {0}".format(service))
                    self.set_service(service, True)

    def retrieve_disk_layouts(self):
        """Get the disk layouts using the format command. NOTE: in the case of a bad drive this can take a REALLY long time."""

        self.log("Searching for disks with format")
        format_process = subprocess.Popen("format", stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, _ = format_process.communicate("\n")

        disk_selection_re = re.compile("\W*(\d+)\. (\w+) (.*)")

        disks = []
        for line in stdout.split('\n'):
            disk_selection_match = disk_selection_re.match(line)
            if disk_selection_match:
                disk = (disk_selection_match.group(1), disk_selection_match.group(2), disk_selection_match.group(3))
                self.log("Found disk {0} {1} {2}".format(disk[0], disk[1], disk[2]))
                disks.append(disk)

        self.log("\n")
        for disk in disks:
            self.log("\nCHECKING DISK {0}:{1}".format(disk[0], disk[1]))
            format_process = subprocess.Popen("format", stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, _ = format_process.communicate("{0}\npartition\nprint\n".format(disk[0]))
            self.log(stdout)

                
class HomeInfo(ServerInfo):
    """Look at how /home and /home/wsi are set up."""

    def __init__(self, results_file):
        super(HomeInfo, self).__init__('Checking how /home and /home/wsi are linked', results_file)

    def generate(self):
        """Check /home and /home/wsi for existance and link status."""
        for file_path in ('/home', '/home/wsi'):
            if not os.path.isdir(file_path):
                self.log("{0} does not exist!!!\n".format(file_path))
                continue
            if os.path.islink(file_path):
                self.log("{0} is a symlink to {1}".format(file_path, os.readlink(file_path)))
            elif os.path.isdir(file_path):
                self.log("{0} is a directory".format(file_path))
            else:
                self.log("{0} is a neither a symlink nor a directory".format(file_path))


class ListFileInfo(ServerInfo):
    """Look through SCADACOM files, particularly data and corefiles."""

    def __init__(self, results_file):
        super(ListFileInfo, self).__init__('Listing all the files in $SUH/data', results_file)
        self.corefiles = []
        self.core_re = re.compile('^core.*$')

    def generate(self):
        """List files in $SUH/data and look for corefiles."""
        self.log("Traversing /home/wsi/data/")
        self.print_tree('/home/wsi/data/')
        self.log("Looking for corefiles in /home/wsi/")
        self.find_corefiles('/home/wsi/')
        self.print_corefiles()

    def find_corefiles(self, directory):
        """Locate anything that looks like a corefile in the directory (or a subdirectory) and add it to the corefile list.
        Args:
            directory: The directory to search through.
        """
        for root, dirs, files in os.walk(directory):
            for file_name in files:
                if 'core' in file_name and self.core_re.match(file_name):
                    self.corefiles.append(os.path.join(root, file_name))

    def print_corefiles(self):
        """Date/size/name of all the corefiles.
        """
        self.log('Found {0} corefiles.'.format(len(self.corefiles)))
        for corefile in sorted(self.corefiles):
            statinfo = os.stat(corefile)
            self.log("{0} {1} {2}".format(datetime.datetime.fromtimestamp(statinfo.st_ctime).strftime('%Y-%m-%d %H:%M:%S'),
                                          convert_size(statinfo.st_size), corefile))

    def print_tree(self, directory):
        """Descend into the given directory (and its subdirectories), printing every file/directory along the way.
        Args:
            directory: The directory to print the structure for.
        """
        for root, dirs, files in os.walk(directory):
            level = root.replace(directory, '').count(os.sep)
            indent = ' ' * 4 * (level)
            self.log('{0}{1}/'.format(indent, os.path.basename(root)))
            subindent = ' ' * 4 * (level + 1)
            for file_name in files:
                self.log('{0}{1}'.format(subindent, file_name))


class NetworkInfo(ServerInfo):
    """Retrieve Networking information."""

    def __init__(self, results_file):
        super(NetworkInfo, self).__init__('Determining Network Configuration', results_file)

    def generate(self):
        """Log network commands and the hosts file."""
        self.run_process_and_log_output(['ifconfig', '-a'])

        # Check if we can reach outside the network to DNS servers.
        nslookup_process = subprocess.Popen(["nslookup", "google.com"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = nslookup_process.communicate()

        if nslookup_process.returncode == 0:
            # We can, so check the network path outside.
            self.log("nslookup of google.com succeeded with stdout:\n{0}\nstderr:\n{1}".format(stdout, stderr))
            self.run_process_and_log_output(['traceroute', '216.58.216.174'])  # google.com

        self.log_file("/etc/hosts")


class SoftwareVersionInfo(ServerInfo):
    """Determine the versions of different pieces of software installed on the system."""
    version_re = re.compile("VERSION='(.*)'")

    def __init__(self, results_file):
        super(SoftwareVersionInfo, self).__init__('Checking software versions', results_file)

    def generate(self):
        """Get versions of all the relevant packages, both packages installed with pkg but also manually installed software."""
        process = subprocess.Popen(['uname', '-a'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        self.log("Solaris version:\n{0}".format(stdout))
        self.log_file('/etc/release')

        process = subprocess.Popen('pkginfo', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        scadacom_packages = []
        solaris_studio_packages = []
        mysql_packages = []
        sybase_packages = []
        clamav_packages = []
        codemeter_packages = []

        self.log("Listing system installed packages:")
        for package_line in stdout.split('\n'):
            try:
                package = (package_line.split())[1]

                for match_string, packages in (('SPRO', solaris_studio_packages), ('scadacom', scadacom_packages),
                                               ('clamav', clamav_packages), ('mysql', mysql_packages), ('WIBU', codemeter_packages)):
                    if match_string in package:
                        packages.append(package)
            except:
                pass  # just an empty line

        for set_name, packages in (("Scadacom", scadacom_packages), ("Solaris Studio", solaris_studio_packages),
                                   ("ClamAV", clamav_packages), ("MySQL", mysql_packages), ("CodeMeter", codemeter_packages)):
            self.log("\n{0}:".format(set_name))
            for package in packages:
                self.log("{0}:\t{1}".format(package, self.get_package_version(package)))

        self.log("\nListing manually installed packages:")

        self.log("\nSybase Version:\n{0}".format(self.get_sybase_version()))
        self.log("\nCrowd Version:\n{0}".format(self.get_crowd_version()))
        self.log("\nPython Version:\n{0}".format(platform.python_version()))

    def get_crowd_version(self):
        """Get the version of crowd by looking in /opt/crowd.
        Returns:
            Version of the installed crowd or UNKNOWN.
        """
        crowd_dir_re = re.compile('atlassian-crowd-([\d\.]+)')
        crowd_versions = []
        for dir in os.listdir('/opt/crowd'):
            crowd_dir_match = crowd_dir_re.match(dir)
            if crowd_dir_match:
                crowd_versions.append(crowd_dir_match.group(1))

        if not crowd_versions:
            return 'UNKNOWN'
        elif len(crowd_versions) == 1:
            return crowd_versions[0]

        self.log("Found multiple crowd versions in /opt/crowd! Contents of /opt/crowd are...")
        for directory in os.listdir('/opt/crowd'):
            self.log("\t{0}".format(directory))

        try:
            current_link = os.readlink('/opt/crowd/current')
            self.log("Current is linked to {0}".format(current_link))
        except:
            self.log("Unable to read link for /opt/crowd/current")

        return 'UNKNOWN'
    
    def get_package_version(self, package_name):
        """Get the version of a package install via Solaris's pkg system.
        Args:
            package_name: The name of the package according to pkginfo.
        Returns:
            Version of the installed package or UNKNOWN if the command failed.
        """
        process = subprocess.Popen(['pkgparam', '-v', package_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        for line in stdout.split('\n'):
            version_match = SoftwareVersionInfo.version_re.match(line)
            if version_match:
                return version_match.group(1)

        self.log("Couldn't find the version for installed package {0}".format(package_name))
        return "UNKNOWN"

    def get_sybase_version(self):
        """Run sybase command to get the version.
        Returns:
            The version according to the command.
        """
        process = subprocess.Popen(['su', '-', 'sybase', '-c', 'dataserver -v'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        return stdout.split('\n')[0]


class SybaseInfo(ServerInfo):
    """Retrieve Sybase configuration."""

    def __init__(self, results_file):
        super(SybaseInfo, self).__init__('Examining Sybase', results_file)

    def generate(self):
        """Run sybase commands to get the information."""
        sybase_statements = ("sp_helpdevice", "go", "sp_helpdb", "go", "exit")
        sybase_input = ""
        for statement in sybase_statements:
            sybase_input += "{0}\n".format(statement)

        # I'd rather do this with an input file but subprocess can't seem to find stdout when I do
        sybase_info_process = subprocess.Popen(['su', '-', 'sybase', '-c', 'isql -Usa -Pscadacom'], stdin=subprocess.PIPE,
                                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = sybase_info_process.communicate(sybase_input)
        self.log(stdout)


if __name__ == "__main__":

    if os.getuid() != 0:
        print("ERROR: Script must be run as root.")
        exit(1)

    hostname = socket.gethostname()
    results_file_path = '/tmp/scadacom_server_info_' + hostname
    results_file = open(results_file_path, 'w')

    parser = optparse.OptionParser("usage: %prog [options] arg")
    parser.add_option("-d", "--debug", action="store_true", help="Print the stack trace when a checker hits an exception.")

    options, args = parser.parse_args()
    
    print("Generating server info for {0}, report will be saved in {1}".format(hostname, results_file_path))

    info_generators = (DiskInfo, HomeInfo, ListFileInfo, NetworkInfo, SoftwareVersionInfo, DeviceInfo, SybaseInfo)

    errors = 0
    for step, info_generator_class in enumerate(info_generators):
        info_generator = info_generator_class(results_file)
        sys.stdout.write("{0}. {1}...".format(step, info_generator.description))
        sys.stdout.flush()
        results_file.write("{0}. {1}\n\n".format(step, info_generator.description.upper()))

        try:
            info_generator.generate()
            print(' success')
        except Exception as exception:
            print(' ERROR')
            if options.debug:
                traceback.print_exc()
        results_file.write("\n")
        results_file.flush()

    print('Generation of server info is complete.')
    if not errors:
        print('All checks succeeded.')
        exit(0)
    else:
        print('{0} check(s) succeeded but {1} check(s) failed.'.format(len(info_generators) - errors, errors))
        exit(1)

    close(results_file_path)
