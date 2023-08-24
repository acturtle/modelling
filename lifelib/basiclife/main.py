import modelx as mx
import time

proj = mx.read_model(r"BasicTerm_S").Projection


print("Start =",  time.strftime("%H:%M:%S", time.localtime()))
total = 0
for i in range(1, 10_000):
    proj.point_id = i
    total += proj.pv_net_cf()
    if i % 100 == 0:
        print("i =", i)
print(total)

print("End =",  time.strftime("%H:%M:%S", time.localtime()))
