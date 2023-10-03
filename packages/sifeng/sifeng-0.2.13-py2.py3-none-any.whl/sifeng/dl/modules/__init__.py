"""
Multiheaded Self Attention Module
A. Vaswani et al., “Attention Is All You Need.” arXiv, Aug. 01, 2023. Accessed: Sep. 25, 2023. [Online]. Available: http://arxiv.org/abs/1706.03762
"""
from .mdl import MultiheadedSelfAttentionModule

"""
Absolute Positional Encoding Moudle
- Constant Sinusoidal Absolute PE
A. Vaswani et al., “Attention Is All You Need.” arXiv, Aug. 01, 2023. Accessed: Sep. 25, 2023. [Online]. Available: http://arxiv.org/abs/1706.03762
- Learnable Absolute PE
A. Dosovitskiy et al., “An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale.” arXiv, Jun. 03, 2021. Accessed: Sep. 28, 2023. [Online]. Available: http://arxiv.org/abs/2010.11929
"""
from .mdl import AbsolutePositionalEncodingModule

"""
Feed Forward Layer
"""
from .mdl import FeedForwardLayer

"""
Transformer Encoder Block
- post layer-norm
A. Vaswani et al., “Attention Is All You Need.” arXiv, Aug. 01, 2023. Accessed: Sep. 25, 2023. [Online]. Available: http://arxiv.org/abs/1706.03762
- pre layer-norm
R. Xiong et al., “On Layer Normalization in the Transformer Architecture.” arXiv, Jun. 29, 2020. Accessed: Sep. 28, 2023. [Online]. Available: http://arxiv.org/abs/2002.04745
- sandwich layer-norm
[UNKNOWN]
- deepnorm (TODO)
H. Wang, S. Ma, L. Dong, S. Huang, D. Zhang, and F. Wei, “DeepNet: Scaling Transformers to 1,000 Layers.” arXiv, Mar. 01, 2022. Accessed: Sep. 28, 2023. [Online]. Available: http://arxiv.org/abs/2203.00555
"""
from .mdl import TransformerEncoderBlock

"""
Mixture of Experts Block
N. Shazeer et al., “Outrageously Large Neural Networks: The Sparsely-Gated Mixture-of-Experts Layer.” arXiv, Jan. 23, 2017. Accessed: Sep. 27, 2023. [Online]. Available: http://arxiv.org/abs/1701.06538
- FastMoE
J. He, J. Qiu, A. Zeng, Z. Yang, J. Zhai, and J. Tang, “FastMoE: A Fast Mixture-of-Expert Training System.” arXiv, Mar. 24, 2021. Accessed: Sep. 28, 2023. [Online]. Available: http://arxiv.org/abs/2103.13262
- ST-MoE (TODO)
B. Zoph et al., “ST-MoE: Designing Stable and Transferable Sparse Expert Models.” arXiv, Apr. 29, 2022. Accessed: Sep. 27, 2023. [Online]. Available: http://arxiv.org/abs/2202.08906
"""
from .mdl import MixtureOfExpertsBlock

"""
Residual Connection Block
K. He, X. Zhang, S. Ren, and J. Sun, “Deep Residual Learning for Image Recognition.” arXiv, Dec. 10, 2015. Accessed: Sep. 26, 2023. [Online]. Available: http://arxiv.org/abs/1512.03385
"""
from .mdl import ResidualBlock
