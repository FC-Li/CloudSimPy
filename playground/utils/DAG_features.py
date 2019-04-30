import tensorflow as tf

class DAG_features(tf.keras.Model):

	def __init__(self, arg):
		super(DAG_features, self).__init__()
		self.arg = arg
		