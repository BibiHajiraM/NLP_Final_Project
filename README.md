# How to use? 
This repository is clearly an offshoot of Homework 5 codes. Hence we are not disturbing the older readme file which contains detailed instructions. Here we, merely want to highlight the steps a user may want to take to run our scripts. 

# What do our scripts do?
In this project, we are training a network to translate english text to SQL query (code). This is similar to English-to-German translation task we did in HW5. 

# What changes have we made? 
We have two pairs of scripts for two models:

1. Baseline Model: Randomly initialized transformer we built in our HWs with BPE tokenizers trained from scratch
2. CodeT5 Model: Using pre-trained CodeT5 model by Salesforce, and corresponding tokenizer (for SQL). 

We have used [spider](https://yale-lily.github.io/spider) dataset which contains manually annotated pairs of questions in English and corresponding SQL queries. 


# What metric have we used? 
BLEU

# What should I do to run the scripts? 

1. `cd <project_folder>` # Same level as this README file
2. `conda create -n nlp_class python=3.8` 
3. `conda activate nlp_class`
4. `pip install --editable .`
5. If your CUDA version is 11.x run `pip install torch==1.10.2+cu113 -f https://download.pytorch.org/whl/cu113/torch_stable.html`

Now, you can create source and target tokenizers:
1. `cd cli`
2. CodeT5: `python create_tokenizer.py --vocab_size 30000 --save_dir tokenizer`
3. Baseline: `python create_tokenizer_without_pre.py --vocab_size 30000 --save_dir tokenizer_without_pre`

Now that you have created tokenizers, which should be available in `tokenizer` and `tokenizer_without_pre` folders for CodeT5 and Baseline models respectively, we can now move on to training. 

To Train, we use wandb sweeps. We need to initiate them. 
1. CodeT5: 
   1. `wandb sweep sweep.yaml` (to be run from the same level as this README file)
   2. Copy the link posted in the terminal 
   3. `cd cli`
   4. Paste the command copied in step 2 and hit enter. This shoudl trigger wandb sweep. In case you haven't logged in yet, you will have to provide API key of your wandb account. 
2. Baseline:
   1. `wandb sweep sweep_without_pre.yaml` (to be run from the same level as this README file)
   2. Copy the link posted in the terminal 
   3. `cd cli`
   4. Paste the command copied in step 2 and hit enter. This shoudl trigger wandb sweep. In case you haven't logged in yet, you will have to provide API key of your wandb account. 


# How to interact? 
1. After you are done training the models, once you pick your best run, you can download the corresponding model and save in `tokenizer` or `tokenizer_without_pre` folder depending on if it was CodeT5 or Baseline model respectively. 
2. Once you have the models with you, you can run the notebook in `notebooks/03_interact_gradio.ipynb`. Ensure that the paths for source tokenizer, target tokenizer and model are correctly defined. 
3. Upon running the notebook in Step 2, you should get a link (both public and local) which could be opened in a browser where you can interact with the model. 