import base64
import os
import subprocess
import re


class IpRun:
    r"""
    IpRun is a utility class for running commands within a network namespace using 'ip netns exec'.

    Args:
        supass (str): The superuser (sudo) password, which is needed for executing commands.
        cmd (str): The base 'ip netns exec' command with the network namespace placeholder.
        startnumber (int): The starting number to create unique network namespaces.
        r_new_networkinterface (str): The IP address range for creating unique network interfaces.

    Attributes:
        supass (str): The superuser (sudo) password.
        cmd (str): The base 'ip netns exec' command.
        startnumber (int): The current number for creating unique network namespaces.
        new_networkinterface (str): The name of the network namespace.

    Methods:
        __call__(self, command, wait_to_complete=True, **kwargs):
            Execute a command within the network namespace.

    Usage:
        Create an IpRun instance, and use it to run commands within network namespaces.
    """
    def __init__(self, supass, cmd, startnumber, r_new_networkinterface):
        r"""
        Initialize an IpRun instance with configuration settings.

        Args:
            supass (str): The superuser (sudo) password, required for executing commands.
            cmd (str): The base 'ip netns exec' command with a network namespace placeholder.
            startnumber (int): The starting number for creating unique network namespaces.
            r_new_networkinterface (str): The IP address range for creating unique network interfaces.

        Attributes:
            supass (str): The superuser (sudo) password.
            cmd (str): The base 'ip netns exec' command.
            startnumber (int): The current number for creating unique network namespaces.
            new_networkinterface (str): The name of the network namespace.

        Returns:
            IpRun: An IpRun instance with the specified configuration.

        Usage:
            Initialize an IpRun instance with the required settings.
        """
        self.cmd = cmd.rstrip()
        self.supass = supass
        self.startnumber = startnumber
        self.new_networkinterface = r_new_networkinterface

    def __str__(self):
        return self.new_networkinterface

    def __repr__(self):
        return self.__str__()

    def __call__(self, command, wait_to_complete=True, **kwargs):
        r"""
        Execute a command within the network namespace.

        Args:
            command (str or list): The command to execute within the network namespace.
            wait_to_complete (bool, optional): Whether to wait for the command to complete (default is True).
            **kwargs: Additional keyword arguments to pass to subprocess.Popen.

        Returns:
            subprocess.Popen: A Popen instance representing the executed subprocess.

        Usage:
            Execute a command within the network namespace associated with this IpRun instance.
        """
        if isinstance(command, list):
            command = ' '.join(command)
        complete_command = self.supass + '\n\n' + self.cmd + ' ' + command.lstrip()
        if 'stdin' in kwargs:
            del kwargs['stdin']
        p = subprocess.Popen('su', stdin=subprocess.PIPE, **kwargs)
        p.stdin.write(complete_command.encode('utf-8'))
        p.stdin.close()
        if wait_to_complete:
            p.wait()
        return p


