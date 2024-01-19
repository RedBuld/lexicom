import random
import string
import uuid

short_names : list[str] = []
full_names : list[str] = []

f_short_names : dict[str,int] = {}

for i in range(700_000):

    name = ''.join( random.choice( string.ascii_letters + string.digits ) for _ in range( 48 ) ) + '-' + str( uuid.uuid4() )

    if name not in short_names:
        short_names.append(name)
        f_short_names[name] = random.randint(0,1)

for i in range(500_000):
    c = len(short_names)-1
    p = random.randint(0,c)
    v = short_names.pop(p)
    ext = ''.join( random.choice( string.ascii_lowercase + string.digits ) for _ in range( random.randint(3,4) ) )
    full_names.append(f'{v}.{ext}')

with open('sn.sql', 'w') as f:
    f.write('INSERT INTO `short_names`(`name`, `status`) VALUES\n')
    for name,status in f_short_names.items():
        f.write(f"('{name}', {status}),\n")

with open('fn.sql', 'w') as f:
    f.write('INSERT INTO `full_names`(`name`, `status`) VALUES\n')
    for name in full_names:
        f.write(f"('{name}', NULL),\n")

# print( f_short_names )
# print( full_names )