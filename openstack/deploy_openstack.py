import openstack

# Connexion à OpenStack
conn = openstack.connect(cloud='my_openstack')

# Créer des machines virtuelles
for i in range(3):  # Trois instances pour le cluster
    server = conn.create_server(
        name=f"docker-node-{i}",
        image="Ubuntu 20.04",
        flavor="m1.small",
        key_name="my-key",
        network="private",
        security_groups=["default"]
    )
    print(f"Created server: {server.name}")
