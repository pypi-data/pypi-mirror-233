import os
import socket
import configparser
import logging
import requests
import uuid
import json

"""
Private function to return true or false if the profile exists in the credential
file in $HOME/.aws/credential
"""
def is_aws_profile_present(profile: str) -> bool:
    home_dir = os.environ.get('HOME')
    retval = False
    home_dir = os.environ.get('HOME')
    config = configparser.ConfigParser()
    config.read(home_dir + '/.aws/credentials')
    all_profiles = config.sections()
    if len(all_profiles) == 0:
        return retval

    for p in config.sections():
        if p in profile:
            retval = True
            break

    return retval

"""
This is a sample krb5.conf file.

    [libdefaults]
    default_realm = UNSKRIPT.VIRT
    kdc_timesync = 1
    ccache_type = 4
    forwardable = true
    dns_lookup_realm = false
    rdns = false
    proxiable = true
    fcc-mit-ticketflags = true
    [realms]
        UNSKRIPT.VIRT = {
            kdc = server.unskript.virt
            admin_server = server.unskript.virt
        }
        UNSKRIPT.VIRT2 = {
            kdc = server.unskript.virt
            admin_server = server.unskript.virt
        }
    [domain_realm]
    .unskript.virt = UNSKRIPT.VIRT
    unskript.virt = UNSKRIPT.VIRT


The Below functions manipulate this file to read, add and delete content to this file.
"""

default_content = """
[libdefaults]
default_realm = EXAMPLE.COM
kdc_timesync = 1
ccache_type = 4
forwardable = true
dns_lookup_realm = false
rdns = false
proxiable = true
fcc-mit-ticketflags = true
[realms]
    EXAMPLE.COM = {
        kdc = server.example.com
        admin_server = server.example.com
    }

[domain_realm]
.example.com = EXAMPLE.COM
example.com = EXAMPLE.COM
"""

"""
Private function to read krb5 file. The default location is in /etc/krb5.conf
"""
def read_krb_file():
    # This is required because by default Configparser does not handle '{ or }'
    # gracefully. The Workaround is to treat these characters as Comments.
    # Both Inline comment prefixes and comment prefixes
    if os.path.exists("/etc/krb5.conf") == False:
        with open("/etc/krb5.conf", "w") as f:
            f.write(default_content)

    config = configparser.ConfigParser(inline_comment_prefixes='{', comment_prefixes='}')
    config.read('/etc/krb5.conf')
    return config

"""
Private function to add new REALM into the krb5 file
"""
def add_new_realm(cfg, realm, kdc, admin_server: str = None):
    if not admin_server:
        admin_server = kdc
    if not cfg:
        return

    if cfg['realms']:
        cfg['realms'][realm.lower()] = f"\nkdc = {kdc.lower()}\nadmin_server = {admin_server.lower()}"
        cfg['domain_realm'].update({'.' + realm.lower(): realm.upper()})
        cfg['domain_realm'].update({realm.lower(): realm.upper()})

"""
Private function to delete a REALM from the krb5 file
"""
def del_realm(cfg, realm):
    try:
        del cfg["realms"][realm.upper()]
        del cfg["domain_realm"]['.' + realm.lower()]
        del cfg["domain_realm"][realm.lower()]
    except Exception as e:
        print("REALM DELETION ERROR: ", e)
        pass

"""
Private function to write back contents to krb5 file
"""

def write_krb_file(cfg):
    content = ""
    for s in cfg.sections():
        if s == "libdefaults":
            content += "[libdefaults]" + '\n'
            for ld in cfg['libdefaults'].items():
                content += f"  {ld[0]} = {ld[1]}" + '\n'
        elif s == "realms":
            content += "[realms]" + '\n'
            for r in cfg["realms"].items():
                content += f"    {r[0].upper()}" +  " = {" + '\n'
                for _r in r[1].split('\n'):
                    if not _r:
                        continue
                    content += "        " + _r + '\n'
                content += "    }" + '\n'
        elif s == "domain_realm":
            content += "[domain_realm]" + '\n'
            for dr in cfg["domain_realm"].items():
                content += f"  {dr[0]} = {dr[1]}" + '\n'

    with open('/etc/krb5.conf', 'w') as f:
        f.write(content)


"""
Private function to add entry for bastion and kdc entry into /etc/hosts file
"""
def add_host_entries(host_list):
    def _safe_entry(name):
        try:
            _ip = socket.gethostbyname(name)
            with open("/etc/hosts", "r") as f:
                content = f.read()
                if name not in content:
                    with open("/etc/hosts", "a") as f2:
                        f2.write(f"{_ip}    {name}")
        except Exception as e:
            raise e

    for h in host_list:
        if h:
            _safe_entry(h)


class TenantCredentials:
    tenant_url: str
    tenant_id: str
    proxy_id: str
    authorization_token: str

