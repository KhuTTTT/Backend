from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
import make_quizz
import pts
from dotenv import load_dotenv
from io import BytesIO
from supabase import create_client, Client
import os
from datetime import datetime
import numpy as np
import pandas as pd
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
import warnings




load_dotenv()
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

class PPT:
    def __init__(self):
        self.presentation = Presentation()

    def add_title_slide(self, title):
        title_slide_layout = self.presentation.slide_layouts[0]
        title_slide = self.presentation.slides.add_slide(title_slide_layout)
        title_shape = title_slide.shapes.title
        title_shape.text = title
        title_shape.text_frame.paragraphs[0].font.size = Pt(44)
        title_shape.text_frame.paragraphs[0].font.bold = True

    def add_content_slide(self, title, content):
        content_slide_layout = self.presentation.slide_layouts[1]
        content_slide = self.presentation.slides.add_slide(content_slide_layout)
        title_shape = content_slide.shapes.title
        content_shape = content_slide.placeholders[1]

        title_shape.text = title
        content_shape.text = content
        title_shape.text_frame.paragraphs[0].font.size = Pt(32)
        content_shape.text_frame.paragraphs[0].font.size = Pt(24)

    def add_image_slide(self, title, image):
        image_slide_layout = self.presentation.slide_layouts[5]
        image_slide = self.presentation.slides.add_slide(image_slide_layout)
        title_shape = image_slide.shapes.title

        left = Inches(1.5)        # x좌표
        top = Inches(1.8)        # y좌표
        width = Inches(7)     # 이미지 가로 길이
        height = Inches(5)  # 이미지 세로 길이

        image_slide.shapes.add_picture(image, left, top, width, height)
        title_shape.text = title
        title_shape.text_frame.paragraphs[0].font.size = Pt(32)


    def create_presentation(self, path):
        summary_string = pts.PdfToString(path)
        wordcloud = WordCloud().generate(summary_string)

        plt.figure()
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")

        # Save the plot to a file
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
        output_file = f"{timestamp}.png"  # Specify your desired output file name and format
        plt.savefig(output_file, bbox_inches='tight', pad_inches=0.2)

        # Optional: Close the plot to release resources (comment this line if you want to display the plot)
        plt.close()

        supabase.storage.from_("url").upload(file=output_file, path=output_file, file_options={"content-type": "image/png"})
        res_image = supabase.storage.from_('url').get_public_url(output_file)

        summary_string = make_quizz.summary(summary_string)
        summary_string_list = summary_string.split("\n\n")

        for i in range(len(summary_string_list)+1):
            if i == 0:
                self.add_title_slide(summary_string_list[i].split(": ")[1])
            elif i > 0 and i < len(summary_string_list):
                data = summary_string_list[i].split(": ")
                self.add_content_slide(data[0], data[1])
            else:
                self.add_image_slide("WordCloud", output_file)

        timestamp1 = datetime.now().strftime("%Y%m%d%H%M%S%f")
        name = f"{timestamp1}.pptx"
        self.presentation.save(name)

        supabase.storage.from_("url").upload(file=name, path=name, file_options={"content-type": "application/vnd.ms-powerpoint"})
        res = supabase.storage.from_('url').get_public_url(name)

        return {"res": res, "res_image": res_image}

# Example usage:

#ppt_generator = PPT()
#ppt_generator.create_presentation("ue.pdf")
