#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
ニューラルネットワークの誤差逆伝播モデル

 11/01 pickle でなぜか weight_* と train_* の中身が保存されない．何で?

 10/22 sigmod_table を使わないように変更
       これを使うと途中から学習が進まなくなるから
"""

__author__ = "mjmania"

import string
import random
import pickle
from math import exp

class BPNNetwork:
    weight_ih = []
    weight_ho = []
    train_input = []
    train_output = []

    net_input = []
    net_output = []
    hidden = []

    sigmoid_table = []

    max_error = 0

    print_frequency = 0

    # 定数
    TABLE_SIZE = 100
    RAND_MAX = 100
    ERROR_THRESHOLD = 0.01
    EPSILON = 0.05

    def __str__(self):
        f = lambda x: str(x) + ", "
        
        return "weight_ih:" + ''.join(map(f, self.weight_ih)) + "\n" + \
               "weight_ho:" + ''.join(map(f, self.weight_ho)) + "\n" + \
               "train_input:" + ''.join(map(f, self.train_input)) + "\n" + \
               "train_output:" + ''.join(map(f, self.train_output))

    def __init__(self, num_learn, num_input, num_hidden,
                 num_output, gain):
        self.num_learn = num_learn
        self.num_input = num_input
        self.num_hidden = num_hidden
        self.num_output = num_output
        self.gain = gain

        # sigmoid テーブルの作成
#        self.sigmoid_table = self._make_sigmoid_table()

        # 重み初期値の設定 (-2〜2)
        for i in range(self.num_input+1):
            self.weight_ih.append([4 * random.randint(0, self.RAND_MAX) / \
                                   self.RAND_MAX -2 \
                                   for j in range(self.num_hidden)])
        
        for i in range(self.num_hidden+1):
            self.weight_ho.append([4 * random.randint(0, self.RAND_MAX) / \
                                   self.RAND_MAX -2 \
                                   for j in range(self.num_output)])

    def _make_sigmoid_table(self):
        """sigmoid テーブルの作成"""
        table = []
        for i in range(self.TABLE_SIZE):
            table.append(self._sigmoid((i - self.TABLE_SIZE / 2) \
                                       * 0.2, self.gain))
        return table

    def calc(self, input):
        """ネットワークの出力を返す．学習後に使用する．"""
        self._forward(input)
        return self.net_output

    def learn(self):
        print "学習スタート!"
        for ilearn in range(self.num_learn):
            self.max_error = 0
            
            for isample in range(self.num_sample):
                self._forward(self.train_input[isample])
                self._eval_error(ilearn, isample)
                self._back(self.train_output[isample])

            # エラー率が閾値以下になったら終了
            if (self.max_error < self.ERROR_THRESHOLD):
                print "学習回数 = %d で終了" % ilearn
                print "最大エラー率 = %f" % self.max_error
                break

    def _sigmoid(self, x, gain):
        return 1.0 / (1.0 + exp(- gain * x))

    def _forward(self, input):
        def lookup_table(x):
            isum = int(sum * 5) + self.TABLE_SIZE / 2
            if (isum > self.TABLE_SIZE - 1):
                isum = self.TABLE_SIZE - 1
            elif (isum < 0):
                isum = 0
            return self.sigmoid_table[isum]

        self.net_input = input[:]
        self.net_input.append(1.0)  # 閾値用

        ## 入力層から中間層へ
        ltmp = []
        for j in range(self.num_hidden):
            sum = 0
            for i in range(self.num_input+1):
                sum = sum + self.weight_ih[i][j] * self.net_input[i]
#            ltmp.append(lookup_table(sum))
            ltmp.append(self._sigmoid(sum, self.gain))
        self.hidden = ltmp
        self.hidden.append(1.0)  # 閾値用

        ## 中間層から出力層へ
        ltmp = []
        for j in range(self.num_output):
            sum = 0
            for i in range(self.num_hidden+1):
                sum = sum + self.weight_ho[i][j] * self.hidden[i]
#            ltmp.append(lookup_table(sum))
            ltmp.append(self._sigmoid(sum, self.gain))
        self.net_output = ltmp

    def _eval_error(self, ilearn, isample):
        # 誤差の評価
        error = 0
        for j in range(self.num_output):
            error = error + \
                    (self.train_output[isample][j] - self.net_output[j]) * \
                    (self.train_output[isample][j] - self.net_output[j])
        error = float(error) / float(self.num_output)

        if (self.print_frequency != 0) and \
           (ilearn % self.print_frequency == 0):
            print "学習回数 = %d, 訓練データNO. = %d, 誤差 = %f" % \
                  (ilearn, isample+1, error)
        if (error > self.max_error):
            self.max_error = error

    def _back(self, toutput):
        # 出力層素子の逆伝播
        output_back = [self.gain *
                       (self.net_output[j] - toutput[j]) * 
                       (1.0 - self.net_output[j]) * self.net_output[j] 
                       for j in range(self.num_output)]
            
        # 隠れ層素子の逆伝播
        ltmp = []
        for i in range(self.num_hidden):
            sum = 0
            for j in range(self.num_output):
                sum = sum + self.weight_ho[i][j] * output_back[j]
            ltmp.append(self.gain * sum * (1.0 - self.hidden[i])
                        * self.hidden[i])
        hidden_back = ltmp

        # 重みの修正
        for i in range(self.num_input+1):
            for j in range(self.num_hidden):
                self.weight_ih[i][j] = self.weight_ih[i][j] - \
                                       self.EPSILON * \
                                       self.net_input[i] * hidden_back[j]
        for i in range(self.num_hidden+1):
            for j in range(self.num_output):
                self.weight_ho[i][j] = self.weight_ho[i][j] - \
                                       self.EPSILON * self.hidden[i] *\
                                       output_back[j]
                
    def set_train_data(self, data):
        self.num_sample = 0
        for datum in data:
            self.train_input.append(datum[:self.num_input][:])
            self.train_output.append(datum[self.num_input:
                                          self.num_input+self.num_output][:])
            self.num_sample = self.num_sample + 1

        for i in range(len(self.train_input)):
            self.train_input[i] = map(int, self.train_input[i])
        for i in range(len(self.train_output)):
            self.train_output[i] = map(int, self.train_output[i])
            
    def open_data_file(self, filename):
        f = open(filename, 'r')
        data = []
        for l in f.readlines():
            lst = string.split(l)
            data.append(lst)
        self.set_train_data(data)

    def print_train_data(self):
        print "訓練データ:"
        for i in range(len(self.train_input)):
            print "入力: ",
            print self.train_input[i],
            print "出力: ",
            print self.train_output[i]
        print

    def set_print_frequency(self, frequency):
        self.print_frequency = frequency

    def save(self, filename):
        f = open(filename, 'w+')
        pickle.dump(self, f)
        f.close()

        self._save_weight(filename)

    def _save_weight(self, filename):
        f = open(filename + "_w_ih", 'w')
        pickle.dump(self.weight_ih, f)
        f.close()
        
        f = open(filename + "_w_ho", 'w')
        pickle.dump(self.weight_ho, f)
        f.close()

    def set_weight(self, w_ih, w_ho):
        self.weight_ih = w_ih
        self.weight_ho = w_ho


def restore(filename):
    """重みが保存できないので，別々にロードするのが面倒．
    なのでこれで一気にロードしちまえ!"""

    file = open(filename)
    bp = pickle.load(file)
    file.close()

    f = open(filename + "_w_ih")
    w_ih = pickle.load(f)
    f.close()
    
    f = open(filename + "_w_ho")
    w_ho = pickle.load(f)
    f.close()

    bp.set_weight(w_ih, w_ho)
    return bp

def test():
    bp = BPNNetwork(1000, 3, 5, 1, 1.0)

    bp.open_data_file("example/training.dat")
    bp.print_train_data()
    bp.learn()

    inputs = [[0, 1, 0], [0, 1, 1]]
    for input in inputs:
        print "入力:",
        print input,
        print "出力:",
        print bp.calc(input)

#    bp.save("example/test.bp")

def main():
    test()
    
if __name__ == "__main__":
    main()
    
