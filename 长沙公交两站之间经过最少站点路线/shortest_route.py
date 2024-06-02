import requests
from bs4 import BeautifulSoup 

# 定义请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

# 基础URL
base_url = "http://changsha.gongjiao.com/xianlu_"

bus_lines = {} # 存储公交线路
stations = {} # 存储公交站点

# 定义站点类
class Station:
    def __init__(self, name):
        self.name = name
        self.lines = set()
        self.neighbours = {}

# 爬取所有线路
print("querying bus lines...")
for num in range(28657, 28859):
    url = base_url + str(num)
    # print(f"querying {url}")
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 获取线路名
    line_num = soup.find('div', class_='gj01_lineSite_title').text.split()[0]
    line_num = line_num[:line_num.find('路') + 1]  

    # 如果有线路
    if line_num: 
        ul = soup.find('ul', class_='gj01_line_img') 
        bus_lines[line_num] = [a.text for a in ul.find_all('a', href=True)]
        for station in bus_lines[line_num]:
            if station not in stations:
                stations[station] = Station(station)
            stations[station].lines.add(line_num)

# 添加邻居
for line, stops in bus_lines.items():
    for i, name in enumerate(stops):
        if i > 0:
            stations[name].neighbours[stops[i - 1]] = line
        if i < len(stops) - 1:
            stations[name].neighbours[stops[i + 1]] = line

# Dijkstra算法计算最短路径
def dijkstra(start, end):
    # 初始化最短路径字典，键为节点，值为一个三元组（前驱节点，当前最短距离，当前线路）
    shortest_paths = {start: (None, 0, next(iter(stations[start].lines)))}
    current_node = start # 当前处理的节点
    current_line = shortest_paths[start][2] # 当前线路
    visited = set() # 已访问的节点集合

    while current_node != end: # 当当前节点不是终点时
        visited.add(current_node) # 将当前节点标记为已访问
        destinations = stations[current_node].neighbours # 获取当前节点的邻居节点及其对应的线路
        weight_to_current_node = shortest_paths[current_node][1] # 获取到当前节点的最短距离

        for next_node in destinations: # 遍历每一个邻居节点
            line = destinations[next_node] # 获取邻居节点的线路
            weight = 1 # 假设每个站点之间的距离为1
            total_weight = weight_to_current_node + weight # 计算从起点到达该邻居节点的总距离

            if next_node not in shortest_paths: # 如果邻居节点未被记录在最短路径字典中
                shortest_paths[next_node] = (current_node, total_weight, line) # 更新该邻居节点的最短路径信息
            else:
                current_shortest_weight = shortest_paths[next_node][1] # 获取当前记录的邻居节点的最短距离
                if current_shortest_weight > total_weight: # 如果新计算的距离更短，则更新该邻居节点的最短路径信息
                    shortest_paths[next_node] = (current_node, total_weight, line)

        next_destinations = {node: shortest_paths[node] for node in shortest_paths if node not in visited} # 筛选出所有未访问的节点
        if not next_destinations: # 如果没有未访问的节点，说明路径不可达
            return "Route Not Possible"
        current_node = min(next_destinations, key=lambda k: next_destinations[k][1]) # 选择具有最短距离的未访问节点作为下一个当前节点

    path = [] # 构建最短路径，通过回溯前驱节点
    while current_node is not None:
        path.append(current_node)
        next_node, _, line = shortest_paths[current_node]
        if line != current_line and current_line is not None: # 如果线路发生变化，添加转乘信息
            path.append(f"转乘 {line}")
        current_line = line # 更新当前线路
        current_node = next_node # 回溯到前驱节点
    path = path[::-1] # 反转路径，使其从起点到终点
    return path, shortest_paths[end][1], shortest_paths[start][2] # 返回最短路径，路径总长度和起始线路


# 获取用户输入的起始站点和目标站点
print(f"可供选择的站点有：{', '.join(stations.keys())}\n")
start_station = input('起始站点名： ')
end_station = input('目标站点名：')
print()

# 计算最短路径
path, total_stops, first_line = dijkstra(start_station, end_station)
if path == "Route Not Possible":
    print(f"无法从 {start_station} 到 {end_station}")
else:
    print(f"总共需要经过 {total_stops} 站")
    print(f"首先乘坐的线路是 {first_line}")
    print(f"从 {start_station} 到 {end_station} 的最短路径为：")
    print(' -> '.join(path))