## My experience on starting with fine tuning LLMs with custom data - copied from Reddit r/localLlaMa

I keep seeing questions about "How I make a model to answer based on my data. I have [wiki, pdfs, whatever other documents]"

Currently I am making a living by helping companies built chatbots fine tuned on their custom data.

Most of those are support or Q&A chatbots to answer questions from clients at any hour and day. There are also internal chatbots to be used to train new people joining the company and several other use cases.

So, I was thinking to share my experience (it might be wrong and I might be doing everything wrong, but it is my experience and based on this I have a dozen chatbots running in production and talking with clients with few dozen more in different stages of testing).

The actual training / fine-tuning, while it might initially seem like a daunting task due to the plethora of tools available (FastChat, Axolot, Deepspeed, transformers, LoRA, qLoRA, and more), I must tell you - this is actually the easiest part of the whole process! All you need to do is peek into their repositories, grab an example, and tweak it to fit your model and data.

However, the real challenge lies in preparing the data. A massive wiki of product documentation, a thousand PDFs of your processes, or even a bustling support forum with countless topics - they all amount to nothing if you don't have your data in the right format. Projects like Dolly and Orca have shown us how enriching data with context or system prompts can significantly improve the final model's quality. Other projects, like Vicuna, use chains of multi-step Q&A with solid results. There are many other datasets formats, depending of the expected result. For example, a dataset for quotes is much simpler, because there will be no actual interaction, the quote is a quote.

Personally, I mostly utilize the #instruction, #input, #output format for most of my fine-tuning tasks.

So, shaping your data in the correct format is, without a doubt, the most difficult and time-consuming step when creating a Language Learning Model (LLM) for your company's documentation, processes, support, sales, and so forth.

Many methods can help you tackle this issue. Most choose to employ GPT4 for assistance. Privacy shouldn't be a concern if you're using Azure APIs, though they might be more costly, but offer privacy. However, if your data is incredibly sensitive, refrain from using them. And remember, any data used to train a public-facing chatbot should not contain any sensitive information.

Automated tools can only do so much; manual work is indispensable and in many cases, difficult to outsource. Those who genuinely understand the product/process/business should scrutinize and cleanse the data. Even if the data is top-notch and GPT4 does a flawless job, the training could still fail. For instance, outdated information or contradictory responses can lead to poor results.

In many of my projects, we involve a significant portion of the organization in the process. I develop a simple internal tool allowing individuals to review rows of training data and swiftly edit the output or flag the entire row as invalid.

Once you've curated and correctly formatted your data, the fine-tuning can commence. If you have a vast amount of data, i.e., tens of thousands of instructions, it's best to fine-tune the actual model. To do this, refer to the model repo and mimic their initial training process with your data.

However, if you're working with a smaller dataset, a LoRA or qLoRA fine-tuning would be more suitable. For this, start with examples from LoRA or qLoRA repositories, use booga UI, or experiment with different settings. Getting a good LoRA is a trial and error process, but with time, you'll become good at it.

Once you have your fine-tuned model, don't expose it directly to clients. Instead, run client queries through the model, showcasing the responses internally and inviting internal users to correct the answers. Depending on the percentage of responses modified by users, you might need to execute another fine-tuning with this new data or completely redo the fine-tuning if results were really poor.

On the hardware front, while it's possible to train a qLoRA on a single 3090, I wouldn't recommend it. There are too many limitations, and even browsing the web while training could lead to OOM. I personally use a cloud A6000 with 48GB VRAM, which costs about 80 cents per hour.

For anything larger than a 13B model, whether it's LoRA or full fine-tuning, I'd recommend using A100. Depending on the model and dataset size, and parameters, I run 1, 4, or 8 A100s. Most tools are tested and run smoothly on A100, so it's a safe bet. I once got a good deal on H100, but the hassle of adapting the tools was too overwhelming, so I let it go.

Lastly, if you're looking for a quick start, try embeddings. This is a cheap, quick, and acceptable solution for internal needs. You just need to throw all internal documents into a vector db, put a model in front for searching, and voila! With no coding required, you can install booga with the superbooga extension to get started.

UPDATE:

I saw some questions repeating, sorry that I am not able to answer to everyone, but I am updating here, hope that this helps. Here are some answers for the repeated questions:

1. I do not know how to train a pre-trained model with "raw" data, like big documents. From what I know, any further training of a pre-trained model is done by feeding data tokenized and padded to maximum context size of the original model, no more.

2. Before starting, make sure that the problem that needs to be solved and the expectations are fully defined. "Teaching the model about xyz" is not a problem, it is a wish. It is hard to solve "wishes", but we can solve problems. For example: "I want to ask the model about xyz and get accurate answers based on abc data". This is needed to offer non stop answering chat for customers. We expect customer to ask "example1, 2, 3, .. 10" and we expect the answers to be in this style "example answers with example addressation, formal, informal, etc). We do not want the chat to engage in topics not related to xyz. If customer engage in such topics, politely explain that have no knowledge on that. (with example). This is a better description of the problem.

3. It is important to define the target audience and how the model will be used. There is a big difference of using it internally inside an organisation or directly expose it to the clients. You can get a lot cheaper when it is just an internal helper and the output can be ignored if not good. For example, in this case, full documents can be ingested via vectordb and use the model to answer questions about the data from the vectordb. If you decide to go with the embeddings, this can be really helpful: https://github.com/HKUNLP/instructor-embedding

4. It is important to define what is the expected way to interact with the model. Do you want to chat with it? Should it follow instructions? Do you want to provide a context and get output in the provided context? Do you want to complete your writing (like Github Copilot or Starcoder)? Do you want to perform specific tasks (eg grammar checking, translation, classification of something etc)?

5. After all the above are decided and clarified and you decided that embeddings are not what you want and want to proceed further with fine tuning, it is the time to decide on the data format.

    - #instruction,#input,#output is a popular data format and can be used to train for both chat and instruction following. This is an example dataset in this format: https://huggingface.co/datasets/yahma/alpaca-cleaned . I am using this format the most because it is the easiest to format unstructured data into, having the optional #input it makes it very flexible

    - It was proven that having better structured, with extra information training data will produce better results. Here is Dolly dataset that is using a context to enrich the data: https://huggingface.co/datasets/databricks/databricks-dolly-15k

    - A newer dataset that further proved that data format and quality is the most important in the output is Orca format. It is using a series of system prompts to categorize each data row (similar with a tagging system). https://huggingface.co/datasets/Open-Orca/OpenOrca

    - We don't need complicated data structure always. For example, if the expecation is that we prompt the model "Who wrote this quote: [famous quote content]?" and we expect to only get name of the author, then a simple format is enough, like it is here: https://huggingface.co/datasets/Abirate/english_quotes

    - For a more fluid conversation, there is the Vicuna format, an Array of Q&A. Here is an example: https://huggingface.co/datasets/ehartford/wizard_vicuna_70k_unfiltered
There are other datasets formats, in some the output is partially masked (for completion suggestion models), but I have not worked and I am not familiar with those formats.

6. From my experiments, things that can be totally wrong:

    - directly train a pre-trained model with less than 50000 data row is more or less useless. I would think of directly train a model when I have more than 100k data rows, for a 13B model and at least 1 mil for a 65B model.

    - with smaller datasets, it is efficient to train LoRA of qLoRA.

    - I prefer to train a 4 bit qLora 30B model than a fp16 LoRA for a 13B model (about same hw requirements, but the results with the 4bit 30B model are superior to the 13B fp16 model)
