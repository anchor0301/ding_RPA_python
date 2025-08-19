law = [{"TC":1,"RAMP":2,"PWR":3},{"TC":4,"RAMP":5,"PWR":6},{"TC":7,"RAMP":8,"PWR":9},{"TC":11,"RAMP":12,"PWR":13}]

data_list = [[] for _ in range(len(law[0]))]
for item in law:
    for idx, key in enumerate(item):
        data_list[idx].append(item[key])
print(data_list)
