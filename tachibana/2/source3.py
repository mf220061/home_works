import random, math

class System:
    def __init__(self, N):
        self.queue              = []
        self.size               = N
        self.history            = []            # 正直、適切では無い気がするが、別の方法を考えるのも面倒なので、とりあえずそのままにする
        self.service_end_time   = float('inf')
        self.rejection_count    = 0
        self.arrival_count      = 0

    def add(self, packet):
        if len(self.queue) >= self.size:
            self.rejection_count += 1
        else:
            self.queue.append(packet)

    def update(self, time):
        self.history.append([len(self.queue), time])

    def finish(self):
        self.queue.pop(0)
        time = self.service_end_time
        if len(self.queue) == 0:
            self.service_end_time = float('inf')
        else:
            self.service_end_time += self.queue[0]
        return time

    def arrive(self, arrival_time, service_time):
        self.arrival_count += 1
        if len(self.queue) == 0:
            self.service_end_time = arrival_time + service_time
        self.add(service_time)


def exponential_distribution_random(L):
    return (-1 / L) * math.log(1 - random.random())

def simulation(count, system, L, M):
    arrival_time = exponential_distribution_random(L)
    while system.arrival_count < count:
        if arrival_time < system.service_end_time:
            service_time = exponential_distribution_random(M)
            system.arrive(arrival_time, service_time)
            system.update(arrival_time)
            arrival_time += exponential_distribution_random(L)
        else:
            system.update(system.finish())

# 平均システム内パケット数の計算
def calculation_average_system_packets(history):
    c = 0
    st = []
    while c < len(history) - 1:
        t = history[c+1][1] - history[c][1]
        st.append(t * history[c][0])
        c += 1
    return sum(st) / history[-1][1]

# 平均システム内遅延の計算
def calculation_average_system_delay(history, arrival_packets):
    c = 0
    st = []
    while c < len(history) - 1:
        t = history[c+1][1] - history[c][1]
        st.append(t * history[c][0])
        c += 1
    return sum(st) / arrival_packets

# 平均システム内待ち行列遅延の計算
def calculation_average_system_queue_delay(history, arrival_packets):
    c = 0
    st = []
    while c < len(history) - 1:
        t = history[c+1][1] - history[c][1]
        num = history[c][0] - 1 
        if num < 0:
            num = 0
        st.append(t * num)
        c += 1
    return sum(st) / arrival_packets

def main():
    K = 20
    count = 10 ** 6 # あとで変更する必要がある
    system = System(K)
    simulation(count, system, 0.3, 1.0)

    print("""
    パケット到着数
    total:   {}
    """.format(
        system.arrival_count
        ))

    print("""
    パケット棄却率
    total:   {}
    """.format(
        system.rejection_count / system.arrival_count
        ))

    average_packets = calculation_average_system_packets(system.history)
    print("""
    平均システム内パケット数
    total:   {}
    """.format(
        average_packets
        )) 

    total_history = [[system.history[i][0], system.history[i][1]] for i in range(len(system.history))]
    print("""
    平均システム内遅延
    total:   {}
    """.format(
        calculation_average_system_delay(system.history, system.arrival_count - system.rejection_count)
        ))

    print("""
    平均システム内待ち行列遅延
    total:   {}
    """.format(
        calculation_average_system_queue_delay(system.history, system.arrival_count - system.rejection_count)
        ))

if __name__ == "__main__":
    main()
