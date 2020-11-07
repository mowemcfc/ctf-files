import requests

def main():
    target_url = 'http://hello-world.ctf.fifthdoma.in:2000/'    
    string = ''
    with open('responses.txt', 'rw') as f:
        for i in range(0,100):
            string += 'a'
            print(string)
            resp = requests.get(target_url, data={'name':string})
            f.write(resp.text + '\n') 

main()

