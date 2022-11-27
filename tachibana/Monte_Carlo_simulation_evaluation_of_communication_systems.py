# 通信システムのモンテカルロシミュレーション評価

import random, math

# バッファクラス
class Buffer:
    def __init__(self, size):
        self.buffer = []
        self.size = size
        self.history = []
        self.service_end_time = float('infinity')
        self.packet_rejection_count = 0
        self.packet_arrival_count = 0

    def add(self, packet):
        if len(self.buffer) >= self.size:
            self.packet_rejection_count += 1
        self.buffer.append(packet)

    # パケットの出入りの履歴を更新する関数
    def update_history(self, event_time):
        self.history.append([len(self.buffer), event_time])

    def finish_service(self):
        self.buffer.pop(0)
        event_time = self.service_end_time
        if len(self.buffer) == 0:
            self.service_end_time = float('infinity')
        else:
            self.service_end_time += self.buffer[0]
        return event_time

    def arrival_packet(self, packet_arrival_time, arrival_packet_service_time, next_packet_arrival_time):
        self.packet_arrival_count += 1
        if len(self.buffer) == 0:
            self.service_end_time = packet_arrival_time + arrival_packet_service_time
        self.add(next_packet_arrival_time)


# 指数分布に従う乱数
def exponential_distribution_random(Lambda):
    return (-1 / Lambda) * math.log(1 - random.random())

# シミュレーションを行う関数
def simulation(count, bufferA, bufferB, lambda1=0.7, lambda2=1.1, p=0.4):

    # パケット到着時間
    packet_arrival_time = 0

    time = 0

    while bufferA.packet_arrival_count + bufferB.packet_arrival_count < count:
        if packet_arrival_time < bufferA.service_end_time and packet_arrival_time < bufferB.service_end_time:
            arrival_packet_service_time = exponential_distribution_random(lambda1)
            next_packet_arrival_time = exponential_distribution_random(lambda2)

            if random.random() < p:
                bufferA.arrival_packet(packet_arrival_time, arrival_packet_service_time, next_packet_arrival_time)

            else:
                bufferB.arrival_packet(packet_arrival_time, arrival_packet_service_time, next_packet_arrival_time)

            time = packet_arrival_time
            packet_arrival_time += next_packet_arrival_time

        elif bufferA.service_end_time < bufferB.service_end_time:
            time = bufferA.finish_service()

        else:
            time = bufferB.finish_service()
            
        bufferA.update_history(time)
        bufferB.update_history(time)

def calculation_average_system_packets(buffer_history):
    c = 0
    history = []
    counts = []
    while c < len(buffer_history) - 1:
        t = buffer_history[c+1][1] - buffer_history[c][1]
        history.append(t)
        counts.append(buffer_history[c][0])
        c += 1
    return sum(counts) / sum(history)

def calculation_average_system_delay(buffer_history, arrival_packets):
    c = 0
    st = []
    while c < len(buffer_history) - 1:
        t = buffer_history[c+1][1] - buffer_history[c][1]
        st.append(t * buffer_history[c][0])
        c += 1
    return sum(st) / (arrival_packets * buffer_history[-1][1])

def calculation_average_system_queue_delay(buffer_history, arrival_packets):
    c = 0
    st = []
    while c < len(buffer_history) - 1:
        t = buffer_history[c+1][1] - buffer_history[c][1]
        num = buffer_history[c][0] - 1 
        if num < 0:
            num = 0
        st.append(t * num)
        c += 1
    return sum(st) / (arrival_packets * buffer_history[-1][1])

def main():

    A = 10
    B = 20
    Count = 10 ** 6

    # BufferクラスからbufferAとbufferBを生成
    bufferA = Buffer(A)
    bufferB = Buffer(B)

    simulation(Count, bufferA, bufferB, 0.5, 1.1)

    print("""
    パケット到着数
    total:   {}
    bufferA: {}
    bufferB: {}""".format(
        bufferA.packet_arrival_count + bufferB.packet_arrival_count, 
        bufferA.packet_arrival_count, 
        bufferB.packet_arrival_count
        ))

    print("""
    パケット棄却率
    total:   {}
    bufferA: {}
    bufferB: {}
    """.format((
        bufferA.packet_rejection_count + bufferB.packet_rejection_count) / (bufferA.packet_arrival_count + bufferB.packet_arrival_count), 
        bufferA.packet_rejection_count/bufferA.packet_arrival_count, 
        bufferB.packet_rejection_count/bufferB.packet_arrival_count
        ))

    bufferA_average_packets = calculation_average_system_packets(bufferA.history)
    bufferB_average_packets = calculation_average_system_packets(bufferB.history)
    print("""
    平均システム内パケット数
    total:   {}
    bufferA: {}
    bufferB: {}""".format(
        bufferA_average_packets + bufferB_average_packets,
        bufferA_average_packets,
        bufferB_average_packets
        )) 

    print("""
    平均システム内遅延
    total:   {}
    bufferA: {}
    bufferB: {}""".format(
        calculation_average_system_delay(
            bufferA.history + bufferB.history, 
            bufferA.packet_arrival_count + bufferB.packet_arrival_count - bufferA.packet_rejection_count - bufferB.packet_rejection_count
            ),
        calculation_average_system_delay(bufferA.history, bufferA.packet_arrival_count - bufferA.packet_rejection_count),
        calculation_average_system_delay(bufferB.history, bufferB.packet_arrival_count - bufferB.packet_rejection_count)
        ))

    print("""
    平均システム内待ち行列遅延
    total:   {}
    bufferA: {}
    bufferB: {}
    """.format(
        calculation_average_system_queue_delay(
            bufferA.history + bufferB.history, 
            bufferA.packet_arrival_count + bufferB.packet_arrival_count - bufferA.packet_rejection_count - bufferB.packet_rejection_count
            ),
        calculation_average_system_queue_delay(bufferA.history, bufferA.packet_arrival_count - bufferA.packet_rejection_count),
        calculation_average_system_queue_delay(bufferB.history, bufferB.packet_arrival_count - bufferB.packet_rejection_count)
        ))

if __name__ == "__main__":
    main()
