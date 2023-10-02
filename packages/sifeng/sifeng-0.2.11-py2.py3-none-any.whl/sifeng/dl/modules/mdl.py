import numpy as np
import torch
from torch import nn
from torch.nn.parameter import Parameter
from torch.nn.init import xavier_uniform_

from typing import Optional, Literal, Callable

class MultiheadedSelfAttentionModule(nn.Module):
    """The Multiheaded Self-Attention Module

    Parameters
    ----------
    num_head: int
        number of self-attention heads
    embed_dim: int
        the dimension of input embeddings
    qk_dim: Optional[int], default `None`
        the dimension of qk vectors
    v_dim: Optional[int], default `None`
        the dimension of v vectors
    dropout: float, default `0.0`
        probability of dropout

    Input shape
    -----------
    [bsz * slen * embed_dim]
    """
    def __init__(self,
                 num_head: int,
                 embed_dim: int,
                 qk_dim: Optional[int] = None,
                 v_dim: Optional[int] = None,
                 dropout: float = 0.0,
                 ) -> None:
        super(MultiheadedSelfAttentionModule, self).__init__()
        self.num_head = num_head
        self.embed_dim = embed_dim
        self.qk_dim = qk_dim if qk_dim is not None else embed_dim
        self.v_dim = v_dim if v_dim is not None else embed_dim
        self.uniform_qkv_dim = (self.embed_dim == self.qk_dim and self.embed_dim == self.v_dim)

        if self.uniform_qkv_dim:
            self.head_dim = self.embed_dim // self.num_head
            assert self.head_dim * self.num_head == self.embed_dim, \
                "embed_dim not divisible by num_head"
            self.W_QKV = Parameter(torch.empty(self.embed_dim, self.embed_dim * 3))
        else:
            self.qk_head_dim = self.qk_dim // self.num_head
            self.v_head_dim = self.v_dim // self.num_head
            assert self.qk_head_dim * self.num_head == self.qk_dim, \
                "qk_dim not devisible by num_head"
            assert self.v_head_dim * self.num_head == self.v_dim, \
                "v_dim not divisible by num_head"
            self.W_QK = Parameter(torch.empty(self.embed_dim, self.qk_dim * 2))
            self.W_V = Parameter(torch.empty(self.embed_dim, self.v_dim))
        self.W_Out = Parameter(torch.empty(self.v_dim, self.embed_dim))
        self.softmax = nn.Softmax(dim=-1)
        self.dropout = nn.Dropout(dropout)

        self._init_params()

    def _init_params(self) -> None:
        if self.uniform_qkv_dim:
            xavier_uniform_(self.W_QKV)
        else:
            xavier_uniform_(self.W_QK)
            xavier_uniform_(self.W_V)
        xavier_uniform_(self.W_Out)

    def forward(self,
                x: torch.Tensor, # [bsz * slen * embed_dim]
                ) -> torch.Tensor:
        bsz, slen, embed_dim = x.shape
        if self.uniform_qkv_dim:
            qkv = torch.matmul(x, self.W_QKV).reshape(bsz, slen, self.num_head, self.head_dim, 3).transpose(1, 2) # [bsz * num_head * slen * head_dim * 3]
            q, k, v = qkv[:, :, :, :, 0], qkv[:, :, :, :, 1], qkv[:, :, :, :, 2] # [bsz * num_head * slen * head_dim]
        else:
            qk = torch.matmul(x, self.W_QK).reshape(bsz, slen, self.num_head, self.qk_head_dim, 2).transpose(1, 2) # [bsz * num_head * slen * qk_head_dim * 2]
            q, k = qk[:, :, :, :, 0], qk[:, :, :, :, 1] # [bsz * num_head * slen * qk_head_dim]
            v = torch.matmul(x, self.W_V).reshape(bsz, slen, self.num_head, self.v_head_dim).transpose(1, 2) # [bsz * num_head * slen * v_head_dim]
        attn = self.softmax(torch.matmul(q, k.transpose(2, 3)) / np.sqrt(self.qk_dim)) # [bsz * num_head * slen * slen]
        attn = self.dropout(attn) # [bsz * num_head * slen * slen]
        out = torch.matmul(attn, v).transpose(1, 2).reshape(bsz, slen, self.v_dim) # [bsz * slen * v_dim]
        out = torch.matmul(out, self.W_Out)
        return out

