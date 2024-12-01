Basicamente você precisa de uma conta no pushbullet (https://www.pushbullet.com), e colocar a a sua api no dailyupdater.py ou em um .env.

O medsedit.py é o programa que você roda para editar os medicamentos e etc.

Para fazer rodar diariamente, eu recomendo você colocar esse repositório dentro da pasta do usuário público do seu PC, depois utilizar um programa como o auto-py-to-exe (https://pypi.org/project/auto-py-to-exe/) para converter seu arquivo dailyupdater.py para exe e aí você coloca um atalho para ele no shell:common startup pra rodar quando você ligar o PC e também coloca ele em horários específicos no TaskScheduler do Windows. Eu coloquei às 8 da manhã e da noite.
