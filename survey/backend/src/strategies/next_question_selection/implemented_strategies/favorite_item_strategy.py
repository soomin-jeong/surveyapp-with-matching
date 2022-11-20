from backend.src.strategies.next_question_selection.abstract_class.item_selection_base import BaseStrategy
from backend.src.strategies.preprocessing.hierarchical_clustering import HierarchicalCluster


class Strategy(BaseStrategy):
    def __init__(self, dataset_name: str):
        self.dataset_name = dataset_name
        self.clustering = HierarchicalCluster(dataset_name)

    def has_next(self, choices_so_far_str: str) -> bool:
        return True
    
    def get_next_items(self, current_ratings):

        return []
    


