
import abc
import os
import pickle

from backend.src.strategies.preprocessing.hierarchical_clustering import HierarchicalCluster
from backend.src.strategies.preprocessing.hierarchical_clustering import UserCluster

from backend.src.utils.utils import strategy_result_path


class abstract_attribute(object):
    def __get__(self, obj, type):
        raise NotImplementedError("This attribute was not set in a subclass")


## abstract SQLAlchemy Model class
## this class does not exist as table in db, only the instantiations do


class BaseStrategy(metaclass=abc.ABCMeta):
    # to force giving it a name ...
    strategy_name = abstract_attribute()

    def __init__(self, dataset_name: str):
        self.dataset_name = dataset_name

        if os.path.exists(strategy_result_path(self.strategy_name, self.dataset_name)):
            self._load_clustered_results(self.strategy_name, self.dataset_name)
        else:
            self.clustering = HierarchicalCluster(dataset_name)
            # add representative items to each cluster
            self.add_representative_item_to_user_clusters_in_hc(self.clustering.root_cluster)
            self._save_clustered_results(self.strategy_name, self.dataset_name)

    def _load_clustered_results(self, strategy_name, dataset_name):
        with open(strategy_result_path(strategy_name, dataset_name), 'rb') as strategy_file_r:
            saved_strategy = pickle.load(strategy_file_r)
            self.clustering = saved_strategy.clustering

    def _save_clustered_results(self, strategy_name, dataset_name):
        dir = '/'.join(strategy_result_path(self.strategy_name, dataset_name).split('/')[:-1])
        if not os.path.exists(dir):
            os.makedirs(dir)

        with open(strategy_result_path(strategy_name, dataset_name), 'wb') as strategy_file_w:
            pickle.dump(self, strategy_file_w)


    def add_representative_item_to_user_clusters_in_hc(self, curr_cluster: UserCluster):
        self.add_representative_items_to_children(curr_cluster)
        for each_child_cluster in curr_cluster.child_clusters:
            self.add_representative_item_to_user_clusters_in_hc(each_child_cluster)

    @abc.abstractmethod
    def add_representative_items_to_children(self, parent_cluster: UserCluster):
        raise NotImplementedError("{}.{} should be implemented".format(self.__class__.__name__, self.__module__.__name__))

    @abc.abstractmethod
    def has_next(self, *args, **kwargs) -> bool:
        """
        This function returns if this strategy has next items to return
        If it returns false, it means that it has already reached the final level of hierarchical clustering,
        where the cluster has only one user in it.
        In this case, regardless of the matching strategy, the offline user should be matched with the online user
        """
        raise NotImplementedError("{}.{} should be implemented".format(self.__class__.__name__, self.__module__.__name__))
