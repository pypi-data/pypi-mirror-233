from research_framework.base.flyweight.base_flyweight_manager import BaseFlyManager
from research_framework.container.container import Container
from research_framework.pipeline.model.pipeline_model import PipelineModel

from rich import print

class FitPredictPipeline:
    def __init__(self, doc:PipelineModel):
        print("\n* Pipeline: ")
        print(doc.model_dump())
        self.pipeline:PipelineModel = doc 
        
    def start(self) -> None:
        try:
            train_input = self.pipeline.train_input
            test_input = self.pipeline.test_input
            
            train_input_manager = Container.get_filter_manager(train_input.clazz,train_input.params)
            test_input_manager = Container.get_filter_manager(test_input.clazz, test_input.params)
            
            train_hash, train_data_name, train_f = train_input_manager.predict(data_name=train_input.name)
            test_hash, test_data_name, test_f  = test_input_manager.predict(data_name=test_input.name)
            
            train_input.items.append(Container.fly.get_item(train_hash))
            test_input.items.append(Container.fly.get_item(test_hash))
            
            for filter_model in self.pipeline.filters:
                filter_manager:BaseFlyManager = Container.get_filter_manager(filter_model.clazz, filter_model.params)
                
                filter_manager.fit(train_hash, train_f)
                
                if not filter_manager.hashcode is None:
                    filter_model.item = Container.fly.get_item(filter_manager.hashcode)
                
                train_hash, train_data_name, train_f = filter_manager.predict(train_hash, train_data_name, train_f)
                test_hash, test_data_name, test_f  = filter_manager.predict(test_hash, test_data_name, test_f)
                
                
                train_input.items.append(Container.fly.get_item(train_hash))
                test_input.items.append(Container.fly.get_item(test_hash))
            
            
            for idx, metric in enumerate(self.pipeline.metrics):
                m_wrapper = Container.get_metric(metric.clazz)
                metric.value = m_wrapper.predict(test_f)
                self.pipeline.metrics[idx] = metric
                
        except Exception as ex:
            raise ex
