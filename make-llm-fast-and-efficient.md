# How to server LLM fast and with limited resources

## Inference servers: web server that can provide a REST/grpc or other interface to interact with your model as a service. 

- Huggingface TGI (No more open sourced)
- vLLM/fastchat
- Ctranslate2

## Quantizations

- HG Transformers with BitsAndBytes
- GPTQ (AutoGPTQ, GPTQ-for-Llaama, exllama)
- GGML/Llamaa.cpp( Llama-cpp-python, CTranslate2, CTransformer)

## Besides quantization

- MLC/TVM: this looks really promising !
- layer fusion
- batch reordering
- attention hijacking: xformers, torch sdp attention
- group query attenction (llama 2)

## Distributed Inference and Parallelization

Mostly about using 'deepspeed' which I have not really looked into....
