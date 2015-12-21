import gamep2p

client = gamep2p.Gamep2p('listen')
client.main()

while True:
    input = raw_input('Enter Position')
    client.text = input