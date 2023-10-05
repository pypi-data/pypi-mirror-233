"""
logics is a domain-specific expression language with a Python-style syntax,
that can be compiled and executed in any of ViUR's runtime contexts.
"""
from .parser import LogicsParser
from .value import Value, parse_float, parse_int, unescape

'''
# --- replace ----------------------------------------------------------------------------

def _replace(s, f = " ", r=""):
    # handle a list when passed to replace multiple strings
    if isinstance(f, list):
        for i in f:
            s = _replace(s, i, r)

        return s

    f = str(f)
    if not f: #hack to 'find' the empty string, this causes endless-loop in PyJS
        return "".join([(str(r) + x) for x in str(s)])

    return str(s).replace(f, str(r))

self.addFunction("replace", _replace)

# --- strip, lstrip, rstrip --------------------------------------------------------------
self.addFunction("lstrip", lambda s, c=" \t\r\n": str(s).lstrip(c))
self.addFunction("rstrip", lambda s, c=" \t\r\n": str(s).rstrip(c))
self.addFunction("strip", lambda s, c=" \t\r\n": str(s).strip(c))

# --- join -------------------------------------------------------------------------------

def _join(entries, delim=", ", lastDelim=None):
    if lastDelim is None:
        return str(delim).join(entries)

    ret = ""
    for entry in entries:
        ret += str(entry)

        if entry is not entries[-1]:
            if lastDelim is not None and entry is entries[-2]:
                ret += str(lastDelim)
            else:
                ret += str(delim)

    return ret

self.addFunction("join", _join)

# --- split -------------------------------------------------------------------------------

self.addFunction("split", lambda s, d=" ": s.split(d))

# --- currency ----------------------------------------------------------------------------

def currency(value, deciDelimiter=",", thousandDelimiter=".", currencySign=u"€"):
    ret = "%.2f" % parseFloat(value)
    before, behind = ret.split(".", 1)
    before = reversed(before)

    ret = ""
    for i, ch in enumerate(before):
        if i > 0 and i % 3 == 0:
            ret = ch + thousandDelimiter + ret
        else:
            ret = ch + ret

    ret = ret + deciDelimiter + behind

    # append currency if defined
    if currencySign:
        ret += " " + currencySign

    return ret.strip()

self.addFunction(currency)

# --- range -------------------------------------------------------------------------------

def _range(start, end=None, step=None):
    if step:
        return range(parseInt(start), parseInt(end), parseInt(step))
    if end:
        return range(parseInt(start), parseInt(end))

    return range(parseInt(start))

self.addFunction("range", _range)

# --- fill --------------------------------------------------------------------------------

self.addFunction("lfill", lambda s, l, f=" ": "".join([str(f) for x in range(len(str(s)), parseInt(l))]) + str(s))
self.addFunction("rfill", lambda s, l, f=" ": str(s) + "".join([str(f) for x in range(len(str(s)), parseInt(l))]))
'''


_parser = LogicsParser()


class _Stack(list):
    def op0(self, value):
        super().append(Value(value))

    def op1(self, fn):
        self.op0(fn(self.pop()))

    def op2(self, fn):
        b = self.pop()
        self.op0(fn(self.pop(), b))

    def op3(self, fn):
        c = self.pop()
        b = self.pop()
        self.op0(fn(self.pop(), b, c))


