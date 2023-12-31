# -*- coding: utf-8 -*-
"""Self-Attention-Transformer(Single Headed).ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1T8GTJyZ1_AcuPIE6KKWA5wb1cXCEGpMB
"""

import numpy as np
import math

source = "My Name is Shashank"
source_tokens = source.split(" ")
L = len(source_tokens)
d_k = 8
d_v = 8

# initialising the k, q , v vectors randomly
q = np.random.randn(L, d_k)
k = np.random.randn(L, d_k)
v = np.random.randn(L, d_v)

print("Q\n", q)
print("K\n", k)
print("V\n", v)

"""# Self Attention = Softmax(q. k /  sqrt(d_k) + M)  
new V = self atttn . v
"""

attention_score = np.matmul(q, k.T)
print(attention_score)

# See here why we need to normalize the score with sqrt(d_k)
# variance difference between q, k and q . kT is very high to normalize the variance and keep it balanced
q.var(), k.var(), attention_score.var()

"""Here we can see the variance is not stabilized"""

# After scaling let's how much there is variability of variance
scaled_attention = attention_score / math.sqrt(d_k)
q.var(), k.var(), scaled_attention.var()

# This scaled attention produces better represent the words instead of normal attention
scaled_attention

"""# Masking
It is important for decoder side when we don't want to see the future words context
"""

# creates a triangular matrix where lower half is filled with ones as it will help get information only from past for each token
# For eg: for "My" it will get 1, 0, 0, 0 so no other furture words
mask = np.tril(np.ones( (L,L)))
mask

mask[mask == 0] = -np.infty
mask[mask == 1] = 0
mask

scaled_masked_attn = scaled_attention + mask
print(scaled_masked_attn)

def softmax(x):
  return (np.exp(x).T / np.sum(np.exp(x), axis = -1)).T

softmax_attn = softmax(scaled_masked_attn)

softmax_attn

new_V = np.matmul(softmax_attn, v)
print(new_V)

# compare and see with the old v for each word
# For the first word 1x8 dimensional representation would be same but for subsequent words it will be more context rich
v

"""# Combining the complete thing as a function"""

def softmax(x):
  return (np.exp(x).T / np.sum(np.exp(x), axis=-1)).T

def scaled_dot_product_attention(q, k, v, mask=None):
  d_k = q.shape[-1]
  scaled = np.matmul(q, k.T) / math.sqrt(d_k)
  if mask is not None:
    scaled = scaled + mask
  attention = softmax(scaled)
  out = np.matmul(attention, v)
  return out, attention

values, attention = scaled_dot_product_attention(q, k, v, mask=mask)
print("Q\n", q)
print("K\n", k)
print("V\n", v)
print("New V\n", values)
print("Attention\n", attention)

