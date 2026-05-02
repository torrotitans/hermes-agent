---
name: ldap
description: >
  Implement LDAP authentication, directory services, and user management for Torro.
  Covers LDAP protocol (RFC 4511), OpenLDAP configuration, LDIF data format,
  directory schema design, bind authentication, search operations, and integration
  with Torro's Auth middleware. USE FOR: LDAP setup, user sync, directory config,
  bind operations, search filters, LDIF management, OpenLDAP, Active Directory.
  DO NOT USE FOR: JWT token management (use next-auth), database queries, OAuth.
location: .roo/skills/ldap/SKILL.md
metadata:
  created: "2026-04-27"
  version: "1.0.0"
  compatibility:
    - openldap>=2.6
    - ldap3>=2.9 (Python)
    - python-ldap>=3.4
---

# LDAP Authentication Skill

## When to Use This Skill

- Setting up OpenLDAP/Active Directory servers
- Implementing LDAP bind authentication
- Writing LDIF data files for directory initialization
- Configuring user/group synchronization
- Debugging LDAP connection issues
- Implementing LDAP search filters
- Managing directory schema and object classes

## When NOT to Use This Skill

- JWT/session management → use next-auth skill
- OAuth provider integration → use next-auth skill
- Database user queries → use backend-architecture skill
- Password hashing → use backend-coding-standards skill

## Inputs Required

1. LDAP server URL and port
2. Base DN configuration
3. Bind DN and credentials
4. Search base and filter for users
5. Group/object class mappings

## Workflow

### Step 1: LDAP Protocol Basics

LDAP (Lightweight Directory Access Protocol) is defined in RFC 4511. It provides:
- Directory information tree (DIT) structure
- Bind (authenticate) operations
- Search and filter operations
- Modify/Add/Delete operations
- Unbind (session termination)

From Wikipedia: https://en.wikipedia.org/wiki/Lightweight_Directory_Access_Protocol

### Step 2: Directory Structure (DIT)

From [`assets/resource/ldap/torro.ldif`](assets/resource/ldap/torro.ldif):

```ldif
# Base entry - Organization root
dn: dc=torro,dc=com
dc: torro
o: Torro Company
objectclass: top
objectclass: dcObject
objectclass: organization

# Admin entry
dn: cn=admin,dc=torro,dc=com
cn: admin
objectclass: organizationalRole

# Users container
dn: cn=users,dc=torro,dc=com
cn: users
gidnumber: 500
objectclass: posixGroup
objectclass: top

# Group container
dn: cn=groups,dc=torro,dc=com
cn: groups
objectclass: posixGroup
objectclass: top
```

### Step 3: User Entry Schema

From [`assets/resource/ldap/torro.ldif`](assets/resource/ldap/torro.ldif):

```ldif
# User entry with inetOrgPerson + posixAccount
dn: cn=james.wilson,cn=users,dc=torro,dc=com
cn: james.wilson
sn: Wilson
uid: james.wilson
uidnumber: 1001
gidnumber: 5003
homedirectory: /home/users/james.wilson
mail: james.wilson@torro.ai
displayname: James Wilson
title: Senior Developer
userpassword: {SSHA}encrypted_password_hash
objectclass: top
objectclass: inetOrgPerson
objectclass: posixAccount

# User with multiple titles/roles
dn: cn=ashesh.kumar@hdfcbank.com,cn=users,dc=torro,dc=com
cn: ashesh.kumar@hdfcbank.com
sn: ashesh.kumar@hdfcbank.com
uid: ashesh.kumar@hdfcbank.com
uidnumber: 1102
gidnumber: 500
homedirectory: /home/users/ashesh.kumar@hdfcbank.com
mail: ashesh.kumar@hdfcbank.com
displayname: Ashesh Kumar
title: hdfc_owner
title: hdfc_uc1_owner
title: hdfc_it
title: hdfc_team
userpassword: {SSHA}encrypted_password_hash
objectclass: top
objectclass: inetOrgPerson
objectclass: posixAccount
```

### Step 4: Object Classes Reference

```
# Required object classes for Torro users:
objectclass: top                    # Base class (always required)
objectclass: inetOrgPerson          # Internet user (name, email, etc.)
objectclass: posixAccount           # Unix account (uid, gid, home)

# Optional object classes:
objectclass: organizationalPerson   # Extended person info
objectclass: person                 # Minimal person (sn, cn)
objectclass: groupOfNames           # Group with members
objectclass: posixGroup             # Unix group (gid, memberUid)

# Container object classes:
objectclass: dcObject               # Domain component
objectclass: organization           # Organization unit
objectclass: organizationalUnit     # OU for grouping
objectclass: container              # Generic container
```

