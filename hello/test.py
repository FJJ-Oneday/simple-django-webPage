import os

print(os.path.abspath(__file__))
print(os.path.dirname(__file__))
print()
print(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'media'))