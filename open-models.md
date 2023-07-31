
[The open source models arena](https://twitter.com/Yampeleg/status/1685539560975933441)

I try not to post too much about open models until we reach a point where there will no longer be any debate about if they are at the level of closed models.

So let's make it brief. 

## LLaMA 2

The open models arena heated up last week with the release of LLaMA 2.

The model is a direct continuation of the base model for the LLaMA from Meta and marks a significant leap from the first model that can be attributed mainly to the double amount of data on which the model was trained on.

(And probably also the quality of this data, which remained confidential)

The model was also released in a chat version but I will not expand on it at this stage, that chat version suffers from several problems and it is considered not very useful at the moment.

(But the paper do list many tricks used when training the chat version and those tricks are especially interesting and useful. recommended)

## Update Versions

Since the release, nearly all groups working on open source models have updated their models to use the new base model.

We received updated versions from some of the most powerful open models today:

- New WizardLM model: https://huggingface.co/WizardLM/WizardLM-13B-V1.2 (from @WizardLM_AI)

- New Airoboros model: https://huggingface.co/jondurbin/airoboros-l2-70b-gpt4-1.4.1 (from @jon_durbin)

- New Hermes model: https://huggingface.co/NousResearch/Nous-Hermes-Llama2-13b (from @NousResearch)

## The most powerful model today: Stable Beluga 2 (from @StabilityAI & @carperai)

Last week we also got one of the most powerful open models we've seen so far from StabilityAI.

The model is comparable to ChatGPT in almost [1] all measurable metrics and is currently holding the first place on Huggingface's leaderboard.

- Stable Beluga 2: https://huggingface.co/stabilityai/FreeWilly2

## Long Models

The research on extending the context window length also continues in full force we received longer versions of the base model itself, which you can find here:

- LLaMA 7B 16K: https://huggingface.co/conceptofmind/LLongMA-2-7b-16k (from @EnricoShippole)

- LLaMA 13B 16K: https://huggingface.co/conceptofmind/LLongMA-2-13b-16k (from @EnricoShippole)

- LLaMA 7B 32K: https://huggingface.co/togethercomputer/LLaMA-2-7B-32K (from @togethercompute)

## Small Powerful Models

Another interesting model we got is a 3B-parameter model that is as powerful as a 7B model.

This goes to show what most of us have feel for a long time: We have not yet reached the limit of these models. There is more to push.

You are probably thinking that the trick is simply more data: as always.

Surprise.

## The tricks are:

-  A large (600B) fully de-duped dataset: SlimPajama. This is the first model to train on slim pajama end 2 end [1] 
- SwiGLU [2]
- ALiBI [3]
- Variable Sequence Length (2 stage training: short then long) [4]
- Maximal update parameterization (muP): Allows you to "guess" the best hyper-parameters before starting to train. [5]
- BTLM-8K-Base: https://huggingface.co/cerebras/btlm-3b-8k-base (from @CerebrasSystems)

- [1] https://huggingface.co/datasets/cerebras/SlimPajama-627B
- [2] https://arxiv.org/pdf/2002.05202.pdf
- [3] https://arxiv.org/abs/2108.12409
- [4] https://cerebras.net/blog/variable-sequence-length-training-for-long-context-large-language-models/
- [5] https://arxiv.org/pdf/2203.03466.pdf (remember that on GPT-4's paper, the loss was "predicted" before the training started?)

## Open model defeats ChatGPT in MMLU

Although a single number on a single test does not reflect reality, Last week for the first time we got a model that defeats ChatGPT at MMLU.

(And is not particularly trained to do so. That's why it's impressive)

The model:https://huggingface.co/Mikael110/llama-2-70b-guanaco-qlora

## Multi-Turn Chats

One of the main differences setting apart open source models at the moment is multi-turn conversations, (in my humble opinion) we already got to the point where in a single turn our models compete with the closed models but when it comes to multi-turn conversations: Open models tend to go off topic.

This is about to change.

A particularly interesting model was released serveral days ago: Another model trained according to Orca's methods (adding detailed explanations to each answer) BUT for multi-turn long chats.

The model was created with a window length of 8K and according to initial impressions it is one of the best models released.

The model: https://huggingface.co/OpenAssistant/llama2-13b-orca-8k-3319 (from @Shahules786)

## Chinese models are putting up a fight

Even before the release of Lemma 2, it was clear that the Chinese models are already particularly strong.
And you are advised to try them, their English is excellent and some of them are very useful.

The most powerful programming model for its size: CodeGeex2

The Chinese coding model CodeGeeX2 comes to us with a tiny size of 6B parameters (trained from the flagship Chinese model ChatGLM) and overtakes all models of this size scoring 35.9 on HumanEval (Pass@1).

The model: https://huggingface.co/THUDM/codegeex2-6b (from @thukeg)

## More details on the Chinese models

Lately I find myself reading more and more posts translated from Chinese via Google Translate.

Infrastructure for LLMs training and dealing with data coming from China is often times particularly high-quality and also incorporate techniques that do not exist in more popular code bases.

(Such as: training with masking, bidirectional training, architecture improvements and delicate tokenizer work  to support the Chinese language)

I recommend everyone in the field to also read about the advances of the Chinese models.

## Are the open models already at the level of ChatGPT?

Short answer: Not yet, but they are on their way.

Usually when someone say that open source models are on the level of ChatGPT, immediately someone comes up with the hardest test they can think of to show that the open source models are not on the same level as ChatGPT. 
According to rumors, ChatGPT was trained on somewhere around 6 times the data of LLaMA 2.

If you want to find holes, you will find them.

Nonetheless, in the real world: I use open models everyday they are just as good as ChatGPT.

## What is still left to do?

After the release of the Stable Beluga 2 model I wrote a post summarizing all the metrics from all the datasets where the model's results still don't crush ChatGPT.

You can find it here:https://twitter.com/Yampeleg/status/1682502030076571649

## How do we measure the quality of models?

There are several main "holes" that separate the open models from the closed models, you can read about these holes and the differences between the various models here: https://kaistai.github.io/FLASK

## From the news: Open source model from OpenAI?

On the background of this, we recently received an interesting news article about the efforts within OpenAI to release an open model.

Link:https://theinformation.com/articles/pressure-grows-on-openai-to-respond-to-metas-challenge

It is not known if the information in this article is correct, but according to the article, open source models are putting pressure on OpenAI they are currently working on an open model as a response to the LLaMA 2.

The model does not compete with the quality of ChatGPT (and certainly not with GPT-4).
