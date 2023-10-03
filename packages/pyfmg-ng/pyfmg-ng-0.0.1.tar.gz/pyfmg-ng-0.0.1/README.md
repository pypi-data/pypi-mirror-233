# pyfmg-ng
FortiManager SDK Next Generation

This is a work in progress SDK with simpler access to FortiManger. 


'''
import pyfmg-ng.client
import pyfmg-ng.pyfmg.adom
from pyfmg-ng.fmgapi import FmgAPIObjectExists, FmgApiObjectNotFound

fmg_username = "demo"
fmg_password = "pass"
fmg_host = "fmg.example.com"
adom_name = "root"
vdom = "root"
firewall = "demo-200f"

client = pyfmg-ng.client.FmgClient(fmg_host,fmg_username, fmg_password,adom_name)

client.adom.lock()
try:
    client.adom.vdom_add(firewall,vdom)
    client.install(firewall,vdom)
    client.adom.policy_package_create(vdom)
    client.adom.policy_package_install_target(vdom,firewall,vdom)
except FmgAPIObjectExists as ex:
    print(f"Warning! VDOM Allready exists! {ex}")


script_name = "test.conf"
script_raw = ""
try:
    client.adom.script_delete(script_name)
except FmgApiObjectNotFound as ex:
    pass
finally:
    client.adom.script_upload_remote_fg(script_name, script_raw)
    #Check if we should skip executing the script on the fortigate
    client.adom.script_run(script_name,firewall,vdom)
    client.adom.script_delete(script_name)

client.adom.unlock()
client.rest.logout()
'''