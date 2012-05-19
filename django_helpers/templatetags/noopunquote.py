from django import template
from urllib2 import unquote

register = template.Library()


class NoOopNode(template.Node):
    def __init__(self, text):
        self.text = text

    def render(self, context):
        output = ""
        for bit in self.text:
            if isinstance(bit, basestring):
                output += bit
            else:
                output += bit.render(context)
        while output.find('\n') >= 0:
            output = output.replace('\n', '')
        return unquote(output)


@register.tag
def unquote_noop(parser, token):
    text_and_nodes = []
    while 1:
        token = parser.tokens.pop(0)
        if token.contents == 'endnoop':
            break

        if token.token_type == template.TOKEN_VAR:
            text_and_nodes.append('{{')
            text_and_nodes.append(token.contents)

        elif token.token_type == template.TOKEN_TEXT:
            text_and_nodes.append(token.contents)

        elif token.token_type == template.TOKEN_BLOCK:
            try:
                command = token.contents.split()[0]
            except IndexError:
                parser.empty_block_tag(token)

            try:
                compile_func = parser.tags[command]
            except KeyError:
                parser.invalid_block_tag(token, command, None)
            try:
                node = compile_func(parser, token)
            except template.TemplateSyntaxError, e:
                if not parser.compile_function_error(token, e):
                    raise
            text_and_nodes.append(node)

        if token.token_type == template.TOKEN_VAR:
            text_and_nodes.append('}}')
    return NoOopNode(text_and_nodes)