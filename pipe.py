import pandas as pd
import numpy as np

from sklearn.preprocessing import LabelEncoder, OneHotEncoder

dbfile = 'data/drugbank_embds.pkl'
negfile = 'data/negative_samples_thrsh_12'
fngrfile = 'data/chem_cid_SMILE_fngr_vector_fngr.pickle'
valfile = 'data/val_samples.pkl'
vfngrfile = 'data/val_fingerprints.pkl'

class Data:

	def __init__(self):
		self.load_maps()


	def load_maps(self):
		fingerprints = pd.read_pickle(fngrfile)
		fingerprints['cid'] = fingerprints['cid'].astype(int)
		db = pd.read_pickle(dbfile)

		db = db.merge(fingerprints, how = 'right', right_on='cid', left_on='pubchem_id')
		db = db[db['fingerprint'].notnull()]
		db = db[(db.fingerprint.notnull()) & (db.target_amino.notnull()) & (db.target_gene.notnull())]
		
		db['target_gene_code'] = db['target_gene'].apply(lambda x: ''.join(list(x.split('\n')[1:])))
		db['target_amino_code'] = db['target_amino'].apply(lambda x: ''.join(list(x.split('\n')[1:])))

		# val = pd.read_pickle('val_samples.pkl')

		# self.smiles_map = pd.concat([
		# 	drugbank[['SMILE', 'fingerprint']], val[['SMILE', 'fingerprint']]
		# ], axis=0, ignore_index=True, sort=False).drop_duplicates('SMILE') \
		# 	.rename(columns={'fingerprint', 'drug_fingerprint'})#.set_index('drug_id')

		self.drug_map = db[['drug_id', 'fingerprint']].drop_duplicates('drug_id') \
			.rename(columns={'fingerprint': 'drug_fingerprint'})#.set_index('drug_id')
		self.target_map = db[['target_id', 'target_gene_code', 'target_amino_code']].drop_duplicates('target_id')#.set_index('gene_id')


	def load_drugbank(self, target='gene'):
		data = pd.read_pickle(dbfile).rename(columns={'drug_fingerprint' : 'fingerprint_em'})

		data = data.merge(self.drug_map, how='left', on='drug_id').merge(self.target_map, how='left', on='target_id')
		data = data[(data.drug_fingerprint.notnull()) & (data.target_amino_code.notnull()) & (data.target_gene_code.notnull())]

		return data[['drug_id', 'target_id', 'drug_fingerprint', 'target_gene_code', 'target_amino_code']]


	def load_negative_samples(self):
		data = pd.read_csv(negfile)[['node_0','node_1','shortest_path']] 
		data = data.rename(columns = {'node_0': 'drug_id', 'node_1': 'target_id'})
		data = data[data['drug_id'].str.contains('DB') & data['target_id'].str.contains('BE')]

		data = data.merge(self.drug_map, how='left', on='drug_id').merge(self.target_map, how='left', on='target_id')
		data = data[(data.drug_fingerprint.notnull()) & (data.target_amino_code.notnull()) & (data.target_gene_code.notnull())]

		return data[['drug_id', 'target_id', 'drug_fingerprint', 'target_gene_code', 'target_amino_code']]


	def encode_labels(self, l):

		if l[0].count(' ') == 0:
			vocab = list(set([i for j in l for i in j]))
		else:
			vocab = list(set([i for j in l for i in j.split()]))

		
		le = LabelEncoder()
		le.fit(vocab)

		if l[0].count(' ') == 0:
			encoding = [le.transform([i for i in j]) for j in l]
		else:
			encoding = [le.transform([i for i in j.split()]) for j in l]

		return encoding


	def pad_inputs(self, inputs, balanced=True):
		maxlen = max(len(i) for i in inputs)

		if balanced:
			padded = [int( (maxlen - len(i)) / 2 ) * [-1] + i.tolist() + int( (maxlen - len(i)) / 2 ) * [-1] for i in inputs]
			padded = [i + (maxlen - len(i)) * [-1] for i in padded]
		else:
			padded = [i.tolist() + (maxlen - len(i)) * [-1] for i in inputs]

		return padded


	def load_conv_train(self, thresh = 5, is_amino = True):
		drugbank = self.load_drugbank()
		drugbank['label'] = 1

		ns = self.load_negative_samples().sample(n=len(drugbank))
		ns['label'] = 0

		train = pd.concat([drugbank, ns], axis=0, ignore_index=True,sort=False)
		train['set'] = 'train'

		if is_amino:
			target_col = 'target_amino_code'

			val = pd.read_pickle(valfile)
			fgrprints = pd.read_pickle(vfngrfile)

			val = val.merge(fgrprints, how='left', left_on='pubchem_id', right_on='cid') \
				.rename(columns={'BindingDB Target Chain  Sequence' : 'target_amino_code',
					'fingerprint' : 'drug_fingerprint'})

			val = val[(val.drug_fingerprint.notnull()) & (val.target_amino_code.notnull())]

			val.at[val[val['IC50 (nM)'].apply(np.log) < thresh].index, 'label'] = 1
			val.at[val[val['IC50 (nM)'].apply(np.log) >= thresh].index, 'label'] = 0
			val = val[['drug_fingerprint', 'target_amino_code', 'label']]
			val['set'] = 'val'

			data = pd.concat([train[['drug_fingerprint', 'target_amino_code', 'label', 'set']], val], ignore_index=True, sort=False)

		else:
			target_col = 'target_gene_code'
			data = train[['drug_fingerprint', 'target_gene_code', 'label', 'set']].copy()

		data['d_enc'] = self.encode_labels(data.drug_fingerprint.tolist())
		data['t_enc'] = self.encode_labels(data[target_col].tolist())

		data['d_len'] = data.d_enc.apply(len)
		data['t_len'] = data.t_enc.apply(len)

		data['d_enc_p'] = self.pad_inputs(data.d_enc.tolist())
		data['t_enc_p'] = self.pad_inputs(data.t_enc.tolist())

		return data





# Load Data
# Select Samples
# Transform columns

if __name__ == '__main__':
	d = Data()
	# print(d.drug_map)
	# print(d.target_map)
	data = d.load_conv_train(is_amino=False)
	print(data.head())
