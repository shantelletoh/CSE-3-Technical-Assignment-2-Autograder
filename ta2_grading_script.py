import os
from bs4 import BeautifulSoup, Comment
import re
import requests
import base64
import csv

# check for correct html file type
def check_type_html(file_name):
    global total_score
    if not file_name.lower().endswith(".html"):
        print("Error: The file is not an HTML file.")
        print("Total Score: 0")
        print("Please email your assignment with the correct .html file ending to your TA so it can be graded.")
        total_score -= 1000
        return

    with open(file_name, "r", encoding="utf-8") as f:
        html_content = f.read()
        print(f"File: {file_name}\n")
        soup = BeautifulSoup(html_content, "html.parser")
        return soup

    
# 1. Title (this is different than a heading) (50 points)
def check_title():
    global total_score
    title_tag = soup.find("title")
    if title_tag is None:
        print("-50: The file does not have a title.")
        total_score -= 50
        

# 2. Headings of two different sizes (ex. h1, h2, h3, etc.) (50 points each)
def check_headings():
    global total_score
    headings = soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])
    heading_sizes = set()
    for heading in headings:
        heading_sizes.add(heading.name)

    if len(heading_sizes) == 1:
        print("-50: The HTML file contains only headings of one size (instead of two different sizes): ", ", ".join(heading_sizes))
        total_score -= 50
        
    elif len(heading_sizes) < 1:
        print("-100: The file does not contain at least two headings of different sizes.")
        total_score -= 100

# 3. Add a tooltip (or "hover box") to your first use of the h1 tag. (50 points)
def check_tooltip():
    global total_score
    h1_tag = soup.find("h1")
    if h1_tag:
        nested_tags_with_title = h1_tag.find_all(lambda tag: tag.has_attr("title"))
        tooltip = h1_tag.get("title")
        h1_class = h1_tag.get("class")
        if tooltip or len(nested_tags_with_title) > 0:
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
                    return
            print("-50: The first <h1> tag in the file does not have a tooltip or hover box.")
            total_score -= 50
            return
    else:
        print("The file does not contain any <h1> tags.")
        total_score -= 50


# 4. Colored background (other than white) (100 points)
def check_colored_background():
    global total_score
    # colored background set in the CSS style tag
    style_tags = soup.find_all("style")
    for style_tag in style_tags:
        if "background-color" in style_tag.text and not "background-color: white" in style_tag.text:
            return

    # colored background also be set in the body tag
    body_tags = soup.find_all("body")
    if body_tags:
        for body_tag in body_tags:
            bgcolor = body_tag.get("bgcolor")
            if bgcolor:
                return
            elif body_tag.has_attr("style") and "background-color" in body_tag["style"]:
                return
        print("-100: The file does not have a colored background.")
        total_score -= 100


# 5. "Mailto" link to your email address (50 points)
def check_mailto():
    global total_score
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
    print(f"-50: The file does NOT have a \"mailto\" link to your email address.")
    total_score -= 50


# 6. Hyperlink to another website (must use a URL, not a file path) (50 points)
def check_hyperlink():
    global total_score
    anchor_tags = soup.find_all("a", href=True)

    for anchor_tag in anchor_tags:
        url = anchor_tag["href"]
        # Check if the URL is a valid HTTP or HTTPS link
        if re.match(r"^https?://", url):
            return
    print("-50: The file does not contain a hyperlink to another website.")
    total_score -= 50


# 7. Bold text and italic text (50 points each)
def check_bold_and_italic():
    global total_score
    bold_tags = soup.find_all(["b", "strong"]) # Find all bold and strong tags
    italic_tags = soup.find_all(["i", "em"]) # Find all italic and emphasis tags
    if not bold_tags:
        print("-50: The file does not contain bold text.")
        total_score -= 50

    if not italic_tags:
        print("-50: The file does not contain italic text.")
        total_score -= 50


# 8. Centered text or photo (50 points)
def check_centered_text_or_photo():
    global total_score
    style_tag = soup.find("style")
    if style_tag:
        style_text = style_tag.get_text()
        if "text-align: center" in style_text:
            return

    centered_elements_html = soup.find_all("center")
    centered_text_elements_css = soup.find_all(style=lambda value: value and "text-align: center" in value) # Find all elements with text-align: center; style
    centered_img_elements_css = soup.find_all("img", style=lambda value: value and "margin: auto" in value) # Find all img tags with margin: auto; style
    
    
    if not centered_elements_html and not centered_text_elements_css and not centered_img_elements_css:
        print(f"-50: The file does not contain centered content.")
        total_score -= 50


# 9. Horizontal line (aka "horizontal rule") (50 points)
def check_horizontal_line():
    global total_score
    horizontal_lines = soup.find_all("hr")
    if not horizontal_lines:
        print("-50: The file does not contain horizontal lines (horizontal rules).")
        total_score -= 50


