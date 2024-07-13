from collections import defaultdict, deque

nat_list = [
  "1 - us-west1-a",
  "2 - us-west1-b",
  "3 - us-west1-b",
]
subnet_list = [
  "1 - us-west1-a",
  "2 - us-west1-b",
  "3 - us-west1-b",
  "4 - us-west1-c"
]

def conver_array_to_dict(arr):
    dict = {}
    for item in arr:
        nat, region = item.split(" - ")
        if region not in dict:
            dict[region] = []
        dict[region].append(nat)
    return dict


def allocate_subnets(nat_instances, subnets):
    allocation = defaultdict(list)
    unallocated_subnets = []

    for az, az_subnets in subnets.items():
        if az in nat_instances:
            nat_queue = deque([(nat, az) for nat in nat_instances[az]])
            for subnet in az_subnets:
                if nat_queue:
                    nat_instance, nat_az = nat_queue.popleft()
                    allocation[f"{nat_instance} - {nat_az}"].append((subnet, az))
                    nat_queue.append((nat_instance, nat_az))
                else:
                    unallocated_subnets.append((subnet, az))
        else:
            unallocated_subnets.extend([(subnet, az) for subnet in az_subnets])

    nat_queue = deque([(nat, az) for az in nat_instances for nat in nat_instances[az]])
    for subnet, az in unallocated_subnets:
        if nat_queue:
            nat_instance, nat_az = nat_queue.popleft()
            allocation[f"{nat_instance} - {nat_az}"].append((subnet, az))
            nat_queue.append((nat_instance, nat_az))

    return dict(allocation)

allocation = allocate_subnets(conver_array_to_dict(nat_list), conver_array_to_dict(subnet_list))

for nat, subs in allocation.items():
    print(f"Instance ({nat}):")
    for sub, az in subs:
        print(f" subnet ({sub} - {az})")