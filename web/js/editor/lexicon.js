// Společné seznamy slov pro zvýrazňování a našeptávač.
export const KEYWORDS = ['False', 'None', 'True', 'and', 'as', 'assert', 'async', 'await', 'break', 'case', 'class', 'continue',
  'def', 'del', 'elif', 'else', 'except', 'finally', 'for', 'from', 'global', 'if', 'import', 'in', 'is', 'lambda', 'match',
  'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'try', 'while', 'with', 'yield'];
export const BUILTINS = ['abs', 'all', 'any', 'bool', 'dict', 'enumerate', 'filter', 'float', 'format', 'input', 'int', 'isinstance',
  'len', 'list', 'map', 'max', 'min', 'open', 'print', 'range', 'reversed', 'round', 'set', 'sorted', 'str', 'sum', 'tuple', 'type', 'zip',
  'Exception', 'ValueError', 'TypeError', 'KeyError', 'IndexError', 'FileNotFoundError', 'ZeroDivisionError', 'self'];
export const esc = (s) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
export const span = (cls, t) => `<span class="${cls}">${t}</span>`;
