import torch
from lightwood.encoders.text.helpers.rnn_helpers import Lang
import numpy as np


UNCOMMON_WORD = '<UNCOMMON>'
UNCOMMON_TOKEN = 0

class CategoricalEncoder:

    def __init__(self, is_target = False):
        self._lang = None
        self._pytorch_wrapper = torch.FloatTensor
        self._prepared = False

    def prepare_encoder(self, priming_data):
        print('\n\n')
        print(priming_data)
        print('\n\n')
        if self._prepared:
            raise Exception('You can only call "prepare_encoder" once for a given encoder.')

        self._lang = Lang('default')
        self._lang.index2word = {UNCOMMON_TOKEN: UNCOMMON_WORD}
        self._lang.word2index = {UNCOMMON_WORD: UNCOMMON_TOKEN}
        self._lang.word2count[UNCOMMON_WORD] = 0
        self._lang.n_words = 1
        for category in priming_data:
            if category != None:
                self._lang.addWord(str(category))

        self._prepared = True

    def encode(self, column_data):
        if not self._prepared:
            raise Exception('You need to call "prepare_encoder" before calling "encode" or "decode".')
        print(column_data)
        ret = []
        v_len = self._lang.n_words

        for word in column_data:
            encoded_word = [0]*v_len
            if word != None:
                word = str(word)
                index = self._lang.word2index[word] if word in self._lang.word2index else UNCOMMON_TOKEN
                encoded_word[index] = 1

            ret.append(encoded_word)
        print(ret)
        print(self.decode(ret))
        exit()
        return self._pytorch_wrapper(ret)


    def decode(self, encoded_data):
        encoded_data_list = encoded_data.tolist()
        ret = []

        for vector in encoded_data_list:
            ohe_index = np.argmax(vector)

            ret.append(self._lang.index2word[ohe_index])
        return ret


if __name__ == "__main__":

    data = ['category 1', 'category 3', 'category 4', None]

    enc = CategoricalEncoder()

    enc.fit(data)
    encoded_data = enc.encode(data)
    decoded_data = enc.decode(enc.encode(['category 2', 'category 1', 'category 3', None]))

    assert(len(encoded_data) == 4)
    assert(decoded_data[1] == 'category 1')
    assert(decoded_data[2] == 'category 3')
    for i in [0,3]:
        assert(encoded_data[0][i] == UNCOMMON_TOKEN)
        assert(decoded_data[i] == UNCOMMON_WORD)

    print(f'Encoded values: \n{encoded_data}')
    print(f'Decoded values: \n{decoded_data}')
