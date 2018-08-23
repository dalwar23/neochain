# neochain
Network Evolution Observation for Blockchain


## Getting Started
```python
python setup.py install
```

# Description
Network Evolution Observation for Blockchain (neochain).

### Framework Architecture for `neochain`
The proposed prototypical framework can be expressed in brief as follwing:

- Find top $n$ communities $C_t^{top}$ from a snapshot of a graph $\mathcal{G}_t$ at time $t$
- Generate a sub-snapshot $\mathcal{G}_{sub_{t}}$ of graph $\mathcal{G}_t$, where vertex $V_t \in \mathcal{G}_{sub_{t}}$
is like $V_t \in C_{top}$ 
- Create a graph $\mathcal{G}_{t, t+1}$ by merging sub-snapshot $\mathcal{G}_{sub_{t}}$ with new graph snapshot
$\mathcal{G}_{t+1}$ at time $t+1$
- Find top $n$ communities $C_{t+1}^{top}$ from snapshot of graph $\mathcal{G}_{t, t+1}$ at time $t+1$
- Find maximum overlapping communities $C_{t, t+1}^{max}$ from $C_t^{top}$ and $C_{t+1}^{top}$ and report cluster's
status in community structure lifecycle.

### Community detection
 