class AbsolutePositionalEncodingModule(nn.Module):
    """The Absolute Positional Encoding Module

    Parameters
    ----------
    embed_dim: int
        the dimension of input embeddings
    dropout: float
        the probability of dropout
    max_len: int, dafault `128`
        the maximum length of positional encoding
    mode: Literal["const", "variable"], default `"variable"`
        mode of positional encoding
        - `"const"`: constant sin/cos encoding
        - `"variable"`: learnable parameter

    Input shape
    -----------
    [bsz * slen * embed_dim]
    """
    def __init__(self,
                 embed_dim: int,
                 dropout: float = 0.0,
                 max_len: int = 128,
                 mode: Literal["const", "variable"] = "variable",
                 ) -> None:
        super(AbsolutePositionalEncodingModule, self).__init__()
        self.mode = mode
        self.embed_dim = embed_dim
        assert mode in ["const", "variable"], "unsupported mode"

        self.dropout = nn.Dropout(p=dropout)
        if self.mode == "const":
            self.Encoding = torch.empty(1, max_len, embed_dim)
            x = torch.arange(max_len, dtype=torch.float32).reshape(-1, 1) / torch.pow(10000, torch.arange(0, embed_dim, 2, dtype=torch.float32) / embed_dim)
            self.Encoding[:, :, 0::2] = torch.sin(x)
            self.Encoding[:, :, 1::2] = torch.cos(x)
        elif self.mode == "variable":
            self.Encoding = nn.Parameter(torch.rand(1, max_len, embed_dim))

    def forward(self,
                x: torch.Tensor, # [bsz * slen * embed_dim]
                ) -> torch.Tensor:
        bsz, slen, embed_dim = x.shape
        return x + self.dropout(self.Encoding[:, :slen, :])

class FeedForwardLayer(nn.Module):
    """The Feed-Forward Layer
    
    Parameters
    ----------
    embed_dim: int
        the dimension of input embeddings
    activation: torch.nn.Module, default torch.nn.ReLU
        the activation module used in the feed-forward sandwich
    elementwise_affine: bool, default `False`
        whether to enable element-wise affine in layer norm
    *args, **kwargs:
        Parameters for the activation function

    Input shape
    -----------
    [bsz * ?? * embed_dim]
    """
    def __init__(self,
                 embed_dim: int,
                 activation: nn.Module = nn.ReLU,
                 *args, **kwargs) -> None:
        super(FeedForwardLayer, self).__init__()
        self.sequential = nn.Sequential(
            nn.Linear(embed_dim, 4 * embed_dim),
            activation(*args, **kwargs),
            nn.Linear(4 * embed_dim, embed_dim)
        )
    
    def forward(self,
                x: torch.Tensor, # [bsz * ?? * embed_dim]
                ) -> torch.Tensor:
        return self.sequential(x)

class TransformerEncoderBlock(nn.Module):
    """The Transformer Encoder Block

    Parameters
    ----------
    num_head: int
        the number of self-attention heads for the attention module
    embed_dim: int
        the dimension of input embeddings
    qk_dim: Optional[int], default `None`
        the dimension of qk vectors for the attention module
    v_dim: Optional[int], default `None`
        the dimension of v vectors for the attention module
    dropout: float, default `0.0`
        probability of dropout
    feed_forward: nn.Module, default `sifeng.dl.modules.FeedForwardLayer`
        the choice of feedforward layer
    layernorm_mode: Literal["post", "pre", "sanwich"], default `"pre"`
        The mode of layernorm
        - "post": layernorm happens after residual connection
        - "pre": layernorm happens before attention block, better when training without warmup
        - "sanwich": layernorm happens before and after attention block, better when training under FP16
    *args, **kwargs:
        parameters for your choice of feed forward network
    
    Input shape
    -----------
    [bsz * slen * embed_dim]
    """
    def __init__(self,
                 num_head: int,
                 embed_dim: int,
                 qk_dim: Optional[int] = None,
                 v_dim: Optional[int] = None,
                 dropout: float = 0.0,
                 feed_forward: nn.Module = FeedForwardLayer,
                 layernorm_mode: Literal["post", "pre", "sanwich"] = "pre",
                 *args, **kwargs) -> None:
        super(TransformerEncoderBlock, self).__init__()
        self.layernorm_mode = layernorm_mode
        self.layernorm = nn.LayerNorm(embed_dim, elementwise_affine=False)
        self.feed_forward = feed_forward(embed_dim=embed_dim, *args, **kwargs)
        self.attention = MultiheadedSelfAttentionModule(num_head, embed_dim, qk_dim=qk_dim, v_dim=v_dim, dropout=dropout)
        self.dropout = nn.Dropout(dropout)

    def forward(self,
                x: torch.Tensor, # [batch * slen * embed_dim]
                ) -> torch.Tensor:
        if self.layernorm_mode == "post":
            x = self.layernorm(x + self.dropout(self.attention(x))) # [batch * slen * embed_dim]
            x = self.layernorm(x + self.dropout(self.feed_forward(x))) # [batch * slen * embed_dim]
        elif self.layernorm_mode == "pre":
            x = x + self.dropout(self.attention(self.layernorm(x))) # [batch * slen * embed_dim]
            x = x + self.dropout(self.feed_forward(self.layernorm(x))) # [batch * slen * embed_dim]
        elif self.layernorm_mode == "sandwich":
            x = x + self.dropout(self.layernorm(self.attention(self.layernorm(x)))) # [batch * slen * embed_dim]
            x = x + self.dropout(self.layernorm(self.feed_forward(self.layernorm(x)))) # [batch * slen * embed_dim]
        return x

