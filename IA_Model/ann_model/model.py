import torch
import torch.nn as nn

class TabularModel(nn.Module):
    
    def __init__(self,emb_szs, n_cont,n_bin, out_szs, layers, p=0.5):
        super().__init__()
        
        self.embeds = nn.ModuleList([nn.Embedding(ni,nf) for ni,nf in emb_szs])
        self.emb_drop = nn.Dropout(p)
        self.bn_cont = nn.BatchNorm1d(n_cont)
        self.soft = nn.Softmax(dim=1)
        
        layerlist = []
        n_emb = sum([nf for ni,nf in emb_szs])
        n_in = n_emb + n_cont + n_bin
        
        for i in layers:
            layerlist.append(nn.Linear(n_in,i))
            layerlist.append(nn.Sigmoid())
            layerlist.append(nn.BatchNorm1d(i))
            layerlist.append(nn.Dropout(p))
            n_in = i
            
        layerlist.append(nn.Linear(layers[-1], out_szs))
        if out_szs == 1:
            layerlist.append(nn.Sigmoid())
        self.layers = nn.Sequential(*layerlist)
        
        
    def forward(self, x_cat, x_cont, x_bin):
        embeddings = []
        
        for i,e in enumerate(self.embeds):
            embeddings.append(e(x_cat[:,i]))
    
        x = torch.cat(embeddings,1)
        x = self.emb_drop(x)
        
        x_cont = self.bn_cont(x_cont)
        x = torch.cat([x,x_cont,x_bin],1)
        x = self.layers(x)
        
        return x