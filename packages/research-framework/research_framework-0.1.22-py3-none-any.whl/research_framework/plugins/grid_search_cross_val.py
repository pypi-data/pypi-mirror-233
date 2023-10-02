from typing import List
from sklearn.model_selection import ShuffleSplit, StratifiedShuffleSplit, StratifiedKFold
from research_framework.base.plugin.base_plugin import BasePlugin
from research_framework.base.plugin.base_wrapper import BaseWrapper
from research_framework.container.container import Container

from rich import print
from research_framework.base.utils.grid_seach import generate_combis
from research_framework.pipeline.model.pipeline_model import MetricModel

import json
import numpy as np
import pandas as pd

@Container.bind()
class CrossValGridSearch(BasePlugin):
    split_algorithms={
        "ShuffleSplit":ShuffleSplit,
        "StratifiedShuffleSplit":StratifiedShuffleSplit,
        "StratifiedKFold":StratifiedKFold
    }
    def __init__(self, split_alg='ShuffleSplit', n_splits=3, test_size=0.3, random_state=43, scorers=[MetricModel(clazz='F1')], refit=True, filters=[]):
        self.n_splits = n_splits
        self.test_size = test_size
        self.random_state = random_state
        self.filters = filters
        self.scorers = scorers
        self.refit = refit
        self.alg = CrossValGridSearch.split_algorithms[split_alg]
        self.best_pipeline:List[BaseWrapper] = []
        self.best_config:str = None


    def fit(self, x):
        if callable(x) and x.__name__ == "<lambda>":
            x = x()

        print("\n--------------------[CrossValGridSearch]-----------------------\n")
        print(self.filters)
        print("\n---------------------------------------------------------------\n")
        cv = self.alg(
            n_splits=self.n_splits, 
            test_size=self.test_size, 
            random_state=self.random_state
        )
        combi_dict = {}
        for combi in generate_combis(self.filters):
            combi_str = json.dumps(combi)
            combi_dict[combi_str] = combi
            results = {}
            for train, test in cv.split(x):
                if type(x) == pd.DataFrame:
                    x_train = x.iloc[train]
                    x_test = x.iloc[test]
                else:
                    x_train = x[train]
                    x_test = x[test]
                    
                for clazz, params in combi.items():
                    wrapper:BaseWrapper = Container.get_wrapper(clazz, params)
                    wrapper.fit(x_train)
                    
                    x_train = wrapper.predict(x_train)
                    x_test = wrapper.predict(x_test)
                    
                for metric in self.scorers:
                    m_wrapper = Container.get_metric(metric.clazz)
                    result = results.get(combi_str, [])
                    result.append(m_wrapper.predict(x_test))
                    results[combi_str] = result
        
        print("\n-------------------------------------------\n")
        print("- Results: ")
        results_means = dict(map(lambda x: (x[0], np.mean(x[1])), results.items()))
        print("\n.....................\n")
        for config, value in results_means.items():
            print(f'Config -> {config}')
            print(f'Value  -> {value}')
            print("\n.....................\n")
        
        print("\n-------------------------------------------\n")
        print("- Max values: ")
        print("\n.....................\n")
        config, value = max(results_means.items(), key=lambda x: x[1])
        print(f'Max Combination –> {config}')
        print(f'Max value       –> {value}')
        
        print("\n-------------------------------------------\n")
        print("- Refit of best model: ")
        
        for clazz, params in combi_dict[config].items():
            wrapper:BaseWrapper = Container.get_wrapper(clazz, params)
            wrapper.fit(x)
            
            self.best_pipeline.append(wrapper)
            
            x = wrapper.predict(x)
            
                                    
    
    def predict(self, x): 
        if callable(x) and x.__name__ == "<lambda>":
            x = x()
        
        for wrapper in self.best_pipeline:
            x = wrapper.predict(x)
        
        print("- Test Result:")
        for metric in self.scorers:
            m_wrapper = Container.get_metric(metric.clazz)
            f'{metric.clazz} : {m_wrapper.predict(x)}'
            
        return x
        
         