# utils.py
import json
import time
from pathlib import Path
import global_variable as gv
from game_class.upgrade import UPGRADES, Upgrade_Type

def save_game():
    date = time.strftime("%d-%m-%Y %H-%M-%S", time.gmtime())

    base_dir = Path(__file__).resolve().parent
    save_dir = base_dir / "save_files"
    save_dir.mkdir(parents=True, exist_ok=True)

    file_path = save_dir / f"{date}.json"

    upgrade_data = [
        {
            "cost": u.cost,
            "value": u.value,
            "remaining_level": u.remaining_level,
        }
        for u in UPGRADES
    ]

    data = {
        "upgrades": upgrade_data,
        "points": gv.points,
        "player_size": gv.player_size,
        "player_max_speed": gv.player_max_speed,
        "player_health": gv.player_health,
        "ball_size": gv.ball_size,
        "ball_value": gv.ball_value,
        "max_ball_on_screen": gv.max_balls_on_screen,
        "round_time": gv.round_time
    }

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def load_game() -> bool:
    base_dir = Path(__file__).resolve().parent
    save_dir = base_dir / "save_files"
    if not save_dir.exists():
        return False

    save_files = sorted(save_dir.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not save_files:
        return False

    latest_save = save_files[0]
    with open(latest_save, "r", encoding="utf-8") as f:
        data = json.load(f)

    gv.points = data.get("points", gv.points)
    gv.player_size = data.get("player_size", gv.player_size)
    gv.player_max_speed = data.get("player_max_speed", gv.player_max_speed)
    gv.player_health = data.get("player_health", gv.player_health)
    gv.ball_size = data.get("ball_size", gv.ball_size)
    gv.ball_value = data.get("ball_value", gv.ball_value)
    gv.max_balls_on_screen = data.get("max_ball_on_screen", gv.max_balls_on_screen)
    gv.round_time = data.get("round_time", gv.round_time)

    saved_upgrades = {
        u.get("name"): u for u in data.get("upgrades", []) if isinstance(u, dict) and "name" in u
    }

    for upgrade in UPGRADES:
        saved = saved_upgrades.get(upgrade.name)
        if not saved:
            continue

        upgrade.cost = saved.get("cost", upgrade.cost)
        upgrade.value = saved.get("value", upgrade.value)
        upgrade.remaining_level = saved.get("remaining_level", upgrade.remaining_level)
