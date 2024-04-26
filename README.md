# A Tulu Resource for Machine Translation

## Overview

We present an *English*-*Tulu* machine translation model developed using a transfer learning approach that exploits similarities between high-resource and low-resource languages. This model and its training approach is heavily inspired from [NMT-Adapt](https://github.com/wjko2/NMT-Adapt) and the findings of the associated [paper](https://aclanthology.org/2021.acl-long.66/).

We also present the first parallel dataset for *English*-*Tulu* translation. Our dataset is constructed by integrating human translations into the multilingual machine translation resource FLORES-200. We use this dataset for evaluating our translation model.

[*Tulu*](https://en.wikipedia.org/wiki/Tulu_language) ([*Tcy*](https://www.ethnologue.com/language/tcy/)), classified within the South Dravidian linguistic family branch, is predominantly spoken by approximately 2.5 million individuals in southwestern India. We use [*Kannada*](https://en.wikipedia.org/wiki/Kannada) ([*Kan*](https://www.ethnologue.com/language/kan/)) as a closely related high-resource language for the transfer learning approach.

For more details, see our [paper](https://arxiv.org/abs/2403.19142).

## Requirements



## Dataset

### Training datasets

*En-Kan* parallel: [Samanantar](https://ai4bharat.iitm.ac.in//samanantar/)

Tcy monolingual: Sentences extracted from 1894 articles on the [Tulu Wikipedia](https://tcy.wikipedia.org) archived [here](https://dumps.wikimedia.org/tcywiki/latest/) using [wikiextractor](https://github.com/attardi/wikiextractor).

En-Tcy test dataset: 1300 sentences in English and Tulu, created by us from the 2009 publicly available sentences in the [FLORES-200](https://github.com/openlanguagedata/flores) benchmark. _This is an ongoing project._

## Model Training

Pre-trained model: [IndicBARTSS](https://huggingface.co/ai4bharat/IndicBARTSS)
Tokenizer: AlbertTokenizer

[YANMTT](https://github.com/prajdabre/yanmtt) was used to follow an iterative training procedure based on [NMT-Adapt](https://github.com/wjko2/NMT-Adapt) as laid out in our paper.

### Task 1:

Fine-tune the _IndicBARTSS_ model in *Kan*-*En* direction using the parallel training dataset, forming the base model for *Tcy*-*En* translation.

### Task 2:

Fine-tune a second _IndicBARTSS_ model with backtranslated data of *Tcy* sentences in the monolingual dataset using the model from _Task 1_, forming the base model for *En*-*Tcy* translation.

### Task 3:

Fine-tune the model from _Task 2_ using *En*-*Kan* from the parallel dataset.

### Task 4:

Denoising autoencoding step using *noised* sentences prepared from the monolingual *Tcy* dataset and the *Kan* training dataset by random shuffling and masking of words.

### Task 5:

FInetune the *En*-*Tcy* model from _Task 4_ with back-translated pairs. This model is the used to generate the *En* side of the back-translated pairs, and this data is then used to repeat _Task 2_ to _Task 5_ on the *Tcy*-*En* base model from *Task 1*.

## Evaluation

Evaluation was done using [*sacreBLEU*](https://github.com/mjpost/sacrebleu) scores.

## Model Adaptation



## Results



## Usage Examples



## Acknowledgements



## References



## Contact



