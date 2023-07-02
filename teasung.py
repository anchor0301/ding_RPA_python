import os
import datetime

path_dir = "/Users/anchor/Desktop/사진"

file_list = os.listdir(path_dir)
file_list_gettime = os.path.getctime(path_dir)
print(file_list.sort(reverse=True))


for i in range(3, 8):
    create_time =  os.path.getctime(f'{path_dir}/{file_list[i]}')
    create_time = datetime.datetime.fromtimestamp(create_time)
    create_time = datetime.datetime.strftime(create_time, '%Y-%m-%d %H:%M')

    print(f'[{i - 2}]', end="\t  ")
    print(file_list[i], end="\t")
    print(create_time)
