##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##

import os
import tempfile
import requests
import paramiko
import subprocess

from typing import List
from pydantic import ValidationError
from unskript.legos.utils import UnskriptClient
from unskript.connectors.schema.ssh import SSHSchema, AuthSchema, PrivateKeySchema, VaultSchema, KerberosSchema
from unskript.connectors.interface import ConnectorInterface


def join_path(h,f, e,t, r):
    return str(h + '/' + f + '/' + e.lstrip('/') + '/' + t + "/" + r.lstrip('/'))

class SSHOutput():
    def __init__(self, host:str, stdoutChannel:any, stdoutString:List[str]=None):
        self.host = host
        self.stdoutChannel = stdoutChannel
        self.stdoutString = stdoutString

    @property
    def stdout(self):
        if self.stdoutString is not None:
            return self.stdoutString

        if not self.stdoutChannel:
            return
        return self.stdoutChannel.readlines()

class SSHClient():
    def __init__(self, port:int, username:str):
        self.port = port
        self.username = username
        self.hostHandles = {}
        self.timeout = 30

    def create_auth_handle(self, hosts:List[str], password:str, proxy_host:str=None, proxy_user:str=None, proxy_password:str=None, proxy_port:int=22):
        for host in hosts:
            jumpbox_channel = None
            try:
                target=paramiko.SSHClient()
                target.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                entry = {'host':target}
                if proxy_host is not None:
                    jumpbox=paramiko.SSHClient()
                    entry["jumpbox"] = jumpbox
                    jumpbox.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    proxyUser = self.username
                    if proxy_user is not None:
                        proxyUser = proxy_user
                    jumpbox.connect(proxy_host, proxy_port, username=proxyUser, password=proxy_password, timeout=self.timeout)
                    jumpbox_transport = jumpbox.get_transport()
                    src_addr = (proxy_host, proxy_port)
                    dest_addr = (host, self.port)
                    jumpbox_channel = jumpbox_transport.open_channel("direct-tcpip", dest_addr, src_addr, timeout=self.timeout)
                self.hostHandles[host] = entry
                self.hostHandles[host]['host'].connect(host, self.port, username=self.username, password=password, sock=jumpbox_channel)
            except Exception as e:
                print(f'Not able to connect to {host}, {str(e)}')
                continue

        return self

    def create_pem_handle(self, hosts:List[str], pkey:str, proxy_host:str=None, proxy_user:str=None, proxy_pkey:str=None, proxy_port:int=22):
        for host in hosts:
            jumpbox_channel = None
            try:
                target=paramiko.SSHClient()
                target.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                entry = {'host':target}
                if proxy_host is not None:
                    jumpbox=paramiko.SSHClient()
                    entry["jumpbox"] = jumpbox
                    jumpbox.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    proxyUser = self.username
                    if proxy_user is not None:
                        proxyUser = proxy_user
                    k = paramiko.RSAKey.from_private_key_file(proxy_pkey)
                    jumpbox.connect(proxy_host, proxy_port, username=proxyUser, pkey=k, timeout=self.timeout)
                    jumpbox_transport = jumpbox.get_transport()
                    src_addr = (proxy_host, proxy_port)
                    dest_addr = (host, self.port)
                    jumpbox_channel = jumpbox_transport.open_channel("direct-tcpip", dest_addr, src_addr, timeout=self.timeout)
                k = paramiko.RSAKey.from_private_key_file(pkey)
                self.hostHandles[host] = entry
                self.hostHandles[host]['host'].connect(host, self.port, username=self.username, pkey=k, sock=jumpbox_channel, timeout=self.timeout)
            except Exception as e:
                print(f'Not able to connect to {host}, {str(e)}')
                continue
        return self

    def create_vault_handle(self, hosts:List[str], pkey:str, cert_file:str, proxy_host:str=None, proxy_port:int=22, proxy_user:str=None):
        for host in hosts:
            jumpbox_channel = None
            try:
                target=paramiko.SSHClient()
                target.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                entry = {'host':target}
                if proxy_host is not None:
                    jumpbox=paramiko.SSHClient()
                    entry["jumpbox"] = jumpbox
                    jumpbox.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    proxyUser = self.username
                    if proxy_user is not None:
                        proxyUser = proxy_user
                    k = paramiko.RSAKey.from_private_key_file(pkey)
                    jumpbox.connect(proxy_host, proxy_port, username=proxyUser, pkey=k, key_filename=cert_file, timeout=self.timeout)
                    jumpbox_transport = jumpbox.get_transport()
                    src_addr = (proxy_host, proxy_port)
                    dest_addr = (host, self.port)
                    jumpbox_channel = jumpbox_transport.open_channel("direct-tcpip", dest_addr, src_addr, timeout=self.timeout)
                k = paramiko.RSAKey.from_private_key_file(pkey)
                self.hostHandles[host] = entry
                self.hostHandles[host]['host'].connect(host, self.port, username=self.username, pkey=k, key_filename=cert_file, sock=jumpbox_channel, timeout=self.timeout)
            except Exception as e:
                print(f'Not able to connect to {host}, {str(e)}')
                continue
        return self

    # For Kerberos 
    def create_kerberos_handle(self, 
                            hosts:List[str], 
                            kerberos_user_with_realm: str, 
                            password: str, 
                            proxy_host:str=None,  
                            proxy_user:str=None, 
                            proxy_password:str=None, 
                            proxy_port:int=22):
        if not kerberos_user_with_realm:
            raise ValueError("Username With REALM is a mandatory parameter")
        
        if password:
            cmd = f'echo "{password}" | kinit {kerberos_user_with_realm};klist'
            t_process = subprocess.Popen(cmd,
                                shell=True,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
            _, stderr = t_process.communicate()
            if t_process.returncode != 0:
                raise ValueError(f"An Error occurred: {stderr.decode('utf-8')}")
        else:
            t_process = subprocess.run(['kinit', kerberos_user_with_realm])
            if t_process.returncode != 0:
                raise ValidationError(f"Unable to Authenticate with Kerberos Server. {t_process.stderr()}")
        
        for host in hosts:
            jumpbox_channel = None
            try:
                target=paramiko.SSHClient()
                target.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                entry = {'host':target}
                if proxy_host is not None:
                    jumpbox=paramiko.SSHClient()
                    entry["jumpbox"] = jumpbox
                    jumpbox.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    proxyUser = self.username
                    if proxy_user is not None:
                        proxyUser = proxy_user
                    jumpbox.connect(proxy_host, 
                                    proxy_port, 
                                    username=proxyUser, 
                                    password=proxy_password, 
                                    timeout=self.timeout,
                                    gss_auth=True, 
                                    gss_kex=True, 
                                    gss_deleg_creds=True)
                    jumpbox_transport = jumpbox.get_transport()
                    src_addr = (proxy_host, proxy_port)
                    dest_addr = (host, self.port)
                    jumpbox_channel = jumpbox_transport.open_channel("direct-tcpip", dest_addr, src_addr, timeout=self.timeout)
                self.hostHandles[host] = entry
                self.hostHandles[host]['host'].connect(host, 
                                                       self.port, 
                                                       username=self.username, 
                                                       password=password,
                                                       sock=jumpbox_channel,
                                                       gss_auth=True, 
                                                       gss_kex=True, 
                                                       gss_deleg_creds=True)
            except Exception as e:
                print(f'Not able to connect to {host}, {str(e)}')
                continue

        return self

    def run_command(self, command:str, sudo:bool=False):
        runCommandOutput = []
        if sudo is True:
            ## prefix sudo to the command.
            command = "sudo " + command
        for host, handle in self.hostHandles.items():
            try:
                stdin, stdout, stderr = handle['host'].exec_command(command)
                exit_status = stdout.channel.recv_exit_status()
                if exit_status == 0:
                    runCommandOutput.append(SSHOutput(host, stdout))
                else:
                    o = f'command {command} failed on {host}, exit status {exit_status}'
                    print(o)
                    runCommandOutput.append(SSHOutput(host, stdoutString=[o]))
            except Exception as e:
                print(f'Run command {command} failed for {host}, {str(e)}')
                runCommandOutput.append(SSHOutput(host, stdoutString=[str(e)]))
        return runCommandOutput

    def copy_file(self, local_file: str, remote_file: str, receive_from_remote_server: bool = True):
        for host, handle in self.hostHandles.items():
            try:
                #Get the sftp client for this host
                ftpClient = handle['host'].open_sftp()
                if receive_from_remote_server:
                    ftpClient.get(remote_file, local_file)
                else:
                    ftpClient.put(local_file, remote_file)
            except Exception as e:
                print(f'scp failed for {host}, {str(e)}, local_file {local_file}, remote_file {remote_file}, direction {receive_from_remote_server}')

    def join(self):
        # Close the connection.
        for host, handle in self.hostHandles.items():
            try:
                handle['host'].close()
                if 'jumpbox' in handle:
                    handle['jumpbox'].close()
            except Exception as e:
                print(f'connection close failed, {str(e)}')
                continue


class SSHConnector(ConnectorInterface):
    def get_handle(self, data):
        try:
            sshCredential = SSHSchema(**data)
        except ValidationError as e:
            raise e
        sshClient = SSHClient(sshCredential.port, sshCredential.username)
        if isinstance(sshCredential.authentication, AuthSchema):
            return lambda h, proxy_host: sshClient.create_auth_handle(hosts=h,
                                                          password=sshCredential.authentication.password.get_secret_value(),
                                                          proxy_host=sshCredential.proxy_host,
                                                          proxy_port=sshCredential.proxy_port,
                                                          proxy_user=sshCredential.authentication.password.proxy_user,
                                                          proxy_password=sshCredential.authentication.password.proxy_password) if proxy_host is None else sshClient.create_auth_handle(hosts=h,
                                                                                                                                                            password=sshCredential.authentication.password.get_secret_value(),
                                                                                                                                                            proxy_host=proxy_host,
                                                                                                                                                            proxy_port=sshCredential.proxy_port,
                                                                                                                                                            proxy_user=sshCredential.authentication.password.proxy_user,
                                                                                                                                                            proxy_password=sshCredential.authentication.password.proxy_password)
        elif isinstance(sshCredential.authentication, PrivateKeySchema):
            handler, name = tempfile.mkstemp()
            os.write(handler, str.encode(sshCredential.authentication.private_key))
            os.close(handler)
            proxy_pkey = None
            if sshCredential.authentication.proxy_private_key is not None:
                proxy_handler, proxy_pkey = tempfile.mkstemp()
                os.write(proxy_handler, str.encode(sshCredential.authentication.proxy_private_key))
                os.close(proxy_handler)

            return lambda h, proxy_host: sshClient.create_pem_handle(hosts=h,
                                                         pkey=name,
                                                         proxy_host=sshCredential.proxy_host,
                                                         proxy_port=sshCredential.proxy_port,
                                                         proxy_user=sshCredential.proxy_user,
                                                         proxy_pkey=proxy_pkey) if proxy_host is None else sshClient.create_pem_handle(hosts=h,
                                                                                                            pkey=name,
                                                                                                            proxy_host=proxy_host,
                                                                                                            proxy_port=sshCredential.proxy_port,
                                                                                                            proxy_user=sshCredential.proxy_user,
                                                                                                            proxy_pkey=proxy_pkey)

        elif isinstance(sshCredential.authentication, VaultSchema):
            proxy_rsa_file = os.environ.get('HOME') + '/.ssh/id_rsa'
            proxy_pub_file = os.environ.get('HOME') + '/.ssh/id_rsa.pub'
            proxy_cert_file = os.environ.get('HOME') + '/.ssh/id_rsa-cert.pub'
            if not os.path.exists(proxy_pub_file):
                import subprocess

                cmd = ["ssh-keygen", "-t", "rsa", "-q", "-f", proxy_rsa_file, "-N", ""]
                try:
                    subprocess.check_output(cmd)
                except Exception as e:
                    raise e


            # Get the public key signed from Vault
            try:
                client = UnskriptClient(os.environ['TENANT_URL'], os.environ['UNSKRIPT_TOKEN'])
                vault_token = client.fetch_vault_token()
            except Exception as e:
                print(f'Failed to fetch vault token: {str(e)}')
                raise Exception(f"unable to fetch vault token: {str(e)}")

            vault_url = join_path(sshCredential.authentication.vault_url, "v1",
                                sshCredential.authentication.vault_secret_path, "sign",
                                sshCredential.authentication.vault_role)

            with open(proxy_pub_file) as f:
                pem_key = f.readlines()

            encoded_body = {"public_key": pem_key[0].strip('\n')}
            hdr = {"X-Vault-Token": vault_token}
            try:
                result = requests.post(vault_url,headers=hdr, json=encoded_body)
                result.raise_for_status()
                output = result.json()
                with open(proxy_cert_file, "w") as f:
                    f.writelines(output.get('data').get('signed_key'))
            except Exception as e:
                print(f'Failed to sign cert {str(e)}')
                raise e

            #For Vault case, we dont need the proxy private key as it should be the same as the host private key.
            return lambda h, proxy_host: sshClient.create_vault_handle(hosts=h,
                                        pkey=proxy_rsa_file,
                                        cert_file=proxy_cert_file,
                                        proxy_host=sshCredential.proxy_host,
                                        proxy_port=sshCredential.proxy_port,
                                        proxy_user=sshCredential.proxy_user) if proxy_host is None else sshClient.create_vault_handle(hosts=h,
                                                                                                            pkey=proxy_rsa_file,
                                                                                                            cert_file=proxy_cert_file,
                                                                                                            proxy_host=proxy_host,
                                                                                                            proxy_port=sshCredential.proxy_port,
                                                                                                            proxy_user=sshCredential.proxy_user)
        elif isinstance(sshCredential.authentication, KerberosSchema):
            kerberos_user_with_realm = sshCredential.authentication.user_with_realm
            return lambda h, proxy_host: sshClient.create_kerberos_handle(hosts=h,
                                        kerberos_user_with_realm=kerberos_user_with_realm,
                                        password=sshCredential.authentication.password.get_secret_value(),
                                        proxy_host=sshCredential.proxy_host,
                                        proxy_user=sshCredential.proxy_user,
                                        proxy_password=sshCredential.authentication.proxy_password.get_secret_value(),
                                        proxy_port=sshCredential.proxy_port) if proxy_host is None else  sshClient.create_kerberos_handle(hosts=h,
                                                                                                            kerberos_user_with_realm=kerberos_user_with_realm,
                                                                                                            password=sshCredential.authentication.password.get_secret_value(),
                                                                                                            proxy_host=sshCredential.proxy_host,
                                                                                                            proxy_user=sshCredential.proxy_user,
                                                                                                            proxy_password=sshCredential.authentication.proxy_password.get_secret_value(),
                                                                                                            proxy_port=sshCredential.proxy_port)