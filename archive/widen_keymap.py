path = "config/boards/shields/oregano/oregano.keymap"
with open(path, encoding="utf-8") as f:
    lines = f.readlines()

OLD_UNIT = 8
NEW_UNIT = 10
START = 3
NUM_CELLS = 6
GAP = 3

old_left_b = [START + OLD_UNIT * i for i in range(NUM_CELLS + 1)]
old_right_start = old_left_b[-1] + 1 + GAP
old_right_b = [old_right_start + OLD_UNIT * i for i in range(NUM_CELLS + 1)]


def transform(line):
    assert len(line) == 104, "unexpected length %d: %r" % (len(line), line)
    out = []
    out.append(line[0:3])  # "// "
    for i in range(NUM_CELLS):
        b_char = line[old_left_b[i]]
        cell = line[old_left_b[i] + 1:old_left_b[i + 1]]
        out.append(b_char)
        if set(cell) == {"\u2500"}:
            out.append("\u2500" * 9)
        else:
            assert len(cell) == 7
            out.append(" " + cell + " ")
    out.append(line[old_left_b[6]])
    gap_content = line[old_left_b[6] + 1:old_right_b[0]]
    out.append(gap_content)
    for i in range(NUM_CELLS):
        b_char = line[old_right_b[i]]
        cell = line[old_right_b[i] + 1:old_right_b[i + 1]]
        out.append(b_char)
        if set(cell) == {"\u2500"}:
            out.append("\u2500" * 9)
        else:
            assert len(cell) == 7
            out.append(" " + cell + " ")
    out.append(line[old_right_b[6]])
    return "".join(out)


blocks = [(53, 62), (71, 80), (90, 99), (109, 118)]
for start, end in blocks:
    for i in range(start, end):
        line = lines[i].rstrip("\n")
        if line.startswith("//") and len(line) == 104:
            newline = transform(line)
            lines[i] = newline + "\n"

with open(path, "w", encoding="utf-8") as f:
    f.writelines(lines)

print("done")