### Step 5: Group Entry Schema

From [`assets/resource/ldap/torro.ldif`](assets/resource/ldap/torro.ldif):

```ldif
# POSIX group
dn: cn=engineers,dc=torro,dc=com
cn: engineers
gidnumber: 5003
memberuid: james.wilson
memberuid: jessica.martinez
objectclass: top
objectclass: posixGroup

# Group of names (AD-style)
dn: cn=data_governors,dc=torro,dc=com
cn: data_governors
description: Data Governors - CEO, CTO, VP Engineering
member: cn=adam.johnson,cn=users,dc=torro,dc=com
member: cn=sarah.williams,cn=users,dc=torro,dc=com
objectclass: top
objectclass: groupOfNames
```

### Step 6: Python LDAP Connection (ldap3)

From [`scripts/setup_ldap.py`](scripts/setup_ldap.py):

```python
from ldap3 import Server, Connection, ALL, SUBTREE, ADD

# LDAP Configuration
LDAP_HOST = "localhost"
LDAP_PORT = 389
LDAP_BASE_DN = "dc=torro,dc=ai"
LDAP_ADMIN_DN = "cn=admin,dc=torro,dc=ai"
LDAP_ADMIN_PASSWORD = "LldapDev123!"
DEFAULT_PASSWORD = "Torro123!"

# Connect to LDAP server
server = Server(LDAP_HOST, port=LDAP_PORT, use_ssl=False, get_info=ALL)
conn = Connection(server, user=LDAP_ADMIN_DN, password=LDAP_ADMIN_PASSWORD, auto_bind=True)

# Search for users
conn.search(
    search_base='cn=users,dc=torro,dc=com',
    search_filter='(objectClass=inetOrgPerson)',
    attributes=['cn', 'sn', 'mail', 'uid', 'title', 'displayname']
)

# Get results
users = [entry['attributes'] for entry in conn.entries]

# Bind authentication (verify credentials)
user_conn = Connection(server, user='cn=james.wilson,cn=users,dc=torro,dc=com', password='password')
user_conn.bind()
if user_conn.bound:
    print("Authentication successful")
    user_conn.unbind()
```

### Step 7: Torro Auth Integration

From [`src/api/login/tasks/login_interface_tasks.py`](src/api/login/tasks/login_interface_tasks.py):

```python
from utils.auth_helper import Auth

class LoginInterfaceTasks:
    @staticmethod
    def handle_login(request_data) -> Dict[str, Any]:
        """Authenticate user and return profile with new token."""
        login_name = request_data.get('login_name')
        login_password = request_data.get('login_password')
        offline_flag = request_data.get('is_offline', False)

        # Auth.authenticate() handles LDAP bind internally
        auth_result = Auth.authenticate(login_name, login_password, offline_flag)
        
        if auth_result.get('code') != 200:
            return auth_result
        
        user_data = auth_result.get('data', {})
        # user_data contains: token, id, account_id, account_cn, roles, etc.
        return user_data
```

### Step 8: LDIF File Management

From [`assets/resource/ldap/torro.ldif`](assets/resource/ldap/torro.ldif):

```bash
# Import LDIF file into OpenLDAP
ldapadd -x -D "cn=admin,dc=torro,dc=com" -W -f torro.ldif

# Export existing directory
ldapsearch -x -D "cn=admin,dc=torro,dc=com" -W -b "dc=torro,dc=com" > export.ldif

# Search specific entry
ldapsearch -x -D "cn=admin,dc=torro,dc=com" -W \
  -b "cn=users,dc=torro,dc=com" "(uid=james.wilson)"

# Delete entry
ldapdelete -x -D "cn=admin,dc=torro,dc=com" -W \
  "cn=james.wilson,cn=users,dc=torro,dc=com"
```

### Step 9: Common Search Filters

```python
# Search by UID
"(uid=james.wilson)"

# Search by email
"(mail=james.wilson@torro.ai)"

# Search by object class
"(objectClass=inetOrgPerson)"
"(objectClass=posixGroup)"

# Search by group membership
"(memberUid=james.wilson)"

# Search with multiple criteria
"(&(objectClass=inetOrgPerson)(title=Senior Developer))"

# Search for users in specific title range
"(|(title=CEO)(title=CTO)(title=VP*))"

# Search for active users
"(&(objectClass=inetOrgPerson)(!(userPassword=)))"

# Wildcard search
"(cn=*wilson)"
"(mail*@torro.ai)"
```

