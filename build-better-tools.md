## Tips for writing useful tools (Copied from LlamaIndex blog)

- write useful tool prompts: be concise, list args with type information, given example values, explain return data
- make tools tolerant of partial inputs: be forgiving, use context & state to infer as much as possible
- validating input and agent error handling: detect error early and give clear instruction on how to recover from error
- provide simple functions related to the tool: LLMs are stateless, it’s your job to tell it the date and time
- Returning prompts from functions that perform mutations: if the action changed something, tell the agent about how it went
- Storing large responses in indices for the Agent to read: often times APIs respond with long text. Avoid flooding the context window by storing data in working memory and search for most relevant context
- Verify how the Agent understands the tool: a super useful trick to debug your tool. If the agent misses details in the explanation, it probably can’t reason about it well enough!
