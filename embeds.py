import discord

from save import Save


class SettingsEmbed:
    def __init__(self, save: Save):
        self.save = save
        workers: str = str(list(map(lambda x: self.save.get_user_by_id(x), self.save.worker_ids)))
        helpers: str = str(list(map(lambda x: self.save.get_user_by_id(x), self.save.helper_ids)))
        active_worker: str = self.save.get_user_by_id(self.save.current_worker_id)

        if self.save.current_helper_id:
            active_worker += " unterstützt von " + self.save.get_user_by_id(self.save.current_helper_id)

        self.embed = discord.Embed(title="Küchendienst Einstellungen")

        self.embed.add_field(name="Aktiver Küchendienst",
                             value=active_worker,
                             inline=False)
        self.embed.add_field(name="Helfer", value=workers, inline=False)
        self.embed.add_field(name="Aushilfe", value=helpers, inline=False)
        self.embed.add_field(name="Wechsel am",
                             value=self.save.change_time_day.display_name + " um " + str(
                                 self.save.change_time_time) + " Uhr",
                             inline=False)
