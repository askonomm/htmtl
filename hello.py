from htmtl import Htmtl


def main():
    Htmtl("<!DOCTYPE html><html><head></head><body><div>as<img>more text goes here</div></body></html>").toHtml()


if __name__ == "__main__":
    main()