# 10. Ordered list (numbered list) and unordered list (bulleted list) (50 points each)
def check_ordered_and_unordered_list():
    global total_score
    
    # li tags without parent count as unordered lists, so don't deduct points if there are such li tags
    check_unordered = True
    li_tags = soup.find_all("li")
    if len(li_tags) > 0:
        for li in li_tags:
            if li.find_parent(["ul", "ol"]) is None: # li tag has no ul or ol parent tag
                check_unordered = False
    
    ordered_lists = soup.find_all("ol")
    unordered_lists = soup.find_all("ul")
    if not ordered_lists:
        print("-50: The file does not contain ordered lists (numbered lists).")
        total_score -= 50

    if check_unordered and not unordered_lists:
        print("-50: The file does not contain unordered lists (bulleted lists).")
        total_score -= 50


# 11. A working picture, hosted online. You can link to an existing photo or upload your own image to photo-sharing sites like Google Photos or imgur.com. Make sure the photo is shared properly, and test your page on someone else's device to be certain. (100 points)
def check_picture():
    global total_score
    picture_tags = soup.find_all("img")

    for picture_tag in picture_tags:
        src = picture_tag.get("src")
        print("src:", src)

        if src is None:
            print("-100: The file does not contain a working picture hosted online.")
            total_score -= 100
            return
        
        # allow encoded images
        if src.startswith("data:image/"):
            encoded_data = re.search(r"base64,(.*)", src).group(1)
            base64.b64decode(encoded_data)
            return
            
        elif src.startswith("https://i.imgur.com/"): # special case so it won't give too many requests error
            return
        
        else:
            try:
                response = requests.head(src)
                print("src:", src)
                print("response:", response)
                print("response.status_code:", response.status_code)
                if response.status_code == 200:
                    print("The file contains a working picture hosted online:")
                    print("Image URL:", src)
                    return
            except Exception as e:
                print("-100: The file does not contain a working picture hosted online.")
                total_score -= 100
                return
    print("-100: The file does not contain a working picture hosted online.")
    total_score -= 100


# 12. Set the width and height of your photo. Recommend 450x600 for portrait layout, or 600x450 for landscape. If your source photo isn't 4:3 aspect ratio, this may look odd. (100 points)
def check_picture_width_height():
    global total_score
    picture_tags = soup.find_all("img")

    for picture_tag in picture_tags:
        width = picture_tag.get("width")
        height = picture_tag.get("height")
        if width and height:
            return
        inline_style = picture_tag.get("style")
        if inline_style and ("width" in inline_style) and ("height" in inline_style):
            return
    
    # find all <style> tags to extract CSS
    style_tags = soup.find_all("style")
    css_styles = []
    for style_tag in style_tags:
        css_styles.append(style_tag.get_text())

    # check if CSS contains width and height styles for img and image classes
    for css_style in css_styles:
        if "img" in css_style and ("width" in css_style and "height" in css_style):
            return
        if "image" in css_style and ("width" in css_style and "height" in css_style):
            return
    
    print("-100: The file does not contain an image with both width and height attributes set.")
    total_score -= 100


# 13. Add a comment at the very bottom of your source code, listing the tools you used to create this: operating system, text editor, and the web browser you used to test it. (100 points)
def check_comment():
    global total_score
    comments = soup.find_all(string=lambda text: isinstance(text, Comment))
    for comment in comments:
        words = comment.strip().split()
        if len(words) >= 3:
            return

    comment_pattern = r"<!--\s*(?:\w+\W+){2,}"
    matches = soup.find_all(string=lambda text: re.search(comment_pattern, str(text)))
    if len(matches) > 0:
        return

    print("-100: The file does NOT contain a comment for the tools used.")
    total_score -= 100


# Extra Credit: Add a video to your page, using YouTube, Vimeo, or other video hosting service. Find a video, look for the "Share" option, and select "Embed" or "Link" to find a working video link.
def check_extra_credit_video():
    global total_score
    iframe_tags = soup.find_all("iframe")

    for iframe_tag in iframe_tags:
        src = iframe_tag.get("src")
        if src and ("youtube.com/embed" in src or "player.vimeo.com/video" in src):
            print("+100 extra credit: The file contains a video from a video hosting service.")
            print("Video URL:", src)
            total_score += 100
            return


if __name__ == "__main__":
    
    output_file = "student_scores.csv"
    with open(output_file, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)

        folder_path = "./TA2_Submissions/"
        submissions_folder = sorted(os.listdir(folder_path)) # Get a list of all files in the folder in alphabetical order
        for file_name in submissions_folder:
            total_score = 1000
            
            file_path = os.path.join(folder_path, file_name)
            parts = file_name.split("_")
            prefix = parts[0] # prefix (before 1st underscore) is lastnamefirstname of student

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
            
            print("\n\n\n")

            writer.writerow([prefix, total_score])