class MixtureOfExpertsBlock(nn.Module):
    """The Mixture of Experts Module

    Parameters
    ----------
    embed_dim: int
        the dimension of input embeddings
    num_experts: int
        the number of expert modules
    topk: int, default `2`
        the number of topk experts to activate
    gate: Optional[Callable[[torch.Tensor], torch.Tensor]], default `None`
        the gate layer, if `None` default to simple linear transformation
    expert: torch.nn.Module, default `sifeng.dl.FeedForwardLayer`
        the choice of expert module
    *args, **kwargs:
        parameters for your choice of the expert module

    Input shape
    -----------
    [bsz * ?? * embed_dim]

    """
    def __init__(self,
                 embed_dim: int,
                 num_experts: int,
                 topk: int = 2,
                 gate: Optional[Callable[[torch.Tensor], torch.Tensor]] = None,
                 expert: nn.Module = FeedForwardLayer,
                 *args, **kwargs) -> None:
        super(MixtureOfExpertsBlock, self).__init__()
        self.embed_dim = embed_dim
        self.num_experts = num_experts
        self.topk = topk

        self.softmax = nn.Softmax(dim=-1)
        self.gate = gate if gate is not None else nn.Linear(embed_dim, self.num_experts)
        self.experts = nn.ModuleList([expert(embed_dim=embed_dim, *args, **kwargs) for _ in range(self.num_experts)])

    def forward(self,
                x: torch.Tensor, # [bsz * ?? * embed_dim]
                ) -> torch.Tensor:
        device = x.device
        fsz = x.shape[:-1] # fsz = [bsz * ??]
        x = x.flatten(start_dim=0, end_dim=-2) # [fsz * embed_dim]
        gate = self.gate(x) # [fsz * num_experts]
        topk_values, topk_indices = torch.topk(gate, k=self.topk, dim=-1, sorted=True) # [fsz * topk], [fsz * topk]
        topk_weight = self.softmax(topk_values) # [fsz * topk]
        mask = torch.zeros([topk_weight.shape[0], self.num_experts], device=device, dtype=topk_weight.dtype).scatter(dim=1, index=topk_indices, src=topk_weight) # [fsz * num_experts]
        activators = [mask[:, i].nonzero().squeeze(-1) for i in range(self.num_experts)] # List([?], len=num_experts)
        weights = [mask[:, i].index_select(dim=0, index=activators[i]) for i in range(self.num_experts)]
        inputs = [x.index_select(dim=0, index=activators[i]) for i in range(self.num_experts)] # List([? * embed_dim], len=num_experts)
        outputs = [torch.mul(self.experts[i](inputs[i]), weights[i].unsqueeze(dim=-1)) for i in range(self.num_experts)] # List([? * embed_dim], len=num_experts)
        x = torch.zeros(x.shape[0], outputs[0].shape[-1], device=device, dtype=x.dtype) # [fsz * embed_dim]
        for i in range(self.num_experts):
            x = x.scatter_add(0, activators[i].unsqueeze(dim=-1).repeat_interleave(outputs[0].shape[-1], dim=-1), outputs[i]) # [fsz * embed_dim]
        x = x.unflatten(dim=0, sizes=fsz) # [bsz * ?? * embed_dim]
        return x

class ResidualBlock(nn.Module):
    """The Residual Connection Block

    Parameters
    ----------
    model: Callable[[torch.Tensor], torch.Tensor]
        The module to be residual connected
    affine: Optional[Callable[[torch.Tensor], torch.Tensor]], default None
        The affine from input to the same shape as the output of the model

    """
    def __init__(self,
                 model: Callable[[torch.Tensor], torch.Tensor],
                 affine: Optional[Callable[[torch.Tensor], torch.Tensor]] = None,
                 ) -> None:
        super(ResidualBlock, self).__init__()
        self.residualed = model
        self.affine = affine

    def forward(self,
                x,
                ) -> torch.Tensor:
        if self.affine is not None:
            return self.affine(x) + self.residualed(x)
        else:
            return x + self.residualed(x)
