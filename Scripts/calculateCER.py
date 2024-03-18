import os
from evaluate import load

output_dir = './AccuracyMeasure/outputs-set1-2/'
ground_truth_dir = './AccuracyMeasure/ground-truths'

def read_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return file.read().splitlines()
    except UnicodeDecodeError:
        with open(filepath, 'r', encoding='ISO-8859-1') as file:
            return file.read().splitlines()

cer = load("cer")
accuracies = []

for output_file in os.listdir(output_dir):
    output_path = os.path.join(output_dir, output_file)
    ground_truth_path = os.path.join(ground_truth_dir, output_file)

    if os.path.isfile(ground_truth_path):
        output_text = read_file(output_path)
        ground_truth_text = read_file(ground_truth_path)

        max_length = max(len(output_text), len(ground_truth_text))
        output_text.extend([""] * (max_length - len(output_text)))
        ground_truth_text.extend([""] * (max_length - len(ground_truth_text)))

        print(f'{os.path.splitext(output_file)[0]}')
        cer_score = cer.compute(predictions=output_text, references=ground_truth_text)
        accuracy = (1 - cer_score)*100
        accuracies.append(accuracy)
        # print(f'CER for {os.path.splitext(output_file)[0]}: {cer_score:.2f}')
        print(f'Accuracy for {os.path.splitext(output_file)[0]}: {accuracy:.2f}')

    else:
        print(f'Ground truth file not found for {output_file}')

# accuracy range table
accuracy_ranges = [
    [100, 0],  # 100 %
    [95, 100, 0],   # [95-100) %
    [90, 95, 0],    # [90-95) %
    [80, 90, 0],    # [80-90) %
    [70, 80, 0],    # [70-80) %
    [60, 70, 0],    # [60-70) %
    [50, 60, 0],    # [50-60) %
    [0, 50, 0],     # less than 50%
]

for accuracy in accuracies:
    for acc_range in accuracy_ranges:
        if accuracy == 100.0:
            acc_range[1] += 1
            break

        elif acc_range[0] <= accuracy < acc_range[1]:
            acc_range[2] += 1
            break

for i in range(len(accuracy_ranges)):
    if i == 0:
        print(f'Accuracy 100%: {accuracy_ranges[i][1]} files')
    
    else:
        print(f'Accuracy {accuracy_ranges[i][0]}-{accuracy_ranges[i][1]}%: {accuracy_ranges[i][2]} files')