# CRUD de Ve�culos

* Para execu��o desse projeto primeiro devemos certificar que a API esteja rodando corretamente, para isso siga os seguintes passos:
- acesse a pasta *car-api*
- execute o seguinte comando

###### npm
```
cd car-api 
npm install
```

###### yarn
```
cd car-api 
yarn install
```

* Ap�s todas depend�ncias instaladas corretamente basta executar o comando para executar a API:###### npm
```
npm run start:dev
```

###### yarn
```
yarn run start:dev
```

## Adicionando um carro para aparecer no front
* Abra uma aplica��o tal como POSTMAN ou INSOMNIA
* Crie uma resi��o do tipo **POST** 
* Adicione a URL http://localhost:3000/cars
* Copie o body do tipo JSON para aplica��o e mande executar.
```json
{
  "placa": "YZA567",
  "chassi": "9I5J7K9L1M3N5O7P0",
  "renavam": "90123456789",
  "modelo": "SUV",
  "marca": "Mercedes-Benz",
  "ano": 2019
}
```

* Uma vez a api rodando corretamente pode ser executado o frontend na pasta *car-front*

* Seguinto os mesmos passos da API primeiro devemos instalar as depend�ncias do Angular.

###### npm
```
cd car-front 
npm install
```

###### yarn
```
cd car-front 
yarn install
```

* Uma vez instalado as depend�ncias basta executar o comando de execu��o do frontend, esperar compilar e acessar a url: [URL](http://localhost:4200)
