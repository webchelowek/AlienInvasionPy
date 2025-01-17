class GameStats():
    # """Отслеживание статистики для игры Alien Invasion."""

    def __init__(self, ai_game):
        # """Инициализирует статистику."""
        self.settings = ai_game.settings
        self.reset_stats()
        self.game_active = True

    def reset_stats(self):
        # """Инициализирует статистику, изменяющуюся в ходе игры."""
        self.ships_left = self.settings.ship_limit
        self.score = 0