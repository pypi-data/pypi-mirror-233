Related work
============

The CAPPr computation is well-known; you'll find it as a subroutine in papers from GPT-2
to Self-Consistency. The ``cappr`` implementation includes a few computational and
statistical optimizations, while maintaining a simple interface.

Here are some papers which focus on the idea of aggregating token probabilities.

While `benchmarking this method`_ on the Winograd Schema Challenge, I found that
`this paper`_\ [#]_ is very similar.

.. _benchmarking this method: https://github.com/kddubey/cappr/blob/main/demos/superglue/wsc.ipynb

.. _this paper: https://arxiv.org/abs/1806.02847

`PET with multiple masks`_\ [#]_ also aggregates token probabilities to do
prompt-completion classification, but these probabilities are assumed to come from
masked language models like BERT.

.. _PET with multiple masks: https://arxiv.org/abs/2009.07118

References
----------

.. [#] Trinh, Trieu H., and Quoc V. Le. "A simple method for commonsense reasoning."
    arXiv preprint arXiv:1806.02847 (2018).

.. [#] Schick, Timo, and Hinrich Schütze. "It's not just size that matters: Small
    language models are also few-shot learners." arXiv preprint arXiv:2009.07118 (2020).
