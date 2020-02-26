#!/usr/bin/env python3


class Program():

    def __init__(self):
        pass

    def method1(self):
        print("Success!")
    
    def method2(self):
        self.method1()


if __name__ == "__main__":
    main = Program()
    main.method2()
