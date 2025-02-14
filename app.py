text = 'Provérbios 1 Propósito e tema 1- Provérbios de Salomão, filho de Davi, rei de Israel. 2- Eles ajudarão a adquirir a sabedoria e a instrução; a compreender as palavras que dão entendimento; 3- a receber a instrução para proceder com sensatez, fazendo a justiça, o juízo e a retidão; 4- ajudarão a dar prudência aos ingênuos e conhecimento e bom senso aos jovens. 5- Ouça o sábio e aumente o seu saber, e quem tem discernimento obterá orientação 6- para compreender provérbios e parábolas, os ditados dos sábios e os seus enigmas. 7- O temor do Senhor é o princípio do conhecimento, mas os insensatos desprezam a sabedoria e a instrução. Prólogo: Exortações a buscar a sabedoria Advertência contra o engano 8- Ouça, meu filho, a instrução do seu pai e não abandone o ensino da sua mãe. 9- Eles serão um belo diadema sobre a sua cabeça e um colar para adornar o seu pescoço. 10- Meu filho, se pecadores tentarem seduzi‑lo, não ceda! 11- Talvez eles digam: “Venha conosco, fiquemos de tocaia para derramar sangue, vamos armar uma emboscada sem causa contra quem de nada suspeita! 12- Vamos engoli‑los vivos, como a sepultura, e inteiros, como os que descem à cova; 13- acharemos todo tipo de objetos valiosos e encheremos as nossas casas com despojos; 14- lance a sua sorte conosco; dividiremos em partes iguais tudo o que conseguirmos!”. 15- Meu filho, não se deixe levar por essa gente! Afaste os pés do caminho que eles seguem, 16- pois os pés deles correm para fazer o mal, estão sempre prontos para derramar sangue. 17- Certamente é inútil estender a rede à vista de qualquer espécie de pássaro, 18- mas eles fazem tocaia contra o próprio sangue; armam emboscadas contra si mesmos! 19- Tal é a vereda de todos os que lucram pela ganância, e essa ganância toma a vida de todos os que a possuem. Advertência contra a rejeição à sabedoria 20- A sabedoria clama em alta voz nas ruas, ergue a voz nas praças públicas. 21- De cima dos muros ela clama; nas portas da cidade faz o seu discurso: 22- “Até quando vocês, ingênuos, amarão a sua ingenuidade? Vocês, zombadores, até quando terão prazer na zombaria? E vocês, tolos, até quando desprezarão o conhecimento? 23- Se acatarem a minha repreensão, compartilharei com vocês os meus pensamentos íntimos e lhes revelarei os meus ensinos. 24- Contudo, visto que vocês me rejeitaram quando os chamei e ninguém se importou quando estendi a mão; 25- visto que desprezaram totalmente o meu conselho e não quiseram aceitar a minha repreensão, 26- eu, da minha parte, vou rir da sua desgraça; zombarei quando o que temem sobrevier a vocês, 27- quando aquilo que temem sobrevier a vocês como uma tempestade, quando a desgraça os atingir como um vendaval, quando a angústia e a dor os dominarem. 28- “Então, vocês me chamarão, mas eu não responderei; procurarão por mim, mas não me encontrarão. 29- Visto que desprezaram o conhecimento e não escolheram temer ao Senhor, 30- não quiseram aceitar o meu conselho e fizeram pouco caso de toda a minha repreensão, 31- comerão do fruto dos seus caminhos e se fartarão das suas próprias maquinações. 32- Porque a rebeldia dos ingênuos os matará, e a tranquilidade dos tolos os destruirá, 33- mas quem me ouvir viverá em segurança e estará tranquilo, sem temer nenhum mal”.'
tokens = list(text.encode(encoding='UTF-8', errors='strict'))
tokenizer_vocab = {byte: chr(byte) for byte in sorted(set(tokens))}

def get_stats(ids):
    pair_counts = {}
    
    for i in range(len(ids) - 1):
        pair = (ids[i], ids[i+1])
        
        if pair in pair_counts:
            pair_counts[pair] += 1
        else:
            pair_counts[pair] = 1
        
    return pair_counts

def merge(ids, pair, new_token):
    new_ids = []
    i = 0
    while i < len(ids):
        if i < len(ids) - 1 and (ids[i], ids[i+1]) == pair:
            new_ids.append(new_token)
            i += 2
        else:
            new_ids.append(ids[i])
            i += 1
            
        if new_token not in tokenizer_vocab:
            tokenizer_vocab[new_token] = tokenizer_vocab[pair[0]] + tokenizer_vocab[pair[1]]
    return new_ids
            
stats = get_stats(tokens)

FREQUENCY_THRESHOLD = 3

merge_history = []

while stats:
    most_frequent_pair = max(stats, key=stats.get)
    
    highest_frequency = stats[most_frequent_pair]
    if highest_frequency < FREQUENCY_THRESHOLD:
        break
    
    new_token = max(tokens) + 1
    merge_history.append((new_token, most_frequent_pair))
    
    tokens = merge(tokens, most_frequent_pair, new_token) 
    stats = get_stats(tokens) 

def decode(tokens, merge_history):
    for new_token, pair in reversed(merge_history):
        decoded_tokens = []
        i = 0
        while i < len(tokens):
            if tokens[i] == new_token:
                decoded_tokens.extend(pair)
            else:
                decoded_tokens.append(tokens[i])
            i += 1
        tokens = decoded_tokens
        
    return bytes(tokens).decode('UTF-8')

decoded_text = decode(tokens, merge_history)