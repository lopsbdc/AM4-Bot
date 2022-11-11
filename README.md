# AM4-Bot
Bot VintePila - Airline Manager 4

Este é um bot para pesquisar preços de Combustivel e CO2 do jogo Airline Manager 4. 

O bot verifica os preços periodicamente (através de webscrapping com Selenium), realizando o login no sistema, e depois abrindo as abas de preços.
Caso os valores estejam dentro do esperado, o bot envia uma mensagem pelo Telegram (em um grupo pré determinado), 
e posteriormente faz uma postagem direto no Wordpress, informando estes mesmos dados.

A cada 30 minutos, o bot realiza uma nova busca (tempo médio de atualização de preços dentro do game). Atualmente, hospedado no AWS EC2

Também há tratativas de erros, para evitar que o bot fique offline, bem como logs de sucessos e erros
