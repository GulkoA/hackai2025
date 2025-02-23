from humanoid import Humanoid

class HumanoidManager():
  def __init__(self):
    # maps id to Humanoid
    self.humanoids: dict[int, Humanoid] = {}


  