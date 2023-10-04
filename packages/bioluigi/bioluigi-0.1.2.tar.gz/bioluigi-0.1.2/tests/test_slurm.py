import luigi
from bioluigi.scheduled_external_program import ScheduledExternalProgramTask

class Success(ScheduledExternalProgramTask):
    scheduler = 'slurm'
    def program_args(self):
        return ['true']

    def complete(self):
        return self.run()

luigi.build([Success()], workers=1, local_scheduler=True)
