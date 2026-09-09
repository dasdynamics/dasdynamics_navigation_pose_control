# dasdynamics_navigation_pose_control
Navigation pose control repository.

## Описание репозитория: 'dasdynamics_navigation'

Репозиторий содержит ROS 2-пакет с файлами запуска и конфигурационными файлами для навигации робота в среде Gazebo.

Так-же репозиторий содержит ноды, добавляющие дополнительный функционал.
К ним относится:
 - 'waypoints_control_node' - нода подписывается на топик "/user_command" и при получении команды "save_waypoint:<name>" - сохраняет текущее положение робота на карте мира. Команда "go_to_waypoint:<name>" - отправляет робота на сохраненную точку.

 Примечание: Файл, в который происходит сохранение точек не ориентируется на название карты. Если изменилась карта, или сместилась точка отсчета на текущей карте, сохраненные точки будут иметь недостоверные координаты.

***

## Требования и установка

Для работы пакета требуется установленный ROS 2. В данном случае используется дистрибутив **ROS 2 Lyrical**.

так - же необходимо установить пакеты навигации и slam:
```bash
sudo apt install ros-lyrical-slam-toolbox
sudo apt install ros-lyrical-twist-mux
sudo apt install ros-lyrical-nav2-controller
sudo apt install ros-lyrical-nav2-planner
sudo apt install ros-lyrical-nav2-behaviors
sudo apt install ros-lyrical-nav2-bt-navigator
sudo apt install ros-lyrical-nav2-lifecycle-manager
sudo apt install ros-lyrical-nav2-regulated-pure-pursuit-controller
sudo apt install ros-lyrical-nav2-navfn-planner
```

### Зависимости

Также необходимо иметь подготовленный пакет симуляции робота. Для тестирования можно использовать пакет `dasdynamics_simulation`, который можно колнировать с помощью команды:

```bash
git clone https://github.com/dasdynamics/dasdynamics_simulation.git
```
***

## Быстрый запуск

После сборки пакета для быстрого запуска используйте следующую команду:

```bash
ros2 launch dasdynamics_navigation navigation.launch.py
```

***

## Настройка параметров запуска

Основные параметры запуска можно изменить, отредактировав файл `navigation.launch.py`.

### Доступные для изменения параметры:

- `slam_pkg_name` — имя робота в симуляции

- `simulation_pkg_name` — название пакета Slam (для совместимости с устаревшими или новыми версиями)
- `navigation_pkg_name` — название пакета симуляции робота
- `rviz2_config_file_name` — название файла конфигурации RViz2

> **Примечание:** Для редактирования откройте файл запуска `navigation.launch.py` в директории `launch` и измените параметры на соответствующие вашему проекту.

> Если функционала пакета будет недостаточно, вам потребуется изменить основную часть файла запуска или один из конфигурационных файлов в директории `config`.

***

## Структура репозитория

```
config/
    mapper_params_online_async.yaml — параметры ToolBox
    nav2_params.yaml    — параметры навигации робота
    twist_mux_params.yaml   — параметры TwistMux (сейчас не активны, но могут пригодиться в будущем)


launch/
    simulation.launch.py           — основной файл запуска пакета

dasdynamics_navigation/
    waypoints_control_node.py      — описание мира для симуляции в Gazebo
rviz/
    rviz2_navigation_config.rviz    — конфигурационный файл для запуска RViz2
```

***

## Новости разработки

Последние новости о разработке проекта публикуются в группе ВКонтакте:

- **ВКонтакте:** [ДАС Динамика](https://vk.ru/dasdynamics)

***

## Контакты

Если у вас остались вопросы, вы можете связаться по следующим контактам:

- **Почта:** [das-dev-md@mail.com](mailto:das-dev-md@mail.com)
- **Telegram:** [@das_dev_tg](https://t.me/das_dev_tg)

***

