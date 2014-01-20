from suds.mx.appender import Appender,Content


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
