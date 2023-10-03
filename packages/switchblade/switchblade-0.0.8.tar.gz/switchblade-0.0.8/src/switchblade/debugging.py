'''
useful modules for debugging code
'''

def console():
    '''
    a console you can just plug in, instead of 
    many print() lines :)

    Doesn't work very well with scoping but this can 
    help in basic bug cases.
    '''
    while True:
        cmd = input('>> ')
        if cmd.lower() in ['quit', 'quit()']:
            break
        try:
            exec(cmd)
        except Exception as e:
            print(e)