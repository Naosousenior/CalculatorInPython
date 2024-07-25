import tests as t
import help as hp


print('Welcome to my favorite calculator')
print('Here you can make advanced calcs')

print('Type "help" to access the menu help')

while True:

    command = input('>> ')

    if command == 'exit':
        break

    if command == 'help':
        hp.help()
        continue

    t.test_evaluate(command)