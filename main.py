import Simulacion as simul


title = '''
    ██████  ▄▄▄       ▄▄▄▄    ▄▄▄       ███▄    █  ▄▄▄           ▄████  ▄▄▄       ███▄ ▄███▓▓█████
  ▒██    ▒ ▒████▄    ▓█████▄ ▒████▄     ██ ▀█   █ ▒████▄        ██▒ ▀█▒▒████▄    ▓██▒▀█▀ ██▒▓█   ▀
  ░ ▓██▄   ▒██  ▀█▄  ▒██▒ ▄██▒██  ▀█▄  ▓██  ▀█ ██▒▒██  ▀█▄     ▒██░▄▄▄░▒██  ▀█▄  ▓██    ▓██░▒███
    ▒   ██▒░██▄▄▄▄██ ▒██░█▀  ░██▄▄▄▄██ ▓██▒  ▐▌██▒░██▄▄▄▄██    ░▓█  ██▓░██▄▄▄▄██ ▒██    ▒██ ▒▓█  ▄
  ▒██████▒▒ ▓█   ▓██▒░▓█  ▀█▓ ▓█   ▓██▒▒██░   ▓██░ ▓█   ▓██▒   ░▒▓███▀▒ ▓█   ▓██▒▒██▒   ░██▒░▒████▒
  ▒ ▒▓▒ ▒ ░ ▒▒   ▓▒█░░▒▓███▀▒ ▒▒   ▓▒█░░ ▒░   ▒ ▒  ▒▒   ▓▒█░    ░▒   ▒  ▒▒   ▓▒█░░ ▒░   ░  ░░░ ▒░ ░
  ░ ░▒  ░ ░  ▒   ▒▒ ░▒░▒   ░   ▒   ▒▒ ░░ ░░   ░ ▒░  ▒   ▒▒ ░     ░   ░   ▒   ▒▒ ░░  ░      ░ ░ ░  ░
  ░  ░  ░    ░   ▒    ░    ░   ░   ▒      ░   ░ ░   ░   ▒      ░ ░   ░   ░   ▒   ░      ░      ░
        ░        ░  ░ ░            ░  ░         ░       ░  ░         ░       ░  ░       ░      ░  ░
                          ░
  '''

print(title)
image = '''
                        /@@@@@@@@@@@@@@@@@@@@@@.
                *@@@@@@@@,                    &@@
              @@@*                            .@@,
              @@*                          *@@@@@@@@@@@@@@@
        (@@@@@@@@@@@&                                     .@@,
      ,@@*                                                #@@
      ,@@*                      %@@@@@@@@@@@@@@@@@@@@@@@@@@*
        # @@@@@@@@@@@@@@@@@@@@@@@@(       @@%
                          @@@           @@%         &@@@@@@@@@@@@@@%
                          @@@         (@@@         @@&            &@@@@@@
                          &@@    .@@@@%,      @@@@@@@#                  @@,
                            # @@@@@@@%         ,@@.         @@@@@@@@@@@@@@@@
                                  @@%           @@@@@@@@@@@@    *@@
                                  @@%                   @@@     *@@
                                  @@%                   @@@  @@@@@
                                  @@%                    @@@@@@
                  @@@@@@@@@@@&    @@%             ,%@@#     #@@
            *@@@@#          #@@@@@@%   ,%@@@@@@@@@/..@@@@& #@@  %@@@@@@@&
        # @@@@*                   @@@@@@@/.               @@@@@@@(.     .@@@&
    &@@@@.                       @@%  &@@@@&               #@@@@@@.       .@@@&
  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

  '''
print(image)

print('----------------------------------------------------------------------------------------------------------------------')
print('''
    __  ___
    /  |/  /__ ___  __ __
  / /|_/ / -_) _ \/ // /
  /_/  /_/\__/_//_/\_,_/ ''')

print('----------------------------------------------------------------------------------------------------------------------')
print('\n')
print('\t\t1) Configuracion por defecto')
print('\t\t2) Configuraccion personalizada')
print('\t\t3) Salir')

print('\n')
opcion = input('--Porfavor introduzca una opcion--::')

if opcion == '1':
    juego = simul.Simulacion()
    juego.run()
if opcion == '2':
    n_columnas = input('--Porfavor introduzca el numero de columnas--::')
    n_filas = input('--Porfavor introduzca el numero de filas--::')
    if n_columnas*n_filas < 18:
        print('Tamaño tablero invalido, porfavor genere un tablero de almenos 18 casillas')
        print('------SIMULACION TERMINADA------')
        quit()

    n_animales = input('--Porfavor introd1uzca el numero de animales --::')
    if n_animales < 18:
        print('Numero de animales invalido, porfavor genere un tablero de almenos 18 animales para cumplir con las proporciones solicitadas')
        print('------SIMULACION TERMINADA------')
        quit()

    n_manadas = input('--Porfavor introduzca  el numero de manadas--::')
    if n_manadas < 2:
        print('Numero de manadas invalido, porfavor introduzca almenos 2 manadas para cumplir con las especificaciones solicitadas')
        print('------SIMULACION TERMINADA------')
        quit()

    juego = simul.Simulacion(n_columnas, n_filas, n_animales, n_manadas)
    juego.run()
if opcion == '3':
    quit()

print(opcion)
print('------SIMULACION TERMINADA------')
input('--Porfavor presione enter para terminar-::')


# Controlar nnumero de animales y de manadas
