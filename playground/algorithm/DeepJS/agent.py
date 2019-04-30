import time
import copy
import numpy as np
import tensorflow as tf


class Agent(object):
    def __init__(self, name, brain, gamma, reward_to_go, nn_baseline, normalize_advantages, model_save_path=None,
                 summary_path=None):
        super().__init__()

        self.gamma = gamma
        self.reward_to_go = reward_to_go
        self.baseline = nn_baseline
        self.normalize_advantages = normalize_advantages
        self.optimizer = tf.train.AdamOptimizer(learning_rate=0.001)
        self.global_step = tf.train.get_or_create_global_step()
        self.summary_path = summary_path if summary_path is not None else './tensorboard/%s--%s' % (
            name, time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime()))
        self.summary_writer = tf.contrib.summary.create_file_writer(self.summary_path)

        self.brain = brain
        self.checkpoint = tf.train.Checkpoint(brain=self.brain)
        self.model_save_path = model_save_path

    def restore(self, model_path):
        self.checkpoint.restore(model_path)

    def save(self):
        self.checkpoint.save(self.model_save_path)

    def _sum_of_rewards(self, rewards_n):
        """
            Monte Carlo estimation of the Q function.

            arguments:
                rewards_n: shape(...).

            returns:
                q_n: shape: (...).
            ----------------------------------------------------------------------------------

            Your code should construct numpy arrays for Q-values which will be used to compute
            advantages.

            Recall that the expression for the policy gradient PG is

                  PG = E_{tau} [sum_{core=0}^T grad log pi(a_t|s_t) * (Q_t - b_t )]

            where

                  tau=(s_0, a_0, ...) is a trajectory,
                  Q_t is the Q-value at time core, Q^{pi}(s_t, a_t),
                  and b_t is a baseline which may depend on s_t.

            You will write code for two cases, controlled by the flag 'reward_to_go':

              Case 1: trajectory-based PG

                  (reward_to_go = False)

                  Instead of Q^{pi}(s_t, a_t), we use the total discounted reward summed over
                  entire trajectory (regardless of which time step the Q-value should be for).

                  For this case, the policy gradient estimator is

                      E_{tau} [sum_{core=0}^T grad log pi(a_t|s_t) * Ret(tau)]

                  where

                      Ret(tau) = sum_{core'=0}^T gamma^core' r_{core'}.

                  Thus, you should compute

                      Q_t = Ret(tau)

              Case 2: reward-to-go PG

                  (reward_to_go = True)

                  Here, you estimate Q^{pi}(s_t, a_t) by the discounted sum of rewards starting
                  from time step core. Thus, you should compute

                      Q_t = sum_{core'=core}^T gamma^(core'-core) * r_{core'}


            Store the Q-values for all timesteps and all trajectories in a variable 'q_n'.
        """
        q_s = []
        for re in rewards_n:
            q = []
            cur_q = 0
            for reward in reversed(re):
                cur_q = cur_q * self.gamma + reward
                q.append(cur_q)
            q = list(reversed(q))
            q_s.append(q)

        if self.reward_to_go:
            return q_s
        else:
            q_n = []
            for q in q_s:
                q_n.append([q[0]] * len(q))
            return q_n

    def _compute_advantage(self, q_n):
        """
            Computes advantages by (possibly) subtracting a baseline from the estimated Q values

            arguments:
                q_n: shape: (...).

            returns:
                adv_n: shape: (...).
        """
        # Computing Baselines
        if self.baseline:
            adv_n = copy.deepcopy(q_n)
            max_length = max([len(adv) for adv in adv_n])
            for adv in adv_n:
                while len(adv) < max_length:
                    adv.append(0)
            adv_n = np.array(adv_n)
            adv_n = adv_n - adv_n.mean(axis=0)

            adv_n__ = []
            for i in range(adv_n.shape[0]):
                original_length = len(q_n[i])
                adv_n__.append(list(adv_n[i][:original_length]))
            return adv_n__
        else:
            adv_n = q_n.copy()
            return adv_n

    def estimate_return(self, rewards_n):
        """
            Estimates the returns over a set of trajectories.


            arguments:
                re_n: shape(...).

            returns:
                q_n: shape: (...).
                adv_n: shape: (...).
        """
        q_n = self._sum_of_rewards(rewards_n)
        adv_n = self._compute_advantage(q_n)

        # Advantage Normalization
        if self.normalize_advantages:
            # On the next line, implement a trick which is known empirically to reduce variance
            # in policy gradient methods: normalize adv_n to have mean zero and std=1.
            adv_s = []
            for advantages in adv_n:
                for advantage in advantages:
                    adv_s.append(advantage)
            adv_s = np.array(adv_s)
            mean = adv_s.mean()
            std = adv_s.std()
            adv_n__ = []
            for advantages in adv_n:
                advantages__ = []
                for advantage in advantages:
                    advantages__.append((advantage - mean) / (std + np.finfo(np.float32).eps))
                adv_n__.append(advantages__)
            adv_n = adv_n__
        return q_n, adv_n

    def _loss(self, X, y, adv):
        logits = self.brain(X)
        logprob = - tf.losses.sparse_softmax_cross_entropy(labels=y, logits=logits)
        return logprob * adv

    def update_parameters(self, all_observations, all_actions, all_advantages):
        """
            Update the parameters of the policy.

            arguments:
                all_observations: shape: (...)
                all_actions: shape: (...).
                all_advantages: shape: (...)

            returns:
                nothing
        """
        loss_values = []
        advantages__ = []
        for observations, actions, advantages in zip(all_observations, all_actions, all_advantages):
            grads_by_trajectory = []
            cnt = 1
            for observation, action, advantage in zip(observations, actions, advantages):
                if observation is None or action is None:
                    continue
                with tf.GradientTape() as t:
                    loss_value = - self._loss(observation, [action], advantage)
                # assert loss_value.numpy() == 0

                grads = t.gradient(loss_value, self.brain.variables)
                grads_by_trajectory.append(grads)
                loss_values.append(loss_value)
                advantages__.append(advantage)

                if cnt % 1000 == 0:
                    # assert len(grads_by_trajectory) == 1000
                    self.optimize(grads_by_trajectory)
                    grads_by_trajectory = []
                cnt += 1
            if len(grads_by_trajectory) > 0:
                self.optimize(grads_by_trajectory)

        self.log('loss', np.mean(loss_values), self.global_step)
        self.log('adv', np.mean(advantages__), self.global_step)

    def optimize(self, grads_by_trajectory):
        average_grads = []
        for grads_by_layer in zip(*grads_by_trajectory):
            average_grads.append(np.array([grad.numpy() for grad in grads_by_layer]).mean(axis=0))

        assert len(average_grads) == len(self.brain.variables)
        for average_grad, variable in zip(average_grads, self.brain.variables):
            assert average_grad.shape == variable.shape

        self.optimizer.apply_gradients(zip(average_grads, self.brain.variables), self.global_step)

    def log(self, name, loss_value, step):
        with self.summary_writer.as_default(), tf.contrib.summary.always_record_summaries():
            tf.contrib.summary.scalar(name, loss_value, step=step)
