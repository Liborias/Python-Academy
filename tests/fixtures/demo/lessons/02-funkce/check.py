from dilna_check import check
c = check()
if c.defines_function("secti", 2):
    ns = c.load()
    c.returns(ns, "secti", (2, 3), 5)
    c.returns(ns, "secti", (-1, 1), 0)
c.not_uses_call("eval", "eval() nepoužívejte.")
c.done()