def get_tenants_credentials(body:dict, disable_token_check:bool) -> TenantCredentials:
    tenants_creds = TenantCredentials()
    tenants_creds.tenant_url = ''
    tenants_creds.tenant_id = ''
    tenants_creds.proxy_id = ''
    tenants_creds.authorization_token = ''
    credentials_keys = ['tenant_url', 'tenant_id', 'proxy_id', 'authorization_token']

    globalCredentials = True
    if body != None:
        for key in credentials_keys:
            if key in body['metadata']:
                globalCredentials = False

    if globalCredentials:
      tenants_creds.tenant_url = os.environ.get('UNSKRIPT_TENANT_URL', 'https://app.unskript.io')
      tenants_creds.tenant_id  = os.environ.get('UNSKRIPT_TENANT_ID', '')
      tenants_creds.proxy_id = os.environ.get('UNSKRIPT_PROXY_ID', '')
    else:
      if 'tenant_url' in body['metadata']:
        tenants_creds.tenant_url = body['metadata']['tenant_url']
      if 'tenant_id' in body['metadata']:
        tenants_creds.tenant_id  = body['metadata']['tenant_id']
      if 'proxy_id' in body['metadata']:
        tenants_creds.proxy_id = body['metadata']['proxy_id']

    tenants_creds.authorization_token = os.environ.get('UNSKRIPT_CONNECTOR_TOKEN', '')

    if disable_token_check == False:
        if tenants_creds.tenant_url == '':
            raise Exception("Tenant URL is Required!")
        if tenants_creds.tenant_id == '':
            raise Exception("Tenant ID is Required!")
        if tenants_creds.proxy_id == '':
            raise Exception("Proxy ID is Required!")
        if tenants_creds.authorization_token == '' and disable_token_check == False:
            raise Exception("Connector Token is Required!")

    return tenants_creds

# get_genai_credentials_from_saas get the genAI credentials from Saas. It returns
# a dictionary with organization_id, api_key as keys.
def get_genai_credentials_from_saas(metadata:dict, genai_type: str)-> dict:
    tenants_creds = get_tenants_credentials(metadata, disable_token_check=False)
    urlPath = "v1alpha1/integrations/config"
    urldict = {'req_hdr.tid': str(uuid.uuid4()), 'tenant_id':tenants_creds.tenant_id, 'integration_type':genai_type}

    url = '/'.join([tenants_creds.tenant_url, urlPath])
    hdrtoken = "Unskript-SHA " + tenants_creds.authorization_token
    hdr = {'Authorization': hdrtoken}
    try:
        response = requests.get(url, headers=hdr, params=urldict)
        response.raise_for_status()
    except Exception as e:
        logging.exception(f'Failed to get openAI config')
        raise e
    responseDict = response.json()
    return responseDict

# create_genai_request creates the genai request to SaaS and returns the request_id.
def create_genai_request_to_saas(body:dict)-> dict:
    tenants_creds = get_tenants_credentials(body, disable_token_check=False)
    urlPath = "v1alpha1/genai/requests"
    data_dict = body.get('metadata').copy()
    data_dict['tid'] = str(uuid.uuid4())

    url = '/'.join([tenants_creds.tenant_url, urlPath])
    hdrtoken = "Unskript-SHA " + tenants_creds.authorization_token
    hdr = {'Authorization': hdrtoken, 'Content-Type': 'application/json'}
    try:
        response = requests.post(url, headers=hdr, data=json.dumps(data_dict))
        response.raise_for_status()
    except Exception as e:
        logging.exception(f'Create genAI request failed')
        raise e
    responseDict = response.json()
    return responseDict

# get_genai_request_status gets the genai request status.
def get_genai_request_status(body:dict)-> dict:
    metadata = body.get('metadata')
    request_id = metadata.get('genai_request_id')
    tenants_creds = get_tenants_credentials(body, disable_token_check=False)
    urlPath = "v1alpha1/genai/requests" + "/" + request_id
    url_params = {}
    url_params['tid'] = str(uuid.uuid4())
    url_params['tenant_id'] = metadata.get('tenant_id')
    url = '/'.join([tenants_creds.tenant_url, urlPath])
    hdrtoken = "Unskript-SHA " + tenants_creds.authorization_token
    hdr = {'Authorization': hdrtoken, 'Content-Type': 'application/json'}
    try:
        response = requests.get(url, headers=hdr, params=url_params)
        response.raise_for_status()
    except Exception as e:
        logging.exception(f'Get genAI request status failed')
        raise e
    responseDict = response.json()
    # inputSchema needs to be converted to an array
    if 'action_details' in responseDict:
        # Keep in mind that inputSchema is the json dumps of the schema.
        responseDict['action_details']['inputschema'] = [json.loads(responseDict.get('action_details').get('inputSchema'))]
        responseDict['action_details'].pop('inputSchema')
    return responseDict
