#!/usr/bin/python
#vim:set fileencoding=utf-8 sw=2

#
# Remove unused catalog text lines from ".po" file.
#

def unquote(s):
  s = s.strip()
  if s[0] != '"' or s[-1] != '"':
    raise RuntimeError
  return s[1:-1]

def read_po(fp):
  st = 1
  comment = key = value = rkey = rvalue = ''
  for line in fp:
    if line[0] == '#' or line.strip() == '':
      if st == 2:
	yield (comment, key, value, rkey, rvalue)
	st = 1
	comment = key = value = rkey = rvalue = ''
      comment += line
    elif line[0] == '"':
      if st == 1:
	key += unquote(line)
	rkey += line
      else:
	value += unquote(line)
	rvalue += line
    elif line.startswith('msgid '):
      st = 1
      key = unquote(line[5:])
      rkey = line
    elif line.startswith('msgstr '):
      st = 2
      value = unquote(line[6:])
      rvalue = line
    else:
      raise RuntimeError

  if st == 2:
    yield (comment, key, value, rkey, rvalue)

def main():
  import sys

  d = {}
  it = read_po(file(sys.argv[1]))
  (comment, key, value, rkey, rvalue) = it.next()
  d[key] = rvalue
  sys.stdout.write(comment)
  for (comment, key, value, rkey, rvalue) in it:
    d[key] = rvalue

  it = read_po(file(sys.argv[2]))
  (comment, key, value, rkey, rvalue) = it.next()
  sys.stdout.write(rkey)
  sys.stdout.write(d.get(key, rvalue))
  for (comment, key, value, rkey, rvalue) in it:
    sys.stdout.write(comment)
    sys.stdout.write(rkey)
    sys.stdout.write(d.get(key, rvalue))

if __name__ == '__main__':
  main()
