import json

from enums import Weekday


class Save:
    worker_ids: list[int] = []
    current_worker_id: int = None
    helper_ids: list[int] = []
    current_helper_id: int = None
    change_time_day: Weekday = Weekday.MONDAY
    change_time_time: int = 0

    def __init__(self):
        self.load_save_file()

    def load_save_file(self):
        try:
            with open("savefile.json", "r") as savefile:
                save_dict = json.load(savefile)
                self.worker_ids = save_dict["workers"]
                self.current_worker_id = save_dict["current_worker"]
                self.helper_ids = save_dict["helper"]
                self.change_time_day = Weekday(value=save_dict["day"])
                self.change_time_time = save_dict["time"]
        except FileNotFoundError:
            print("No savefile found. Created one")
            self.save_to_file()

    def save_to_file(self):
        with open("savefile.json", "w") as savefile:
            json.dump(
                {
                    "workers": self.worker_ids,
                    "current_worker": self.current_worker_id,
                    "helper": self.helper_ids,
                    "day": self.change_time_day.value,
                    "time": self.change_time_time
                },
                savefile,
                indent=4
            )
            savefile.close()
        print("Saved configuration to file")

    def get_user_by_id(self, id: int) -> str:
        return "<@" + str(id) + ">"

    def skip_to_new_week(self):
        worker_pos = self.worker_ids.index(self.current_worker_id)
        if worker_pos+1 >= len(self.worker_ids):
            self.current_worker_id = self.worker_ids[0]
        else:
            self.current_worker_id = self.worker_ids[worker_pos+1]

        self.save_to_file()
