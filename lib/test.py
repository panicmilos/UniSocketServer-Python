from Server import Server


def main():
    s = Server(3030)
    s.listen()


if __name__ == "__main__":
    main()