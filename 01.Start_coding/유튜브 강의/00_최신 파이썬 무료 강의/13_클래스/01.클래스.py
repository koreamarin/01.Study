class Monster :
    def __init__(self, name, age) :
        self.name = name
        self.age = age
    
    def say(self):
        print(f'나는 {self.name}! {self.age}살임')

shark = Monster('상어', 7)
wolf = Monster('늑대', 4)

shark.say()
wolf.say()
