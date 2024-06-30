from evaluate import load
cer = load("cer")
def calc_accuracy(ground_truth_text, output_text):   
        max_length = max(len(output_text), len(ground_truth_text))
        output_text.extend([""] * (max_length - len(output_text)))
        ground_truth_text.extend([""] * (max_length - len(ground_truth_text)))
        if '' not in ground_truth_text:
            cer_score = cer.compute(predictions=output_text, references=ground_truth_text)
            accuracy = (1 - cer_score)*100
        return accuracy
        