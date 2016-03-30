# Satellite Simulator


###Описание методов API

Ниже приводятся все методы для работы с данными имитационного комплекса.

#####СПУТНИКИ


**satellites.get** - возвращает расширенную информацию о спутниках.

*Параметры:*
- *satellite_ids* - перечисленные через запятую номера спутников в базе данных NORAD.
- *fields* - список дополнительных полей, которые необходимо вернуть. Доступные значения: *classification, launch_year, launch_number, launch_piece, epoch_year, epoch, bstar, version, inclination, node_ascension, eccentricity, perigee, mean_anomaly, mean_motion, revolutions*.
