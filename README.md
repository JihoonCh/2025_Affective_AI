# Decoupled Fusion Strategy: Cross-Attention for Private Modality Representations in Sentiment Analysis


![d392f005f037c515a88c9ada65de278608f9062e](https://github.com/user-attachments/assets/7a1fec91-c76d-4c46-8c11-bab88b970b7f)


### Setup the environment

We work with a conda environment.

```
conda env create -f environment.yml
conda activate misa-code
```

### Data Download

- Install [CMU Multimodal SDK](https://github.com/A2Zadeh/CMU-MultimodalSDK). Ensure, you can perform ```from mmsdk import mmdatasdk```.    
- Option 1: Download [pre-computed splits](https://drive.google.com/drive/folders/1IBwWNH0XjPnZWaAlP1U2tIJH6Rb3noMI?usp=sharing) and place the contents inside ```datasets``` folder.     
- Option 2: Re-create splits by downloading data from MMSDK. For this, simply run the code as detailed next.

### Running the code

1. ```cd src```
2. Set ```word_emb_path``` in ```config.py``` to [glove file](http://nlp.stanford.edu/data/glove.840B.300d.zip).
3. Set ```sdk_dir``` to the path of CMU-MultimodalSDK.
2. ```python train.py --data mosei```. Replace ```mosei``` with ```mosi```  for other datasets.

