from SpiralEval.spiraleval import EvalSummary

api_path = "../../../openai_api.txt"
reference_path = '../../../val_references.json'

eval_summary = EvalSummary(api_path, reference_path)

eval_summary.run()
