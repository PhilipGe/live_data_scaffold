from dev_api.descriptor import AppBuilder
from time import sleep
from random import random

counter = 0
def stream_1(p1_update, p2_update): 
    global counter
    p1_update(str(counter))
    p2_update(str(-counter))
    counter += 1

i1 = 0
def point_stream_1():
    global i1
    x = [(i, random()) for i in range(i1,i1+2)]
    i1 += 2
    return x

i2 = 0
def point_stream_2():
    global i2
    x = [(i, random()) for i in range(i2,i2+2)]
    i2 += 2
    return x

if __name__ == '__main__':
    builder = AppBuilder()

    builder.add_parameter('L1', True)
    builder.add_parameter('L2', False)
    builder.add_parameter('L3', False)
    builder.add_parameter('L4', False)
    builder.add_parameter('L5', False)
    builder.add_parameter('L6', False)
    builder.add_parameter('L7', False)
    builder.add_parameter('L8', True)

    builder.add_button('L1',['L1'],lambda l1: print(f'It works! Value of L1: {l1}'))

    builder.add_indicator_stream(['L2','L4'], stream_1)

    builder.add_graph('One','x','y')
    builder.add_graph('Two','x','y')

    builder.add_point_stream('One', point_stream_1, poll_interval_s=0.2)

    builder.add_point_stream('Two', point_stream_2, poll_interval_s=0.1)

    builder.build_app().run()