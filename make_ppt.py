from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
import make_quizz
import pts

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

    def create_presentation(self, path):
        summary_string = pts.PdfToString(path)
        summary_string = make_quizz.summary(summary_string)
        summary_string_list = summary_string.split("\n\n")

        for i in range(len(summary_string_list)):
            if i == 0:
                self.add_title_slide(summary_string_list[i].split(": ")[1])
            else:
                data = summary_string_list[i].split(": ")
                self.add_content_slide(data[0], data[1])

        self.presentation.save(summary_string_list[0].split(": ")[1] + ".pptx")
        return summary_string_list[0].split(": ")[1] + ".pptx"

# Example usage:
# ppt_generator = PPT()
# ppt_generator.create_presentation("your_pdf_path.pdf")
