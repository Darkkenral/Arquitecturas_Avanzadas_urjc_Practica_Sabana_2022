import Simulacion as simu

if __name__ == "__main__":
    main()


def main():

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
        #@@@@@@@@@@@@@@@@@@@@@@@@(       @@%                                      
                          @@@           @@%         &@@@@@@@@@@@@@@%             
                          @@@         (@@@         @@&            &@@@@@@        
                          &@@    .@@@@%,      @@@@@@@#                  @@,      
                            #@@@@@@@%         ,@@.         @@@@@@@@@@@@@@@@       
                                  @@%           @@@@@@@@@@@@    *@@               
                                  @@%                   @@@     *@@               
                                  @@%                   @@@  @@@@@                
                                  @@%                    @@@@@@                   
                  @@@@@@@@@@@&    @@%             ,%@@#     #@@                   
            *@@@@#          #@@@@@@%   ,%@@@@@@@@@/..@@@@& #@@  %@@@@@@@&        
        #@@@@*                   @@@@@@@/.               @@@@@@@(.     .@@@&     
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
    if opcion == 3:
        quit()
    elif opcion == 2:
        juego = simu.Simulacion()
        juego.run()
    elif opcion == 1:
        n_columnas = input('--Porfavor introduzca el numero de columnas--::')
        n_filas = input('--Porfavor introduzca el numero de filas--::')
        n_animales=input('--Porfavor introduzca el numero de animales --::')
        n_manadas=input('--Porfavor introduzca  el numero de manadas--::')
        juego = simu.Simulacion(n_columnas,n_filas,n_animales,n_manadas)
        juego.run()
    print('------SIMULACION TERMINADA------')
    input('--Porfavor presione enter para terminar-::')
    


# Controlar nnumero de animales y de manadas
