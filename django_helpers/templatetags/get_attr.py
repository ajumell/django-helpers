from django import template
from django.conf import settings
from django.template.base import TemplateSyntaxError
from django.template.defaulttags import Node

register = template.Library()
label = settings.PROJECT_LABEL

class GetAttrNode(Node):
    def __init__(self, parser, obj, name):
        Node.__init__(self)
        self.name = name
        self.obj = obj
        self.parser = parser

    def render(self, context):
        p = self.parser
        v = self.obj
        n = self.name
        tkn = p.compile_filter(n)
        n = tkn.resolve(context)
        if n:
            v = str(v) + '.' + str(n)
        v = p.compile_filter(v)
        return v.resolve(context)


class GetMatrixNode(Node):
    def __init__(self, parser, obj, x, y):
        Node.__init__(self)
        self.x = x
        self.y = y
        self.obj = obj
        self.parser = parser

    def compile(self, val, context, s=True):
        p = self.parser
        tkn = p.compile_filter(val)
        k = tkn.resolve(context)
        if s: return str(k)
        return k

    def render(self, context):
        v = self.obj
        x = self.compile(self.x, context)
        y = self.compile(self.y, context)
        v = self.compile(v + '.' + x + '.' + y, context, False)
        return v


@register.tag(name="get_attr")
def get_attr(parser, token):
    bits = token.split_contents()
    if len(bits) != 3:
        raise TemplateSyntaxError("'%s' takes exactly two arguments." % bits[0])
    obj = bits[1]
    name = bits[2]
    return GetAttrNode(parser, obj, name)


@register.tag(name="get_matrix")
def get_attr(parser, token):
    bits = token.split_contents()
    if len(bits) != 4:
        raise TemplateSyntaxError("'%s' takes exactly three arguments." % bits[0])
    obj = bits[1]
    x = bits[2]
    y = bits[3]
    return GetMatrixNode(parser, obj, x, y)
