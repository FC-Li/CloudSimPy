import tensorflow as tf

class Neural_Network(tf.keras.Model):

	def __init__(self, state_size):
		super().__init__()
		self.dense_1 = tf.keras.layers.Dense(3, input_shape=(None, state_size), activation=tf.tanh)
		self.dense_2 = tf.keras.layers.Dense(6, activation=tf.tanh)
		self.dense_3 = tf.keras.layers.Dense(6, activation=tf.tanh)
		self.dense_4 = tf.keras.layers.Dense(1)

	def call(self, state):
		state = self.dense_1(state)
		state = self.dense_2(state)
		state = self.dense_3(state)
		state = self.dense_4(state)
		return tf.expand_dims(tf.squeeze(state, axis=-1), axis=0)

class DAG_feature_synthesize(object):
	def __init__(self, neural_network, model_save_path=None, summary_path=None):
		self.summary_path = summary_path if summary_path is not None else './little_tensorboard/%s--%s' % (
            name, time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime()))
        self.summary_writer = tf.contrib.summary.create_file_writer(self.summary_path)

		self.optimizer = tf.train.AdamOptimizer(learning_rate=0.001)
		self.global_step = tf.train.get_or_create_global_step()
		self.neural_network = neural_network
		self.checkpoint = tf.train.Checkpoint(brain=self.brain)
        self.model_save_path = model_save_path

    def restore(self, model_path):
    	self.checkpoint.restore(model_path)

    def save(self):
    	self.checkpoint.save(self.model_save_path)

    def _loss(self, X, y, adv):
    	logits = self.neural_network(X)
    	logprob = -tf.losses.sparse_softmax_cross_entropy(labels=y, logits=logits)
    	return logprob * adv

    def optimize(self, grads_by_trajectory):
        average_grads = []
        for grads_by_layer in zip(*grads_by_trajectory):
            average_grads.append(np.array([grad.numpy() for grad in grads_by_layer]).mean(axis=0))

        assert len(average_grads) == len(self.brain.variables)
        for average_grad, variable in zip(average_grads, self.brain.variables):
            assert average_grad.shape == variable.shape

        self.optimizer.apply_gradients(zip(average_grads, self.brain.variables), self.global_step)

    def update_parameters(self, all_observations, all_actions, all_advantages):
    	loss_values = []
    	advantages_ = []
    	for observations, actions, advantages in zip(all_observations, all_actions, all_advantages):
    		grads_by_trajectory = []
    		cnt = 1
    		for observation, action, advantage in zip(observations, actions, advantages):
    			if observation is None or action is None:
    				continue
    			with tf.GradientTape() as t:
    				loss_value = -self._loss(observation, [action], advantage)

    			grads = t.gradinent(loss_value, self.neural_network.variables)
    			grads_by_trajectory.append(grads)
    			loss_values.append(loss_value)
    			advantages_.append(advantages)

    			if cnt % 1000 == 0:
    				self.optimize(grads_by_trajectory)
    				grads_by_trajectory = []

    			cnt += 1
    		if len(grads_by_trajectory)>0:
    			self.optimize(grads_by_trajectory)
		