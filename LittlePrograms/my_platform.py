import platform

def get_os_version():
    os = platform.system()
    version = platform.version()

    if os == 'Windows':
        return f'Windows {platform.win32_ver()[0]}'
    elif os == 'Darwin':  # Darwin is the base OS for macOS
        return f'macOS {platform.mac_ver()[0]}'
    elif os == 'Linux':
        # Try to get the distribution name and version
        try:
            with open('/etc/os-release', 'r') as f:
                lines = f.readlines()
                distro_info = {}
                for line in lines:
                    line = line.strip()
                    if line.startswith('NAME='):
                        distro_info['name'] = line.split('=')[1].strip('"')
                    elif line.startswith('VERSION='):
                        distro_info['version'] = line.split('=')[1].strip('"')
                if 'name' in distro_info and 'version' in distro_info:
                    return f"{distro_info['name']} {distro_info['version']}"
        except FileNotFoundError:
            pass
        # If /etc/os-release is not available, fall back to uname
        uname_info = platform.uname()
        return f'{uname_info.system} {uname_info.release}'
    else:
        return f'{os} {version}'

print(get_os_version())
