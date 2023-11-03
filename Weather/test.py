import Weather.weather

test = Weather.weather.WeatherForecast()
test.set_param(station=1, var_station='mpei', var_nwp_provider='icon')
test.get_json()
test = test.get_param_weather()
print(test)
