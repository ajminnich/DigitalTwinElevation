from src.gui.TankAnimator import TankAnimator
from src.gui.TankAnimatorElevation import TankAnimatorElevation

def main():
    ta = TankAnimator()
    ta.animate()

def mainElev():
    ta = TankAnimatorElevation()
    ta.animate()

if __name__ == '__main__':
    main()