# DeepDrugRepurposer

Files/filestructure
* raw data folder
* intermediated or miscillanious folder (I usually title misc_save, but whatever people think is best)
* (file or notebook for molecule embedding)
* (file or notebook for creating sample dataset)
* (file for model).py
* sometimes I make a python configuration size, titled config.py, to include metavaribles across multiple files. For instance, DIM_EMBED could be to streamline both embedding training and the model input. Just if we think it's useful

Future...
* File for creating and partitining testing samples
* Folder for files to interact with web-server