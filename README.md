# LLMs for working data scientists and machine learning practitioners

Large Language Models(LLM) are changing the landscape of data science - whether this represents a paradigm shift in the way information is produced, aggregated and consumed, or this is just another
passing fad, the jury is still out. In any case, AI/LLM as a tool, increasingly an indispensable one, is becoming the accepted norm, especially among programmers and data scientists.

This collection of notes is basically a brain dump for me - it captures my personal learnings to make sense of this exploding field and try to keep myself sane.

# Table of Contents

- [History](#history)
- [Fundamentals](#fundamental)
- [Closed Foundation Models](#closed-foundation-models)
- [Open Foundation Models](#open-foundation-models)
- [Frameworks and Ecosystems](#frameworks-and-ecosystems)
- [FAQs](#faqs)

---

## History

These are the important milestones leading up to the current state of LLM.

- Transformer:
    * THE transformer paper: [Attention Is All You Need](https://arxiv.org/pdf/1706.03762.pdf)
    * A detailed anatomy of transfomer : [Transformer from scratch](https://e2eml.school/transformers.html)
    * The python implementation of the original transformer: [The annotated transformer](http://nlp.seas.harvard.edu/annotated-transformer/)

- The Zoo of LLMs
    * [An overview and hitory of LLMs:](https://arxiv.org/abs/2302.09419)
    * [List of transfomers: ](https://github.com/abacaj/awesome-transformers)
    * [A catalog of transfomer models](https://arxiv.org/pdf/2302.07730.pdf)

- GPT style decoder only models
    * GPT 1.0: [Improving Language Understanding by Generative Pre-Training](https://www.cs.ubc.ca/~amuham01/LING530/papers/radford2018improving.pdf)
    * GPT 2.0: [Language Models are Unsupervised Multitask Learners](https://d4mucfpksywv.cloudfront.net/better-language-models/language_models_are_unsupervised_multitask_learners.pdf)
    * GPT 3.0: [Language models are few-shot learners](https://papers.nips.cc/paper/2020/file/1457c0d6bfcb4967418bfb8ac142f64a-Paper.pdf)
    * GPT 4: [GPT-4 Technical Report](https://openai.com/research/gpt-4)
    * [Kaparthy's NanoGPT Impementation](https://github.com/karpathy/nanoGPT)

- Bert style encoder only models 
    * BERT: [BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding](https://aclanthology.org/N19-1423.pdf)

- T5 style encoder-decoder models 
    * T5: [Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer](https://jmlr.org/papers/v21/20-074.html)
    * T0: [Multitask Prompted Training Enables Zero-Shot Task Generalization](https://arxiv.org/abs/2110.08207)

- "Making it bigger" - scaling and emergent properties
   * Scaling Law: [Scaling Laws for Neural Language Models](https://arxiv.org/pdf/2001.08361.pdf)   
   * Switch Transformers: [Switch Transformers: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity](https://arxiv.org/pdf/2101.03961.pdf)
   * Chinchilla: [An empirical analysis of compute-optimal large language model training](https://www.deepmind.com/publications/an-empirical-analysis-of-compute-optimal-large-language-model-training)
   * Emergent Abilities: [Emergent Abilities of Large Language Models](https://openreview.net/pdf?id=yzkSU5zdwD)

- Instruction finetuning and alignment
    * InstructGPT: [Training language models to follow instructions with human feedback](https://arxiv.org/pdf/2203.02155.pdf)
    * Flan-T5/PaLM: [Scaling Instruction-Finetuned Language Models](https://arxiv.org/pdf/2210.11416.pdf)
    * FLAN:  [Finetuned Language Models are Zero-Shot Learners](https://openreview.net/forum?id=gEZrGCozdqR)

- The birth of ChatGPT: the cambrian explosion started from here: Nov 2022

- The race to catch up with ChartGPT in the open source community
   * LLaMA: [LLaMA: Open and Efficient Foundation Language Models](https://research.facebook.com/publications/llama-open-and-efficient-foundation-language-models/)

## Prerequisites

The field is moving so fast you absolutely need a hacker's mentality

- Python/Numpy/Pandas: basic skills needed to code up something quickly. Fortunately with tools like copilot/ChatGPT/Replit, it's quite easy to get up to speed quickly in this department, especially you
are a programmer. For instance I came from a C++/R/Haskell background, and made a switch from R to Python
quite smoothly.

- Torch: Most transformer models are in torch. Invest some time to get you comfortable with both the tensor
library and building blocks for neural networks.

- Git and github: You will clone a tons of repos to experiment, so invest some time in building your own commands to quickly get things done.

- Huggingface ecosystem: this is a must now. Not just the `transformers` library itself, but also `peft`, 
`accelerate`, etc.

- Linux, bash, and command line tools: Get a mac and get comfortable with command lines tools. Trust me it is worth your time.

## Fundamentals

- Pre-training
- Common datasets for pre-training
- Fine-tuning
- Common datasets for fine-tuning
    * Apalca: generated from ChatGPT
    * Wizard(Evol-instruct from microsoft) : WizardLM/WizardLM_evol_instruct_V2_196k
    * Vicuna(From sharedGPT) : 
    * [Open Assistant Conversation](https://huggingface.co/datasets/OpenAssistant/oasst1): used for QLoRA training
- Infererence
- Deployment

## Closed Foundation Models

- OpenAI
- Google
- Anthropic

## Open Foundation Models

### LLaMA and finetuned variants

- [Alpaca](https://github.com/tatsu-lab/stanford_alpaca)
- [Vicuna](https://lmsys.org/)
- [WizardLM](https://github.com/nlpxucan/WizardLM)
- [Wizard Dataset + Vicuna Finetuning](https://github.com/melodysdreamj/WizardVicunaLM)
- [Open Assistant](https://github.com/LAION-AI/Open-Assistant)
- [QLora/Guanaco](https://github.com/artidoro/qlora)

### LLaMA alternatives

- [OpenLLaMA](https://github.com/openlm-research/open_llama)
- [Falcon](https://falconllm.tii.ae/)
- [Mosiac ML](https://github.com/mosaicml/llm-foundry)
- [StabilityAI](https://github.com/Stability-AI/StableLM)
- [BigCode Project/HuggingFace](https://github.com/bigcode-project)
- [Replit](https://github.com/replit/ReplitLM)

## Frameworks and Ecosystems

- Huggingface: transformers/feft/accelerate/bitsandbytes
- Torch Lightning
- GGML/Llama.cpp
- GPT4all
- GPTQ/AutoGPTQ
- FlexGen
- LangChain
- LLamaIndex
- Text generation web gui

## Stay Current 

From Kaparthy: 

1. [papers:](https://papers.labml.ai/papers/weekly)
2. [papers+code:](https://paperswithcode.com)
3. [code:](https://github.com/trending)

## FAQs

1. Why should I care about LLMs ?
2. What are the common use cases for LLMs ?
3. I am new to the field, where shoud I get started ?
