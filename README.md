# Parsen und umwandeln von THW Adressdaten in ein annähernd brauchbares Format

Das Technische Hilfswerk stellt unter
https://www.govdata.de/web/guest/suchen/-/details/ubersicht-der-thw-liegenschaften
eine Liste seiner Dienststellen zur Verfügung.

Leider sind diese Daten in einem meiner Meinung nach vollkommen unbenutzbaren
Format. Ausserdem fehlen Daten zur Erreichbarkeit per Telefon / EMail; diese
müssen erst aufwändig von thw.de gescraped werden.

Dieses Script kombiniert die beiden Datensätze und gibt eine JSON-Datei mit
folgendem Format aus:

```
{
  "Leitung Technisches Hilfswerk": {
    "name": "Leitung Technisches Hilfswerk",
    "street": "Provinzialstra\u00dfe 93",
    "zip": "53127",
    "city": "Bonn",
    "phone": "02289400",
    "fax": "02289401520",
    "email": "poststelle@thw.de",
    "code": "TLTG"
  },
  ...
}
```

