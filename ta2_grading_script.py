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


if __name__ == "__main__":
    file_path = input("Enter the path to the HTML file: ")

    soup = check_type_html(file_path)
    if soup:
        check_title()
        check_headings()
        check_tooltip()
    
    print("\n\n\n")