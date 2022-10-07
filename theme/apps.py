from django.apps import AppConfig
import os


class ThemeConfig(AppConfig):
    name = 'theme'
    def ready(self):
        run_once = os.environ.get('CMDLINERUNNER_RUN_ONCE') 
        if run_once is not None:
            return
        os.environ['CMDLINERUNNER_RUN_ONCE'] = 'True' 
        from .gym_scheduler import smsGymScheduler
        print('scheduler start ......')
        smsGymScheduler.start_scheduler()