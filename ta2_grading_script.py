import os
from bs4 import BeautifulSoup

# check for correct html file type
def check_type_html(file_name):
    if not file_name.lower().endswith(".html"):
        print("Error: The file is not an HTML file.")

    with open(file_name, "r") as f:
        html_content = f.read()
        print(f"File: {file_name}\n")
        soup = BeautifulSoup(html_content, "html.parser")
        return soup

    
# 1. Title (this is different than a heading) (50 points)
def check_title():
    title_tag = soup.find("title")
    if title_tag:
        print("The file has a title:", title_tag.text)
    else:
        print("The file does not have a title.")
        

# 2. Headings of two different sizes (ex. h1, h2, h3, etc.) (50 points each)
def check_headings():
    headings = soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])
    heading_sizes = set()
    for heading in headings:
        heading_sizes.add(heading.name)

    if len(heading_sizes) >= 2:
        print("The file contains headings of at least two different sizes:", ", ".join(heading_sizes))
        print("Heading sizes found:", ", ".join(heading_sizes))
    else:
        print("The HTML file does not contain at least two headings of different sizes.")

# 3. Add a tooltip (or "hover box") to your first use of the h1 tag. (50 points)
def check_tooltip():
    h1_tag = soup.find("h1")
    if h1_tag:
        tooltip = h1_tag.get("title")
        h1_class = h1_tag.get("class")
        if tooltip:
            return
        if h1_class and any("tooltip" in cls.lower() for cls in h1_class):
            return
        else:
            # find all <style> tags to extract CSS
            style_tags = soup.find_all("style")
            css_styles = []
            for style_tag in style_tags:
                css_styles.append(style_tag.get_text())

            # check if CSS contains styles for h1:hover or .tooltip class
            for css_style in css_styles:
                if "h1:hover" in css_style or ".tooltip" in css_style:
                    # print("The HTML file contains CSS for h1:hover or .tooltip class.")
                    return
            print("The first <h1> tag in the HTML file does not have a tooltip or hover box.")
            return
    else:
        print("The HTML file does not contain any <h1> tags.")


# 4. Colored background (other than white) (100 points)
def check_colored_background():
    # colored background set in the CSS style tag
    style_tags = soup.find_all("style")
    for style_tag in style_tags:
        if "background-color" in style_tag.text and not "background-color: white" in style_tag.text:
            print("The HTML file has a colored background.")
            return
        # elif "background-color" not in style_tag.text:
            # print("The file does NOT have a colored background.")

    # colored background also be set in the body tag
    body_tags = soup.find_all("body")
    if body_tags:
        for body_tag in body_tags:
            bgcolor = body_tag.get("bgcolor")
            if bgcolor:
                print("The HTML file has a colored background.")
                return
        print("The file does not have a colored background.")


# 5. "Mailto" link to your email address (50 points)
def check_mailto():
    pass


# 6. Hyperlink to another website (must use a URL, not a file path) (50 points)
def check_hyperlink():
    pass


# 7. Bold text and italic text (50 points each)
def check_bold_and_italic():
    pass


# 8. Centered text or photo (50 points)
def check_centered_text_or_photo():
    pass


# 9. Horizontal line (aka "horizontal rule") (50 points)
def check_horizontal_line():
    pass


# 10. Ordered list (numbered list) and unordered list (bulleted list) (50 points each)
def check_ordered_and_unordered_list():
    pass


# 11. A working picture, hosted online. You can link to an existing photo or upload your own image to photo-sharing sites like Google Photos or imgur.com. Make sure the photo is shared properly, and test your page on someone else's device to be certain. (100 points)
def check_picture():
    pass


# 12. Set the width and height of your photo. Recommend 450x600 for portrait layout, or 600x450 for landscape. If your source photo isn't 4:3 aspect ratio, this may look odd. (100 points)
def check_picture_width_height():
    pass


# 13. Add a comment at the very bottom of your source code, listing the tools you used to create this: operating system, text editor, and the web browser you used to test it. (100 points)
def check_comment():
    pass


# Extra Credit: Add a video to your page, using YouTube, Vimeo, or other video hosting service. Find a video, look for the "Share" option, and select "Embed" or "Link" to find a working video link.
def check_extra_credit_video():
    pass


if __name__ == "__main__":
    file_path = input("Enter the path to the HTML file: ")

    soup = check_type_html(file_path)
    if soup:
        check_title() # 1.
        check_headings() # 2.
        check_tooltip() # 3.
        check_colored_background() # 4.
        check_mailto() # 5.
        check_hyperlink() # 6.
        check_bold_and_italic() # 7.
        check_centered_text_or_photo() # 8.
        check_horizontal_line() # 9.
        check_ordered_and_unordered_list() # 10.
        check_picture() # 11.
        check_picture_width_height() # 12.
        check_comment() # 13.
        check_extra_credit_video()
    