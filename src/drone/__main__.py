
import sys
import drone
from drone.balloon import balloon


def main(game: str = "balloon") -> None:
    """
    Runs the selected game.

    Args:
        game (str): The game to run (balloon, snowglobe)
    """
    if game == "balloon":
        balloon()
    else:
        print(f"Unknown tracking library: {game} (expected: balloon)")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main()
