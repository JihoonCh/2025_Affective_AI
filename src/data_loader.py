import random
import numpy as np
from tqdm import tqdm_notebook
from collections import defaultdict

import torch
import torch.nn as nn
from torch.nn.utils.rnn import pad_sequence, pack_padded_sequence, pad_packed_sequence
from torch.utils.data import DataLoader, Dataset
from transformers import RobertaTokenizer


from create_dataset import MOSI, MOSEI, UR_FUNNY, PAD, UNK


roberta_tokenizer = RobertaTokenizer.from_pretrained('roberta-base')


class MSADataset(Dataset):
    def __init__(self, config):

        ## Fetch dataset
        if "mosi" in str(config.data_dir).lower():
            dataset = MOSI(config)
        elif "mosei" in str(config.data_dir).lower():
            dataset = MOSEI(config)
        elif "ur_funny" in str(config.data_dir).lower():
            dataset = UR_FUNNY(config)
        else:
            print("Dataset not defined correctly")
            exit()
        
        self.data, self.word2id, self.pretrained_emb = dataset.get_data(config.mode)
        self.len = len(self.data)

        # print(self.data[0])

        config.visual_size = self.data[0][0][1].shape[1]
        config.acoustic_size = self.data[0][0][2].shape[1]

        config.word2id = self.word2id
        config.pretrained_emb = self.pretrained_emb


    def __getitem__(self, index):
        return self.data[index]

    def __len__(self):
        return self.len



def get_loader(config, shuffle=True):
    """Load DataLoader of given DialogDataset"""

    dataset = MSADataset(config)
    
    print(config.mode)
    config.data_len = len(dataset)


    def collate_fn(batch):
        '''
        Collate functions assume batch = [Dataset[i] for i in index_set]
        '''
        # for later use we sort the batch in descending order of length
        batch = sorted(batch, key=lambda x: x[0][0].shape[0], reverse=True)
        
        # get the data out of the batch - use pad sequence util functions from PyTorch to pad things


        labels = torch.cat([torch.from_numpy(sample[1]) for sample in batch], dim=0)
        sentences = pad_sequence([torch.LongTensor(sample[0][0]) for sample in batch], padding_value=PAD)
        visual = pad_sequence([torch.FloatTensor(sample[0][1]) for sample in batch])
        acoustic = pad_sequence([torch.FloatTensor(sample[0][2]) for sample in batch])

        ## BERT-based features input prep

        SENT_LEN = sentences.size(0)
        # Create bert indices using tokenizer

        roberta_details  = []
        for sample in batch:
            text = " ".join(sample[0][3])
            encoded_roberta_sent = roberta_tokenizer.encode_plus(
                text, max_length=SENT_LEN+2, add_special_tokens=True, padding='max_length', truncation=True)
            roberta_details.append(encoded_roberta_sent)


        # Bert things are batch_first
        roberta_sentences = torch.LongTensor([sample["input_ids"] for sample in roberta_details])
        roberta_sentence_att_mask = torch.LongTensor([sample["attention_mask"] for sample in roberta_details])

        # lengths are useful later in using RNNs
        lengths = torch.LongTensor([sample[0][0].shape[0] for sample in batch])

        return sentences, visual, acoustic, labels, lengths, roberta_sentences, roberta_sentence_att_mask

    data_loader = DataLoader(
        dataset=dataset,
        batch_size=config.batch_size,
        shuffle=shuffle,
        collate_fn=collate_fn)

    return data_loader
