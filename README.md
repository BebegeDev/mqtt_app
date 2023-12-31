# РАЗРАБАТЫВАЕТСЯ И ПЛАНИРУЕТСЯ ИСПОЛЬЗОВАТЬСЯ СОВМЕСТНО С app_calculations https://github.com/BebegeDev/app_calculations.git
# mqtt_app #
Данный репозиторий содержит код, который выступает в роли шлюза, для связи оборудования и пользователя. В качестве прослойки выбран протокол mqtt. 
Доступное оборудование на данный момент: SM3300, Victron BMV-702.

*Примечание*: В описании речь будет идти про SM3300 и BMV-702. Но вы можете использовать свое оборудование, если он схоже с указанным выше. Если у вас есть BMV-702 и нет SM3300 или наоборот, код будет работать, если следовать инструкции, пожалуйста прочитай рукводство полностью. Все что косается ДГУ можете игнорировать.

## Установка ##
Добавте себе репозиторий любым удобным способом. Перейдите в папку lib, установите необходимые зависимости.

```
pip install -r requirements.txt
```

# Предварительная настройка #
Убедитесь, что на вашем сервере произведена установка и настройка MQTT-клиента.

*Примечание*: У BMV-702 имеется свои настройки mqtt, в данном коде предполагается, что пользователь использует мост для проброса с BMV-702 на свой шлюз. Пожалуйста предусмотрите это.

Перейдите в папку `utils` откройте файл и отредактируйте `setting.ini`.
`[MQTT]` - укажите IP вашего сервера, его порт, время опроса, укажите имя и пароль пользователя.
`[EM]` - укажите IP ваших SM3300


Далее перейдите в папку `CreateJsonTopic`, откройте `create_json_topic.py` и отредактируйте следующим образом.
`create_json_topic.py` - нужно запускать после изменения блока.
### Для Victron
1. Измените `pref` на тот, который обозначен в вашем продукте, обычно она обозначена как `VRM ID портала` <https://www.victronenergy.com/live/vrm_portal:start>
2. По желанию отредактируйте `topics`
3. Аналогично для следующего блока.


На этом предварительная настройка готова.

# Настройка работы программы #
В файле `main.py` находятся основные вызовы. Для дальнейшей настройки вам следует отредактировать код под ваше количество оборудования, рассмотрите пример ниже:

Если у вас есть в количестве 2 штк. SM3300, вы можете оставить следующие строчки кода 
```
    emulators_contact = Emulators.emulators_contact.ContactEmulators(mqttc)
    emulators_command = Emulators.emulators_command.CommandEmulators(mqttc, emulators_contact)
    emulators_contact.get_data_emulators()
    Emulators.emulators_contact.ContactEmulators.close_socket(emulators_contact.supplySocket_1)
    Emulators.emulators_contact.ContactEmulators.close_socket(emulators_contact.supplySocket_2)
```
Если выше количество отличается, отредактируйте файлы в папке `Emulators` добавьте или убавьте количество соокетов и тд. под ваше кол-во SM3300.
Аналогично с BMV-702 отредактируйте файлы в папке`Victron` под ваши нужды.

## Парсер для прогноза погоды
1. Необходимо импортировать
```
import Weather.weather
```
2. Создать экземпляр класса ```Weather``` 
```
test = Weather.weather.WeatherForecast()
```
3. По желанию (необязтельный шаг) можно менять параметры станции и провайдера. Значения по умолчанию, как в примере. Ознакомится со станциями и провайдером можете у партнера http://194.35.116.172:3000/d/ca80eadb-275c-4bbd-8d69-a5cb6e6fade0/dannye-chpp?orgId=1&var-station=mpei&var-nwp_provider=bm&from=1698267600000&to=1698872399999 и документация http://62.109.30.150:81/docs#/
```
test.set_param(station=1, var_station='mpei', var_nwp_provider='icon')
```
4. Используйте метод ```get_json()```. Метод покажет статус запроса и в случае статуса 200 сохранит JSON в папке utils.
```
test.get_json()
```
5. Используйте ```get_param_weather()```. В метод передаются необходимый час и необходимые параметры прогноза погоды. Если час не будет указан по умолчанию выводтся следующий час. Если параметры погоды не будут указаны по умолчанию выводятся все.
Данные прогноза хранятся на каждые 24 часа, при пересчете следущие данные на 24 часа будт отсчитыватся от текущего времени.
```
test.get_param_weather(1, 'time', 'id')
```

# Проверка работы
Для проверки работоспособности рекомендую использовать MQTT Explorer <https://mqtt-explorer.com/>
