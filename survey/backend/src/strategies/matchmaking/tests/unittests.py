import pandas as pdimport numpy as npfrom backend.src.strategies.matchmaking.implemented_strategies.random_matchmaking_strategy import StrategyDUMMY_RATINGS = pd.DataFrame(data=np.array([['459', '5618', '5.0', '1520233615'],                                            ['477', '5618', '4.0', '1201159360'],                                            ['298', '5618', '2.5', '1447598312'],                                            ['219', '1262', '3.5', '1194685902'],                                            ['483', '1262', '3.5', '1178293076'],                                            ['45', '1262', '5.0', '1020802351'],                                            ['606', '1262', '3.5', '1184619962'],                                            ['290', '1084', '5.0', '974938169'],                                            ['445', '6016', '2.0', '1454621781'],                                            ['455', '440', '3.0', '836436201']]),                             columns=['userId', 'movieId', 'rating', 'timestamp'])def test_naive_strategy_returns_existing_user():    naive_st = Strategy(DUMMY_RATINGS)    matched_user_id = str(naive_st.get_matched_offline_user())    offline_user_ids = DUMMY_RATINGS['userId'].unique()    assert matched_user_id in offline_user_ids, "the matched user by naive strategy does not exist in the offline users"def test_if_implemented_strategies_contain_only_one_strategy():    assert 1 == 2