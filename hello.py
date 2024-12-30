from htmtl import Htmtl


def main():
    print(Htmtl("<div inner-text=\"hello {something}\">asdasd</div>", {'something': 'nothing'}).html())


if __name__ == "__main__":
    main()
