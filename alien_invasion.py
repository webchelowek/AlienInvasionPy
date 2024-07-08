import sys
from time import sleep
import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats


class AlienInvasion:

    def __init__(self):
        pygame.init()
        self.settings = Settings()
        # Игра Alien Invasion запускается в активном состоянии.
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.ship = Ship(self)
        # Создание экземпляра для хранения игровой статистики.
        self.stats = GameStats(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()
        pygame.display.set_caption("Alien Invasion")

    def run_game(self):
        while True:
            # Отслеживание событий клавиатуры и мыши.
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_aliens()
                self._update_bullets()
            self._update_screen()

    def _create_fleet(self):
        """Создает флот пришельцев."""
        # Создание пришельца и вычисление количества пришельцев в ряду
        # Интервал между соседними пришельцами равен ширине пришельца.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        # """Определяет количество рядов, помещающихся на экране."""
        ship_height = self.ship.rect.height

        available_space_y = (self.settings.screen_height -
                           (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # Создание флота вторжения.
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _ship_hit(self):
        # """Обрабатывает столкновение корабля с пришельцем."""
        if self.stats.ships_left > 0:
            # Уменьшение ships_left.
            self.stats.ships_left -= 1

            # Очистка списков пришельцев и снарядов.
            self.aliens.empty()
            self.bullets.empty()

            # Создание нового флота и размещение корабля в центре.

            self._create_fleet()
            self.ship.center_ship()

            # Пауза.
            sleep(0.5)
        else:
            self.stats.game_active = False

    def _update_aliens(self):
        # """Обновляет позиции всех пришельцев во флоте."""
        self.aliens.update()
        self._check_fleet_edges()
        # Проверить, добрались ли пришельцы до нижнего края экрана.
        self._check_aliens_bottom()
        # Проверка коллизий "пришелец — корабль".
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

    def _check_aliens_bottom(self):
        # """Проверяет, добрались ли пришельцы до нижнего края экрана."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Происходит то же, что при столкновении с кораблем.
                self._ship_hit()
                break

    def _create_alien(self, alien_number, row_number):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        # """Реагирует на достижение пришельцем края экрана."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        # """Опускает весь флот и меняет направление флота."""
        self.settings.fleet_direction *= -1
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed

    def _update_bullets(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        # Проверка попаданий в пришельцев.
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        # """Обработка коллизий снарядов с пришельцами."""
        # Удаление снарядов и пришельцев, участвующих в коллизиях.
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)
        if not self.aliens:
            # Уничтожение существующих снарядов и создание нового флота.
            self.bullets.empty()
            self._create_fleet()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)

            if event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        match event.key:
            case pygame.K_LEFT:
                self.ship.moving_left = True
            case pygame.K_RIGHT:
                self.ship.moving_right = True
            case pygame.K_DOWN:
                self.ship.moving_down = True
            case pygame.K_UP:
                self.ship.moving_up = True
            case pygame.K_q:
                sys.exit()
            case pygame.K_SPACE:
                self._fire_bullet()

    def _check_keyup_events(self, event):
        match event.key:
            case pygame.K_LEFT:
                self.ship.moving_left = False
            case pygame.K_RIGHT:
                self.ship.moving_right = False
            case pygame.K_DOWN:
                self.ship.moving_down = False
            case pygame.K_UP:
                self.ship.moving_up = False

    def _fire_bullet(self):
        # """Создание нового снаряда и включение его в группу bullets."""
        new_bullet = Bullet(self)
        self.bullets.add(new_bullet)

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        # Отображение последнего прорисованного экрана.
        pygame.display.flip()


if __name__ == '__main__':
    # Создание экземпляра и запуск игры.
    ai = AlienInvasion()
    ai.run_game()
