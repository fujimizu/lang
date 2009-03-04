"""
�˥塼���ͥåȥ���θ������ť�ǥ�

 11/01 pickle �Ǥʤ��� weight_* �� train_* ����Ȥ���¸����ʤ�������?

 10/22 sigmod_table ��Ȥ�ʤ��褦���ѹ�
       �����Ȥ������椫��ؽ����ʤޤʤ��ʤ뤫��
"""

__author__ = "mfujisa"


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

    # ���
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

        # sigmoid �ơ��֥�κ���
#        self.sigmoid_table = self._make_sigmoid_table()

        # �Ť߽���ͤ����� (-2��2)
        for i in range(self.num_input+1):
            self.weight_ih.append([4 * random.randint(0, self.RAND_MAX) / \
                                   self.RAND_MAX -2 \
                                   for j in range(self.num_hidden)])
        
        for i in range(self.num_hidden+1):
            self.weight_ho.append([4 * random.randint(0, self.RAND_MAX) / \
                                   self.RAND_MAX -2 \
                                   for j in range(self.num_output)])

    def _make_sigmoid_table(self):
        """sigmoid �ơ��֥�κ���"""
        table = []
        for i in range(self.TABLE_SIZE):
            table.append(self._sigmoid((i - self.TABLE_SIZE / 2) \
                                       * 0.2, self.gain))
        return table

    def calc(self, input):
        """�ͥåȥ���ν��Ϥ��֤����ؽ���˻��Ѥ��롥"""
        self._forward(input)
        return self.net_output

    def learn(self):
        print "�ؽ���������!"
        for ilearn in range(self.num_learn):
            self.max_error = 0
            
            for isample in range(self.num_sample):
                self._forward(self.train_input[isample])
                self._eval_error(ilearn, isample)
                self._back(self.train_output[isample])

            # ���顼Ψ�����Ͱʲ��ˤʤä��齪λ
            if (self.max_error < self.ERROR_THRESHOLD):
                print "�ؽ���� = %d �ǽ�λ" % ilearn
                print "���票�顼Ψ = %f" % self.max_error
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
        self.net_input.append(1.0)  # ������

        ## �����ؤ�������ؤ�
        ltmp = []
        for j in range(self.num_hidden):
            sum = 0
            for i in range(self.num_input+1):
                sum = sum + self.weight_ih[i][j] * self.net_input[i]
#            ltmp.append(lookup_table(sum))
            ltmp.append(self._sigmoid(sum, self.gain))
        self.hidden = ltmp
        self.hidden.append(1.0)  # ������

        ## ����ؤ�������ؤ�
        ltmp = []
        for j in range(self.num_output):
            sum = 0
            for i in range(self.num_hidden+1):
                sum = sum + self.weight_ho[i][j] * self.hidden[i]
#            ltmp.append(lookup_table(sum))
            ltmp.append(self._sigmoid(sum, self.gain))
        self.net_output = ltmp

    def _eval_error(self, ilearn, isample):
        # ����ɾ��
        error = 0
        for j in range(self.num_output):
            error = error + \
                    (self.train_output[isample][j] - self.net_output[j]) * \
                    (self.train_output[isample][j] - self.net_output[j])
        error = float(error) / float(self.num_output)

        if (self.print_frequency != 0) and \
           (ilearn % self.print_frequency == 0):
            print "�ؽ���� = %d, �����ǡ���NO. = %d, �� = %f" % \
                  (ilearn, isample+1, error)
        if (error > self.max_error):
            self.max_error = error

    def _back(self, toutput):
        # �������ǻҤε�����
        output_back = [self.gain *
                       (self.net_output[j] - toutput[j]) * 
                       (1.0 - self.net_output[j]) * self.net_output[j] 
                       for j in range(self.num_output)]
            
        # �������ǻҤε�����
        ltmp = []
        for i in range(self.num_hidden):
            sum = 0
            for j in range(self.num_output):
                sum = sum + self.weight_ho[i][j] * output_back[j]
            ltmp.append(self.gain * sum * (1.0 - self.hidden[i])
                        * self.hidden[i])
        hidden_back = ltmp

        # �Ťߤν���
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
        print "�����ǡ���:"
        for i in range(len(self.train_input)):
            print "����: ",
            print self.train_input[i],
            print "����: ",
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
    """�Ťߤ���¸�Ǥ��ʤ��Τǡ��̡��˥��ɤ���Τ����ݡ�
    �ʤΤǤ���ǰ쵤�˥��ɤ����ޤ�!"""

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
        print "����:",
        print input,
        print "����:",
        print bp.calc(input)

#    bp.save("example/test.bp")

def main():
    test()
    
if __name__ == "__main__":
    main()
    
