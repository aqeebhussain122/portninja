import sys
import ldap3
ip = str(sys.argv[1])
server = ldap3.Server(ip, get_info = ldap3.ALL, port = 636, use_ssl = True)
connection = ldap3.Connection(server)
bind = connection.bind()
if bind == True:
    print("Null login is allowed")
    print("Going to dump server info")
    info = server.info
    print(info)

#conn = connection.search('dc=dc1,dc=dc2,dc=dc3,dc=dc4', '(objectclass=*)')
conn = connection.search(search_base='DC=dc1,dc=dc2,dc=dc3,dc=dc4', search_filter='(&(objectClass=*))', search_scope='SUBTREE', attributes='*')
if conn == True:
    print("Can dump objects...")
    print(connection.entries)

