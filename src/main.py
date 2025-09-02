from textnode import TextNode, TextType

def main():
    print("hello world")
    demo = TextNode(
        text="This is some anchor text",
        text_type=TextType.LINK,
        url="https://www.boot.dev",
    )
    print(demo)  # -> TextNode(This is some anchor text, link, https://www.boot.dev)

if __name__ == "__main__":
    main()
