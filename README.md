# LLMs for working data scientists and machine learning practitioners

Large Language Models(LLM) are changing the landscape of data science - whether this represents a paradigm shift in the way information is produced, aggregated and consumed, or this is just another
passing fad, the jury is still out. In any case, AI/LLM as a tool, increasingly an indispensable one, is becoming the accepted norm, especially among programmers and data scientists.

This collection of notes is basically a brain dump for me - it captures my personal learnings to make sense of this exploding field and try to keep myself sane.

# Table of Contents

- [History](#history)
- [Fundamentals](#fundamental)
- [Closed Foundational Models](#closed-foundational-models)
- [Open Foundational Models](#open-foundational-models)
- [Frameworks and Ecosystems](#frameworks-and-ecosystems)
- [FAQs](#faqs)

---

## History

These are the important milestones leading up to the current state of LLM.

- Transformer: 
    * THE transformer paper: [Attention Is All You Need](https://arxiv.org/pdf/1706.03762.pdf)
    * A detailed anatomy of transfomer : [Transformer from scratch](https://e2eml.school/transformers.html)
    * The python implementation of the original transformer: [The annotated transformer](http://nlp.seas.harvard.edu/annotated-transformer/)
    * [A catalog of transfomer models](https://arxiv.org/pdf/2302.07730.pdf)

- GPT style decoder only models
    * [Kaparthy's NanoGPT Impementation](https://github.com/karpathy/nanoGPT)

- Bert style encoder-decoder models 
- "Making it bigger" - scaling and emergent properties
- Instruction finetuning and alignment
- The birth of ChatGPT

## Prerequisites

The field is moving so fast you absolutely need a hacker's mentality

- Numpy and Pandas
- Python and Torch
- Git and github
- Huggingface ecosystem
- Linux, bash, and command line tools

## Fundamentals

- Pre-training
- Common datasets for pre-training
- Fine-tuning
- Common datasets for fine-tuning
- Infererence
- Deployment

## Closed Foundational Models

- OpenAI
- Google
- Anthopic

## Open Foundational Models

- LLama/Aplpaca/Vicuna/Guanaco
- Falcon
- Open Assistant
- MPT - Mosiac ML
- HuggingFace
- OpenLLama - together

## Frameworks and Ecosystems

- Huggingface transformers/feft/accelerate/bitsandbytes
- Torch Lightning
- GGML/Llama.cpp
- GPTQ/AutoGPTQ
- LangChain
- LLamaIndex
- Text generation web gui
- GPT4all

## FAQs

1. Why should I care about LLMs ?
2. What are the common use cases for LLMs ?
3. I am new to the field, where shoud I get started ?
