import pandas as pd
from wonkai.ResultAnalyser import ResultAnalyser
from wonkai.Dict import flatten_dict, deflatten_dict
import random
import string


class ResultComparator():
    
    def __init__(self) :
        column = ["key", "value", "perfect", "score", "metadatas", "id"]
        self.df = pd.DataFrame(columns=column)

    def append_item(self, dict, perfect_dict, metadatas={}, threshold=0.8) :
        result_analyser = ResultAnalyser()
        result_analyser.append_item(dict)
        perfect_flat_dict = flatten_dict(perfect_dict)
        id = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(20))
        for key, perfect_value in perfect_flat_dict.items() :
            value = result_analyser.get_value_max(key, threshold=threshold)
            self.add(key, value, perfect_value, 1, metadatas, id)   

    def add(self, key, value, perfect_value, score, metadatas, id) :
        self.df = pd.concat([self.df, pd.DataFrame([[key, value, perfect_value, score, metadatas, id]],
                                                    columns=self.df.columns)], ignore_index=True)
        
    def reset(self) :
        self.df = pd.DataFrame(columns=self.df.columns)
    
    def get_df(self):
        return self.df
    
    def get_rapport(self) :
        keys = self.df["key"].unique()
        rapport = pd.DataFrame(columns=["key", "good", "wrong", "number", "accuracy", "metadatas"])
        for key in keys :
            wrong_values = []
            df = self.df[self.df["key"] == key]
            good = len(df[df["value"] == df["perfect"]])
            wrong = len(df[df["value"] != df["perfect"]])
            number = len(df)
            accuracy = good / number
            for i in range(len(df)) :
                if df["value"].iloc[i] != df["perfect"].iloc[i] :
                    wrong_values.append({ "got" : df["value"].iloc[i], "expected" : df["perfect"].iloc[i], "metadatas" : df["metadatas"].iloc[i]})
            rapport = pd.concat([rapport, pd.DataFrame([[key, good, wrong, number, accuracy, wrong_values]],
                                                        columns=rapport.columns)], ignore_index=True)
        
        return rapport
            
            

