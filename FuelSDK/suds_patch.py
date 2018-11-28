from logging import getLogger

from suds import *
from suds.mx import *
from suds.mx.appender import Appender
from suds.resolver import Frame


class _PropertyAppender(Appender):
    """
    A L{Property} appender.

    Patched for FuelSDK
    """
        
    def append(self, parent, content):
        p = content.value
        child = self.node(content)
        child_value = p.get()
        if(child_value is None):
            pass
        else:
            child.setText(child_value)
            parent.append(child)
            for item in p.items():
                cont = Content(tag=item[0], value=item[1])
                Appender.append(self, child, cont)


def _bodycontent(self, method, args, kwargs):
    """
    # The I{wrapped} vs I{bare} style is detected in 2 ways.
    # If there is 2+ parts in the message then it is I{bare}.
    # If there is only (1) part and that part resolves to a builtin then
    # it is I{bare}.  Otherwise, it is I{wrapped}.
    #

    Patched for FuelSDK
    """
    if not len(method.soap.input.body.parts):
        return ()
    wrapped = method.soap.input.body.wrapped
    if wrapped:
        pts = self.bodypart_types(method)
        root = self.document(pts[0])
    else:
        root = []
    n = 0
    for pd in self.param_defs(method):
        if n < len(args):
            value = args[n]
        else:
            value = kwargs.get(pd[0])
        n += 1
        if value is None:
            continue
        p = self.mkparam(method, pd, value)
        if p is None:
            continue
        if not wrapped:
            ns = pd[1].namespace('ns0')
            p.setPrefix(ns[0], ns[1])
        root.append(p)
    return root

def _start(self, content):
    log = getLogger(__name__)
    #
    # Start marshalling the 'content' by ensuring that both the 'content'
    # _and_ the resolver are primed with the XSD type information. The
    # 'content' value is both translated and sorted based on the XSD type.
    # Only values that are objects have their attributes sorted.
    #
    log.debug('starting content:\n%s', content)
    if content.type is None:
        name = content.tag
        content.type = self.resolver.find(name, content.value)
        if content.type is None:
            raise TypeNotFound(content.tag)
    else:
        known = None
        if isinstance(content.value, Object):
            known = self.resolver.known(content.value)
            if known is None:
                log.debug('object %s has no type information',
                    content.value)
                known = content.type
        frame = Frame(content.type, resolved=known)
        self.resolver.push(frame)
    frame = self.resolver.top()
    content.real = frame.resolved
    content.ancestry = frame.ancestry
    self.translate(content)
    self.sort(content)
    if self.skip(content):
        log.debug('skipping (optional) content:\n%s', content)
        self.resolver.pop()
        return False
    return True
