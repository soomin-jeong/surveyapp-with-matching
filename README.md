# A Hybrid Evaluation Scheme for Making Qualitative Feedback Available to Recommender Systems Researchers

This README.md is about the extended part of the original work by Ananta Lamichhane. To read the README about the original work, please visit [here](https://github.com/ananta-lamichhane/surveyapp).

This repository is an implementation of my thesis project.

## Abstract
In general, Recommendation Systems (abbreviated as RS onwards) are evaluated based on the offline evaluation dataset. This type of evaluation covers one of the core aspects of an RS, the ability to predict users' preferences for an item. However, a good RS requires more than an accurate prediction. For successful performance, an RS should provide a positive user experience, and it includes but is not limited to usefulness, the easiness to use, and the introduction of new and diverse items. These aspects are highly subjective, so it is challenging to measure them in a quantitative and dead dataset like an offline evaluation dataset. 

The offline evaluation and the online evaluation verify different aspects of an RS. However, there are difficulties for researchers to execute an online evaluation, because it requires a running service where researchers can deploy their RS and ask for feedback directly. Researchers need a live product with abundant users and operating one is costly in time and effort. 

There was a previous study to address this problem by building a web-based survey application for researchers to easily conduct an online evaluation based on an offline evaluation. We extend the prototype of this application and implemented an integrated process which includes preprocessing the data, interacting with an online user to match the user with a similar user in the offline evaluation, and asking a new set of questions to extend the offline evaluation dataset. It assumes that the matched pair of users are so similar that we can expect their responses to be similar as well.

The thesis at hand implemented 3 different strategies and evaluated the accuracy of matching two similar users by introducing one of the offline users into the survey application and verifying if the application matches the introduced user with herself. The results of the evaluation confirmed that these strategies are significantly more powerful in matching two similar users than randomly matching them. Expecting more researchers to join this project, this application has so much opportunity to grow and expand.

## File Structure
<details>

```

├── README.md
└── survey
  ...
    ├── backend
    │   ├── __init__.py
    │   ├── data
    │   │   ├── clustered_results                   # files saving the result of hierarchical clustering
    │   │   │   ├── ml-100k
    │   │   │   │   └── HierarchicalClustering.pkl
    │   │   │   ├── movielens_small
    │   │   │   │   └── HierarchicalClustering.pkl
    │   │   │   ├── test1
    │   │   │   │   └── HierarchicalClustering.pkl
    │   │   │   ├── test2
    │   │   │   │   └── HierarchicalClustering.pkl
    │   │   │   └── test3
    │   │   │       └── HierarchicalClustering.pkl
    │   │   ├── datasets                            # contains examples of offline evaluation datasets
    │   │   │   ├── jester
    │   │   │   │   └── ratings.csv
    │   │   │   ├── ml-100k
    │   │   │   │   ├── README
    │   │   │   │   ├── ratings.csv
    │   │   │   │   └── u.data
    │   │   │   ├── ml-1m
    │   │   │   │   ├── README
    │   │   │   │   ├── movies.dat
    │   │   │   │   ├── ratings.csv
    │   │   │   │   ├── ratings.dat
    │   │   │   │   └── users.dat
    │   │   │   ├── movielens_small
    │   │   │   │   ├── README.txt
    │   │   │   │   ├── links.csv
    │   │   │   │   ├── movies.csv
    │   │   │   │   ├── ratings.csv
    │   │   │   │   └── tags.csv
    │   │   │   ├── test1
    │   │   │   │   └── ratings.csv
    │   │   │   ├── test2
    │   │   │   │   └── ratings.csv
    │   │   │   └── test3
    │   │   │       └── ratings.csv
    ...
    │   │   ├── strategy_rep_items                  # files saving the representative items from each strategy and each dataset
    │   │   │   ├── favorite_item
    │   │   │   │   ├── ml-100k
    │   │   │   │   │   └── StrategyRep.pkl
    │   │   │   │   ├── ml-1m
    │   │   │   │   │   └── StrategyRep.pkl
    │   │   │   │   ├── movielens_small
    │   │   │   │   │   └── StrategyRep.pkl
    │   │   │   │   ├── test1
    │   │   │   │   │   └── StrategyRep.pkl
    │   │   │   │   └── test2
    │   │   │   │       └── StrategyRep.pkl
    │   │   │   ├── maniac
    │   │   │   │   ├── ml-100k
    │   │   │   │   │   └── StrategyRep.pkl
    │   │   │   │   ├── ml-1m
    │   │   │   │   │   └── StrategyRep.pkl
    │   │   │   │   ├── movielens_small
    │   │   │   │   │   └── StrategyRep.pkl
    │   │   │   │   └── test1
    │   │   │   │       └── StrategyRep.pkl
    │   │   │   ├── random
    │   │   │   │   └── test1
    │   │   │   │       └── StrategyRep.pkl
    │   │   │   ├── random_item
    │   │   │   │   ├── ml-100k
    │   │   │   │   ├── ml-1m
    │   │   │   │   │   └── StrategyRep.pkl
    │   │   │   │   ├── movielens_small
    │   │   │   │   │   └── StrategyRep.pkl
    │   │   │   │   └── test1
    │   │   │   │       └── StrategyRep.pkl
    │   │   │   └── rated_by_the_most
    │   │   │       ├── ml-100k
    │   │   │       │   └── StrategyRep.pkl
    │   │   │       ├── ml-1m
    │   │   │       │   └── StrategyRep.pkl
    │   │   │       ├── movielens_small
    │   │   │       │   └── StrategyRep.pkl
    │   │   │       └── test1
    │   │   │           └── StrategyRep.pkl
    ...
    │       ├── strategies                      # matching strategies and questioning strategies
    │       │   ├── __init__.py
    │       │   ├── evaluation                  # evaluation of strategies
    │       │   │   ├── __init__.py
    │       │   │   ├── eval_runner.py          # trigger of evaluations
    │       │   │   ├── evaluation.py           # core evaluation code
    │       │   │   ├── hypothesis_testing_results
    │       │   │   │   ├── test-result_matching_strategies.txt
    │       │   │   │   ├── test-result_ml-100k.txt
    │       │   │   │   ├── test-result_ml-1m.txt
    │       │   │   │   └── test-result_movielens_small.txt
    │       │   │   └── unittests.py
    │       │   ├── matchmaking
    │       │   │   ├── __init__.py
    │       │   │   ├── abstract_class          # abstract template for matching strategies
    │       │   │   │   ├── __init__.py
    │       │   │   │   └── matching_strategy_base.py
    │       │   │   ├── implemented_strategies
    │       │   │   │   ├── __init__.py
    │       │   │   │   ├── least_diff_matching_strategy.py
    │       │   │   │   └── random_matchmaking_strategy.py
    │       │   │   └── tests
    │       │   │       ├── __init__.py
    │       │   │       └── unittests.py
    │       │   ├── next_question_selection
    │       │   │   ├── __init__.py
    │       │   │   ├── abstract_class         # abstract template for matching strategies
    │       │   │   │   ├── item_selection_base.py
    │       │   │   │   ├── item_selection_base_choice.py   # template of choice-type questioning strategy
    │       │   │   │   └── item_selection_base_rate.py     # template of rating-type questioning strategy
    │       │   │   ├── implemented_strategies
    │       │   │   │   ├── __init__.py
    │       │   │   │   ├── favorite_item_strategy.py
    │       │   │   │   ├── maniac_strategy.py
    │       │   │   │   ├── random_selection_strategy.py
    │       │   │   │   └── rated_by_the_most_strategy.py
    │       │   │   ├── tests
    │       │   │   │   ├── __init__.py
    │       │   │   │   └── unittests.py
    │       │   │   └── user_cluster_with_representative_item.py
    │       │   └── preprocessing
    │       │       ├── __init__.py
    │       │       ├── hierarchical_clustering.py          # running hierarchical clustering
    │       │       ├── matrix_builder.py                   # rearranging rating data into user-item matrix
    │       │       └── unittests.py
    ...
    
```

</details>