class Logics:
    MAX_FOR_ITERATIONS: int = 4 * 1024

    def __init__(self, src: str, debug: bool = False):
        super().__init__()
        self.ast = _parser.parse(src)
        self.functions = {
            "bool": bool,
            "float": parse_float,
            "len": len,
            "int": parse_int,
            "lower": lambda val: str(val).lower(),
            "max": max,
            "min": min,
            "round": lambda f, deci=0: Value(round(parse_float(f), parse_int(deci))),
            "str": str,
            "sum": lambda val: sum([Value(i, allow=[bool, int, float], default=0) for i in val]),
            "upper": lambda val: str(val).upper(),
            # todo: Port missing functions from above
        }

        self.debug = debug
        if self.debug:
            self.ast.dump()

    def run(self, values={}):
        stack = _Stack()
        self.__traverse(self.ast, stack, values)

        try:
            return stack.pop()
        except IndexError:
            pass

    def __traverse(self, node, stack, values):
        # Flow operations
        match node.emit:
            case "and" | "or":
                assert len(node.children) == 2
                self.__traverse(node.children[0], stack, values)

                check = stack.pop()
                test = bool(check)
                if node.emit == "or":
                    test = not test

                if test:
                    self.__traverse(node.children[1], stack, values)
                else:
                    stack.append(check)

                return

            case "cmp":
                assert len(node.children) > 1
                self.__traverse(node.children[0], stack, values)

                for node in node.children[1:]:
                    self.__traverse(node.children[0], stack, values)

                    b = stack.pop()
                    a = stack.pop()

                    match node.emit:
                        case "eq":
                            res = a == b
                        case "neq":
                            res = a != b
                        case "lt":
                            res = a < b
                        case "lteq":
                            res = a <= b
                        case "gt":
                            res = a > b
                        case "gteq":
                            res = a >= b

                        case node:
                            raise NotImplementedError(f"Logics VM: cmp {node=} is not implemented")

                    if not res:
                        stack.op0(False)
                        return

                    stack.op0(b)

                stack.op0(True)
                return

            case "call":
                if len(node.children) > 1:
                    self.__traverse(node.children[1], stack, values)
                    args = stack.pop().list()
                else:
                    args = ()

                if fn := self.functions.get(node.children[0].match):
                    # todo: Handle invalid parameters
                    stack.op0(fn(*args))
                else:
                    # todo: should this return a string?
                    raise NotImplementedError(f"Call to unknown function: {node.children[0].match!r}")

                return

            case "comprehension":
                assert len(node.children) in (3, 4)

                # Obtain iterable
                self.__traverse(node.children[2], stack, values)
                items = stack.pop()

                # Extract AST components for faster access
                each = node.children[0]
                name = node.children[1].match
                test = node.children[3] if len(node.children) > 3 else None

                # Loop over the iterator
                ret = []
                for i, item in enumerate(items):
                    # Limit loop to maximum of iterations (#17)
                    if i >= Logics.MAX_FOR_ITERATIONS:
                        break

                    values[name] = item

                    # optional if
                    if test:
                        self.__traverse(test, stack, values)
                        if not bool(stack.pop()):
                            continue

                    self.__traverse(each, stack, values)
                    ret.append(stack.pop())

                stack.op0(ret)
                return

            case "if":
                assert len(node.children) == 3
                # Evaluate condition
                self.__traverse(node.children[1], stack, values)
                # Evaluate specific branch
                self.__traverse(node.children[0 if bool(stack.pop()) else 2], stack, values)
                return

        # Traverse children first (default behavior, except state otherwise above)
        if node.children:
            for child in node.children:
                self.__traverse(child, stack, values)

        # Stack operations
        match node.emit:
            # Pushing values
            case "False":
                stack.op0(False)
            case "Identifier":
                stack.op0(node.match)
            case "None":
                stack.op0(None)
            case "Number":
                if "." in node.match:
                    stack.op0(Value(parse_float(node.match)))
                else:
                    stack.op0(Value(parse_int(node.match)))

            case "String":
                stack.op0(unescape(node.match[1:-1]))  # cut "..." from string.
            case "True":
                stack.op0(True)

            # Operations
            case "add":
                stack.op2(lambda a, b: a + b)
            case "attr":
                stack.op2(lambda value, attr: value[attr])
            case "div":
                stack.op2(lambda a, b: a / b)
            case "entity":
                ...
            case "idiv":
                stack.op2(lambda a, b: a // b)
            case "in":
                stack.op2(lambda a, b: a in b)
            case "invert":
                stack.op1(lambda a: ~a)
            case "list":
                stack.op0(list(reversed([stack.pop() for _ in range(len(node.children))])))
            case "mod":
                stack.op2(lambda a, b: a % b)
            case "mul":
                stack.op2(lambda a, b: a * b)
            case "neg":
                stack.op1(lambda a: -a)
            case "not":
                stack.op1(lambda a: not a)
            case "outer":
                stack.op2(lambda a, b: a not in b)
            case "pos":
                stack.op1(lambda a: +a)
            case "pow":
                stack.op2(lambda a, b: a ** b)
            case "index":
                stack.op2(lambda value, idx: value[idx])
            case "load":
                stack.op1(lambda name: values.get(str(name)))
            case "slice":
                # TODO
                # stack.op3(lambda value, from, to: value.__getitem__(from, to))
                pass
            case "strings":
                stack.op0("".join([stack.pop() for _ in range(node.children.length)]))

            case "sub":
                stack.op2(lambda a, b: a - b)
            case "vars":
                stack.op0(values)

            case node:
                raise NotImplementedError(f"Logics VM: {node=} is not implemented")
