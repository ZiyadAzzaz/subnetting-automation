import ipaddress
import networkx as nx
import matplotlib.pyplot as plt

def hosts_to_prefix(hosts):
    for prefix in range(32, 0, -1):
        if (2 ** (32 - prefix) - 2) >= hosts:
            return prefix
    return 32

def ip_to_binary(ip):
    return '.'.join(f"{int(octet):08b}" for octet in str(ip).split('.'))

def get_usable_range(net):
    if net.prefixlen >= 31:
        return ("N/A", "N/A")
    hosts = list(net.hosts())
    return (str(hosts[0]), str(hosts[-1]))

def allocate_subnets(base_cidr, host_needs):
    base_net = ipaddress.ip_network(base_cidr, strict=False)
    sorted_needs = sorted(host_needs, reverse=True)

    allocated_subnets = []
    current_ip = base_net.network_address

    for hosts in sorted_needs:
        prefix = hosts_to_prefix(hosts)
        subnet = ipaddress.ip_network(f"{current_ip}/{prefix}", strict=False)

        if subnet.network_address < base_net.network_address or subnet.broadcast_address > base_net.broadcast_address:
            raise ValueError(f"Subnet {subnet} out of base network range {base_net}")

        allocated_subnets.append(subnet)
        current_ip = subnet.broadcast_address + 1

    return allocated_subnets

def print_subnet_info(idx, net):
    usable_hosts = net.num_addresses - 2 if net.prefixlen < 31 else net.num_addresses
    first_usable, last_usable = get_usable_range(net)
    print(f"Subnet {idx}: {net.with_prefixlen}")
    print(f"Usable Hosts: {usable_hosts}")
    print(f"Range: {first_usable} - {last_usable}")
    print(f"Broadcast: {net.broadcast_address}")
    print(f"Subnet Mask: {net.netmask}")
    print(f"IP Address (binary): {ip_to_binary(net.network_address)}")
    print(f"Subnet Mask (binary): {ip_to_binary(net.netmask)}")
    print(f"Broadcast Address (binary): {ip_to_binary(net.broadcast_address)}\n")

def visualize_subnets(base_cidr, subnets):
    G = nx.DiGraph()
    base_net = ipaddress.ip_network(base_cidr)
    base_label = f"Base: {base_net.with_prefixlen}"
    G.add_node(base_label)

    for subnet in subnets:
        usable_hosts = subnet.num_addresses - 2 if subnet.prefixlen < 31 else subnet.num_addresses
        first_usable, last_usable = get_usable_range(subnet)
        label = (f"{subnet.with_prefixlen}\n"
                 f"Hosts: {usable_hosts}\n"
                 f"Range: {first_usable} - {last_usable}\n"
                 f"Broadcast: {subnet.broadcast_address}")
        G.add_node(label)
        G.add_edge(base_label, label)

    plt.figure(figsize=(12, 7))
    pos = nx.spring_layout(G, seed=42)
    nx.draw(G, pos, with_labels=True, node_size=4000, node_color="lightblue",
            font_size=10, font_weight="bold", arrows=True, arrowstyle='-|>')
    plt.title("Subnet Allocation Topology")
    plt.show()

if __name__ == "__main__":
    print("Advanced Subnetting Automation\n")

    base_cidr = input("Enter base CIDR block (e.g., 10.0.0.0/24): ").strip()

    while True:
        try:
            host_input = input("Enter required hosts per subnet separated by commas (e.g., 50,20,5): ")
            host_needs = [int(h.strip()) for h in host_input.split(",") if h.strip().isdigit()]
            if not host_needs:
                raise ValueError("No valid host counts entered.")
            break
        except ValueError as ve:
            print(f"Invalid input: {ve}. Please try again.")

    try:
        allocated_subnets = allocate_subnets(base_cidr, host_needs)
        print(f"\nTotal subnets allocated: {len(allocated_subnets)}\n")
        for i, subnet in enumerate(allocated_subnets, 1):
            print_subnet_info(i, subnet)
        visualize_subnets(base_cidr, allocated_subnets)

    except Exception as e:
        print(f"Error: {e}")
