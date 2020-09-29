from statistics.club import GamblersClub
from magazine.reporter import Reporter

intervalo_numeros = 60              
quantidade_numeros_sorteados = 6      
jogadores = 30                     

quantidade_numeros_jogados = range(6, 8)
jogos_por_jogador = [100_000, 50_000]


def generate_samples(quantidade_numeros_jogados,
                     jogos_por_jogador):

    
    for numeros, tentativas in zip(quantidade_numeros_jogados, jogos_por_jogador):

        gamblers = GamblersClub(numbers_range=intervalo_numeros,
                                numbers_amount=quantidade_numeros_sorteados,
                                numbers_played=numeros,
                                trials=tentativas,
                                players=jogadores)

        gamblers.play()

        reporter = Reporter(gambler_hits=gamblers.hits_list,
                            numbers_played=gamblers.numbers_played)

        reporter.save_hits()


if __name__ == "__main__":
    
    generate_samples(quantidade_numeros_jogados=quantidade_numeros_jogados,
                     jogos_por_jogador=jogos_por_jogador)

      