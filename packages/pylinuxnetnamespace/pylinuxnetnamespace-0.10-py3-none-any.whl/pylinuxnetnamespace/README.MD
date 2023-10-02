# Binds an IP-address to a subprocess through network namespaces - Linux only 

## Tested against Ubuntu / Python 3.11 + 3.10 / Anaconda

## pip install pylinuxnetnamespace

### Simplifies Network Namespace Management: 

This library streamlines the 
process of creating and managing network namespaces and routing rules, 
reducing complexity and manual configuration efforts.

### Effortless Command Execution: 

With this library, executing commands 
within network namespaces becomes straightforward, allowing users to 
interact with isolated environments effortlessly.

### Automation for Isolated Environments: 

It provides a convenient way to 
automate the setup of isolated network environments, making it
ideal for automating testing or development environments.

### Streamlined Source NAT Configuration: 

The library simplifies the 
configuration of Source NAT (SNAT) rules, a common requirement for network management.



```python

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

```