def get_bound_subprocess_Popen(su_password:str,
                               networkip:str,

                               networkinterface:str='eth0',
                               nameserver:str='8.8.8.8',
                               new_ip_start:str='192.168.',
                               virtual_namespace_prefix:str=f'eth'):
    r"""
    Create a subprocess with a pre-configured network namespace and routing rules to bind an IP address to a process.

    Args:
        su_password (str): The superuser (sudo) password.
        networkip (str): The IP address to bind to the process.
        networkinterface (str, optional): The network interface to apply NAT rules to (default is 'eth0').
        nameserver (str, optional): The DNS nameserver IP address (default is '8.8.8.8').
        new_ip_start (str, optional): The starting IP address range for creating network interfaces (default is '192.168.').
        virtual_namespace_prefix (str, optional): The prefix for naming network namespaces (default is 'eth').

    Returns:
        IpRun: An IpRun instance with the specified configuration.

    Usage:
        # Create a bound subprocess that binds an IP address to a process using network namespaces.
         from pylinuxnetnamespace import get_bound_subprocess_Popen
        bindedsubproc = get_bound_subprocess_Popen(su_password='1',
                                       networkip='192.168.9.100',

                                       networkinterface='enx344b50000000',
                                       nameserver='8.8.8.8',
                                       new_ip_start='192.168.',
                                       virtual_namespace_prefix=f'eth')
        # bindedsubproc behaves like the subprocess.Popen class
        # you have to create it only once and can use it multiple times
        bindedsubproc('ping 1.1.1.1', shell=True)
        bindedsubproc('ping google.com', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    """
    ip_netns_stdout = subprocess.run('ip netns', shell=True, capture_output=True).stdout.decode('utf-8',
                                                                                                'backslashreplace')

    startnumber = 0
    new_networkinterface = f'{virtual_namespace_prefix}{startnumber}_ns'
    while new_networkinterface in ip_netns_stdout:
        startnumber += 1
        new_networkinterface = f'{virtual_namespace_prefix}{startnumber}_ns'

    ip_route_stdout = subprocess.run('ip route', shell=True, capture_output=True).stdout.decode('utf-8',
                                                                                                'backslashreplace')
    r_startnumber = 1
    r_new_networkinterface = f'{new_ip_start}{r_startnumber}'
    while r_new_networkinterface in ip_route_stdout:
        r_startnumber += 1
        r_new_networkinterface = f'{new_ip_start}{r_startnumber}'

    with open(r'/etc/sysctl.conf', mode='rb') as f:
        data = f.read()

    if re.findall(rb"net\.ipv4\.ip_forward\s*=\s*1", data):
        if re.findall(rb"#[^\n]*net\.ipv4\.ip_forward\s*=\s*1", data):
            addtocommand = '''\n\necho "net.ipv4.ip_forward = 1" | tee -a /etc/sysctl.conf\n\n'''
        else:
            addtocommand = ''
    else:
        addtocommand = '''\n\necho "net.ipv4.ip_forward = 1" | tee -a /etc/sysctl.conf\n\n'''

    postrouting = f'''sudo iptables -t nat -A POSTROUTING -s {r_new_networkinterface}.0/24 -o {networkinterface} -j SNAT --to-source {networkip}'''
    script_file_path = os.path.join(os.getcwd(), 'iptables_script.sh')
    with open(script_file_path, mode='w', encoding='utf-8') as f:
        f.write(
            f'''
#!/bin/bash
{postrouting}

    '''
        )

    execute_permission = 0o755
    os.chmod(script_file_path, execute_permission)
    iptables_command = (f'''
sudo ip netns add {new_networkinterface}
sudo ip link add v_{virtual_namespace_prefix}{startnumber}a type v{virtual_namespace_prefix} peer name v_{virtual_namespace_prefix}{startnumber}b
sudo ip link set v_{virtual_namespace_prefix}{startnumber}a netns {new_networkinterface}
sudo ip netns exec {new_networkinterface} ip addr add {r_new_networkinterface}.10/24 dev v_{virtual_namespace_prefix}{startnumber}a
sudo ip netns exec {new_networkinterface} ip link set dev v_{virtual_namespace_prefix}{startnumber}a up
sudo ip addr add {r_new_networkinterface}.20/24 dev v_{virtual_namespace_prefix}{startnumber}b
sudo ip link set dev v_{virtual_namespace_prefix}{startnumber}b up
sudo ip netns exec {new_networkinterface} ip route add default via {r_new_networkinterface}.20 dev v_{virtual_namespace_prefix}{startnumber}a
{addtocommand}
sudo sysctl -p
sudo -S {script_file_path}
sudo ip netns exec {new_networkinterface} bash -c 'echo "nameserver {nameserver}" > /etc/resolv.conf'
sudo ip netns exec {virtual_namespace_prefix}{startnumber}_ns systemctl status systemd-resolved
sudo ip netns exec {virtual_namespace_prefix}{startnumber}_ns systemctl restart systemd-resolved
    '''.strip() + '\n\n').encode('utf-8')
    base64_encoded_command = base64.b64encode(iptables_command).decode()

    executecommand = f'''{su_password}\n\necho {base64_encoded_command} | base64 -d | bash'''.encode()

    p = subprocess.Popen(
        "su",
        stdin=subprocess.PIPE, shell=True, start_new_session=True)
    p.stdin.write(executecommand)
    p.stdin.close()
    p.wait()
    pi = IpRun(su_password, f'ip netns exec {new_networkinterface}', startnumber, r_new_networkinterface)
    try:
        os.remove(script_file_path)
    except Exception:
        pass
    return pi

