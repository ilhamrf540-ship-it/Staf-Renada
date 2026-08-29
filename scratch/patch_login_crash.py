import re

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('u.username.toLowerCase()', 'String(u.username).toLowerCase()')
text = text.replace('mu.username.toLowerCase()', 'String(mu.username).toLowerCase()')
text = text.replace('lu.username.toLowerCase()', 'String(lu.username).toLowerCase()')

# Also handle saveEditedPersonnel
text = text.replace('u.username !== oldUsername', 'String(u.username) !== String(oldUsername)')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)
print("Replaced!")
