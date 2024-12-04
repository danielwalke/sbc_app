import torch
def initialize_ref_nodes(app):
    app.state.median_ref_node = torch.tensor([ 59.0000,   1.0000,   7.8000,   7.4000,   4.2300,  87.7000, 236.0000])
    app.state.mean_ref_node = torch.tensor([ 56.7933,   0.5038,   7.5724,   8.2361,   4.1218,  87.7919, 243.2722])