from apscheduler.schedulers.asyncio import AsyncIOScheduler


class WeeklyScheduler:
    def __init__(self, job_func, save):
        self.save = save
        self.job_func = job_func
        self.scheduler = AsyncIOScheduler()
        self.update_jobs()

    def start_schedule(self):
        self.scheduler.start()

    def update_jobs(self):
        print("Updated Job Schedule")
        self.save.load_save_file()
        self.scheduler.remove_all_jobs()
        self.scheduler.add_job(self.job_func, 'cron', day_of_week=self.save.change_time_day.cron,
                               hour=self.save.change_time_time)
