# Satosa-saml2saml
An example configuration to deploy SATOSA SAML-to-SAML one-to-many proxy with an Additional SAML2 backed for SPID (Italian Digital Identity System).

Official docs:
- [SaToSa Saml2Saml Documentation](https://github.com/IdentityPython/SATOSA/blob/master/doc/one-to-many.md)
- [Use cases](https://github.com/IdentityPython/SATOSA/wiki#use-cases)

--------------------------------------

![big picture](gallery/spid_proxy.png)

**Figure1** : _A quite common scenario, many pure SAML2 SP being proxied through SATHOSA SPID Backend to have compliances on AuthnRequest and Metadata operations_


## Requirements

The SaToSa example contained in this project works if the following patchs will be used:


#### Regarding SPID (not mandatory for other SAML2 use cases)

- [[Micro Service] Decide backend by target entity ID](https://github.com/IdentityPython/SATOSA/pull/220)
  This is a work in progress but it just works as it is!
- [date_xsd_type] https://github.com/IdentityPython/pysaml2/pull/602/files
- [disabled_weak_algs] https://github.com/IdentityPython/pysaml2/pull/628
- [ns_prefixes] https://github.com/IdentityPython/pysaml2/pull/625

We can also get all those patches and features merged in this branches:
- [pysaml2](https://github.com/peppelinux/pysaml2/tree/pplnx-v6.5.0)
- [SATOSA](https://github.com/peppelinux/SATOSA/tree/pplnx-v7.0.1)


#### Installing requirements

###### Prepare environment
```
virtualenv -ppython3 satosa.env
source satosa.env/bin/activate
```

###### Dependencies
````
apt install -y libffi-dev libssl-dev xmlsec1 python3-pip xmlsec1 procps

git clone https://github.com/peppelinux/Satosa-saml2saml.git
cd Satosa-saml2saml
pip install -r requirements.txt
````

## First Run

Create certificates for SAML2 operations, thanks to [psmiraglia](https://github.com/psmiraglia/spid-compliant-certificates).
````
export WD="spid_cert/"

mkdir $WD && cd $WD
ln -s ../oids.conf .

# create your values inline 
cat > my.env <<EOF
export COMMON_NAME="Comune di Roma"
export LOCALITY_NAME="Roma"
export ORGANIZATION_IDENTIFIER="PA:IT-c_h501"
export ORGANIZATION_NAME="Comune di Roma"
export SERIAL_NUMBER="1234567890"
export SPID_SECTOR="public"
export URI="https://spid.comune.roma.it"
export DAYS="7300"
EOF

. my.env

bash ../build_spid_certs.sh
````

Configure SATOSA with environment variables:
````
export SATOSA_BASE_EID="https://satosa.testunical.it"
export SATOSA_STATE_ENCRYPTION_KEY="that_random_sequence"
export SATOSA_USER_ID_HASH_SALT="that_random_sequence_4_hash"
export SATOSA_UNKNOW_ERROR_REDIRECT_PAGE="https://ds.auth.unical.it/info_page/authproxy-error-page/"
export SATOSA_DEBUG_LOG="/var/log/uwsgi/satosa_debug.log"

# SAML2 Backend related
export SATOSA_IDP_BLACKLIST_FILE="/path/to/blacklist.json"
export SATOSA_SAML2_BACKEND_KEY_FILE=""
export SATOSA_SAML2_BACKEND_CRT_FILE=""
````


## Todo:

- [Single Logout in Satosa](https://github.com/IdentityPython/SATOSA/issues/211)


## References
- https://github.com/IdentityPython/SATOSA
- [IDP/SP Discovery service](https://medium.com/@sagarag/reloading-saml-idp-discovery-693b6bff45f0)
- https://github.com/IdentityPython/SATOSA/blob/master/doc/README.md#frontend
- [saml2.0 IdP and SP for tests](https://samltest.id/)
