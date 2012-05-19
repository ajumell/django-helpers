from django.template.loader_tags import do_include, BaseIncludeNode
from helpers import remove_breaks
from django import template

register = template.Library()

class SpacelessIncludeNode(BaseIncludeNode):
    def __init__(self, template, *args, **kwargs):
        BaseIncludeNode.__init__(self, *args, **kwargs)
        self.template = template

    def render(self, context):
        if not self.template:
            return ''
        op = self.render_template(self.template, context)
        return remove_breaks(op)


@register.tag('spaceless_include')
def spaceless_include(parser, token):
    node = do_include(parser, token)
    args_dict = {
        "extra_context": node.extra_context,
        "isolated_context": node.isolated_context,
        "template": node.template
    }
    return SpacelessIncludeNode(**args_dict)