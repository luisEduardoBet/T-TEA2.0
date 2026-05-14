import random

DIR =  "/home/luis-bet/.local/share/ttea"

INSTITUTION = DIR + "/institutionfacilities"
HEALTHPRO = DIR + "/healthprofessionals"
PLAYERS =  DIR + "/players"






# for i in range(1, 1000): 
#     file = open(INSTITUTION  + f"/{i}_institution{i}_institutionfacility.csv", "x")
#     file.write("id;name;address;phone;email;website;social_network;type\n")
#     inst_type = random.randrange(1,7);     
#     file.write(f"{i};Institution{i};asdaksdo;499999999;jasfasf@gmail.com;www.teste.com;@hostpital;{inst_type}")


for i in range(1, 5000): 

    file = open(HEALTHPRO  + f"/{i}_Fulano{i}_healthprofessional.csv", "x")
    file.write("id;name;type;institutionfacility\n")
    healthtype = random.randrange(1,20);   
    inst = random.randrange(1,1000)
    file.write(f"{i};Fulano{i};{healthtype};{inst}")




for i in range(1, 5000): 
    file = open(PLAYERS  + f"/{i}_Siclano{i}_player.csv", "x")
    file.write("id;name;birth_date;observation\n")
    file.write(f"{i};Siclano{i};2022-02-12; Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec dignissim sagittis interdum. Praesent mollis euismod diam eget commodo. Quisque quis maximus tortor. Proin viverra, elit et placerat mollis, dui dui vehicula ipsum, non congue dui nisi vel ante. Duis ut pulvinar leo. Pellentesque ipsum leo, suscipit id sapien volutpat, egestas.")








# Institution:  

# id;name;address;phone;email;website;social_network;type
# 2;Teste123;asdaksdo;499999999;jasfasf@gmail.com;www.teste.com;@hostpital;1

#Players: 

#id;name;birth_date;observation
#1;Siclano;2026-03-02;asdadads


# HEALTHPRO:
 
#type do 0 ao 20

#id;name;type;institutionfacility
#1;Fulano;7;1





