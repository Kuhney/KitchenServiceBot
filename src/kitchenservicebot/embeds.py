import discord

from kitchenservicebot.save import Save


class SettingsEmbed:
    def __init__(self, save: Save) -> None:
        self.save = save
        workers: str = str([self.save.get_user_by_id(x) for x in self.save.worker_ids])
        helpers: str = str([self.save.get_user_by_id(x) for x in self.save.helper_ids])
        active_worker: str = self.save.get_user_by_id(self.save.current_worker_id)

        if self.save.current_helper_id:
            active_worker += " unterstützt von " + self.save.get_user_by_id(self.save.current_helper_id)

        self.embed = discord.Embed(title="Küchendienst Einstellungen")

        self.embed.add_field(name="Küchendienst der Woche", value=active_worker, inline=False)
        self.embed.add_field(name="Anstehender Küchendienst", value=workers, inline=False)
        self.embed.add_field(name="Mögliche Aushilfe", value=helpers, inline=False)
        self.embed.add_field(
            name="Wechsel am",
            value=self.save.change_time_day.display_name + " um " + str(self.save.change_time_time) + " Uhr",
            inline=False,
        )
