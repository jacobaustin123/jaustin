import jax
import jax.numpy as jnp

import functools
import operator

def tree_add(pytree):
    return jax.tree_util.tree_reduce(operator.add, pytree, 0)

def param_shapes(params):
    return jax.tree_util.tree_map(jnp.shape, params)

def num_params(params):    
    per_node_params = jax.tree_util.tree_map(jnp.size, params)
    return tree_add(per_node_params)