### Step 10: Password Handling

```python
from ldap3 import Server, Connection

# Password storage formats in LDAP:
# {SSHA} - Salted SHA (recommended)
# {SHA} - SHA hash
# {MD5} - MD5 hash (not recommended)
# {CRYPT} - Crypt hash
# plaintext - NOT RECOMMENDED (for testing only)

# Bind with password for authentication
def authenticate_ldap(server, username, password):
    """Authenticate user against LDAP directory."""
    user_dn = f"cn={username},cn=users,dc=torro,dc=com"
    user_conn = Connection(server, user=user_dn, password=password)
    user_conn.bind()
    is_bound = user_conn.bound
    user_conn.unbind()
    return is_bound
```

### Step 11: User Setup Script Pattern

From [`scripts/setup_ldap.py`](scripts/setup_ldap.py):

```python
from ldap3 import Server, Connection, ALL, ADD

def create_user(conn, user_data):
    """Create a new LDAP user entry."""
    dn = f"cn={user_data['uid']},cn=users,{LDAP_BASE_DN}"
    
    entry = {
        'cn': (user_data['cn'],),
        'sn': (user_data['sn'],),
        'uid': (user_data['uid'],),
        'uidnumber': (user_data['gid'],),
        'gidnumber': (user_data['gid'],),
        'homedirectory': (f"/home/users/{user_data['uid']}",),
        'mail': (user_data['mail'],),
        'displayname': (user_data['cn'],),
        'title': (user_data['role'],),
        'userpassword': (DEFAULT_PASSWORD,),
        'objectclass': (b'top', b'inetOrgPerson', b'posixAccount'),
    }
    
    conn.add(dn, **entry)
    return conn.result

def create_group(conn, group_data):
    """Create a new LDAP group entry."""
    dn = f"cn={group_data['cn']},dc=torro,dc=com"
    
    entry = {
        'cn': (group_data['cn'],),
        'gidnumber': (group_data['gid'],),
        'description': (group_data['description'],),
        'objectclass': (b'top', b'posixGroup'),
    }
    
    conn.add(dn, **entry)
    return conn.result
```

### Step 12: OpenLDAP Configuration

```bash
# Main config file: /etc/openldap/slapd.conf
# Schema files: /etc/openldap/schema/

# Basic slapd.conf
include     /etc/openldap/schema/core.schema
include     /etc/openldap/schema/cosine.schema
include     /etc/openldap/schema/inetorgperson.schema
include     /etc/openldap/schema/nis.schema

database    bdb
suffix      "dc=torro,dc=com"
rootdn      "cn=admin,dc=torro,dc=com"
rootpw      {SSHA}admin_password_hash

directory   /var/lib/ldap

index       objectClass eq
index       uid eq,sub
index       mail eq,sub
index       cn eq,sub
index       sn eq,sub
```

## Troubleshooting

### Connection Refused

```bash
# Check if LDAP server is running
systemctl status slapd

# Test connection
ldapsearch -x -H ldap://localhost:389 -b "dc=torro,dc=com" -s base

# Check firewall
telnet ldap-server 389
```

### Bind Failed

```python
# Verify bind DN format
user_dn = f"cn={username},cn=users,dc=torro,dc=com"

# Test with admin credentials first
admin_conn = Connection(server, user="cn=admin,dc=torro,dc=com", password="admin_password")
admin_conn.bind()
```

### Search Returns Empty

```python
# Verify search base
conn.search('dc=torro,dc=com', '(objectClass=*)')  # Should return all

# Check search filter syntax
conn.search('cn=users,dc=torro,dc=com', '(uid=james.wilson)')
```

## Related Files

- [`assets/resource/ldap/torro.ldif`](assets/resource/ldap/torro.ldif)
- [`scripts/setup_ldap.py`](scripts/setup_ldap.py)
- [`src/api/login/tasks/login_interface_tasks.py`](src/api/login/tasks/login_interface_tasks.py)
- [`src/api/login/interface_login.py`](src/api/login/interface_login.py)
- https://en.wikipedia.org/wiki/Lightweight_Directory_Access_Protocol (RFC 4511)
