import pandas as pd


def initialize_pred_proba_dfs(app):
	app.state.baseline_df = pd.read_csv("./models/pred_probas/pred_probas_baseline.csv")
	app.state.prospective_ref_df = pd.read_csv("./models/pred_probas/pred_probas_prospective_mean_diff.csv")
	app.state.prospective_df = pd.read_csv("./models/pred_probas/pred_probas_prospective.csv")
	app.state.retrospective_df = pd.read_csv("./models/pred_probas/pred_probas_retrospective.csv")
