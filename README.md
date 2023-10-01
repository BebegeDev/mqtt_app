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
Перейдите в папку `utils` откройте файл и отредактируйте `setting.ini`.

`[MQTT]` - укажите IP вашего сервера, его порт, время опроса, укажите имя и пароль пользователя.
`[EM]` - укажите IP ваших SM3300


Далее перейдите в папку `CreateJsonTopic`, откройте `create_json_topic.py` и отредактируйте следующим образом.
`create_json_topic.py` - нужно запускать после изменения блока.
### Для Victron
*Примечание*: У BMV-702 имеется свои настройки mqtt, в данном коде предполагается, что пользователь использует мост для проброса с BMV-702 на свой шлюз. Пожалуйста предусмотрите это.
1. Измените `pref` на тот, который обозначен в вашем продукте, обычно она обозначена как `VRM ID портала`
2. По желанию отредактируйте `topics`
3. Аналогично для следующего блока.


На этом предварительная настройка готова.

# Настройка работы программы #
В файле `main.py` находятся основные вызовы. Для дальнейшей настройки вам следует отредактировать код под ваше количество оборудования, рассмотрите пример ниже:
Если у вас есть SM3300, вы можете оставить следующие строчки кода 
```
    emulators_contact = Emulators.emulators_contact.ContactEmulators(mqttc)
    emulators_command = Emulators.emulators_command.CommandEmulators(mqttc, emulators_contact)
    emulators_contact.get_data_emulators()
    Emulators.emulators_contact.ContactEmulators.close_socket(emulators_contact.supplySocket_1)
```
В данном репозитории рассматривается SM3300 в количестве 2 штк.
Если выше количество отличается, отредактируйте файлы в папке `Emulators` добавьте или убавьте количество соокетов и тд. под ваше кол-во SM3300.
Аналогично с BMV-702 отредактируйте код под ваши нужды.
