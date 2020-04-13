from lib.Server import Server


def main():
    s = Server(3030)
    s.on_connection(lambda socket:
                    socket.on("test", lambda data: socket.to("Luka").emit("test", "Daa"))
                    )
    s.listen()


if __name__ == "__main__":
    main()
