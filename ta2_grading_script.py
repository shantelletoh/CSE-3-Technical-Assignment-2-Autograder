import os
from bs4 import BeautifulSoup
import re

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
        print("The file does not contain at least two headings of different sizes.")

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
                    # print("The file contains CSS for h1:hover or .tooltip class.")
                    return
            print("The first <h1> tag in the file does not have a tooltip or hover box.")
            return
    else:
        print("The file does not contain any <h1> tags.")


# 4. Colored background (other than white) (100 points)
def check_colored_background():
    # colored background set in the CSS style tag
    style_tags = soup.find_all("style")
    for style_tag in style_tags:
        if "background-color" in style_tag.text and not "background-color: white" in style_tag.text:
            print("The file has a colored background.")
            return
        # elif "background-color" not in style_tag.text:
            # print("The file does NOT have a colored background.")

    # colored background also be set in the body tag
    body_tags = soup.find_all("body")
    if body_tags:
        for body_tag in body_tags:
            bgcolor = body_tag.get("bgcolor")
            if bgcolor:
                print("The file has a colored background.")
                return
        print("The file does not have a colored background.")


# 5. "Mailto" link to your email address (50 points)
def check_mailto():
    a_tags = soup.find_all("a", href=True)
    for a_tag in a_tags:
        href = a_tag["href"]
        if href.lower().startswith("mailto:"):
            email_match = re.match(r"^mailto:([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,})$", href, re.IGNORECASE)
            return
            # if email_match:
                # email_address = email_match.group(1)
                # print(f"Found email address in "{file_name}": {email_address}")
            # else:
                # print("No valid email address found.")
        # else:
    print(f"The file does NOT have a \"mailto\" link to your email address.")


# 6. Hyperlink to another website (must use a URL, not a file path) (50 points)
def check_hyperlink():
    anchor_tags = soup.find_all("a", href=True)

    for anchor_tag in anchor_tags:
        url = anchor_tag["href"]
        # Check if the URL is a valid HTTP or HTTPS link
        if re.match(r"^https?://", url):
            # print("The file contains a hyperlink to another website.")
            # print("URL:", url)
            return
    print("The file does not contain a hyperlink to another website.")


# 7. Bold text and italic text (50 points each)
def check_bold_and_italic():
    bold_tags = soup.find_all(['b', 'strong']) # Find all bold and strong tags
    italic_tags = soup.find_all(['i', 'em']) # Find all italic and emphasis tags
    # if bold_tags:
        # print("The file contains bold text.")
    if not bold_tags:
        print("The file does not contain bold text.")

    # if italic_tags:
        # print("The file contains italic text.")
    if not italic_tags:
        print("The file does not contain italic text.")


# 8. Centered text or photo (50 points)
def check_centered_text_or_photo():
    style_tag = soup.find("style")
    if style_tag:
        style_text = style_tag.get_text()
        if "text-align: center" in style_text:
            return

    centered_elements_html = soup.find_all("center")
    centered_text_elements_css = soup.find_all(style=lambda value: value and "text-align: center" in value) # Find all elements with text-align: center; style
    centered_img_elements_css = soup.find_all("img", style=lambda value: value and "margin: auto" in value) # Find all img tags with margin: auto; style
    # print("type of centered_elements:", type(centered_elements_html))


    # commented code not working
    # style_pattern = r"<style[^>]*>(.*?)<\/style>"
    # style_matches = re.findall(style_pattern, file_path, re.DOTALL)
    
    # # Check each match for text-align: center;
    # for style_match in style_matches:
    #     if "text-align: center;" in style_match:
    #         print("hi")
    #         return
        
    
    
    if not centered_elements_html and not centered_text_elements_css and not centered_img_elements_css:
        # print(f"The file "{file_name}" contains centered content.")
    # else:
        print(f"The file does not contain centered content.")


# 9. Horizontal line (aka "horizontal rule") (50 points)
def check_horizontal_line():
    horizontal_lines = soup.find_all("hr")
    if not horizontal_lines:
        # print("The file contains horizontal lines (horizontal rules).")
    # else:
        print("The file does not contain horizontal lines (horizontal rules).")


# 10. Ordered list (numbered list) and unordered list (bulleted list) (50 points each)
def check_ordered_and_unordered_list():
    ordered_lists = soup.find_all("ol")
    unordered_lists = soup.find_all("ul")
    if not ordered_lists:
        print("The file does not contain ordered lists (numbered lists).")

    if not unordered_lists:
        print("The file does not contain unordered lists (bulleted lists).")


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
    