from django import template

class LogNode(template.Node):
    def __init__(self, obj):
        self.obj = obj

    def render(self, context):
        obj = self.obj.resolve(context, True)
        print obj
        return ''


def do_log(parser, token):
    bits = token.contents.split()
    if len(bits) < 2:
        raise template.TemplateSyntaxError("'%s' tag at least takes one arguments" % bits[0])
    value = parser.compile_filter(bits[1])
    return LogNode(value)



class DIRNode(template.Node):
    def __init__(self, obj):
        self.obj = obj

    def render(self, context):
        obj = self.obj.resolve(context, True)
        for x in dir(obj): print x
        return ''


def do_dir(parser, token):
    bits = token.contents.split()
    if len(bits) < 2:
        raise template.TemplateSyntaxError("'%s' tag at least takes one arguments" % bits[0])
    value = parser.compile_filter(bits[1])
    return DIRNode(value)


register = template.Library()
register.tag('log', do_log)
register.tag('dir', do_dir)