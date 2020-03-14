import random
from libs.node import Node
from libs.node import Station
from libs.node import StationDcf
from libs.node import StationRl
from libs.channel import Channel
from tqdm import tqdm
from config import Config
#import matplotlib.pyplot as plt

cfg = Config()
global_time = 0
channel = Channel(global_time, [])

station_num = 5
data_rate = 6 #Mbps
#All the lengeth is a mutible of slot

#incule header
pkt_len = 1560
#us
slot_len = 10
sifs = 2
ack_len = 2 + sifs
difs = 4
timeout = ack_len

frame_len = pkt_len * 8 / slot_len / data_rate
stations_list = []
total_time = 0

for i in range(station_num):
    if cfg.stationType == "Dcf":
        station = StationDcf(i, frame_len, channel, global_time, i, timeout, ack_len, difs, sifs)
    elif cfg.stationType == "RL":
        station = StationRl(i, frame_len, channel, global_time, i, timeout, ack_len)
    stations_list.append(station)

for i in tqdm(range(cfg.NUM_EPOCHS)):
    for station in stations_list:
        station.simulate(global_time)
    global_time = global_time + 1
    channel.update_state(global_time)

    if cfg.shuffleStationList:
        random.shuffle(stations_list)

for station in stations_list:
    total_time += station.total_pkt_time
print("==> total_time:", total_time)
total_time_channel = 0
for i in range(len(channel.start)):
    if(i > 0):
        if (channel.start[i] == channel.start[i-1]):
            continue
    if(i < (len(channel.start)-1)):
        if(channel.start[i] == channel.start[i+1]):
            continue
    total_time_channel += frame_len
print("==> total_time_channel:", total_time_channel)

throughput = total_time/channel.time * data_rate * 1500 / 1560
print("==> throughput:", throughput)