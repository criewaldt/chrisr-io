

class Something():
    def __init__(self, something):
        print('something init')
        self.something = something
        


if __name__ == "__main__":
    s = Something('text goes here')
    print(s.something)