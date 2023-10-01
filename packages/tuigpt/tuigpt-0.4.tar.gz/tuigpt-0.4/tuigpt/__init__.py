import sys

import tuigpt.send as send



def main():
    chat = [[]]

    print('tui g4f')
    print('@by_chesnok')
    print('press exit to exit')
    print('=====')

    while 1:
        q = input('input: ')
        if q == 'exit':
            sys.exit()
        chat[0].append('user')
        chat[0].append(q)
        result = send.request(chat)
        chat[0].append('gpt')
        chat[0].append(result)
        print(f'gpt: {result}')
        
        # print(chat)







if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)