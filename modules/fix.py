path = '/Users/zhongweishan/Desktop/shadowinglab/modules/session.py'
with open(path, 'r') as f:
    lines = f.readlines()

# find the function start and end
start = None
end = None
for i, line in enumerate(lines):
    if 'def _recorder_component' in line:
        start = i
    if start and i > start and line.startswith('def ') and i > start + 2:
        end = i
        break

print(f"Function found: lines {start+1} to {end}")
print("First line:", repr(lines[start]))
print("Last line before end:", repr(lines[end-1]))
