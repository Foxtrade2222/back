import pydf
from django.template.loader import get_template


def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html = template.render(context_dict)
    pdf = pydf.generate_pdf(
        html,
        orientation="Landscape",
        page_size="Letter",
    )
    return pdf
