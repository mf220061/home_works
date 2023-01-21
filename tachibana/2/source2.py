# 通信システムのモンテカルロシミュレーション評価

import random, math

# バッファクラス
class Buffer:
    def __init__(self, size):
        self.buffer = []                            # バッファの内部（このリストの0番目を出力リンクとして考える）
        self.size = size                            # バッファサイズ（出力リンク込み）
        self.history = []                           # パケットの出入りの履歴
        self.service_end_time = float('infinity')   # 出力リンクのパケットのサービス時間（出力リンクにパケットがないときは無限）
        self.packet_rejection_count = 0             # パケットが棄却された数
        self.packet_arrival_count = 0               # バッファに到着したパケットの数

    # バッファにパケット追加
    def add(self, packet):
        if len(self.buffer) >= self.size:
            self.packet_rejection_count += 1
        self.buffer.append(packet)

    # パケットの出入りの履歴を更新する関数
    def update_history(self, event_time):
        self.history.append([len(self.buffer), event_time])

    # 出力リンク中のパケットのサービスが終了
    def finish_service(self):
        self.buffer.pop(0)
        event_time = self.service_end_time
        if len(self.buffer) == 0:
            self.service_end_time = float('infinity')
        else:
            self.service_end_time += self.buffer[0]
        return event_time

    # バッファにパケットが到着
    def arrival_packet(self, packet_arrival_time, arrival_packet_service_time, next_packet_arrival_time):
        self.packet_arrival_count += 1
        if len(self.buffer) == 0:
            self.service_end_time = packet_arrival_time + arrival_packet_service_time
        self.add(next_packet_arrival_time)


# 指数分布に従う乱数
def exponential_distribution_random(Lambda):
    return (-1 / Lambda) * math.log(1 - random.random())

# シミュレーションを行う関数
def simulation(count, bufferB, lambda1=0.7, lambda2=1.1):

    # パケット到着時間
    packet_arrival_time = 0

    time = 0

    while bufferB.packet_arrival_count < count:
        if packet_arrival_time < bufferB.service_end_time:

            # 到着したパケットのサービス時間
            arrival_packet_service_time = exponential_distribution_random(lambda1)

            # 次のパケットが到着するまでの時間
            next_packet_arrival_time = exponential_distribution_random(lambda2)

            bufferB.arrival_packet(packet_arrival_time, arrival_packet_service_time, next_packet_arrival_time)

            time = packet_arrival_time
            packet_arrival_time += next_packet_arrival_time

        else:
            time = bufferB.finish_service()
            
        bufferB.update_history(time)

# 平均システム内パケット数の計算
def calculation_average_system_packets(buffer_history):
    c = 0
    st = []
    while c < len(buffer_history) - 1:
        t = buffer_history[c+1][1] - buffer_history[c][1]
        st.append(t * buffer_history[c][0])
        c += 1
    return sum(st) / buffer_history[-1][1]

# 平均システム内遅延の計算
def calculation_average_system_delay(buffer_history, arrival_packets):
    c = 0
    st = []
    while c < len(buffer_history) - 1:
        t = buffer_history[c+1][1] - buffer_history[c][1]
        st.append(t * buffer_history[c][0])
        c += 1
    return sum(st) / arrival_packets

# 平均システム内待ち行列遅延の計算
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
    return sum(st) / arrival_packets

def main():

    B = 20
    Count = 10 ** 5

    # BufferクラスからbufferAとbufferBを生成
    bufferB = Buffer(B)

    simulation(Count, bufferB, 0.3, 1.1)

    print("""
    パケット到着数
    total:   {}
    """.format(
        bufferB.packet_arrival_count
        ))

    print("""
    パケット棄却率
    total:   {}
    """.format(
        bufferB.packet_rejection_count/bufferB.packet_arrival_count
        ))

    bufferB_average_packets = calculation_average_system_packets(bufferB.history)
    print("""
    平均システム内パケット数
    total:   {}
    """.format(
        bufferB_average_packets
        )) 

    total_history = [[bufferB.history[i][0], bufferB.history[i][1]] for i in range(len(bufferB.history))]
    print("""
    平均システム内遅延
    total:   {}
    """.format(
        calculation_average_system_delay(bufferB.history, bufferB.packet_arrival_count - bufferB.packet_rejection_count)
        ))

    print("""
    平均システム内待ち行列遅延
    total:   {}
    """.format(
        calculation_average_system_queue_delay(bufferB.history, bufferB.packet_arrival_count - bufferB.packet_rejection_count)
        ))

if __name__ == "__main__":
    main()
