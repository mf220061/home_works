#import matplotlib.pyplot as plt
import random, math

A = 15
B = 30

# このプログラムではとりあえず、全ての乱数発生は指数分布に基づいて行う

class Buffer:
    def __init__(self, N):
        """
        packets: バッファ内のパケット
        size: バッファの最大サイズ
        """
        self.packets = []
        self.size = N 

    def add(self, packet):
        # パケットの到着イベント
        # バッファの最大までパケットが存在していた場合は棄却される（Falseが返される）
        if len(self.packets) >= self.size:
            return 1
        self.packets.append(packet)
        return 0

class Packet:
    # このクラス要らない
    # やっぱり要るかも
    def __init__(self):
        """
        service: サービス時間（パケットサイズ）
        """
        self.service = exponential_distribution(0.7)


def avarage_packets(update_packets, event_time, target_buffer):
    update_packets.append([len(target_buffer.packets), event_time])
    return update_packets

def cal_avarage_packets(buffer_history):
    #print(len(buffer_history)) # ここの値は今回の到着パケット数の大体2倍くらいの値になる
    #print(buffer_history[:10])
    c = 0
    history = []
    counts = []
    while c < len(buffer_history) - 1:
        t = buffer_history[c+1][1] - buffer_history[c][1]
        history.append(t)
        counts.append(buffer_history[c][0])
        c += 1
    return sum(counts) / sum(history)

def exponential_distribution(Lambda):
    return (-1 / Lambda) * math.log(1 - random.random())


def main():
    # ここら辺の変数名をもう少し整理したほうがいいかも
    # 平均サービス時間を求めるために変数を追加する必要がある
    # また、下記のバッファの処理の部分はAとBで重なる部分が多いので、関数化する

    # t1は次のパケットの到着時間
    # t2aはバッファaのサービス中のパケットのサービス終了時間
    # t2bはバッファbのサービス中のパケットのサービス終了時間
    t1 = 0
    t2a = float('infinity')
    t2b = float('infinity')

    # caはバッファaの棄却数
    # cbはバッファbの棄却数
    ca = 0
    cb = 0

    # cは到着パケット数
    c1 = 0
    c1a = 0
    c1b = 0
    bufferA = Buffer(A)
    bufferB = Buffer(B)

    bufferA_packets_history = []
    bufferB_packets_history = []

    while c1 < 10**5:
        if t1 < t2a and t1 < t2b:
            bufferA_packets_history = avarage_packets(bufferA_packets_history, t1, bufferA)
            bufferB_packets_history = avarage_packets(bufferB_packets_history, t1, bufferB)
            # パケットが到着した
            # 平均到着率はexponential_distribution関数の引数の逆数：つまり1/1で1
            td = exponential_distribution(1)
            packet = Packet()
            # とりあえず、並列でやることにする
            if random.random() < 0.45:
                # 到着したパケットはバッファAに入った
                c1a += 1
                if len(bufferA.packets) == 0:
                    bufferA.add(packet)
                    t2a = t1 + bufferA.packets[0].service
                else:
                    ca += bufferA.add(packet)
            else:
                # 到着したパケットはバッファBに入った
                c1b += 1
                if len(bufferB.packets) == 0:
                    bufferB.add(packet)
                    t2b = t1 + bufferB.packets[0].service
                else:
                    cb += bufferB.add(packet)
            t1 += td
            c1 += 1

        elif t2a < t2b:
            bufferA_packets_history = avarage_packets(bufferA_packets_history, t2a, bufferA)
            bufferB_packets_history = avarage_packets(bufferB_packets_history, t2a, bufferB)
            # バッファAのパケットのサービス時間が満了した
            bufferA.packets.pop(0)
            if len(bufferA.packets) == 0:
                t2a = float('infinity')
            else:
                t2a += bufferA.packets[0].service
        else:
            bufferA_packets_history = avarage_packets(bufferA_packets_history, t2b, bufferA)
            bufferB_packets_history = avarage_packets(bufferB_packets_history, t2b, bufferB)
            # バッファBのパケットのサービス時間が満了した
            bufferB.packets.pop(0)
            if len(bufferB.packets) == 0:
                t2b = float('infinity')
            else:
                t2b += bufferB.packets[0].service

    # 現在は平均棄却率しか求めていないが、平均システム内パケット数、平均システム内遅延、平均システム内待ち行列遅延、なども求める必要がある
    # それぞれの求め方を適当に考える。
    # もしかしたら具体的な数値による計算ではなく、待ち行列理論による計算でもいいのかもしれないが、今回の場合だと数値で求めることが可能なので、実際に計算したほうがよさそう

    # 平均システム内パケット数
    #  これはイベントが発生した時のバッファ内パケット数を数えるしかなさそう

    # 平均システム内遅延
    #  多分、パケットごとにシステム内にいた時間を考える必要がある。
    #  もしかしたら、Packetクラスが役に立つかも。
    #  PacketよりもPacketを管理するバッファで計算するべきな気がする。
    #  計算にかなり時間がかかりそう

    # 平均システム内待ち行列遅延
    #  上記の平均システム内遅延との違いがよくわからないが、
    #  違いとしては、待ち行列とシステムというところかも。
    #  具体的には、上記は出力リンクでの処理の時間も含めるが
    #  こちらはバッファに入ってから出力リンクに入るまでの時間を考えるのかも

    #  ただし、想像でしかないので、質問するべきかも

    print("""パケット到着数
total:   {}
bufferA: {}
bufferB: {}
""".format(c1, c1a, c1b))

    print("""パケット棄却率
total:   {}
bufferA: {}
bufferB: {}
""".format((ca+cb)/c1, ca/c1a, cb/c1b))

    print("""サービス時間
total:   {}
bufferA: {}
bufferB: {}
""".format(t1, None, None)) 
    # これはまじで意味のない表示
    # サービス時間が平均と一致するかを確認しただけ

    aa = cal_avarage_packets(bufferA_packets_history)
    ab = cal_avarage_packets(bufferB_packets_history)
    print("""平均システム内パケット数
total:   {}
bufferA: {}
bufferB: {}
""".format(aa+ab, aa, ab)) 

    print("""平均システム内遅延
total:   {}
bufferA: {}
bufferB: {}
""".format(t1, None, None)) 

    print("""平均システム内待ち行列遅延
total:   {}
bufferA: {}
bufferB: {}
""".format(t1, None, None)) 
            
if __name__ == "__main__":
    main()
