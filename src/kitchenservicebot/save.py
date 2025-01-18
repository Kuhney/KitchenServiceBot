import json

from kitchenservicebot.enums import Weekday


class Save:
    worker_ids: list[int] = []
    current_worker_id: int | None = None
    helper_ids: list[int] = []
    current_helper_id: int | None = None
    change_time_day: Weekday = Weekday.MONDAY
    change_time_time: int = 0
    week_idx: int = 0
    channel = None

    def __init__(self) -> None:
        self.load_save_file()

    def load_save_file(self) -> None:
        try:
            with open("savefile.json") as savefile:
                save_dict = json.load(savefile)
                self.worker_ids = save_dict["workers"]
                self.current_worker_id = save_dict["current_worker"]
                self.helper_ids = save_dict["helper"]
                self.change_time_day = Weekday(value=save_dict["day"])
                self.change_time_time = save_dict["time"]
                self.week_idx = save_dict["week_idx"]
                self.channel = save_dict["channel"]
        except FileNotFoundError:
            print("No savefile found. Created one")
            self.save_to_file()

    def save_to_file(self) -> None:
        with open("savefile.json", "w") as savefile:
            json.dump(
                {
                    "workers": self.worker_ids,
                    "current_worker": self.current_worker_id,
                    "helper": self.helper_ids,
                    "day": self.change_time_day.value,
                    "time": self.change_time_time,
                    "week_idx": self.week_idx,
                    "channel": self.channel,
                },
                savefile,
                indent=4,
            )
            savefile.close()
        print("Saved configuration to file")

    def get_user_by_id(self, idx: int) -> str:
        return "<@" + str(idx) + ">"

    def skip_to_new_week(self) -> None:
        self.week_idx += 1

        self.current_worker_id = self.worker_ids[0]
        self.worker_ids.append(self.worker_ids[0])
        self.worker_ids.pop(0)

        if self.week_idx % (len(self.worker_ids) + 1) == 0:
            self.current_helper_id = self.helper_ids[0]
        elif self.current_helper_id is not None:
            self.current_helper_id = None
        self.save_to_file()
