# OCR on Industrial Packages

Unzip the "all ground truths" folder to access the ground truth data corresponding to each image in the dataset. Each text file within this folder is named after its corresponding image.

Next, open the performOCR.py file and verify the following settings:

1. Ensure that the template_dir variable is correctly set to the appropriate path (i.e., "templates" subdirectory in the "Subset" directory.
2. Confirm that the testfiles_dir variable points to the directory containing the input images.
3. Set the text_files_dir variable to specify the folder where you want to save the OCR results.

After configuring these settings, run the performOCR.py file. Upon completion, all the OCR outputs will be saved in the specified text_files_dir.

Subsequently, open the calculateCER.py file. Here, update the following settings:

1. Set the ground_truth_dir variable to the directory where you extracted the ground truths in the initial step.
2. Set the output_dir variable to the directory containing the OCR results obtained from running the performOCR.py file.
3. Execute the calculateCER.py file. It will provide the number of images falling within the different accuracy ranges.

Please note that we are using a custom-trained model for this project. The required files, named 'alp_num.traineddata' and 'alp_num-v2.traineddata', are included in the "Trained Model" directory. Either one of these files need to be placed in the following directory, which may vary depending on the drive where you installed Tesseract:
"C:\Program Files\Tesseract-OCR\tessdata"
