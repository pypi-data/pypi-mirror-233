import os
import sys
import click
import paramiko
import scp
from .custom_types import NETADDR, NETADDRLIST, OptionalPassword

class CyPerfAgentManager (object):
    AGENT_IPS_HELP_TEXT = 'One or more agent names (IP addresses or hostnames).'      \
                          ' Use quotation marks (`\'` or `"`) for whitespace (` `)'   \
                          ' separated values. Other valid separators are `,`, `;` and `:`.'
    DEFAULT_USER_NAME   = 'cyperf'
    DEFAULT_PASSWORD    = 'cyperf'

    def __init__ (self,
                  agentIPs = [],
                  userName = DEFAULT_USER_NAME,
                  password = DEFAULT_PASSWORD):
        self.userName = userName
        self.password = password
        self.agentIPs = agentIPs
        self.client   = paramiko.client.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def __exec__(self, cmd, sudo=False):
        if sudo:
            cmd = f'sudo -S -p \'\' {cmd}' 
        for agent in self.agentIPs:
            try:
                click.echo (f'>> Connectiong to agent {agent}')
                self.client.connect(agent, username=self.userName, password=self.password)
                channel = self.client.get_transport().open_session()
                channel.set_combine_stderr(1)
                try:
                    click.echo (f'>> Executing command {cmd}')
                    _stdin, _stdout, _stderr = self.client.exec_command (cmd)
                    if sudo:
                        _stdin.write(self.password + "\n")
                        _stdin.flush()
                    click.echo(_stdout.read().decode())
                except paramiko.ssh_exception.SSHException:
                    click.echo (f'Failed to execute command {cmd}')
                self.client.close()
            except paramiko.ssh_exception.NoValidConnectionsError:
                click.echo (f'Connection is refused by the server')
            except paramiko.ssh_exception.AuthenticationException:
                click.echo (f'Login failed because of invalid credentials')
            except TimeoutError:
                click.echo (f'Connection timed out')

    def __copy__(self, localPath, remotePath):
        for agent in self.agentIPs:
            try:
                click.echo (f'>> Connectiong to agent {agent}')
                self.client.connect(agent, username=self.userName, password=self.password)
                try:
                    click.echo (f'>> Tranferring file {localPath} to {remotePath}')
                    with scp.SCPClient(self.client.get_transport()) as _scp:
                        _scp.put(localPath, remotePath)
                except scp.SCPException:
                    click.echo (f'Failed to transfer file {localPath} to {remotePath}')
                self.client.close()
            except paramiko.ssh_exception.NoValidConnectionsError:
                click.echo (f'Connection is refused by the server')
            except paramiko.ssh_exception.AuthenticationException:
                click.echo (f'Login failed because of invalid credentials')
            except TimeoutError:
                click.echo (f'Connection timed out')

    def ControllerSet (self, controllerIP):
        cmd = f'cyperfagent controller set {controllerIP}'
        self.__exec__(cmd)

    def Reload (self):
        cmd = f'cyperfagent configuration reload'
        self.__exec__(cmd)

    def SetTestInterface (self, iface):
        cmd = f'cyperfagent interface test set {iface}'
        self.__exec__(cmd)

    def InstallBuild (self, debFile):
        remotePath = f'~/{os.path.basename(debFile)}'
        cmd        = f'apt install -y {remotePath}'
        self.__copy__ (debFile, remotePath)
        self.__exec__ (cmd, sudo=True)

pass_agent_manager = click.make_pass_decorator(CyPerfAgentManager)

def agent_ips_option(f):
    def callback(ctx, param, value):
        agentMgr = ctx.ensure_object(CyPerfAgentManager)
        agentMgr.agentIPs = value
        return value
    return click.option('--agent-ips',
                        required = True,
                        type = NETADDRLIST,
                        expose_value = False,
                        help = CyPerfAgentManager.AGENT_IPS_HELP_TEXT,
                        callback = callback)(f)

def user_name_option(f):
    def callback(ctx, param, value):
        agentMgr = ctx.ensure_object(CyPerfAgentManager)
        agentMgr.userName = value
        return value
    return click.option('--username',
                        required = False,
                        type = str,
                        default = CyPerfAgentManager.DEFAULT_USER_NAME,
                        show_default = True,
                        expose_value = False,
                        help = 'A common username for all the agents.',
                        callback = callback)(f)

def password_option(f):
    def callback(ctx, param, value):
        agentMgr = ctx.ensure_object(CyPerfAgentManager)
        agentMgr.password = value
        return value
    return click.password_option(default = CyPerfAgentManager.DEFAULT_PASSWORD,
                                 expose_value = False,
                                 help = 'A common password for all the agents.',
                                 cls = OptionalPassword,
                                 callback = callback)(f)

def common_options(f):
    f = password_option (f)
    f = click.option('--override-password',
                     default = False,
                     required = False,
                     is_flag = True,
                     expose_value = False,
                     help = 'This along with --password option should be used for non default password.')(f)
    f = user_name_option (f)
    f = agent_ips_option (f)
    return f

@click.group()
def agent_manager():
    pass

@agent_manager.command()
@common_options
@pass_agent_manager
@click.option('--controller-ip',
              required = True,
              help     = 'The IP/Hostname of the CyPerf controller.',
              type     = NETADDR,
              prompt   = True)
def set_controller(agentManager, controller_ip):
    agentManager.ControllerSet (controller_ip)

@agent_manager.command()
@common_options
@pass_agent_manager
def reload(agentManager):
    agentManager.Reload ()

@agent_manager.command()
@common_options
@pass_agent_manager
@click.option('--test-interface',
              required = True,
              help     = 'The name of the interface on the agents which will be used for test traffic.',
              type     = str,
              prompt   = True)
def set_test_interface(agentManager, test_interface):
    agentManager.SetTestInterface (test_interface)

@agent_manager.command()
@common_options
@pass_agent_manager
@click.option('--debian-file-path',
              required = True,
              help     = 'Path to the .deb file to be installed.',
              type     = click.Path(exists=True, file_okay=True, dir_okay=False, readable=True),
              prompt   = True)
def install_build(agentManager, debian_file_path):
    agentManager.InstallBuild (debian_file_path)

def main():
    agent_manager()
