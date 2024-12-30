from htmtl import Htmtl


def main():
    print(Htmtl("<div inner-text=\"hello\">asdasd</div>").html())


if __name__ == "__main__":
    main()
