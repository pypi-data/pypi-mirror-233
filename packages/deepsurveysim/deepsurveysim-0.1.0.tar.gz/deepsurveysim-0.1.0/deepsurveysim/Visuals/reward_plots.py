import pandas as pd 
import numpy as np

class RewardPlot: 
    def __init__(self, schedule:dict, schedule_config:dict=None) -> None:
        try: 
            import matplotlib.pyplot as plt 
        except ImportError: 
            raise ImportError("Install matplotlib in your envoriment to produce plots")

        self.schedule = schedule 

        if schedule_config is None: 
            self.config = self.default_config()

        
    def default_config(self): 
        return {
            "reward": "reward", 
            "ra":"ra", 
            "decl":"decl", 
            "band":"band", 
            "time":"mjd"
        }
    
    def plot_cummaltive_reward(): 
        pass 

    def plot_mean_reward(): 
        pass 

    def 