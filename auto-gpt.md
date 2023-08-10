Install AutoGPTQ 0.3.2, which I recommend you do from source due to some install issues at the moment:

```bash
pip3 uninstall -y auto-gptq
git clone https://github.com/PanQiWei/AutoGPTQ
cd AutoGPTQ
pip3 install .
```

Then here's an AutoGPTQ wrapper script I've written, and which I use myself to make these models: https://gist.github.com/TheBloke/b47c50a70dd4fe653f64a12928286682#file-quant_autogptq-py

Example execution:

```bash
python3 quant_autogptq.py /path.to/unquantised-model /path/to/save/gptq wikitext --bits 4 --group_size 128 --desc_act 0 --damp 0.1 --dtype float16 --seqlen 4096 --num_samples 128 --use_fast
```

The example command will use the wikitext dataset for quantisation. If your model is trained on something more specific, like code, or non-English language, then you may want to change to a different dataset. Doing that would require editing quant_autogptq.py to load an alternative dataset.
