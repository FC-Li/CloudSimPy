from core import job as job_module
from playground.DAG.utils.feature_synthesize import task_features


# One way to add feature property
# class Task(job_module.Task):
#     def __init__(self, env, job, task_config):
#         super().__init__(env, job, task_config)
#         self._features = None
#
#     @property
#     def feature(self):
#         self._features = self.job.features[self.task_index]
#         return self._features
#
#
# job_module.Job.task_cls = Task


# One way (Ends)


# Another way to add feature property
def feature(self):
    self._features = self.job.features[self.task_index]
    return self._features


setattr(job_module.Task, 'feature', property(feature))


# Another way (Ends)


class Job(job_module.Job):
    def __init__(self, env, job_config):
        super().__init__(env, job_config)
        self.features = task_features(self)
